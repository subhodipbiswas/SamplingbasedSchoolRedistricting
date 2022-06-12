#! /usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
import time
import pandas as pd
from utils import Utils
from functions import update_property
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                        proposals, updaters, constraints, accept, metrics)


class MCMC:
    """
    The base class for the performing MCMC sampling.
    """

    def __init__(self, args=None, solution=None, seed=123456789, algo='BAA'):
        self.args = args
        self.seed = seed
        self.solution = solution
        self.number_of_flips = 10**7
        self.algo = algo

    def create_partition(self):
        """

        """
        population, capacity, polygons, attributes = self.args[0], self.args[1], self.args[3], self.args[6]
        # Find the initial assignment of polygons to districts and determine additional attributes
        districts, district_ids = self.solution['districts'], self.solution['district_ids']
        polygons['assignment'] = [district_ids[polygons[attributes['Location']][index]]
                                  for index, poly in polygons.iterrows()]
        polygons['capacity'] = [capacity[polygons[attributes['Location']][index]]
                                for index, poly in polygons.iterrows()]
        if 'SHAPE_area' not in polygons.head():
            polygons['SHAPE_Area'] = [polygons['geometry'][index].area
                                      for index, poly in polygons.iterrows()]
        # Create the initial graph using gerrychain library and then create a Geographic Partition from it
        w = 0.1 * self.args[6]['weight']  # weighing 'imbalance' and 'noncompactness'
        initial_partition = GeographicPartition(
            Graph.from_geodataframe(polygons, adjacency='rook'),
            assignment="assignment",
            updaters={
                "cut_edges": updaters.cut_edges,
                "population": updaters.Tally(attributes['Level'] + '_POP',
                                                        alias="population"),
                "capacity": updaters.Tally('capacity', alias="capacity"),
                "area": updaters.Tally("SHAPE_Area", alias="area"),
                "perimeter": updaters.perimeter,
                "noncompactness": metrics.noncompactness,
                "polsby_popper": metrics.polsby_popper,
                "imbalance": metrics.imbalance,
                "balance": metrics.balance,
                "objective": lambda p: w * p['imbalance'] + (1 - w) * p['noncompactness']
            })
        return initial_partition

    def part_to_sol(self, partition, util):
        """

        """
        # Transform a partition to a solution
        district_list = set()
        districts, district_ids = dict(), dict()

        polygons, attributes = self.args[3], self.args[6]

        for index, district_id in partition.assignment.items():
            location = polygons[attributes['Location']][index]
            district_ids[location] = district_id

            if district_id in district_list:
                districts[district_id]['MEMBERS'].append(location)
            else:
                districts[district_id] = util.get_params(MEMBERS=[location],
                                                         DISTRICT=district_id)
                district_list.add(district_id)

        update_property(districts.keys(), self.args, districts)
        final = util.get_partition(districts, district_ids)

        return final

    def create_chain(self, initial_partition):
        """

        """
        # Add the custom constraints for the sampler
        no_vanishing_districts = constraints.no_vanishing_districts
        no_centerless_districts = constraints.no_centerless_districts
        compactness_bound = constraints.no_worse_L_minus_1_polsby_popper
        # compactness_bound = constraints.no_worse_L1_reciprocal_polsby_popper
        # the above line is commented as it throws  'SelfConfiguringUpperBound' object has no attribute '__name__'

        if self.algo == 'BAA':
            '''
            single flip contiguous; balanced, always accept (default)
            This is the default version which is constrained by two custom-made constraints
            compactness_bound: sets a lower bound on the Lminus1 norm of the PP metric
            better_balanced_than_initial: ensures that the newly proposed solutions are better than the initial 
            partition in terms of imbalance
            '''
            better_balanced_than_initial = constraints.UpperBound(
                lambda p: p["imbalance"], initial_partition["imbalance"]
            )
            # Initialize the chain
            chain = MarkovChain(
                proposal=proposals.propose_random_flip,
                constraints=[no_vanishing_districts,
                             no_centerless_districts,
                             compactness_bound,
                             better_balanced_than_initial,
                             constraints.single_flip_contiguous,
                             ],
                accept=accept.always_accept,
                initial_state=initial_partition,
                total_steps=self.number_of_flips
            )
        elif self.algo == 'BCAA':
            '''
            Balanced and Compact; Always Accept
            This is built on top of the default BAA Model by replacing the above two custom-made constraints with 
            another constraint.
            improving_objective_bound: ensures that the newly sampled partitions have better objective than the initial 
            partition.
            '''
            # Add the custom constraints for the sampler
            improving_objective_bound = constraints.UpperBound(
                lambda p: p['objective'], initial_partition['objective']
            )
            # Initialize the chain
            chain = MarkovChain(
                proposal=proposals.propose_random_flip,
                constraints=[no_vanishing_districts,
                             no_centerless_districts,
                             compactness_bound,
                             improving_objective_bound,
                             constraints.single_flip_contiguous
                             ],
                accept=accept.always_accept,
                initial_state=initial_partition,
                total_steps=self.number_of_flips
            )
        elif self.algo == 'AIO':
            '''
            single flip contiguous always accept improving (objective)
            This is based on the BCAA model by replacing the improving_objective_bound by a always accept improving
            acceptance condition. This helps to impart a greedy nature to the algorithm.
            '''
            # Initialize the chain
            chain = MarkovChain(
                proposal=proposals.propose_random_flip,
                constraints=[no_vanishing_districts,
                             no_centerless_districts,
                             compactness_bound,
                             constraints.single_flip_contiguous
                             ],
                accept=accept.always_accept_improving,
                initial_state=initial_partition,
                total_steps=self.number_of_flips
            )
        else:
            # Add the custom constraints for the sampler
            pop_constraint = constraints.better_balanced_than_initial(initial_partition)
            # Initialize the chain
            chain = MarkovChain(
                proposal=proposals.propose_random_flip,
                constraints=[no_vanishing_districts,
                             no_centerless_districts,
                             pop_constraint,
                             constraints.single_flip_contiguous,
                             constraints.no_worse_L_minus_1_polsby_popper
                             ],
                accept=accept.always_accept,
                initial_state=initial_partition,
                total_steps=self.number_of_flips
            )

        return chain


class Sampling(MCMC):

    def search(self, run, argv):
        """
        Sampling technique using graph-based MCMC
        """
        (initialization, state) = argv
        initial = self.solution
        # args = (population, capacity, adjacency, polygons, polygons_nbr, schools, attributes)
        polygons, attributes = self.args[3], self.args[6]
        w = 0.1 * attributes['weight']

        # Create the initial partition
        initial_partition = self.create_partition()
        # Create the initial chain
        chain = self.create_chain(initial_partition)

        # Iterate through the chain and save the best performing partitions
        best_partition = initial_partition
        best_func_val = w * best_partition['imbalance'] + (1 - w) * best_partition['noncompactness']
        print('The initial partition of run {} has functional value: {:.4f}'.format(run, best_func_val))

        t_start = time.time()

        for f, partition in enumerate(chain.with_progress_bar()):
            # Updating the best solution found so far
            if partition['objective'] <= best_func_val:
                best_partition = partition
                best_func_val = partition['objective']

        t_elapsed = (time.time() - t_start) / 60.0  # measures in minutes
        termination = "end of chain reached"
        print('Simulated {} flips for run {} of {}-based MCMC in {:.2f} min'.format(self.number_of_flips, run,
                                                                                    self.algo, t_elapsed))
        print('The final partition of run {} has functional value: {:.4f}\n'.format(run, best_func_val))
        util = Utils(self.args)
        final = self.part_to_sol(best_partition, util)

        # Settings variables of the run
        alg_params = util.get_params(w1=w, w2=1-w,
                                     NumberOfFlips=self.number_of_flips)
        prop, info = util.get_alg_params(run, alg_params, self.number_of_flips, t_elapsed, termination, self.seed,
                                         initialization, state, initial, final)
        return {'properties': prop, 'info': info}

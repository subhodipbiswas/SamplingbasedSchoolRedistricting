import math


def compute_polsby_popper(area, perimeter):
    try:
        return 4 * math.pi * area / perimeter ** 2
    except ZeroDivisionError:
        return math.nan


def polsby_popper(partition):
    """Computes Polsby-Popper compactness scores for each district in the partition.
    """
    return {
        part: compute_polsby_popper(
            partition["area"][part], partition["perimeter"][part]
        )
        for part in partition.parts
    }

# Added by Subhodip Biswas <subhodip@vt.edu>


def mean_polsby_popper(partition):
    """Computes the mean Polsby-Popper compactness scores of all the districts in the partition.
    """
    if 'polsby_popper' in partition.keys():
        pps = partition['polsby_popper']
    else:
        pps = polsby_popper(partition)

    return sum(pps.values()) / len(partition)


def noncompactness(partition):
    """Computes the mean noncompactness scores of all the districts in the partition. The higher
    the value of this score, the more non-compact the distsricts are (on an average).
    """
    return 1 - mean_polsby_popper(partition)


def weighted_polsby_popper(partition):
    """Computes the mean Polsby-Popper compactness scores of all the districts in the partition
    weighted by the population.
    """

    if 'polsby_popper' in partition.keys():
        pps = partition['polsby_popper']
    else:
        pps = polsby_popper(partition)

    return sum([partition['population'][part] * pp for part, pp in pps.items()]) /\
           sum(partition['population'].values())

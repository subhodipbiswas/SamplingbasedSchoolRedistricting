# Added by Subhodip Biswas <subhodip@vt.edu>
def imbalance(partition, pop_key="population", target_key="capacity"):
    return sum(
        [abs(1 - partition[pop_key][d] / partition[target_key][d])
         for d in partition[pop_key].keys()]
    ) / len(partition[pop_key])


def balance(partition, pop_key="population", target_key="capacity"):
    return sum(
        [1 - abs(1 - partition[pop_key][d] / partition[target_key][d])
         for d in partition[pop_key].keys()]
    ) / len(partition[pop_key])

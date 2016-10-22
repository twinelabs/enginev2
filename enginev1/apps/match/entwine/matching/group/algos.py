"""
algos
-------------------------

"""

import algo_all


ALGORITHMS = {
    'order' : algo_all.cluster_order,
    'random': algo_all.cluster_random,
    'fullsearch': algo_all.cluster_fullsearch,
    'greedy': algo_all.cluster_greedy,
    'adaptive': algo_all.cluster_adaptive,
    'greedy_adaptive': algo_all.cluster_greedy_adaptive
 }


def find_groups(distance_matrix, match_config):

    algo_name = match_config['algorithm']['name']
    params = match_config['algorithm']['params']

    algo = ALGORITHMS.get(algo_name, False)
    if not algo:
        raise ValueError("Grouping function not implemented: " + algo_name)

    groups = algo(distance_matrix, params)
    return groups
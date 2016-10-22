"""
algos
-------------------------

"""

import algo_nrmp


ALGORITHMS = {
    'nrmp' : algo_nrmp.residency,
}


def find_assignments(utility_matrix, match_config):

    algo_name = match_config['algorithm']['name']
    algo_params = match_config['algorithm']['params']

    algo = ALGORITHMS.get(algo_name, False)
    if not algo:
        raise ValueError("Assignment function not implemented: " + algo_name)

    assignments = algo(utility_matrix, algo_params)
    return assignments
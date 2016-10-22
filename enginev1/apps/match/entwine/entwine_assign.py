"""
entwine_assign
--------

Runs matching process for assignment task.
"""

import time
import pdb

from matching.assign.utilities import calc_utility_matrix
from matching.assign.algo_nrmp import find_assignments
import etl.load


def load(load_cfg):
    """ Loads 2 data frames for assignment.
    """

    if len(load_cfg) != 2:
        raise ValueError('Should load only two files for assignment task.')

    dfs = etl.load.load_from_config(load_cfg)
    return dfs


def assign_analytics(dfs, assignments):
    return None


def assign(dfs, match_cfg):
    """ Runs assignment using match configuration parameters.
    Returns results, simple statistics, and analytics.
    """

    start_time = time.time()

    utility_matrix = calc_utility_matrix(dfs, match_cfg)
    utility_time = time.time()

    assignments = find_assignments(utility_matrix, match_cfg)
    results_time = time.time()

    output = {}
    output['results'] = assignments

    stats = [
        { 'name': 'utility_time', 'value': utility_time - start_time },
        { 'name': 'results_time', 'value': results_time - utility_time },
        { 'name': 'total_time', 'value': results_time - start_time },
        { 'name': 'n_A', 'value': dfs[0].shape[0] },
        { 'name': 'n_B', 'value': dfs[1].shape[0] },
        { 'name': 'n_components', 'value': len(match_cfg['components']) }
    ]
    output['stats'] = stats

    output['analytics'] = assign_analytics(dfs, assignments)

    return output


def entwine_assign(config):
    """ Loads data objects and match config, runs assignment.
    """

    load_cfg = config['load']
    dfs = load(load_cfg)

    match_cfg = config['match']
    output = assign(dfs, match_cfg)

    return output

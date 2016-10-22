"""
entwine_cluster
--------

Runs matching process for clustering task.
"""

import time

from matching.group.utilities import calc_distance_matrix
from matching.group.algos import find_groups
import etl.load


def load(load_cfg):
    """ Loads data frame for clustering.
    """

    if len(load_cfg) != 1:
        raise ValueError('Should load only one file for clustering task.')

    dfs = etl.load.load_from_config(load_cfg)
    df = dfs[0]
    return df


def group_analytics(df, groups):
    return None


def group(df, match_cfg):
    """ Runs clustering using match configuration parameters.
    Returns results, simple statistics, and analytics.
    """

    start_time = time.time()

    distance_matrix = calc_distance_matrix(df, match_cfg)
    distance_time = time.time()

    groups = find_groups(distance_matrix, match_cfg)
    results_time = time.time()

    output = {}
    output['results'] = groups

    stats = []
    stats.append({ 'name': 'distance_time', 'value': distance_time - start_time })
    stats.append({ 'name': 'results_time', 'value': results_time - distance_time })
    stats.append({ 'name': 'total_time', 'value': results_time - start_time })
    stats.append({ 'name': 'n_rows', 'value': df.shape[0] })
    stats.append({ 'name': 'n_cols', 'value': df.shape[1] })
    stats.append({ 'name': 'n_components', 'value': len(match_cfg['components']) })
    stats.append({ 'name': 'k_size', 'value': match_cfg['algorithm']['params']['k_size'] })
    output['stats'] = stats

    output['analytics'] = group_analytics(df, groups)

    return output


def entwine_group(config):
    """ Loads data and match config, runs clustering.
    """

    load_cfg = config['load']
    df = load(load_cfg)

    match_cfg = config['match']
    output = group(df, match_cfg)

    return output
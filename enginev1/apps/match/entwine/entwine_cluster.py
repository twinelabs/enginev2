"""
entwine_cluster
--------

Runs matching process for clustering task.
"""

import time

import matching.clustering.distance
import matching.clustering.run_new
import etl.load


def load(load_cfg):
    """ Loads data frame for clustering.
    """

    if len(load_cfg) != 1:
        raise ValueError('Should load only one file for clustering task.')

    dfs = etl.load.load_from_config(load_cfg)
    df = dfs[0]
    return df


def cluster_analytics(df, clusters):
    return None


def cluster(df, match_cfg):
    """ Runs clustering using match configuration parameters.
    Returns results, simple statistics, and analytics.
    """

    start_time = time.time()

    distance_matrix = matching.clustering.distance.create_weighted_matrix(df, match_cfg)
    distance_time = time.time()

    clusters = matching.clustering.run_new.cluster(distance_matrix, match_cfg)
    results_time = time.time()

    output = {}
    output['results'] = clusters

    stats = []
    stats.append({ 'name': 'distance_time', 'value': distance_time - start_time })
    stats.append({ 'name': 'results_time', 'value': results_time - distance_time })
    stats.append({ 'name': 'total_time', 'value': results_time - start_time })
    stats.append({ 'name': 'n_rows', 'value': df.shape[0] })
    stats.append({ 'name': 'n_cols', 'value': df.shape[1] })
    stats.append({ 'name': 'n_components', 'value': len(match_cfg['components']) })
    stats.append({ 'name': 'k_size', 'value': match_cfg['algorithm']['params']['k_size'] })
    output['stats'] = stats

    output['analytics'] = cluster_analytics(df, clusters)

    return output


def entwine_cluster(config):
    """ Loads data and match config, runs clustering.
    """

    load_cfg = config['load']
    df = load(load_cfg)

    match_cfg = config['match']
    output = cluster(df, match_cfg)

    return output
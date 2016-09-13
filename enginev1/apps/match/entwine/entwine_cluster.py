"""
entwine_cluster
--------

Runs matching process for clustering task.
"""

import time
import pandas as pd

import matching.clustering.distance
import matching.clustering.run_new

from enginev1.apps.dataset import models


def load(load_config):
    """ Loads data object from DataTable or file.
    Stores as (or converts to) pandas dataframe.
    """

    if len(load_config) != 1:
        raise ValueError('Should only specify one file for clustering task.')

    d = load_config[0]

    if 'data_table' in d:
        data_table_id = d['data_table']['id']
        data_table = models.DataTable.objects.get(pk=data_table_id)
        df = data_table.as_df()

    elif 'file' in d:
        f = d['file']['name']
        if d['file']['type'] == 'csv':
            df = pd.DataFrame.from_csv(f)
        else:
            raise TypeError('Unsupported or missing file type. (in config[load][file][type])')

    else:
        raise TypeError('Unsupported or missing load data. (in config[load]')
    
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

    output = {
        'results': clusters,
        'stats': {
            'distance_time': distance_time - start_time,
            'results_time': results_time - distance_time,
            'total_time': results_time - start_time,
            'n_rows': df.shape[0],
            'n_cols': df.shape[1],
            'n_components': len(match_cfg['components']),
            'k_size': match_cfg['algorithm']['params']['k_size']
        }
    }

    output['analytics'] = cluster_analytics(df, clusters)

    return output


def entwine_cluster(config):
    """ Loads data and match config, runs clustering.
    """

    df = load(config['load'])
    match_cfg = config['match']
    output = cluster(df, match_cfg)

    return output
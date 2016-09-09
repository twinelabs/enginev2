"""
run_cluster
--------

Runs matching process for clustering.
"""

import time
import yaml
import sys

import pandas as pd
import pdb

import matching.clustering.distance
import matching.clustering.run_new

from enginev1.apps.dataset import models, utils

# Loads data or a file. Returns a pandas dataframe.
def load(load_config):
    if len(load_config) != 1:
        print('Should only specify one file for clustering task.')
        return None
    df = ''
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
            print('Please provide a valid file type.')
    else:
        print('Please provide data table or file.')
    
    return df

# Runs clustering
def match(df, match_config):
    distance_matrix = matching.clustering.distance.create_weighted_matrix(df, match_config)
    results = matching.clustering.run_new.cluster(distance_matrix, match_config)        
    return results

def run_from_config(config):
    # All final output goes into one dictionary
    output = {}
    # Load data into a pandas dataframe
    output['df'] = load(config['load'])
    # Matching
    start_time = time.time()
    output['results'] = match(output['df'], config['match'])
    stop_time = time.time()
    output['match_time'] = stop_time - start_time
    # Return the entire output
    output['df'] = False
    return output

if __name__ == '__main__':

    if len(sys.argv) > 1:

        config_file = sys.argv[1]

        with open(config_file, 'r') as f:
            config = yaml.load(f)

        output = run_from_config(config)

    else:
        print('Please provide a configuration file.')

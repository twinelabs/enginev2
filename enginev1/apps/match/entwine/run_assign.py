"""
run_assign
--------

Runs matching process for assignment.
"""

import time
import yaml
import sys

import pandas as pd

import matching.assign.utility
import matching.assign.run_new

# Loads data or a file. Returns a pandas dataframe.
def load(load_config):
    if len(load_config) != 2:
        print('Should specify two files for assignment task.')
        return None
    dfs = []
    for d in load_config:
        if 'data_table' in d:
            obj = d['data']['obj']
            if d['data']['type'] == 'json':
                dfs.append(pd.read_json(obj))
            else:
                print('Please provide a valid data type.')
        elif 'file' in d:
            f = d['file']['name']
            if d['file']['type'] == 'csv':
                dfs.append(pd.DataFrame.from_csv(f))
            else:
                print('Please provide a valid file type.')
        else:
            print('Please provide data or file.')
                  
    return dfs

# Runs assignment
def match(dfs, match_config):
    utility_matrix = matching.assign.utility.utility_matrix(dfs, match_config)
    # Assume that we always run the residency algorithm, for now
    results = matching.assign.run_new.residency(utility_matrix, match_config)        
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
    return output

if __name__ == '__main__':

    if len(sys.argv) > 1:

        config_file = sys.argv[1]

        with open(config_file, 'r') as f:
            config = yaml.load(f)

        output = run_from_config(config)

    else:
        print('Please provide a configuration file.')

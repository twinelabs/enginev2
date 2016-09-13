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
def assign(dfs, match_cfg):
    utility_matrix = matching.assign.utility.utility_matrix(dfs, match_cfg)
    results = matching.assign.run_new.residency(utility_matrix, match_cfg)
    return results


def entwine_assign(config):
    """ Loads data objects and match config, runs assignment.
    """

    dfs = load(config['load'])
    match_cfg = config['match']
    output = assign(dfs, match_cfg)

    return output

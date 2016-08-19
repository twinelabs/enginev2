"""
evaluate_diversity
--------

Runs multiple algorithms to compare their diversity outputs.
"""

import pandas as pd
import sys
import yaml
import copy
import run
import string
import analytics.data_generator

alphabet = [char for char in string.ascii_uppercase]

# GLOBALS in dictionary form. The default parameter dictionary for evaluate_config
globs = {
         'n'        : 100, # Data set size
         'm'        : 2,   # Number of categories
         'probs'    : [],  # Probability distribution for the categories
         'k'        : 5,   # Cluster size
         'algos'    : ["greedy_adaptive"],
         'num_swaps': 100,  # Number of swaps in adaptive search,
         'iter'     : 1 # Iteration number
        }

def evaluate_config(config_file, p=globs):
    # Output dictionary. Contains one entry for each algorithm tested.
    output = {}
    # Metrics is the subset of each full output that we care about.
    metrics = []
    # Times for each algorithm ran.
    times = []
    
    # Creates a new test_file every time. Calls with n=100, m=5, mean=10, std=2, div=False
    analytics.data_generator.create_category_data(p['n'], p['m'], p['probs'])
    with open(config_file, 'r') as f:
        base_config = yaml.load(f)
        # Set global parameters
        base_config['match']['params']['k_size'] = p['k']
        base_config['match']['params']['num_swaps'] = p['num_swaps']
    for algo in p['algos']:
        algo_config = copy.copy(base_config) 
        algo_config['match']['params']['method'] = algo
        output[algo] = run.run_from_config(algo_config)
        times.append(output[algo]['match_time'])
        metrics.append(output[algo]['evaluate_results']['diversity']['class'])
        
    metrics = pd.DataFrame(metrics, index=p['algos']) 
    # Add time as a column to the dataframe
    metrics['time'] = times
    print(metrics)
    return metrics
        
if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        evaluate_config(config_file)        
    else:
        print('Please provide a configuration file!')
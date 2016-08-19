"""
evaluate_algorithms
--------

Runs multiple algorithms to compare their outputs.
"""

import pandas as pd
import sys
import yaml
import copy
import run
import analytics.data_generator

# GLOBALS in dictionary form. The default parameter dictionary for evaluate_config
globs = {
         'n'        : 100, # Data set size
         'm'        : 6,   # Number of features
         'mean'     : 10,
         'std'      : 2,
         'k'        : 5,   # Cluster size
         'algos'    : ["random", "greedy", "adaptive", "greedy_adaptive"],
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
    # Iterations of the algorithm?? - Fix?
    
    # Creates a new test_file every time. Default calls with n=100, m=5, mean=10, std=2
    analytics.data_generator.create_numeric_data(p['n'], p['m'], p['mean'], p['std'])
    with open(config_file, 'r') as f:
        base_config = yaml.load(f)
        # Set global parameters
        base_config['match']['params']['k_size'] = p['k']
        base_config['match']['params']['num_swaps'] = p['num_swaps']
        base_config['match']['distance']['cols'] = ['f%s' % s for s in xrange(p['m'])]
        base_config['evaluate']['distance']['cols'] = ['f%s' % s for s in xrange(p['m'])]
        
    for algo in p['algos']:
        algo_config = copy.copy(base_config) 
        algo_config['match']['params']['method'] = algo
        output[algo] = run.run_from_config(algo_config)
        times.append(output[algo]['match_time'])
        metrics.append(output[algo]['evaluate_results']['distance'])
        
    metrics = pd.DataFrame(metrics, index=p['algos']) 
    # Add time as a column to the dataframe
    metrics['time'] = times
    # Delete column of "count" in the dataframe
    metrics = metrics.drop('count', axis=1)
    # Reorder the columns by ascending mean.
    metrics = metrics.sort(columns='mean')
    print(metrics)
    return metrics
        
if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        evaluate_config(config_file)        
    else:
        print('Please provide a configuration file!')
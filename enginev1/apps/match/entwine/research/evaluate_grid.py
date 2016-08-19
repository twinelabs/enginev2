"""
evaluate_grid
--------

Runs evaluate_algorithms with different parameters to compare their outputs.
"""

import evaluate_algorithms
import pandas as pd
import sys
import yaml

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
    dfs = []
    with open(config_file, 'r') as f:
        base_config = yaml.load(f)
    grid_params = base_config['grid']
    
    for n in grid_params['n']:
        p['n'] = n
        for k in grid_params['k']:
            p['k'] = k
            for num_swaps in grid_params['num_swaps']:
                p['num_swaps'] = num_swaps
                for i in xrange(grid_params['iter']):
                    p['iter'] = i+1
                    metrics = evaluate_algorithms.evaluate_config(config_file, p)
                    # Add columns to indicate the set parameters
                    metrics['n'] = p['n']
                    metrics['m'] = p['m']
                    metrics['k'] = p['k']
                    metrics['num_swaps'] = p['num_swaps']
                    metrics['iter'] = p['iter']
                    dfs.append(metrics)
                
    final_df = pd.concat(dfs)
    final_df = final_df.sort(columns=['n','m','k','num_swaps','iter'])
    print(final_df)
    return final_df
        
if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        final_df = evaluate_config(config_file)    
        final_df.to_csv('eval_grid.csv')    
    else:
        print('Please provide a configuration file!')
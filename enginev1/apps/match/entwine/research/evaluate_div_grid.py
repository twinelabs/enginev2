"""
evaluate_grid
--------

Runs evaluate_algorithms with different parameters to compare their outputs.
"""

import evaluate_diversity
import numpy as np
import pandas as pd
import sys
import yaml

# GLOBALS in dictionary form. The default parameter dictionary for evaluate_config
globs = {
         'n'        : 100, # Data set size
         'm'        : 2,   # Number of categories
         'k'        : 5,   # Cluster size
         'algos'    : ["greedy_adaptive"],
         'num_swaps': 100,  # Number of swaps in adaptive search,
         'iter'     : 1 # Iteration number
        }

# For the probability distributions for different values of m
third = float(1) / 3
probs = {
         2 : [[0.5,0.5],[0.75,0.25],[0.9,0.1]],
         3 : [[third,third,third],[0.5,0.25,0.25],[0.8,0.1,0.1]] 
        }

def evaluate_config(config_file, p=globs):
    mean_dfs = []
    with open(config_file, 'r') as f:
        base_config = yaml.load(f)
    grid_params = base_config['grid']
    
    for n in grid_params['n']:
        p['n'] = n
        for m in grid_params['m']:
            p['m'] = m
            for dist in probs[m]:
                p['probs'] = dist
                for k in grid_params['k']:
                    p['k'] = k
                    # Keep a list of all dataframes for the iterations - to be averaged!
                    dfs_iter = []
                    for i in xrange(grid_params['iter']):
                        p['iter'] = i+1
                        metrics = evaluate_diversity.evaluate_config(config_file, p)
                        dfs_iter.append(metrics)
                    # Concatenate all dfs, to be averaged
                    df = pd.concat(dfs_iter) 
                    # Take out example list of entropies
                    example_entropies = df['All Cluster Entropy'][0]
                    df = df.drop('All Cluster Entropy', 1)
                    # Mean of all values over the number of iterations 
                    mean_df = pd.DataFrame(df.mean()).T
                    # Now add back the column of averaged individual entropies
                    mean_df['Example Cluster Entropy'] = str(example_entropies)
                    # Add columns to indicate the set parameters
                    mean_df['n'] = p['n']
                    mean_df['m'] = p['m']
                    mean_df['probs'] = str(p['probs'])
                    mean_df['k'] = p['k']
                    mean_df['num_swaps'] = p['num_swaps']
                    mean_df.index = p['algos']
                    mean_dfs.append(mean_df)
                    print(mean_df)
                    
    final_df = pd.concat(mean_dfs)
    final_df = final_df.sort(columns=['n','m','k','num_swaps'])
    return final_df
        
if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        final_df = evaluate_config(config_file)    
        final_df.to_csv('eval_div_grid.csv')    
    else:
        print('Please provide a configuration file!')
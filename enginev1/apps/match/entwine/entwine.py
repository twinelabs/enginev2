"""
run_match
--------

Runs matching process for specified match task.
Currently supports clustering and assignment.
"""

import sys
import yaml
import run_cluster
import run_assign
import pdb

def run_from_config(config):
    output = None
    if config['match']['task'] == 'cluster':
        output = run_cluster.run_from_config(config)
    elif config['match']['task'] == 'assign':
        output = run_assign.run_from_config(config)
    else:
        print('Unsupported match task. Config file should specify match or assign.')
    return output

if __name__ == '__main__':

    if len(sys.argv) > 1:

        config_file = sys.argv[1]

        with open(config_file, 'r') as f:
            config = yaml.load(f)

        output = run_from_config(config)
        print(output)

    else:
        print('Please provide a configuration file.')

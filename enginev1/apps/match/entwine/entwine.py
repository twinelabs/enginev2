"""
entwine
--------

Executes matching for specified match task.
Runs from config dictionary or from file.
"""

import sys
import yaml

from entwine_group import entwine_group
from entwine_assign import entwine_assign

def run_from_config(config):
    """ Run matching process from config dictionary specifying match parameters.
    """
    output = None

    if config['match']['task'] == 'group':
        output = entwine_group(config)
    elif config['match']['task'] == 'assign':
        output = entwine_assign(config)
    else:
        print('Unsupported or missing task type in match config. (in config[match][task])')
    return output


# ===
# COMMAND LINE INTERFACE (internal/research use)
# ===

if __name__ == '__main__':

    if len(sys.argv) > 1:
        config_file = sys.argv[1]

        with open(config_file, 'r') as f:
            config = yaml.load(f)

        output = run_from_config(config)
        print(output)

    else:
        print('Please provide a configuration file.')

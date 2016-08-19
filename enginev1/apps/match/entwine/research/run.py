"""
run
--------

Runs matching process.
"""

import copy

import time

import utils.io.io_csv

import analytics

import etl.match_data
import etl.qualtrics_data

import matching.distance.A_functions
import matching.distance.AB_functions

import matching.assign.symmetric
import matching.clustering.run

import display.assignments
import display.clusters

import yaml
import sys

import pdb


def load_match_data_list(load_config):
    """ Creates list of match data objects.
    """

    prefix = load_config['prefix'] if 'prefix' in load_config else ''
    suffix = load_config['suffix'] if 'suffix' in load_config else ''

    match_data_list = []

    for md in load_config['mds']:

        #
        # LOAD DATA FILE

        filename = prefix + md['filename'] + suffix
        if not 'type' in md:
            raise TypeError("No file type specified in load config.")
        elif md['type'] == 'csv':
            data_file = utils.io.io_csv.load_csv(filename)
        else:
            raise TypeError("Attempt to load unsupported file type: " + md['type'])

        #
        # ETL

        if not 'etl' in md:
            raise TypeError("No ETL type specified in load config.")
        elif md['etl'] == "none":
            match_data = etl.match_data.MatchData(data_file, md['desc'])
        elif md['etl'] == "qualtrics":
            n_skip = md['n_skip'] if 'n_skip' in md else 0
            match_data = etl.qualtrics_data.QualtricsData(data_file, md['desc'], n_skip)
        else:
            raise TypeError("Attempt to transform unsupported ETL type: " + md['etl'])

        match_data_list.append(match_data)

    return match_data_list


# ---
# REMAPPING
# ---

def in_dict(val, m):
    return m[val] if val in m else val

def load_dicts(dicts_config):

    prefix = dicts_config['prefix'] if 'prefix' in dicts_config else ''
    suffix = dicts_config['suffix'] if 'suffix' in dicts_config else ''

    dicts = {}
    for dict_config in dicts_config['dicts']:

        filename = prefix + dict_config['filename'] + suffix
        if dict_config['type'] == 'csv':
            data_file = utils.io.io_csv.load_csv(filename)
        else:
            raise TypeError("Attempt to load unsupported file type")

        dicts[dict_config['name']] = dict(data_file)

    return dicts


def remap_match_data_list(mdl, remap_config):
    """ Applies custom map to match data list, returning new match data list
    with new columns and new data according to given functions.

    :param match_data: Match data list
    :param remap_config: map configuration to apply, in format
    :return: Remapped match data list.
    """

    dicts = load_dicts(remap_config['dicts_data'])

    mdl_new = []
    for i, map_config in enumerate(remap_config['maps']):

        md_old = mdl[i]

        data_copy = copy.deepcopy(md_old.data)
        data_new = []

        for row_old in data_copy:

            row_new = []
            for map_item in map_config:

                if isinstance(map_item['i'], list):
                    i_s = map_item['i_s'] if 'i_s' in map_item else ''
                    item_old = i_s.join([row_old[i] for i in map_item['i']])

                else:
                    item_old = row_old[map_item['i']]


                if map_item['f'] == "none":
                    item_new = item_old

                elif map_item['f'] == "equality":
                    valid = map_item['f_val']
                    if isinstance(valid, list):
                        item_new = (item_old in valid)
                    else:
                        item_new = (item_old == valid)

                elif map_item['f'] == "contains":
                    item_new = map_item['f_true'] if map_item['f_s'] in item_old else map_item['f_false']

                elif map_item['f'] == "in_dict":
                    item_new = in_dict(item_old, dicts[map_item['f_dict']])

                elif map_item['f'] == "concatenate_dicts":
                    inds = []
                    for j, i in enumerate(map_item['i']):
                        inds += in_dict(row_old[i], dicts[map_item['f_dicts'][j]]).split('+')
                    inds = [ind for ind in inds if ind != '']
                    inds = '+'.join(list(set(inds)))
                    item_new = inds

                elif map_item['f'] == "trimright":
                    item_new = item_old[-map_item['n']:]

                else:
                    raise TypeError("Map function not implemented: " + map_item['f'])

                row_new.append(item_new)
            data_new.append(row_new)

        header = [ map_item['col'] for map_item in map_config ]
        raw_data = [header] + data_new

        md_new = etl.match_data.MatchData(raw_data, 'remapped ' + md_old.desc, False)
        mdl_new.append(md_new)

    return mdl_new


def combine_match_data_list(mdl, combine_config):

    prefix = combine_config['prefix'] if 'prefix' in combine_config else ''
    suffix = combine_config['suffix'] if 'suffix' in combine_config else ''

    # new column names
    filename = prefix + combine_config['filename'] + suffix
    colnames = utils.io.io_csv.load_csv(filename)
    colnames = [row[0] for row in colnames]

    mdl_filtered = []
    for i, md in enumerate(mdl):

        # index mapping
        md_config = combine_config['mds'][i]
        index_map_filename = prefix + md_config['filename'] + suffix
        index_map = utils.io.io_csv.load_csv(index_map_filename)
        index_map = [row[0] for row in index_map]

        md_filtered = etl.match_data.filter_cols_by_index(md, index_map)
        mdl_filtered.append(md_filtered)

    combined_match_data = etl.match_data.combine(mdl_filtered, colnames)
    return [combined_match_data]

def match(mdl, match_config):
    """ Runs matches for match data list.
    """
    if match_config['type'] == 'assign':
        utility_matrix = matching.distance.AB_functions.utility_matrix(mdl, match_config)
        capacities = [5] * mdl[1].n_rows
        match_results = matching.assign.symmetric.residency(utility_matrix, capacities)

    elif match_config['type'] == 'cluster':
        distance_matrix = matching.distance.A_functions.distance_matrix(mdl, match_config['distance'])
        match_results = matching.clustering.run.cluster(distance_matrix, match_config['params'])

    else:
        raise TypeError("Match function not implemented")
        
    return match_results
    
def evaluate(mdl, clusters, match_config, evaluate_config):
    """ Evaluates match results based on select criteria.
    """
    # Why have the list of length 1 containing the match data?
    metrics = ''
    if match_config['type'] == 'cluster':
        metrics = analytics.goodness.cluster_evaluation.evaluate(mdl, clusters, match_config, evaluate_config)
    return metrics

def display_results(match_results, mdl, display_config):

    if display_config['display']['type'] == 'assign':
        display_results = display.assignments.display_results(match_results, mdl, config['match'])
    elif display_config['display']['type'] == 'cluster':
        display_results = display.clusters.display_results(match_results, mdl[0])
    else:
        raise TypeError("Display results not implemented for this function type")

    return display_results


def save_match_results(results, save_config):
    """ Saves down match results files.
    """

    prefix = save_config['prefix'] if 'prefix' in save_config else ''
    suffix = save_config['suffix'] if 'suffix' in save_config else ''

    for result in save_config['results']:

        varname = result['varname']
        filename = prefix + result['filename'] + suffix

        if result['type'] == 'csv':
            utils.io.io_csv.save_csv(results[varname], filename)
        else:
            raise TypeError("Attempt to save unsupported file type")


def run_from_config(config):

    output = {}
    if 'load' in config:
        output['mdl'] = load_match_data_list(config['load'])

    if 'remap' in config:
        output['mdl'] = remap_match_data_list(output['mdl'], config['remap'])

    if 'combine' in config:
        output['mdl'] = combine_match_data_list(output['mdl'], config['combine'])

    if 'match' in config:
        start_time = time.time()
        output['match_results'] = match(output['mdl'], config['match'])
        stop_time = time.time()
        output['match_time'] = stop_time - start_time
        
    if 'evaluate' in config:
        output['evaluate_results'] = evaluate(output['mdl'], output['match_results'], config['match'], config['evaluate'])

    if 'display' in config:
        output['display_results'] = display_results(output['match_results'], output['mdl'], config)

    if 'save' in config:
        save_match_results(output, config['save'])

    return output


if __name__ == '__main__':

    if len(sys.argv) > 1:

        config_file = sys.argv[1]

        with open(config_file, 'r') as f:
            config = yaml.load(f)

        run_from_config(config)

    else:
        print('Please provide a configuration file.')

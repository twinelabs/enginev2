"""
etl.remap
--------

Remap raw data with simple functions, dictionaries, and lookups.

"""

import copy
import etl.match_data


def apply_map(match_data, mmap):
    """ Applies custom map to match data, returning new match data object
    with new columns and new data according to given functions.

    :param match_data: Match data object
    :param mmap: map to apply, in format: [ ("column name", column_function), ... ]
    :return: Remapped match data object.

    """

    data_copy = copy.deepcopy(match_data.data)
    data = [[ f_col(row) for colname, f_col in mmap ] for row in data_copy ]

    header = [ colname for colname, f_col in mmap ]
    raw_data = [header] + data

    match_data_new = etl.match_data.MatchData(raw_data, 'remapped ' + match_data.desc, False)

    return match_data_new

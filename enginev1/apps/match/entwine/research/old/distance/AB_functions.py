"""
matching.distance.B_functions
-------------------------

Common functions to generate distance matrix from two data sets (A, B).

Scenarios:
(n, f1) + (m, f2) -> (n, m): feature vectors to utility matrix

"""

import numpy as np

def intersect(a, b):
    return list(set(a) & set(b))

def criteria_and_weights(criteria_config):
    matching_criteria = []
    matching_weights = []

    for crit_config in criteria_config:

        if crit_config['f'] == "equality":
            f_crit = lambda a, b: a == b

        elif crit_config['f'] == "inequality":
            f_crit = lambda a, b: a != b

        elif crit_config['f'] == "equality_nonblank":
            f_crit = lambda a, b: a == b if (a != "" or b != "") else False

        elif crit_config['f'] == "gte":
            f_crit = lambda a, b: float(a) >= float(b) if (b != "" and a != "") else False

        elif crit_config['f'] == "lte":
            f_crit = lambda a, b: float(a) <= float(b) if (b != "" and a != "") else False

        elif crit_config['f'] == "intersect":
            f_s = crit_config['f_s']
            f_crit = lambda a, b: len(intersect(a.split(f_s), b.split(f_s))) > 0

        elif crit_config['f'] == "b_contains_a":
            f_s = crit_config['f_s']
            f_crit = lambda a, b: a in b.split(f_s)

        else:
            raise TypeError("Matching criteria not implemented")

        criterion = (crit_config['col'], f_crit)
        matching_criteria.append(criterion)
        matching_weights.append(crit_config['wgt'])

    return matching_criteria, matching_weights


def submatches(match_data_A, i, match_data_B, j, matching_criteria, matching_weights):

    submatches = []
    for field, func in matching_criteria:

        s_val = match_data_A.grab_data_value(field, i)
        a_val = match_data_B.grab_data_value(field, j)
        f_result = func(s_val, a_val)

        submatches.append(f_result)

    return submatches


def calc_utility(submatches, matching_weights):
    utility = sum([match*weight for match, weight in zip(submatches, matching_weights)])
    return utility


def why_matched(submatches, matching_criteria):
    return ', '.join([matching_criteria[i][0] for i, submatch in enumerate(submatches) if submatch])


def utility_matrix(match_data_list, match_config):

    if len(match_data_list) != 2:
        raise TypeError("Match data list must have 2 items for AB_functions.utility_matrix")

    match_data_A = match_data_list[0]
    match_data_B = match_data_list[1]

    matching_criteria, matching_weights = criteria_and_weights(match_config['criteria'])

    n = match_data_A.n_rows
    m = match_data_B.n_rows

    utilities = []
    for i in range(n):

        utilities_row = []
        for j in range(m):

            sm = submatches(match_data_A, i, match_data_B, j, matching_criteria, matching_weights)
            utility = calc_utility(sm, matching_weights)
            utilities_row.append(utility)

        utilities.append(utilities_row)

    utilities = np.array(utilities)

    return utilities


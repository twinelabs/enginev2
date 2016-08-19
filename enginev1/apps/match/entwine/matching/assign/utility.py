"""
matching.assign.utility
-------------------------

Generate a utility matrix from two data sets. Used for assignment.
"""

import numpy as np

def intersect(a, b):
    return list(set(a) & set(b))

def get_matching_criteria(components_config):
    matching_criteria = []

    for component in components_config:

        if component['function'] == "equality":
            f_crit = lambda a, b: a == b

        elif component['function'] == "equality_nonblank":
            f_crit = lambda a, b: a == b if (a != "" or b != "") else False

        elif component['function'] == "gte":
            f_crit = lambda a, b: float(a) >= float(b) if (b != "" and a != "") else False

        elif component['function'] == "lte":
            f_crit = lambda a, b: float(a) <= float(b) if (b != "" and a != "") else False

        elif component['function'] == "intersect":
            f_s = component['f_s']
            f_crit = lambda a, b: len(intersect(a.split(f_s), b.split(f_s))) > 0

        elif component['function'] == "b_contains_a":
            f_s = component['f_s']
            f_crit = lambda a, b: a in b.split(f_s)

        else:
            raise TypeError("Matching criteria not implemented")

        criterion = (component['columns'], f_crit)
        matching_criteria.append(criterion)

    return matching_criteria

def calc_utility(submatches, matching_weights):
    return sum([match * weight for match,weight in zip(submatches, matching_weights)])

def why_matched(submatches, matching_criteria):
    return ', '.join([matching_criteria[i][0] for i, submatch in enumerate(submatches) if submatch])


def utility_matrix(dfs, match_config):
    if len(dfs) != 2:
        raise TypeError("Match data list must have 2 items for AB_functions.utility_matrix")

    # Helper function / subrountine. Makes more sense to be inside this function.        
    def submatches(matching_criteria):

        submatches = []
        for columns, func in matching_criteria:
            col_A = columns[0]
            col_B = columns[1]
            s_val = df_A[col_A][i]
            a_val = df_B[col_B][j]
            f_result = func(s_val, a_val)
    
            submatches.append(f_result)
    
        return submatches
        
    df_A = dfs[0]
    df_B = dfs[1]

    matching_criteria = get_matching_criteria(match_config['components'])
    matching_weights = match_config['weights']

    n = len(df_A)
    m = len(df_B)

    utilities = np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            sm = submatches(matching_criteria)
            utilities[i][j] = calc_utility(sm, matching_weights)

    return utilities


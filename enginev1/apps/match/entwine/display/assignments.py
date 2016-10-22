"""
display.assignments
--------

Scripts to display assignment results.

"""
import pdb
import json

from ..matching.assign.utilities import *


def pretty_csv(match):
    """ Constructs pretty CSV of matching results """

    cfg = match.config['match']
    assignments = json.loads(match.result['results'])

    dt_B = match.data_tables.all()[0]
    df_B = dt_B.as_df()
    dt_B_values = dt_B.values()

    dt_A = match.data_tables.all()[1]
    df_A = dt_A.as_df()
    dt_A_values = dt_A.values()

    matching_criteria = get_matching_criteria(cfg['components'])
    matching_weights = cfg['weights']

    neg_utilities = []

    results = []
    for i, matches in enumerate(assignments):

        # If any A assigned to this B:
        if matches:
            curr_rows = []
            for j, m in enumerate(matches):

                sm = []
                for columns, func in matching_criteria:
                    col_A = columns[0]
                    col_B = columns[1]
                    s_val = df_A[col_A][m]
                    a_val = df_B[col_B][i]
                    f_result = func(s_val, a_val)

                    sm.append(f_result)

                utility = calc_utility(sm, matching_weights)

                curr_row = [utility, ''] + dt_A_values[m] + ['<->'] + dt_B_values[i] + [''] + sm
                curr_rows.append(curr_row)

        # If no A assigned to this B:
        else:
            curr_rows = [['',''] * dt_A.n_cols + ['no match'] + dt_B_values[i]]
            utility = 0

        results.append(curr_rows)
        neg_utilities.append(-1*utility)

    results = [result for (neg_utility, result) in sorted(zip(neg_utilities, results))]

    header = [['Twine score', ''] + dt_A.header() + ['***'] + dt_B.header() + ['']]
    res = header + [row for result in results for row in result]

    return(res)

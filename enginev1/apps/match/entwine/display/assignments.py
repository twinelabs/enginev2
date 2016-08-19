"""
display.assignments
--------

Scripts to display assignment results.

"""
import pdb

import matching.distance.AB_functions

def display_results(assignments, match_data_list, match_config):
    """ Constructs pretty CSV of matching results """

    if len(match_data_list) != 2:
        raise TypeError("Match data list must have 2 items for display.assignments.pretty_results")

    match_data_A = match_data_list[0]
    match_data_B = match_data_list[1]

    data_A = match_data_A.data
    data_B = match_data_B.data

    matching_criteria, matching_weights = matching.distance.AB_functions.criteria_and_weights(match_config['criteria'])

    results = []
    neg_utilities = []
    for i, matches in enumerate(assignments):

        # If any A assigned to this B:
        if matches:
            curr_rows = []
            for j, m in enumerate(matches):

                submatches = matching.distance.AB_functions.submatches(match_data_A, m, match_data_B, i, matching_criteria, matching_weights)
                why_matched = matching.distance.AB_functions.why_matched(submatches, matching_criteria)

                utility = matching.distance.AB_functions.calc_utility(submatches, matching_weights)
                curr_row = data_A[m] + ['<->'] + data_B[i] + ['', why_matched] + submatches
#                print(str(m) + ' and ' + str(i))
                curr_rows.append(curr_row)

        # If no A assigned to this B:
        else:
            curr_rows = [[''] * match_data_A.n_cols + ['no match'] + data_B[i]]
            utility = 0

        results.append(curr_rows)
        neg_utilities.append(-1*utility)

    results = [result for (neg_utility, result) in sorted(zip(neg_utilities, results))]

    header = [match_data_A.col_names + ['***'] + match_data_B.col_names + ['', '**why matched**'] + [x[0] for x in matching_criteria]] + []
    res = header + [row for result in results for row in result]

    return(res)

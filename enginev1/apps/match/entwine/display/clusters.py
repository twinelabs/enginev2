"""
display.clusters
--------

Scripts to display cluster results.

"""

def display_results(clusters, match_data):
    """ Constructs pretty CSV of matching results """

    results = []
    for i, cluster in enumerate(clusters):
        for member in cluster:
            results.append( [i] + match_data.grab_data_row(member) )

    header = [['cluster #'] + match_data.col_names]
    res = header + results
    return(res)

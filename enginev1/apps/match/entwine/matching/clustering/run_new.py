"""
run_new
-------------------------

FOR NEW SYNTAX OF MATCHING:
Function to run clustering algorithms.
"""

import methods

# Global dictionary mapping algorithm label to its proper function.
# When a new clustering algorithm is developed, add it to this dictionary.
algorithms = {  'order' : methods.cluster_order,
                'random': methods.cluster_random,
                'fullsearch': methods.cluster_fullsearch,
                'greedy': methods.cluster_greedy,
                'adaptive': methods.cluster_adaptive,
                'greedy_adaptive': methods.cluster_greedy_adaptive
             }

def check_clusters(clusters):
    """ Print ERROR if any duplicates
    """
    i_all = [i for cluster in clusters for i in cluster]
    return len(set(i_all)) == len(i_all)
        
    #dups = set([str(i) for i in i_all if i_all.count(i) > 1])
    #if dups:
    #    print "***ERROR: DUPLICATES = " + ", ".join(dups)
    #return True

def cluster(distance_matrix, match_config, check=True):
    algo_name = match_config['algorithm']['name']
    params = match_config['algorithm']['params']
    algo = algorithms.get(algo_name, False)
    if algo:
        clusters = algo(distance_matrix, params)
    else:
        raise ValueError("Cluster function not implemented: " + algo_name)

    if check:
        if not check_clusters(clusters):
            print("Duplicates in clusters!!!")
            return None
    
    return clusters
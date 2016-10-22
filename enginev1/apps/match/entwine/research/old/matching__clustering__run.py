"""
matching.clustering.run
-------------------------

Core cluster function to run clustering algorithms.
"""

import matching.clustering.methods

# Global dictionary mapping algorithm label to its proper function.
# When a new clustering algorithm is developed, add it to this dictionary.
algorithms = {  'order' : matching.clustering.methods.cluster_order,
                'random': matching.clustering.methods.cluster_random,
                'fullsearch': matching.clustering.methods.cluster_fullsearch,
                'greedy': matching.clustering.methods.cluster_greedy,
                'adaptive': matching.clustering.methods.cluster_adaptive,
                'greedy_adaptive': matching.clustering.methods.cluster_greedy_adaptive
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

def cluster(dist_mat, params, check=True):
    algo = algorithms.get(params['method'], False)
    if algo:
        clusters = algo(dist_mat, params)
    else:
        raise ValueError("Cluster function not implemented: " + params['method'])

    if check:
        if not check_clusters(clusters):
            print("Duplicates in clusters!!!")
            return None
    
    return clusters
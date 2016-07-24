"""
matching.clustering.method_adapt
-------------------------

Adaptive random search.
TODO: Remove or generalize cluster_goodness?
"""

import random
import copy
import numpy as np


def cluster_mean_distance(d, cluster):
    """ Average distance for people in a cluster.
    Excludes diagonal distance (same person to themself).
    """
    d_cluster = d[cluster,:][:,cluster]
    d_cluster_triu = d_cluster[np.triu_indices(len(cluster), 1)]
    cluster_mean_distance = d_cluster_triu.mean()
    return cluster_mean_distance


def cluster_adapt(d, params):

    k_size = params['k_size']
    gom_function = cluster_mean_distance

    # first, cluster randomly
    originals = range(d.shape[0])
    random.shuffle(originals)
    clusters = [originals[i:i+k_size] for i in xrange(0, len(originals), k_size)]

    # iterate 100 times
    n_iterations = 100
    i_iteration = 0
    switchee_cluster = True

    while i_iteration < n_iterations and switchee_cluster:

#       print(clusters)
        i_toswitch_cluster = random.randrange(0, len(clusters))
        toswitch_cluster = clusters[i_toswitch_cluster]
        i_toswitch_member = random.randrange(0, len(toswitch_cluster))
        toswitch_member = toswitch_cluster[i_toswitch_member]

        # for each member of each (not-selected) cluster ...
        best_improvement = 0
        switchee_cluster = False
        switchee_cluster_i = False
        switchee_member = False
        switchee_member_i = False
        for j, cluster in enumerate(clusters):
            if j != i_toswitch_cluster:
                for k, member in enumerate(cluster):
                    toswitch_cluster_new = copy.copy(toswitch_cluster)
                    toswitch_cluster_new.remove(toswitch_member)
                    toswitch_cluster_new += [member]

                    cluster_new = copy.copy(cluster)
                    cluster_new.remove(member)
                    cluster_new += [toswitch_member]

                    # consider improvement if switched
                    goodness_curr = gom_function(d, toswitch_cluster) + gom_function(d, cluster)
                    goodness_new = gom_function(d, toswitch_cluster_new) + gom_function(d, cluster_new)
                    improvement = goodness_curr - goodness_new

                    if improvement > best_improvement:
                        best_improvement = improvement
                        switchee_cluster = cluster
                        switchee_cluster_i = j
                        switchee_member = member
                        switchee_member_i = k

#            print(best_improvement)
        if switchee_cluster:
            clusters[i_toswitch_cluster][i_toswitch_member] = switchee_member
            clusters[switchee_cluster_i][switchee_member_i] = toswitch_member
#                print("switch " + str(toswitch_member) + " with " + str(member) + " = " + str(best_improvement))

        i_iteration += 1

    return clusters

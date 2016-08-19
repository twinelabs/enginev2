"""
matching.clustering.methods
-------------------------

Contains all methods to be used for clustering.

The last cluster will not be of size k if the group is not evenly divisible.

"""
import numpy as np
import math
import copy
import itertools
import random
import pdb

import enginev1.apps.match.entwine.analytics.goodness.cluster_evaluation as cluster_evaluation

# from memory_profiler import profile

# Original order clustering. Used to do random clustering if rand is True.
# @profile
def cluster_order(dist_mat, params, rand=False):
    k = params['k_size']
    dist_mat = np.array(dist_mat)
    indices = range(dist_mat.shape[0])
    if rand:
        random.shuffle(indices)
    return [indices[i:i+k] for i in xrange(0, len(indices), k)]
    
# Random clustering
# @profile
def cluster_random(dist_mat, params):
    return cluster_order(dist_mat, params, rand=True)

# Full search clustering. 
# Found that it is almost always infeasible.
# Feasible parameters are roughly (n=12,k=2) and (n=20,k=10)
# @profile
def cluster_fullsearch(dist_mat, params):
    n = dist_mat.shape[0]
    k = params['k_size']
    best_goodness = 0
    best_clusters = False
    # Have a customizable goodness function
    gom_function = cluster_evaluation.cluster_mean_distance
    
    all_combos = all_groups(range(n), k)
    for clusters in all_combos:
        gofs = [gom_function(dist_mat, cluster) for cluster in clusters]
        gof = sum(gofs)
        if gof > best_goodness:
            best_goodness = gof
            best_clusters = clusters
            
    return best_clusters

# Greedy clustering.
# Cluster goodness is evaluated based on average cluster distance.
# Can take in a maximize parameter set to True if you want to maximize.
# @profile
def cluster_greedy(dist_mat, params):
    k = params['k_size']
    # Sets maximize to True only if maximize is in params and is set to True
    maximize = params.get('maximize',False)
    # Put the distance matrix in floats if it wasn't already
    dist_mat = np.array(dist_mat)
    dist_mat = dist_mat.astype(float)
    # Set diagonal indices such that they never get selected
    m_val = float('-inf') if maximize else float('inf')
    dist_mat[np.diag_indices_from(dist_mat)] = m_val
    n = dist_mat.shape[0]
    originals = range(n)
    clusters = []
    left = n
    # Create clusters
    while left > k:
        indices = np.unravel_index(dist_mat.argmax() if maximize else dist_mat.argmin() , dist_mat.shape)
        cluster = list(indices) # First 2 cluster members
        dist_mat[cluster, :] = m_val
        # Finish filling the k spots in the cluster
        while len(cluster) < k:
            dist_all = np.sum(dist_mat[:, cluster], axis=1)
            index = dist_all.argmax() if maximize else dist_all.argmin()
            cluster.append(index)
            # Make sure we never add the same index again
            dist_mat[index, :] = m_val   
        clusters.append(cluster)
        # Remove the rows and columns of indices in the created cluster
        dist_mat = np.delete(dist_mat, cluster, axis=0)
        dist_mat = np.delete(dist_mat, cluster, axis=1)
        left = dist_mat.shape[0]

    if left > 0:
        clusters.append(range(left))

    # Restore original indices
    clusters_original = []
    for cluster in clusters:
        clusters_original.append([originals[c] for c in cluster])
        originals = [o for i,o in enumerate(originals) if i not in cluster]

    return clusters_original

# Adaptive search clustering.
# @profile
def cluster_adaptive(dist_mat, params, clusters=[]):
    # Always use mean distance function, for now
    gom_function = cluster_evaluation.cluster_mean_distance

    # Cluster randomly if clusters is not provided
    if not clusters:
        clusters = cluster_random(dist_mat, params)

    # Iterate num_swaps times if 'num_swaps' is in params, else do 100
    num_swaps = params.get('num_swaps',100)
    for i in xrange(num_swaps):
        random_cluster_index = random.randrange(len(clusters))
        random_cluster = clusters[random_cluster_index]
        random_member_index = random.randrange(len(random_cluster))
        random_member = random_cluster[random_member_index]

        best_improvement = 0
        switched_cluster = switched_cluster_index = switched_member = switched_member_index = False
        
        # For each member of each (not-selected) cluster ...
        for i,cluster in enumerate(clusters):
            if i != random_cluster_index:
                for j,member in enumerate(cluster):
                    random_cluster_new = copy.copy(random_cluster)
                    random_cluster_new.remove(random_member)
                    random_cluster_new += [member]

                    switch_cluster_new = copy.copy(cluster)
                    switch_cluster_new.remove(member)
                    switch_cluster_new += [random_member]

                    # Consider improvement. Assumes we are minimizing distance?
                    goodness_curr = gom_function(dist_mat, random_cluster) + gom_function(dist_mat, cluster)
                    goodness_new = gom_function(dist_mat, random_cluster_new) + gom_function(dist_mat, switch_cluster_new)
                    improvement = goodness_curr - goodness_new

                    if improvement > best_improvement:
                        best_improvement = improvement
                        switched_cluster = cluster
                        switched_cluster_index = i
                        switched_member = member
                        switched_member_index = j

        if switched_cluster:
            clusters[random_cluster_index][random_member_index] = switched_member
            clusters[switched_cluster_index][switched_member_index] = random_member

    return clusters
    
# Combined greedy and adaptive search clustering.
def cluster_greedy_adaptive(dist_mat, params):
    greedy_clusters = cluster_greedy(dist_mat, params)
    final_clusters = cluster_adaptive(dist_mat, params, greedy_clusters)
    return final_clusters
    
# Recursive helper to find all group combinations of size k
def all_groups(remaining, k):
    # If only k or fewer remaining, just return those indices as a group
    if len(remaining) <= k:
        return [tuple(remaining)]
    else:
        groups_size_k = itertools.combinations(remaining, k)
        clusters = []
        for group in groups_size_k:
            new_remaining = [num for num in remaining if num not in group]
            new_clusters = all_groups(new_remaining, k)
            clusters += [group + new_cluster for new_cluster in new_clusters]
        return clusters
        
# n choose k helper function, for testing
def nCk(n,k):
    f = math.factorial
    return f(n) / f(k) / f(n-k)

# Test to see if all_groups is producing all possible groups. Works!
# Shows that combination length blows up really fast.
# n=9, k=3 --> 1680
# n=10, k=3 --> 16800
# n=11, k=3 --> 92400
# n=15, k=3 --> 168168000 (Infeasible)
# n=20, k=4 --> 305540235000 (Nope)
def number_all_groups(n,k):
    total_combos = 1
    remaining = n
    while remaining >= k:
        total_combos *= nCk(remaining,k)        
        remaining -= k
    return total_combos
        
    


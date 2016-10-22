"""
matching.clustering.method_greedy
-------------------------

Simple greedy algorithm.
"""

import numpy as np

def cluster_greedy(d, params):
    """ Runs simple clustering algo (greedy).
    - Finds pair with smallest distance.
    - Finds individual with smallest average additional distance.
    - Continues until group has size m.
    - Proceeds with original data minus resulting group, until < m elements remaining.
    Note: uses average distance (symmetrical). m must be >= 2.
    """
    k_size = params['k_size']

    ds = (d + d.T)/2    # symmetrical distance
    max_val = 99999
    ds[np.diag_indices_from(ds)] = max_val
    n = ds.shape[0]
    originals = range(n)

    clusters = []
    n_left = n
    m = k_size # random.randint(4, 5)
    j = 0
    while n_left > m:
        i_min = np.argmin(ds)
        cluster = [ i_min % n_left, i_min / n_left ]    # first 2 cluster members
        ds[cluster, :] = 100
        i = 2   # 3rd through Mth cluster member
        while i < m:
            d_all = np.sum(ds[:, cluster], axis=1)
            i_min = np.argmin(d_all)
            cluster.append(i_min)
            ds[i_min, :] = max_val
            i = i + 1

        clusters.append(cluster)
        ds = np.delete(ds, cluster, axis=0)
        ds = np.delete(ds, cluster, axis=1)
        n_left = ds.shape[0]

        m = k_size
        j = j + 1

    if n_left > 0:
        clusters.append(range(n_left))

    # restore original indices
    clusters_original = []
    for cluster in clusters:
        clusters_original.append([originals[c] for c in cluster])
        originals = [o for i, o in enumerate(originals) if i not in cluster]

    return clusters_original


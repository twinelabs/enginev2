"""
matching.clustering.method_fullsearch
-------------------------

Exhaustive search.

WARNING: COMBINATORIC - CAN BE PROHIBITIVE.
"""


def all_combos_r(self, remaining, k):

    if len(remaining) <= k:
        res = [[list(x) for x in itertools.combinations(remaining, len(remaining))]]
        return res

    else:
        these = [list(x) for x in itertools.combinations(remaining, k)]
        res = []
        for this in these:
            new_remaining = [r for r in remaining if r not in this]
            new_clusters = self.all_combos_r(new_remaining, k)
            res += [[this] + new_cluster for new_cluster in new_clusters]
        return res

def cluster_fullsearch(self, d, params):

    n = d.shape[0]
    k = params['k_size']

    print("WARNING: running full search on n=" + str(n) + ", k=" + str(k))

    best_goodness = 0
    best_clusters = False

    all_combos = self.all_combos_r(range(n), k)

    for clusters in all_combos:
        gofs = [self.cluster_goodness(d, cluster) for cluster in clusters]
        gof = sum(gofs)
        if gof > best_goodness:
            best_goodness = gof
            best_clusters = clusters

    return best_clusters

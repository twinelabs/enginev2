"""
matching.clustering.method_random
-------------------------

Random search.
"""


def cluster_random(self, d, params):
    # NOTE: cluster size = k_size, except for (possibly) last cluster
    k_size = params['k_size']
    originals = range(d.shape[0])
    random.shuffle(originals)
    clusters = [originals[i:i+k_size] for i in xrange(0, len(originals), k_size)]
    return clusters


"""
matching.clustering.method_order
-------------------------

Cluster in order
"""



def cluster_order(self, d, m):
    originals = range(d.shape[0])
    clusters = [originals[i:i+m] for i in xrange(0, len(originals), m)]
    return clusters

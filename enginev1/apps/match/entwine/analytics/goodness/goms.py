"""
analytics.goodness.goms
-------------------------

Evaluates matching results (goodness-of-match).
"""

import numpy as np

def goodness(d, clusters):
    """ Evaluates goodness-of-fit (gof) for all clusters.
    """
    goms = numpy.array([cluster_mean_distance(d, cluster) for cluster in clusters])
    g = { 'all': gofs, 'mean': gofs.mean(), 'std': numpy.std(gofs),
                 'min': gofs.min(), 'max': gofs.max() }
    return ("%.3f" % g['mean']) + ' +/- ' + ("%.3f" % g['std']) + ' [' + ("%.3f" % g['min']) + ' to ' + ("%.3f" % g['max']) + ']'


def goodness_all(self, d):
    gofs = numpy.array([self.cluster_goodness(d, cluster) for cluster in self.clusters])
    return gofs


def mean_distance(d, clusters):
    """ Average distance for all clusters.
    """
    mean_distances = [cluster_mean_distance(d, cluster) for cluster in clusters]
    mean_distance = np.array(mean_distances).mean()
    return mean_distance


def cluster_mean_distance(d, cluster):
    """ Average distance for people in a cluster.
    Excludes diagonal distance (same person to themself).
    """
    d_cluster = d[cluster,:][:,cluster]
    d_cluster_triu = d_cluster[np.triu_indices(len(cluster), 1)]
    cluster_mean_distance = d_cluster_triu.mean()
    return cluster_mean_distance

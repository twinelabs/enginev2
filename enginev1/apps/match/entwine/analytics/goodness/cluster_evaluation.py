"""
analytics.goodness.cluster_evaluation
-------------------------

Evaluates the output clustering.

TO DO:
    
    Test with greedy / adaptive algorithm on just the normally distributed features
    Then evaluate the fit of those features
    Then evaluate the non considered features, such as gender sameness or diversity
    
    Later...
    Develop clustering algorithms that take into account these other features, such as gender?
    OR allow other features (such as gender) to be taken into account in the distance matrix somehow?
"""

import numpy as np
import pandas as pd
import enginev1.apps.match.entwine.matching as matching
from math import log
import random

def evaluate(mdl, clusters, match_config, evaluate_config):
    # cluster_types is a dictionary that maps a feature to a list of lists,
    # which is a list of features in each cluster. The ordering should be the same as
    # in clusters.
    match_data = mdl[0]
    metrics = {}
    if 'distance' in evaluate_config:
        dist_mat = matching.distance.A_functions.distance_matrix(mdl, evaluate_config['distance'])
        dist_mat = np.array(dist_mat)
        avg_distances = avg_cluster_distance(dist_mat, clusters)
        # Call describe() on the pandas Series to get all relevant metrics.
        metrics['distance'] = avg_distances.describe()
    if 'diversity' in evaluate_config:
        metrics['diversity'] = {}
        for feature in evaluate_config['diversity']:
            selected_col = np.array(match_data.select_cols_by_name([str(feature)]))
            all_cluster_types = [selected_col[cluster] for cluster in clusters]
            # Report different metrics for each feature, in dictionary form
            metrics['diversity'][feature] = {} 
            all_entropies = all_cluster_entropy(all_cluster_types)
            metrics['diversity'][feature]['All Cluster Entropy'] = str(all_entropies)
            metrics['diversity'][feature]['Entropies STD'] = np.std(all_entropies)
            metrics['diversity'][feature]['Population Entropy'] = population_entropy(all_cluster_types)
            metrics['diversity'][feature]['Scaled Population Entropy'] = scaled_population_entropy(all_cluster_types)
            metrics['diversity'][feature]['Multigroup Entropy'] = multigroup_entropy(all_cluster_types)
            metrics['diversity'][feature]['Random Multigroup Entropy'] = random_multigroup_entropy(all_cluster_types)
            # Group everything into one pandas series
            metrics['diversity'][feature] = pd.Series(metrics['diversity'][feature])
            
    return metrics
    

# Ways to evaluate goodness of fit.

# Diversity. Based on entropy.

def avg_cluster_diversity(all_cluster_types, num_classes, sameness=False):
    """ Average distance for all clusters.
    """
    diversities = [cluster_diversity(cluster_types, num_classes, sameness) for cluster_types in all_cluster_types]
    return np.array(diversities).mean()

def cluster_diversity(cluster_types, num_classes, sameness=False):
    # Throw error if num_classes is less than 2.
    if num_classes <= 1: 
        raise ValueError('Number of classes must be greater than 1!')
    # Throw error if the cluster contains more class types than specified. 
    if len(set(cluster_types)) > num_classes:
        raise ValueError('More class types in the cluster than in num_classes!')
    length = len(cluster_types)
    # Ensures that clusters with smaller sizes than the total number of types are
    # not penalized for not including all types.
    if length < num_classes:
        num_classes = length
    # Calculate probabilities of element occurrence in the cluster
    probs = {elem:float(sum([elem == s for s in cluster_types]))/length for elem in set(cluster_types)}
    entropy = -sum([probs[p] * log(probs[p]) for p in probs])
    max_entropy = log(num_classes)
    diversity = float(entropy) / max_entropy
    return (1 - diversity) if sameness else diversity

# Calculates entropy of a cluster    
def cluster_entropy(cluster_types):
    length = len(cluster_types)
    probs = {elem:float(sum([elem == s for s in cluster_types]))/length for elem in set(cluster_types)}
    h = -sum([probs[p] * log(probs[p]) for p in probs])
    return h
    
# Calculates the entropy of each cluster, and returns a list of group entropies
def all_cluster_entropy(all_cluster_types):
    return [cluster_entropy(cluster_types) for cluster_types in all_cluster_types]
    
# Calculates the entropy of the total population given a list of clusters
def population_entropy(all_cluster_types):
    population = [i for cluster_types in all_cluster_types for i in cluster_types]
    E = cluster_entropy(population)
    return E

# Gives population entropy relative to the maximum value. Returns a value between 0 and 1.
def scaled_population_entropy(all_cluster_types):
    population = [i for cluster_types in all_cluster_types for i in cluster_types]
    num_classes = len(set(population))
    max_entropy = log(num_classes)
    return population_entropy(all_cluster_types) / max_entropy
    
# Multigroup entropy
def multigroup_entropy(all_cluster_types):
    cluster_sizes = [len(cluster) for cluster in all_cluster_types]
    T = sum(cluster_sizes)
    E = population_entropy(all_cluster_types)
    h = sum([cluster_sizes[i] * (E - cluster_entropy(all_cluster_types[i])) / (E * T)
                                        for i in xrange(len(all_cluster_types))])
    # h is normally 0 for maximum integration and 1 for maximum segregation
    # So take 1 - h to have more diversity be closer to 1
    return 1 - h
    
# Calculates the multigroup entropy of random clustering, averaged over a number of rounds.   
def random_multigroup_entropy(all_cluster_types, rounds=100):
    cluster_sizes = [len(cluster) for cluster in all_cluster_types]
    population = [i for cluster_types in all_cluster_types for i in cluster_types]
    indices = np.hstack((0,np.cumsum(cluster_sizes)))
    avg_div_index = []
    for r in xrange(rounds):
        random.shuffle(population)
        random_clusters = [population[indices[i]:indices[i+1]] for i in xrange(len(indices)-1)]
        div = multigroup_entropy(random_clusters)
        avg_div_index.append(div)
    return np.mean(np.array(avg_div_index))
    
# Mean distance.    
    
def avg_cluster_distance(dist_mat, clusters):
    """ Average distance for all clusters.
        Returns a pandas Series of all average cluster distances.
        Call Series.describe() to get mean, std, and percentiles
    """
    mean_distances = [cluster_mean_distance(dist_mat, cluster) for cluster in clusters]
    return pd.Series(mean_distances)

def cluster_mean_distance(dist_mat, cluster):
    """ Average distance for people in a cluster.
    Excludes diagonal distance (same person to themself).
    """
    cluster_dists = dist_mat[cluster,:][:,cluster]
    cluster_triu_dists = cluster_dists[np.triu_indices(len(cluster), 1)]
    return cluster_triu_dists.mean()

"""
matching.clustering.distance
-------------------------

Generate a distance matrix from single data set. Used for clustering.

"""

import numpy as np
import scipy.stats as st
import pandas as pd

def create_single_matrix(df, component, zscore=True):
    selected_cols = df[component['columns']].values
    if zscore:
        selected_cols = st.mstats.zscore(selected_cols)
    distance_matrix = None
    if component['function'] == "euclidean_distance":
        distance_matrix = euclidean_distance(selected_cols)
    elif component['function'] == "binary_same":
        distance_matrix = binary_same(selected_cols)
    elif component['function'] == "binary_diff":
        distance_matrix = binary_diff(selected_cols)
    else:
        raise NotImplementedError("Unsupported distance function for clustering.")
    return distance_matrix
    
def create_weighted_matrix(df, match_config):
    components = match_config['components']
    n = len(components)
    weights = match_config['weights']
    matrices = []
    for component in components:
        matrix = create_single_matrix(df, component)
        matrices.append(matrix)
    
    matrix_3d = np.array(matrices)
    matrix_3d_weighted = np.array([matrix_3d[i] * weights[i] for i in range(n)])
    final_matrix = np.sum(matrix_3d_weighted, axis=0)
    return final_matrix
    
'''
Creates a 2D matrix with each entry as the euclidean distance between the 
attribute vectors of each person.
'''
def euclidean_distance(rows):
    return [[np.linalg.norm(r1 - r2) for r1 in rows] for r2 in rows]
    
''' 
Creates a 2D matrix with 0 if same entry, 1 if different entry. 
When minimizing average intra-cluster distance, this maximizes SIMILARITY.
Can only be used on a single variable column.
'''
def binary_same(column):
    return np.array([[0 if i == j else 1 for j in column] for i in column])

'''
Creates a 2D matrix with 0 if different entry, 1 if same entry
When minimizing average intra-cluster distance, this maximizes DIVERSITY.
Can only be used on a single variable column.
'''
def binary_diff(column):
    return np.array([[0 if i != j else 1 for j in column] for i in column])
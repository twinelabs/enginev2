"""
matching.group.distance_matrix
-------------------------

Generate a distance matrix from single data set. Used for grouping.

"""

import numpy as np


# ===
# CORE DISTANCE FUNCTIONS
# ===

DISTANCE_FUNCTIONS = {
    "euclidean_distance": lambda x: euclidean_distance(x),
    "euclidean_distance_inv": lambda x: euclidean_distance_inv(x),
    "binary_same": lambda x: binary_same(x),
    "binary_diff": lambda x: binary_diff(x)
}

def euclidean_distance(rows):
    ''' Euclidean distance between attributes of each entity.
    (When minimizing average intra-cluster distance, this MINIMIZES DISTANCE.)
    '''
    return [[np.linalg.norm(r1 - r2) for r1 in rows] for r2 in rows]


def euclidean_distance_inv(rows):
    ''' (Approximate) inverse of euclidean distance between attributes of each entity.
    (When minimizing average intra-cluster distance, this MINIMIZES DISTANCE.)
    '''
    return [[1.0/(0.1 + np.linalg.norm(r1 - r2)) for r1 in rows] for r2 in rows]


def binary_same(column):
    ''' Distance = 0 if same entry, 1 if different entry.
    (When minimizing average intra-cluster distance, this maximizes SIMILARITY.)
    NOTE: Can only be used on a single variable column.
    '''
    return np.array([[0 if i == j else 1 for j in column] for i in column])


def binary_diff(column):
    ''' Distance = 1 if same entry, 0 if different entry.
    (When minimizing average intra-cluster distance, this maximizes DIFFERENCE.)
    NOTE: Can only be used on a single variable column.
    '''
    return np.array([[0 if i != j else 1 for j in column] for i in column])


# ===
# WRAPPERS/PROCEDURAL FUNCTIONS
# ===

def create_single_matrix(df, component, zscore=False):
    """ Creates distance matrix for a single matching criterion.
    Function must be defined in "distance functions" dictionary.
    """
    selected_cols = df[component['columns']].values
    if zscore:
        selected_cols = st.mstats.zscore(selected_cols)

    distance_function = DISTANCE_FUNCTIONS.get(component['function'], False)
    if not distance_function:
        raise NotImplementedError("Unsupported distance function for grouping.")

    distance_matrix = distance_function(selected_cols)
    return distance_matrix
    

def calc_distance_matrix(df, match_config):
    """ Creates distance matrix for each matching criteria, combines into
    weighted (numpy) matrix.
    """
    components = match_config['components']
    weights = match_config['weights']

    n = len(components)
    matrices = [create_single_matrix(df, component) for component in components]

    matrices_3d = np.array(matrices)
    matrices_3d_weighted = np.array([matrices_3d[i] * weights[i] for i in range(n)])
    weighted_matrix = np.sum(matrices_3d_weighted, axis=0)

    return weighted_matrix

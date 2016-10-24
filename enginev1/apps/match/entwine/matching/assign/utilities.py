"""
matching.assign.utility
-------------------------

Generate a utility matrix from two data sets. Used for assignment.
"""

import pdb
import numpy as np


# ===
# CORE UTILITY FUNCTIONS
# ===

UTILITY_FUNCTIONS = {
    "equality": lambda a, b, params: equality(a, b, params),
    "inequality": lambda a, b, params: inequality(a, b, params),
    "equality_nonblank": lambda a, b, params: equality_nonblank(a, b, params),
    "gte": lambda a, b, params: gte(a, b, params),
    "lte": lambda a, b, params: lte(a, b, params),
    "intersect": lambda a, b, params: intersect(a, b, params),
    "intersect_comma": lambda a, b, params: intersect_comma(a, b, params),
    "a_contains_b": lambda a, b, params: a_contains_b(a, b, params)
}


def intersection(a, b):
    return list(set(a) & set(b))


def equality(a, b, params):
    return a == b

def inequality(a, b, params):
    return a != b

def equality_nonblank(a, b, params):
    return a == b if (a != "" or b != "") else False

def gte(a, b, params):
    return float(a) >= float(b) if (b != "" and a != "") else False

def lte(a, b, params):
    return float(a) <= float(b) if (b != "" and a != "") else False

def intersect(a, b, params):
    f_s = params['f_s'] if 'f_s' in params else ','
    return len(intersection(a.split(f_s), b.intersection(f_s))) > 0

def intersect_comma(a, b, params):
    return intersect(a, b, {'f_s': ','} )

def b_contains_a(a, b, params):
    f_s = params['f_s'] if 'f_s' in params else ','
    return a in b.split(f_s)

def a_contains_b(a, b, params):
    f_s = params['f_s'] if 'f_s' in params else ','
    return b in a.split(f_s)


# ===
# WRAPPERS/PROCEDURAL FUNCTIONS
# ===


def calc_single_utility_matrix(dfs, component):

    utility_function = UTILITY_FUNCTIONS.get(component['function'], False)

    if not utility_function:
        raise NotImplementedError("Unsupported utility function for assignment.")

    df_A = dfs[0]
    df_B = dfs[1]

    col_A = component['columns'][0]
    col_B = component['columns'][1]

    n = len(df_A)
    m = len(df_B)
    utilities = np.zeros((n, m))

    for i in range(n):
        for j in range(m):
            val_A = df_A[col_A][i]
            val_B = df_B[col_B][j]
            utility = utility_function(val_A, val_B, component)
            utilities[i][j] = utility

    return utilities


def calc_utility_matrix(dfs, match_config):

    components = match_config['components']
    weights = match_config['weights']

    n = len(components)
    matrices = [calc_single_utility_matrix(dfs, component) for component in components]

    matrices_3d = np.array(matrices)
    matrices_3d_weighted = np.array([matrices_3d[i] * weights[i] for i in range(n)])
    weighted_matrix = np.sum(matrices_3d_weighted, axis=0)

    return weighted_matrix


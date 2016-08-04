from enginev1.apps.dataset.utils import *
from entwine_cluster import *
from enginev1.apps.match.models import *

import numpy as np
import time
import json

def l2(x, y):
    x2 = x if isinstance(x, list) else x.tolist()
    y2 = y if isinstance(y, list) else y.tolist()
    a = [float(i) for i in x2]
    b = [float(i) for i in y2]
    diff = np.subtract(a, b)
    return np.linalg.norm(diff)


def l2_norm(data_rows):
    return [[l2(row_1, row_2) for row_1 in data_rows] for row_2 in data_rows]


def binary_same(x):
    return [[0 if i == j else 1 for j in x] for i in x]


def combine_ds(ds):
    w = 1.0/len(ds)
    ds_np = [np.array(d) for d in ds]
    d = sum([w*d_i for d_i in ds_np])
    return d

def distance_matrix(df, params):

    ds = []
    colnames_s = params['column_names']
    colnames = json.loads(colnames_s)

    for i, colname in enumerate(colnames):
        data_row = [x[0] for x in df[[colname]].values.tolist()]
        d_i = binary_same(data_row)
        ds.append(d_i)

    d = combine_ds(ds)
    return d


def run_match(match):

    config = match.config

    if config['task'] == "cluster":
        if len(match.data_tables.all()) > 1:
            raise TypeError("Cannot cluster more than one data table.")

        data_table = match.data_tables.all()[0]
        df = data_table_to_df(data_table)

        d = distance_matrix(df, config)
        clusters = cluster_adapt(d, config)

        match.result = { 'clusters' : str(clusters) }
        match.save()

        return True

    elif config['task'] == "assign":
        raise TypeError("Assign not yet built")

    else:
        raise TypeError("Attempt to run unsupported match type")

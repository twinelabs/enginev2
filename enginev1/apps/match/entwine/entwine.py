from enginev1.apps.dataset.utils import *
from entwine_cluster import *
from enginev1.apps.match.models import *

import numpy as np
import time

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
    colnames = params['colnames'].split(',')
    for i, colname in enumerate(colnames):
        data_row = [x[0] for x in df[[colname]].values.tolist()]
        d_i = binary_same(data_row)
        ds.append(d_i)

    d = combine_ds(ds)
    return d


def run_match(config):

    client = config.client
    params = config.params

    if params['task'] == "cluster":

        run_start = time.time()
        dataset_objs = client.alpha_set.all()
        df = dataset_objects_to_pandas_df(dataset_objs)

        d = distance_matrix(df, params)
        clusters = cluster_adapt(d, params)
        run_end = time.time()

        result_output = {
            'clusters': str(clusters),
            'run_start': run_start,
            'run_end': run_end
        }

        return result_output

    elif params['task'] == "assign":
        raise TypeError("Assign not yet built")

    else:
        raise TypeError("Attempt to run unsupported match type")

from enginev1.apps.dataset.utils import *
from entwine_cluster import *
from models import *

import numpy as np


def l2(x, y):
    x2 = x if isinstance(x, list) else x.tolist()
    y2 = y if isinstance(y, list) else y.tolist()
    a = [float(i) for i in x2]
    b = [float(i) for i in y2]
    diff = np.subtract(a, b)
    return np.linalg.norm(diff)


def l2_norm(data_rows):
    return [[l2(row_1, row_2) for row_1 in data_rows] for row_2 in data_rows]


def distance_matrix(df, params):

    colnames = params['colnames'].split(',')
    data_rows = df[colnames].values.tolist()
    distance_matrix = l2_norm(data_rows)
    return np.array(distance_matrix)


def match_from_config(config):

    client = config.client
    params = config.params

    if params['task'] == "cluster":

        dataset_objs = client.alpha_set.all()
        df = dataset_objects_to_pandas_df(dataset_objs)

        d = distance_matrix(df, params)
        clusters = cluster_adapt(d, params)

        result_data = {
            'd': d,
            'clusters': clusters
        }
        result = Result(client = client, data = result_data)
        result.save()

        return True

    elif params['task'] == "assign":
        raise TypeError("Assign not yet built")

    else:
        raise TypeError("Attempt to run unsupported match type")

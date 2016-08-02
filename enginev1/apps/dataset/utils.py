import json
import xlrd

import pandas as pd
import numpy as np

import models

"""
from enginev1.apps.welcome.models import *
from enginev1.apps.dataset.utils import *
c = Client.objects.all()[5]
alphas = c.alpha_set.all()
df = dataset_objects_to_pandas_df(alphas)
"""

def dataset_objects_to_pandas_df(dataset_objects):
    """
    :param dataset_objects: list or queryset of Dataset objects
    :return: Pandas dataframe
    """

    list_of_dicts = [obj.data for obj in dataset_objects]
    df = pd.DataFrame.from_dict(list_of_dicts)

    colnames = list(df.columns.values)
    desired_order = ['First name', 'Last name', 'Email ', 'College', 'Graduation year', 'Major', 'Ethnicity', 'Gender', 'Status', 'business_offering', 'business_type', 'incorporated', 'industries', 'looking_for', 'most_help', 'phase', 'received_capital', 'revenue', 'sales_or_users', 'success', 'total_capital', 'users']

    desired_order.reverse()
    for colname in desired_order:
        if colname in colnames:
            new_cols = [colname] + [x for x in colnames if x != colname]
            df = df[new_cols]
            colnames = list(df.columns.values)

    return df


def pandas_df_to_dashboard_format(df, df_id, df_name, filter_viz=False):
    """
    :param df: Pandas dataframe
    :return: JSON object for usage in data dashboard
    """

    df2 = df.apply(pd.to_numeric, errors='ignore')
    colnames = df2.columns.values
    coltypes = df2.dtypes

    cols = []
    for i, coltype in enumerate(coltypes):
        cols.append((colnames[i], "number" if coltype == np.int64 else "string"))

    if filter_viz:
        cols = [col for col in cols if len(df[col[0]].unique()) < 10]

    res = {
        "id": df_id,
        "name": df_name,
        "columns": [{"name": col[0], "type": col[1]} for col in cols],
        "data": df.to_dict(orient='records')
    }

    return res


def import_csv_as_dataset(client, alpha_or_beta, csv_file):
    """
    :param client: Client = owner.
    :param csv_file: File path of CSV
    :param alpha_or_beta: Whether to save into Alpha or Beta.
    :return: True if successfully saved
    """

    if alpha_or_beta == 'alpha':
        my_model = models.Alpha
    else:
        my_model = models.Beta

    df = pd.read_csv(csv_file)
    list_of_dicts = df.to_dict(orient='records')

    for dict in list_of_dicts:
        obj = my_model(client = client, data = dict)
        obj.save()

    return True

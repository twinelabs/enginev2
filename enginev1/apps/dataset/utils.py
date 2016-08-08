import pandas as pd
import numpy as np

import pdb
import models

"""
from enginev1.apps.welcome.models import *
from enginev1.apps.dataset.models import *
dts = DataTable.objects.all()[5]
dt = dts[0]
df = dataset_objects_to_pandas_df(dts)
"""

def data_table_to_df(data_table):
    """
    :param datatable: DataTable object
    :return: Pandas dataframe
    """
    df = pd.DataFrame.from_dict(data_table.data['data'])

    colnames = [dc.name for dc in data_table.datacolumn_set.order_by('order_original')]
    df = df[colnames]

    return df


def data_table_to_lists(data_table, with_index=False):

    df = data_table_to_df(data_table)

    df_header = list(df.columns.values)
    df_values = df.values.tolist()

    if with_index:
        df_header = ['id'] + df_header
        df_values = [ [i] + vals for i, vals in enumerate(df_values) ]

    res = (df_header, df_values)
    return res




def df_to_dashboard(df, df_id, df_name, filter_viz=False):
    """
    :param df: Pandas dataframe
    :return: JSON object for usage in data dashboard
    """

    df2 = df.apply(pd.to_numeric, errors='ignore')
    colnames = df2.columns.values
    coltypes = df2.dtypes

    cols = []
    for i, coltype in enumerate(coltypes):
        cols.append((colnames[i], "number" if (coltype == np.int64 or coltype == np.float64) else "string"))

    if filter_viz:
        cols = [col for col in cols if (col[1] == "number" or len(df[col[0]].unique()) < 10)]

    res = {
        "id": df_id,
        "name": df_name,
        "columns": [{"name": col[0], "type": col[1]} for col in cols],
        "data": df.to_dict(orient='records')
    }

    return res


def import_csv_as_data_table(client, name, csv_file):
    """
    :param client: Client = owner.
    :param csv_file: File path of CSV
    :return: True if successfully saved
    """

    df = pd.read_csv(csv_file)
    n_rows, n_cols = df.shape
    list_of_dicts = df.to_dict(orient='records')

    # Save data table
    data_table = models.DataTable(client = client, name = name,
                                  data = { 'data': list_of_dicts }, n_rows = n_rows, n_cols = n_cols)
    data_table.save()

    # Save columns
    for i, column_name in enumerate(list(df.columns.values)):
        vals = list(df[column_name])
        n_unique = len(set(vals))
        n_nonblank = len([x for x in vals if x != ''])

        data_column = models.DataColumn(
            data_table = data_table,
            name = column_name,
            order_original = i,
            order_custom = i,
            n_unique = n_unique,
            n_nonblank = n_nonblank
        )
        data_column.save()

    return data_table.id

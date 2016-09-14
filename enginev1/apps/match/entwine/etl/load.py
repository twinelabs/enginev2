"""
etl.load
--------

Loading data and data tables into pandas dataframes for matching.

"""

import pandas as pd

from enginev1.apps.dataset import models


def load_data_frame(d):
    """ Loads data frame as specified in config object.
    """

    if 'data_table' in d:
        data_table_id = d['data_table']['id']
        data_table = models.DataTable.objects.get(pk=data_table_id)
        df = data_table.as_df()

    elif 'file' in d:
        f = d['file']['name']
        if d['file']['type'] == 'csv':
            df = pd.DataFrame.from_csv(f)
        else:
            raise TypeError('Unsupported or missing file type. (in config[load][file][type])')

    else:
        raise TypeError('Unsupported or missing load data. (in config[load]')

    return df


def load_from_config(load_cfg):
    """ Loads multiple data tables from config.
    """

    dfs = [load_data_frame(d) for d in load_cfg]

    return dfs

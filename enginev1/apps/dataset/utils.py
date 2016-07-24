import json
import xlrd

import pandas as pd

import models


def dataset_objects_to_pandas_df(dataset_objects):
    """
    :param dataset_objects: list or queryset of Dataset objects
    :return: Pandas dataframe
    """

    list_of_dicts = [obj.data for obj in dataset_objects]
    df = pd.DataFrame.from_dict(list_of_dicts)

    return df


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

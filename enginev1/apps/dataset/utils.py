import json
import pandas as pd


def DatasetObjectsToPandas(dataset_objects):
    """
    :param dataset_objects: list or queryset of Dataset objects
    :return: Pandas dataframe
    """

    dataset_fields = [obj.data for obj in dataset_objects]
    json_str = json.dumps(dataset_fields)
    df = pd.read_json(json_str, orient='records')

    return df


def CSVToPandas(csv_file):
    """
    :param csv_file: File path for CSV
    :return: Pandas dataframe
    """

    df = pd.read_csv(csv_file)
    return df


# from enginev1.apps.dataset.models import Alpha
# from enginev1.apps.dataset.utils import *
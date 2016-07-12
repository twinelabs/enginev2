import json
import pandas as pd


def DatasetObjectsToPandas(dataset_objects):
    """
    :param dataset_objects: list or queryset of Dataset objects
    :return: pandas dataframe with all columns filled
    """

    dataset_fields = [obj.data for obj in dataset_objects]
    json_str = json.dumps(dataset_fields)
    df = pd.read_json(json_str, orient='records')

    return df
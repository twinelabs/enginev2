from django.db import models
from enginev1.apps.welcome.models import Client
from enginev1.apps.dataset.models import DataTable, DataColumn
from django_hstore import hstore

import pdb
import json

class Match(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    data_tables = models.ManyToManyField(DataTable, related_name='matches')

    config = hstore.SerializedDictionaryField()

    run_start = models.DateTimeField(null=True, blank=True)
    run_end = models.DateTimeField(null=True, blank=True)
    result = hstore.DictionaryField()

    class Meta:
        app_label = 'match'

    def __str__(self):
        return self.name


def match_request_to_config(request):
    """ Converts match form into configured match object with configs.

    :param request: request as passed in via match/create_match.html
    :return: match form object (unsaved)
    """

    req = dict(request.iterlists())

    task = req['task'][0]
    if task == 'cluster':
        load_config = [{ "data_table" : { "id": int(req['data_tables_single'][0]) } }]
    elif task == 'assign':
        load_config = [{ "data_table" : { "id": int(id) } } for id in req['data_tables_multiple']]
    else:
        raise TypeError("Unsupported match TASK: " + task )

    match_config = {
        "task": task
    }

    if task == 'cluster':
        match_config['algorithm'] = {
            'name': req['cluster_algo'][0],
            'params': {
                'k_size': int(req['k_size'][0])
            }
        }

        components = []
        weights = []


        for column_id_s in req['task_cluster_columns']:
            column_id = int(column_id_s)
            components.append({
                "columns": [ DataColumn.objects.get(pk=column_id).name ],
                "function": req['cluster_rule_' + str(column_id)][0]
            })
            weights.append( int(req['cluster_weight_' + str(column_id)][0]) )

        match_config['components'] = components
        match_config['weights'] = weights

#    elif task == 'assign':
    else:
        raise TypeError("Unsupported match TASK: " + task )

    config = {
        "load": load_config,
        "match": match_config
    }

    print("==== BEFORE ====")
    print(config)

    return config


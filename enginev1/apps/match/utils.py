import json

import models

def match_config_as_html(match):

    cfg = match.config['match']
    data_tables = match.data_tables.all()
    s = ""

    if cfg['task'] == 'cluster':
        s += "<br />"
        s += "<p>Data Set: <b>" + data_tables[0].name + "</b></p>"
        s += "<p>Group Size: <b>" + str(cfg['algorithm']['params']['k_size']) + "</b></p>"
        s += "<p>Algorithm: <b>" + cfg['algorithm']['name'] + "</b></p>"

        s += "<br />"
        s += "<p>Match Criteria: <ol>"
        for c, w in zip(cfg['components'], cfg['weights']):
            s += "<li><b>" + c['columns'][0] + "</b> - " + c['function'] + " (weight = " + str(w) + ")</li>"
        s += "</ol></p>"

    elif cfg['task'] == 'assign':
        s += "<p>Data Sets: <ul><li>"
        s += "</li><li>".join([ d.name for d in data_tables])
        s += "</li></ul></p>"

    else:
        raise TypeError("Unsupported task for match config: " + cfg['task'])

    return s

def match_results_as_html(match):
    cfg = match.config['match']
    results = json.loads(match.result['results'])
    s = ""

    if cfg['task'] == 'cluster':
        for i, pod in enumerate(results):
            s += "<ul><b>Group " + str(i+1) + "</b>: "
            s += ", ".join([ str(m) for m in pod ])
            s += "</ul>"

    elif cfg['task'] == 'assign':
        s += "<p>Assignments:</p>"

    else:
        raise TypeError("Unsupported task for match config: " + cfg['task'])

    return s

def match_results_as_html_table(match):
    cfg = match.config['match']
    results = json.loads(match.result['results'])

    s = ""
    if cfg['task'] == 'cluster':
        data_table = match.data_tables.all()[0]
        (dt_header, dt_values, dt_count) = data_table.as_table_data()

        groups = [0]*dt_count
        for i, pod in enumerate(results):
            for member in pod:
                groups[member] = i

        dt_header = ['Group #'] +  dt_header
        dt_values = [ ["Group " + str(groups[i])] + row for i, row in enumerate(dt_values) ]

        s += "<thead><tr><th>"
        s += "</th><th>".join([ column_name for column_name in dt_header ])
        s += "</th></tr></thead>"

        s += "<tbody>"
        for row in dt_values:
            s += "<tr><td>"
            s += "</td><td>".join([ str(val) for val in row])
            s += "</tr>"
        s += "</tbody>"

    elif cfg['task'] == 'assign':
        s += "<p>Assignment Table:</p>"

    else:
        raise TypeError("Unsupported task for match config: " + cfg['task'])

    return s


def match_results_for_feedback(match):
    cfg = match.config['match']
    results = json.loads(match.result['results'])

    s = ""
    if cfg['task'] == 'cluster':
        data_table = match.data_tables.all()[0]
        dt_values = data_table.values()

        for i, pod in enumerate(results):
            s += "<br />Group " + str(i+1) + ":"
            for member in pod:
                s += "Member " + str(member) + ", "

    elif cfg['task'] == 'assign':
        s += "<p>Assignment Table:</p>"

    else:
        raise TypeError("Unsupported task for match config: " + cfg['task'])

    return s


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

    else:
        raise TypeError("Unsupported match TASK: " + task )

    config = {
        "load": load_config,
        "match": match_config
    }

    return config


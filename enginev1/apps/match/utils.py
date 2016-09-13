import json

import models

def match_config_as_html(match):

    cfg = match.config['match']
    data_tables = match.data_tables.all()
    s = ""

    if cfg['task'] == 'cluster':
        s += "<h3>" + match.name + "</h3><div class='row'>"

        s += "<div class='col-md-5'><h4>Configuration</h4><ul>"
        s += "<li>Data Set: <b>" + data_tables[0].name + "</b></li>"
        s += "<li>Group Size: <b>" + str(cfg['algorithm']['params']['k_size']) + "</b></li>"
        s += "<li>Algorithm: <b>" + cfg['algorithm']['name'] + "</b></li>"
        s += "</ul></div>"

        s += "<div class='col-md-5 col-md-offset-1'><h4>Matching Rules</h4><ol>"
        for c, w in zip(cfg['components'], cfg['weights']):
            s += "<li><b>" + c['columns'][0] + "</b> - " + c['function'] + " (weight = " + str(w) + ")</li>"
        s += "</ol></div>"

        s += "</div>"

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
    group_numbers = [i+1 for i in range(len(results))]
    matched_columns = [c['columns'][0] for c in cfg['components']]

    s = ""
    if cfg['task'] == 'cluster':
        data_table = match.data_tables.all()[0]
        dt_name = data_table.name
        data = data_table.data['data']

        for i, pod in enumerate(results):
            s += "<div class='feedbackGroup" + str(i+1) + " feedbackGroup' style='display:none;'>"
            s += "<h2>Group #" + str(i+1) + " " + dt_name + "</h2>"
            for j, member in enumerate(pod):
                s += "<div class='row' style='margin-left: 20px; margin-top: 30px;'>"
                s += "<div class='col-md-1'><h4>#" + str(j+1) + "</h4></div>"

                s += "<div class='col-md-5'><h4>Matched Attributes</h4>"
                s += "<table style='border-collapse: separate; border-spacing: 10px 4px;'>"
                for col_name in matched_columns:
                    s += "<tr><td><b>" + col_name + "</b></td><td>" + str(data[member][col_name]) + "</td>"
                    s += "<td><a href='#'>Strong Match</a><br /><a href='#'>Weak Match</a></td></tr>"
                s += "</table></div>"

                unmatched_columns = [col for col in data[member].keys() if col not in matched_columns]
                s += "<div class='col-md-5 col-md-offset-1'><h4>Other Attributes</h4>"
                s += "<table style='border-collapse: separate; border-spacing: 20px 4px;'>"
                for col_name in unmatched_columns:
                    s += "<tr><td><b>" + col_name + "</b></td><td>" + str(data[member][col_name]) + "</td></tr>"
                s += "</table></div>"

                s += "</div>"
            s += "</div>"

    elif cfg['task'] == 'assign':
        s += "<p>Assignment Table:</p>"

    else:
        raise TypeError("Unsupported task for match config: " + cfg['task'])

    return (group_numbers, s)


def match_analytics(match):

    result = match.result

    match_time = result['match_time']
    analytics = [
        {
            'img': "img/demo/match_time.png",
            'title': 'Match Run Time',
            'value': "{0:.2f}".format(float(match_time)) + " sec"
        }
    ]

    if 'stats' in result:
        stats = json.loads(match.result['stats'])

        for stat in stats:
            a = {
                'img': "img/demo/match_strength.png",
                'title': stat['name'],
                'value': stat['result']
            }
            analytics.append(a)

    analytics += [
        {
            'img': "img/demo/match_strength.png",
            'title': 'Overall Match Strength',
            'value': '9.2 (High)'
        },
        {
            'img': "img/demo/match_variables.png",
            'title': '# of Variables',
            'value': '7'
        },
        {
            'img': "img/demo/diversity_coefficient.png",
            'title': 'Diversity Score',
            'value': '0.64 (low)'
        },
        {
            'img': "img/demo/matched_users.png",
            'title': 'Matched Users',
            'value': '275 Roles'
        },
        {
            'img': "img/demo/matches_per_user.png",
            'title': 'Matches per Role',
            'value': '5'
        },
        {
            'img': "img/demo/total_matches.png",
            'title': 'Total # Matches',
            'value': '1,375'
        }
    ]

    return analytics

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
                "columns": [ models.DataColumn.objects.get(pk=column_id).name ],
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


import json
import pdb

import models

def match_config_as_html(match):

    cfg = match.config['match']
    data_tables = match.data_tables.all()

    s = "<h3>" + match.name + "</h3><div class='row'>"
    s += "<div class='col-md-5'><h4>Configuration</h4><ul>"

    if cfg['task'] == 'cluster':
        s += "<li>Data Set: <b>" + data_tables[0].name + "</b></li>"
        s += "<li>Group Size: <b>" + str(cfg['algorithm']['params']['k_size']) + "</b></li>"
        s += "<li>Algorithm: <b>" + cfg['algorithm']['name'] + "</b></li>"
        s += "</ul></div>"

        s += "<div class='col-md-5 col-md-offset-1'><h4>Matching Rules</h4><ol>"
        for c, w in zip(cfg['components'], cfg['weights']):
            s += "<li><b>" + c['columns'][0] + "</b> - " + c['function'] + " (weight = " + str(w) + ")</li>"
        s += "</ol></div>"

    elif cfg['task'] == 'assign':
        s += "<li>Data Sets: <b>" + ", ".join([ d.name for d in data_tables ]) + "</b></li>"
        s += "<li>Capacity: <b>" + str(cfg['algorithm']['params']['capacity']) + "</b></li>"
        s += "<li>Algorithm: <b>NRMP</b></li>"
        s += "</ul></div>"

        s += "<div class='col-md-5 col-md-offset-1'><h4>Matching Rules</h4><ol>"
        for c, w in zip(cfg['components'], cfg['weights']):
            s += "<li><b>" + c['columns'][0] + "</b> with <b>" + c['columns'][1] + "</b> - " + c['function'] + " (weight = " + str(w) + ")</li>"
        s += "</ol></div>"

    else:
        raise TypeError("Unsupported task for match config: " + cfg['task'])

    s += "</div>"

    return s


def match_results_as_html(match):
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
        dt_values = [ [ groups[i] ] + row for i, row in enumerate(dt_values) ]

        s += "<table class='dataset-table nowrap table table-striped table-hover'>"
        s += "<thead><tr><th>"
        s += "</th><th>".join([ column_name for column_name in dt_header ])
        s += "</th></tr></thead>"

        s += "<tbody>"
        for row in dt_values:
            s += "<tr><td>"
            s += "</td><td>".join([ str(val) for val in row])
            s += "</tr>"
        s += "</tbody>"
        s += "</table>"

    elif cfg['task'] == 'assign':
        n_lim = 4

        dt_B = match.data_tables.all()[0]
        dt_B_values = dt_B.values()
        dt_A = match.data_tables.all()[1]
        dt_A_values = dt_A.values()

        header = dt_B.header()[:n_lim] + [""] + dt_A.header()[:n_lim]

        s += "<table class='dataset-table nowrap table table-striped table-hover'>"
        s += "<thead><tr><th>"
        s += "</th><th>".join([ str(val) for val in header])
        s += "</th></tr></thead>"

        s += "<tbody>"
        for i, pod in enumerate(results):
            elem_B = dt_B_values[i]

            for j, member in enumerate(pod):
                elem_A = dt_A_values[member]
                vals = elem_B[:n_lim] + ["<->"] + elem_A[:n_lim]
                s += "<tr><td>"
                s += "</td><td>".join([ str(val) for val in vals])
                s += "</td></tr>"
        s += "</tbody>"
        s += "</table>"

    else:
        raise TypeError("Unsupported task for match config: " + cfg['task'])

    return s


def match_results_for_feedback(match):
    cfg = match.config['match']
    results = json.loads(match.result['results'])
    group_numbers = [i+1 for i in range(len(results))]

    s = ""
    if cfg['task'] == 'cluster':
        matched_columns = [c['columns'][0] for c in cfg['components']]
        data_table = match.data_tables.all()[0]
        dt_name = data_table.name
        data = data_table.data['data']

        for i, pod in enumerate(results):
            s += "<div class='feedbackGroup" + str(i+1) + " feedbackGroup well' style='display:none;'>"
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
        dt_A = match.data_tables.all()[0]
        data_A = dt_A.data['data']
        matched_columns_A = [c['columns'][0] for c in cfg['components']]

        dt_B = match.data_tables.all()[1]
        data_B = dt_B.data['data']

        for i, pod in enumerate(results):
            s += "<div class='feedbackGroup" + str(i+1) + " feedbackGroup' style='display:none;'>"
            s += "<div class='row'>"
            s += "<div class='col-md-6'><div class='well'>"
            s += "<h3>" + dt_B.name + " #" + str(i+1) + "</h3>"

            s += "<table style='border-collapse: separate; border-spacing: 10px 4px;'>"
            for col_name in data_B[i]:
                s += "<tr><td><b>" + col_name + "</b></td><td>" + str(data_B[i][col_name]) + "</td></tr>"
            s += "</table></div></div>"

            s += "<div class='col-md-6'><div class='well'>"
            for j, member in enumerate(pod):
                s += "<h3>Matched " + dt_A.name + " #" + str(j+1) + "</h3>"

                s += "<table style='border-collapse: separate; border-spacing: 10px 4px;'>"
                for col_name in matched_columns_A:
                    s += "<tr><td><b>" + col_name + "</b></td><td>" + str(data_A[j][col_name]) + "</td>"
                    s += "<td><a href='#'>Strong Match</a><br /><a href='#'>Weak Match</a></td></tr>"

                unmatched_columns_A = [col for col in data_A[j].keys() if col not in matched_columns_A]
                for col_name in unmatched_columns_A:
                    s += "<tr><td><b>" + col_name + "</b></td><td>" + str(data_A[j][col_name]) + "</td></tr>"
                s += "</table>"

            s += "</div></div>"
            s += "</div></div>"

    else:
        raise TypeError("Unsupported task for match config: " + cfg['task'])

    return (group_numbers, s)


def match_analytics(match):

    analytics = []

    stats = json.loads(match.result['stats'])
    for stat in stats:
        a = {
            'img': "img/demo/match_strength.png",
            'title': stat['name'],
            'value': stat['value']
        }
        analytics.append(a)

    # TODO: remove when stats are properly formatted
    analytics = []

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


def create_group_request_to_config(request):
    """ Converts create group form into match object with configs.
    """

    req = dict(request.iterlists())
    print(req)

    config = {
        "load": [
            {
                "data_table": {
                    "id": int(req['data_table'][0])
                }
            }
        ],
        "match": {
            "task": "cluster",
            "algorithm": {
                "name": req['algo'][0],
                "params": {
                    "k_size": int(req['k_size'][0])
                }
            }
        }
    }

    components = []
    weights = []

    for key in req:
        if key[:11] == 'match_rule_':
            column_id = int(key[11:])
            components.append({
                "columns": [models.DataColumn.objects.get(pk=column_id).name],
                "function": req[key][0]
            })
            weights.append(int(req['match_importance_' + str(column_id)][0]))

    config['match']['components'] = components
    config['match']['weights'] = weights

    return config


def create_assign_request_to_config(request):
    """ Converts create assign form into match object with configs.
    """

    req = dict(request.iterlists())
    print(req)

    config = {
        "load": [
            {
                "data_table": {
                    "id": int(req['data_table_A'][0])
                }
            },
            {
                "data_table": {
                    "id": int(req['data_table_B'][0])
                }
            }
        ],
        "match": {
            "task": "assign"
        }
    }

    components = []
    weights = []

    for key in req:
        if key[:11] == 'match_rule_':

            column_id_A, column_id_B = key[11:].split('_')
            column_id_A, column_id_B = int(column_id_A), int(column_id_B)

            column_name_A = models.DataColumn.objects.get(pk=column_id_A).name
            column_name_B = models.DataColumn.objects.get(pk=column_id_B).name

            components.append({
                "columns": [column_name_A, column_name_B],
                "function": req[key][0]
            })
            weights.append(int(req['match_importance_' + key[11:]][0]))

    config['match']['components'] = components
    config['match']['weights'] = weights

    return config


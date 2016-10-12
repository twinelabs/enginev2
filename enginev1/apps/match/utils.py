import json
import pdb
import xlwt

from django.http import HttpResponse

from .entwine.display import assignments
import models


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
            "task": "assign",
            "algorithm": {
                "params": {
                    "capacity": int(req['capacity'][0]),
                    "direction": req['direction'][0],
                    "duplicates": req['duplicates'][0]
                }
            }
        }
    }

    components = []
    weights = []

    for key in req:
        if key[:11] == 'match_rule_':
            group_id = key[11:]
            print("group ID: " + group_id)

            tag_A, tag_B = group_id.split('_')
            id_A, id_B = int(tag_A[1:]), int(tag_B[1:])

            column_name_A = models.DataColumn.objects.get(pk=id_A).name
            column_name_B = models.DataColumn.objects.get(pk=id_B).name

            components.append({
                "columns": [column_name_A, column_name_B],
                "function": req[key][0]
            })
            weights.append(int(req['match_importance_' + key[11:]][0]))

    config['match']['components'] = components
    config['match']['weights'] = weights

    return config


def export_assign_as_excel(match):

    pretty_csv = assignments.pretty_csv(match)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + match.name + ' - Export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Results")

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    i_row = 0
    for i_col, colname in enumerate(pretty_csv[0]):
        ws.write(i_row, i_col, colname, font_style)
        ws.col(i_col).width = 4000

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for csv_row in pretty_csv[1:]:
        i_row += 1
        for i_col, x in enumerate(csv_row):
            ws.write(i_row, i_col, x, font_style)

    wb.save(response)

    return response


    s = ""

    n_lim = 999 if full else 4

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

#            pdb.set_trace()

        elem_B = dt_B_values[i]

        for j, member in enumerate(pod):
            elem_A = dt_A_values[member]
            vals = elem_B[:n_lim] + ["<->"] + elem_A[:n_lim]
            s += "<tr><td>"
            s += "</td><td>".join([ str(val) for val in vals])
            s += "</td></tr>"
    s += "</tbody>"
    s += "</table>"

    return s

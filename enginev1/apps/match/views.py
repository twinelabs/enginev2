from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

import datetime
import pdb
import json

from .models import *
from .utils import *
from .forms import MatchForm


def data_table_columns(request):
    data_table_id = request.GET.get('data_table_id', None)
    data_table = DataTable.objects.get(pk=data_table_id)
    data_columns = DataColumn.objects.filter(data_table=data_table)
    column_names = [ c.name for c in data_columns]
    message = ", ".join(column_names)
    data = {
        'message': message
    }
    return JsonResponse(data)


@login_required
def view(request, match_id):

    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    match = Match.objects.get(id=match_id)
    if match.client != c:
        return HttpResponse("You are not permissioned.")

    config_html = match_config_as_html(match)

    has_results = match.has_results()
    if has_results:
        result_html = match_results_as_html(match)
    else:
        result_html = None

    context = {
        'c': c,
        'data_tables': data_tables,
        'matches': matches,

        'match': match,
        'has_results': has_results,
        'config_html': config_html,
        'result_html': result_html,
    }

    return render(request, 'match/view.html', context)


@login_required
def feedback(request, match_id):
    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    match = Match.objects.get(id=match_id)
    if match.client != c:
        return HttpResponse("You are not permissioned.")


    (group_numbers, feedback_s) = match_results_for_feedback(match)

    context = {
        'c': c,
        'data_tables': data_tables,
        'matches': matches,
        'match': match,
        'group_numbers': group_numbers,
        'feedback_s': feedback_s
    }
    return render(request, 'match/feedback.html', context)


@login_required
def feedback_employeerole(request):
    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    context = {
        'c': c,
        'data_tables': data_tables,
        'matches': matches
    }
    return render(request, 'match/feedback_employeerole.html', context)


@login_required
def create(request):

    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    if request.method == 'POST':
        match_form = MatchForm(data=request.POST, client=c)

        if match_form.is_valid():

            name = match_form.cleaned_data['name']
            cfg = match_request_to_config(request.POST)

            # cfg = {u'load': [{u'data_table': {u'id': 12}}, {u'data_table': {u'id': 13}}], u'match': {u'task': u'assign', u'weights': [5], u'algorithm': {u'params': {u'capacity': 5}}, u'components': [{u'function': u'equality', u'columns': [u'Department', u'Department']}]}}

            match = Match(client=c, name=name, config=cfg)
            match.save()

            data_table_ids = [x['data_table']['id'] for x in cfg['load']]
            for data_table_id in data_table_ids:
                data_table = DataTable.objects.get(pk=data_table_id)
                match.data_tables.add(data_table)
            match.save()


            return HttpResponseRedirect('/match/view/' + str(match.id))

        else:
            print match_form.errors

    else:
        match_form = MatchForm(client=c)
        context = {
            'c': c,
            'data_tables': data_tables,
            'matches': matches,
            'match_form': match_form
        }

    return render(request, 'match/create.html', context)


@login_required
def create_employeerole(request):

    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    match_form = MatchForm(client=c)
    context = {
        'c': c,
        'data_tables': data_tables,
        'matches': matches,
        'match_form': match_form
    }

    return render(request, 'match/create_employeerole.html', context)


@login_required
def run(request, match_id):

    c = request.user.client

    match = Match.objects.get(id=match_id)
    if match.client != c:
        return HttpResponse("You are not permissioned.")

    match.run()

    return HttpResponseRedirect('/match/view/' + str(match.id))


@login_required
def analyze(request, match_id):

    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    match = Match.objects.get(id=match_id)
    if match.client != c:
        return HttpResponse("You are not permissioned.")

    analytics = match_analytics(match)

    context = {
        'c': c,
        'data_tables': data_tables,
        'matches': matches,
        'match': match,
        'analytics': analytics
    }

    return render(request, 'match/analyze.html', context)


@login_required
def delete(request, match_id):

    c = request.user.client
    match = Match.objects.get(pk=match_id)

    if match.client != c:
        return HttpResponse("You are not permissioned.")

    match.delete()

    return HttpResponseRedirect('/welcome/home/')

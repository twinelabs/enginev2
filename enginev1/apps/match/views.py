from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

import datetime
import pdb

from entwine import entwine
from models import *
from .forms import MatchForm

@login_required
def feedback(request):
    return render(request, 'match/feedback.html', {})


@login_required
def create(request):

    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    if request.method == 'POST':
        match_form = MatchForm(data=request.POST, client=c)

        if match_form.is_valid():

            name = match_form.cleaned_data['name']
            config = match_request_to_config(request.POST)

            match = Match(client=c, name=name, config=config)
            match.save()

            data_table_ids = [x['id'] for x in match_config['load']]
            for data_table_id in data_table_ids:
                data_table = DataTable.objects.get(data_table_id)
                match.data_tables.add(data_table)

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
def create_custom(request):

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

    return render(request, 'match/create_custom.html', context)


@login_required
def view(request, match_id):

    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    match = Match.objects.get(id=match_id)
    if match.client != c:
        return HttpResponse("You are not permissioned.")

    match_data_tables = match.data_tables.all()
    match_config = match.config

    match_result = match.result if match.result != {} else ''

    context = {
        'c': c,
        'data_tables': data_tables,
        'matches': matches,
        'match': match,
        'match_data_tables': match_data_tables,
        'match_config': match_config,
        'match_result': match_result
    }

    return render(request, 'match/view.html', context)


@login_required
def run(request, match_id):

    c = request.user.client

    match = Match.objects.get(id=match_id)
    if match.client != c:
        return HttpResponse("You are not permissioned.")

    entwine.run_match(match)

    return HttpResponseRedirect('/match/view/' + str(match.id))



@login_required
def analyze(request, match_id):

    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    match = Match.objects.get(id=match_id)
    if match.client != c:
        return HttpResponse("You are not permissioned.")

    context = {
        'c': c,
        'data_tables': data_tables,
        'matches': matches,
        'overview_items': [
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
                'value': '0.64 (employees), 0.73 (roles)'
            },
            {
                'img': "img/demo/matched_users.png",
                'title': 'Matched Users',
                'value': '275 Roles'
            },
            {
                'img': "img/demo/matches_per_user.png",
                'title': 'Matches per Role',
                'value': '5 employees per role'
            },
            {
                'img': "img/demo/total_matches.png",
                'title': 'Total # Matches',
                'value': '1,375 Total Suggestions Made'
            }
        ]
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

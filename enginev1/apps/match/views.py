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
        match_form = MatchForm(data=request.POST)

        if match_form.is_valid():
            client = request.user.client
            data_tables = match_form.cleaned_data['data_tables']
            name = match_form.cleaned_data['name']
            config = {
                'task': match_form.cleaned_data['task'],
                'column_names': [col.name for col in match_form.cleaned_data['columns']],
                'k_size': match_form.cleaned_data['k_size']
            }

            match = Match(client=client, name=name, config=config)
            match.save()
            for data_table in data_tables:
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
                'title': 'Match Strength',
                'value': '9.3 (High)'
            },
            {
                'img': "img/demo/match_variables.png",
                'title': '# of Variables',
                'value': '45'
            },
            {
                'img': "img/demo/diversity_coefficient.png",
                'title': 'Diversity Score',
                'value': '7.8'
            },
            {
                'img': "img/demo/matched_users.png",
                'title': 'Matched Users',
                'value': '1,000'
            },
            {
                'img': "img/demo/matches_per_user.png",
                'title': 'Matches per User',
                'value': '10'
            },
            {
                'img': "img/demo/total_matches.png",
                'title': 'Total # Matches',
                'value': '10,000'
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

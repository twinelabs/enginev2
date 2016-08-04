from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

import datetime

from entwine import entwine
from models import *
from .forms import MatchForm


@login_required
def create(request):

    if request.method == 'POST':
        match_form = MatchForm(data=request.POST)

        if match_form.is_valid():

            client = request.user.client
            data_tables = '???'
            name = match_form.cleaned_data['name']
            config = {
                'task': match_form.cleaned_data['task'],
                'colnames': match_form.cleaned_data['colnames'],
                'k_size': match_form.cleaned_data['k_size']
            }

            match = Match(client=client, data_tables=data_tables, name=name, config=config)
            match.save()

            return HttpResponseRedirect('/match/summary/')

        else:
            print match_form.errors

    else:
        match_form = MatchForm()

    context = { 'match_form': match_form }
    return render(request, 'match/create.html', context)


@login_required
def view(request, match_id):

    c = request.user.client

    match = Match.objects.get(id=match_id)
    if match.client != c:
        return HttpResponse("You are not permissioned.")

    context = {}

    return render(request, 'match/analyze.html', context)


@login_required
def analyze(request, match_id):

    c = request.user.client

    match = Match.objects.get(id=match_id)
    if match.client != c:
        return HttpResponse("You are not permissioned.")

    context = {
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

    return HttpResponseRedirect('/match/summary/')


"""
@login_required
def run_match(request, config_id):

    c = request.user.client
    config = Config.objects.get(pk=config_id)

    if config.client != c:
        return HttpResponse("You are not permissioned.")

    result_output = entwine.run_match(config)
    result_name = config.name + ', run at ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    result = Result(client = c, name = result_name, config = config, output = result_output)
    result.save()

    return HttpResponseRedirect('/match/view/' + str(config.id))
"""
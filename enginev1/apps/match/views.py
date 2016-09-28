from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

import datetime
import pdb
import json

from .models import *
from .utils import *
from .forms import MatchGroupForm, MatchAssignForm


@login_required
def view(request, match_id):
    match = Match.objects.get(id=match_id)

    if match.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    config_html = match_config_as_html(match)

    has_results = match.has_results()
    if has_results:
        result_html = match_results_as_html(match)
    else:
        result_html = None

    context = {
        'match': match,
        'has_results': has_results,
        'config_html': config_html,
        'result_html': result_html,
    }

    return render(request, 'match/view.html', context)


@login_required
def feedback(request, match_id):
    match = Match.objects.get(id=match_id)

    if match.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    (group_numbers, feedback_s) = match_results_for_feedback(match)

    context = {
        'match': match,
        'group_numbers': group_numbers,
        'feedback_s': feedback_s
    }
    return render(request, 'match/feedback.html', context)


@login_required
def feedback_old(request):
    return render(request, 'match/feedback_old.html', {})


@login_required
def feedback_employeerole(request):
    return render(request, 'match/feedback_employeerole.html', {})


@login_required
def create(request):
    return render(request, 'match/create.html', {})


@login_required
def create_group(request):

    if request.method == 'POST':
        name = request.POST['name']
        cfg = create_group_request_to_config(request.POST)

        try:
            match = Match(client=c, name=name, config=cfg)
            match.save()

            data_table_id = cfg['load'][0]['data_table']['id']
            data_table = DataTable.objects.get(pk=data_table_id)
            match.data_tables.add(data_table)
            match.save()

            return HttpResponseRedirect('/match/view/' + str(match.id))

        except:
            return HttpResponse("Improper match parameters")

    else:
        match_group_form = MatchGroupForm()
        context = {
            'match_group_form': match_group_form
        }

    return render(request, 'match/create_group.html', context)


@login_required
def create_assign(request):

    if request.method == 'POST':
        name = request.POST['name']
        cfg = create_assign_request_to_config(request.POST)

        try:
            match = Match(client=c, name=name, config=cfg)
            match.save()

            data_table_id = cfg['load'][0]['data_table']['id']
            data_table = DataTable.objects.get(pk=data_table_id)
            match.data_tables.add(data_table)
            data_table_id = cfg['load'][1]['data_table']['id']
            data_table = DataTable.objects.get(pk=data_table_id)
            match.data_tables.add(data_table)
            match.save()

            return HttpResponseRedirect('/match/view/' + str(match.id))

        except:
            return HttpResponse("Improper match parameters")

    else:
        match_assign_form = MatchAssignForm()
        context = {
            'match_assign_form': match_assign_form
        }

    return render(request, 'match/create_assign.html', context)


@login_required
def create_employeerole(request):

    match_form = MatchForm(client=c)
    context = {
        'match_form': match_form
    }

    return render(request, 'match/create_employeerole.html', context)


@login_required
def run(request, match_id):
    match = Match.objects.get(id=match_id)

    if match.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    match.run()

    return HttpResponseRedirect('/match/view/' + str(match.id))


@login_required
def analyze(request, match_id):
    match = Match.objects.get(id=match_id)

    if match.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    analytics = match_analytics(match)

    context = {
        'match': match,
        'analytics': analytics
    }

    return render(request, 'match/analyze.html', context)


@login_required
def delete(request, match_id):
    match = Match.objects.get(id=match_id)

    if match.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    match.delete()

    return HttpResponseRedirect('/welcome/home/')

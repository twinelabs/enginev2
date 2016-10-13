from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

import pdb

from .models import *
from .utils import *
from .forms import MatchGroupForm, MatchAssignForm


@login_required
def view(request, match_id):
    match = Match.objects.get(id=match_id)

    if match.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    match_config = match.config['match']
    match_data_table_names = match.data_table_names()
    match_rules = zip(match_config['components'], match_config['weights'])
    match_result_data = match.result_data()
    match_result_header = match.result_header()

    context = {
        'match': match,
        'match_config': match_config,
        'match_data_table_names': match_data_table_names,
        'match_rules': match_rules,
        'match_result_data': match_result_data,
        'match_result_header': match_result_header
    }

    return render(request, 'match/view.html', context)


@login_required
def feedback(request, match_id):
    match = Match.objects.get(id=match_id)

    if match.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    match_data_table_names = match.data_table_names()
    match_result_data = match.result_data()
    match_result_header = match.result_header()

    context = {
        'match': match,
        'match_data_table_names': match_data_table_names,
        'match_result_data': match_result_data,
        'match_result_header': match_result_header
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
            match = Match(client=c, name=name, config=cfg, task='group')
            match.save()

            data_table_id = cfg['load'][0]['data_table']['id']
            data_table = DataTable.objects.get(pk=data_table_id)
            MatchDataTable.objects.create(match=match, data_table=data_table, data_table_order=1)

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
            c = request.user.client
            match = Match(client=c, name=name, config=cfg, task='assign')
            match.save()

            data_table_id = cfg['load'][0]['data_table']['id']
            data_table = DataTable.objects.get(pk=data_table_id)
            MatchDataTable.objects.create(match=match, data_table=data_table, data_table_order=1)

            data_table_id = cfg['load'][1]['data_table']['id']
            data_table = DataTable.objects.get(pk=data_table_id)
            MatchDataTable.objects.create(match=match, data_table=data_table, data_table_order=2)

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

    match_form = MatchAssignForm()
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


@login_required
def export_xls(request, match_id):
    match = Match.objects.get(id=match_id)

    if match.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    xls_response = export_assign_as_excel(match)
    return xls_response

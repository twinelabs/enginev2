from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

import datetime

from entwine import entwine
from models import *
from .forms import MatchConfigForm


@login_required
def summary(request):

    c = request.user.client
    matches = c.config_set.all()

    context = {
        'matches': matches,
    }
    return render(request, 'match/summary.html', context)



@login_required
def create_match(request):

    if request.method == 'POST':
        match_config_form = MatchConfigForm(data=request.POST)

        if match_config_form.is_valid():

            client = request.user.client
            name = match_config_form.cleaned_data['name']
            params = {
                'task': match_config_form.cleaned_data['task'],
                'colnames': match_config_form.cleaned_data['colnames'],
                'k_size': match_config_form.cleaned_data['k_size']
            }

            match_config = Config(client=client, name=name, params=params)
            match_config.save()

            return HttpResponseRedirect('/match/summary/')

        else:
            print match_config_form.errors

    else:
        match_config_form = MatchConfigForm()

    context = { 'match_config_form': match_config_form }
    return render(request, 'match/create_match.html', context)


@login_required
def view(request, config_id):

    c = request.user.client
    config = Config.objects.get(pk=config_id)
    results = config.result_set.all()

    if config.client != c:
        return HttpResponse("You are not permissioned.")

    context = {
        'config': config,
        'items': config.params.items(),
        'results': results
    }

    return render(request, 'match/view.html', context)


@login_required
def view_result(request, result_id):

    c = request.user.client
    result = Result.objects.get(pk=result_id)

    if result.client != c:
        return HttpResponse("You are not permissioned.")

    context = {
        'result': result,
        'clusters_with_data': result.clusters_with_data,
        'items': result.output.items()
    }

    return render(request, 'match/view_result.html', context)


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


@login_required
def delete_match(request, config_id):

    c = request.user.client
    config = Config.objects.get(pk=config_id)

    if config.client != c:
        return HttpResponse("You are not permissioned.")

    config.delete()

    return HttpResponseRedirect('/match/summary/')


@login_required
def delete_result(request, config_id, result_id):

    c = request.user.client
    result = Result.objects.get(pk=result_id)

    if result.client != c:
        return HttpResponse("You are not permissioned.")

    result.delete()

    return HttpResponseRedirect('/match/view/' + str(config_id))

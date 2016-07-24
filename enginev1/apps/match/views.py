from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from models import *

@login_required
def summary(request):

    c = request.user.client

    matches = c.config_set.all()
    results = c.result_set.all()

    context = {
        'matches': matches,
        'results': results,
    }

    return render(request, 'match/summary.html', context)


@login_required
def view(request, config_id):

    c = request.user.client
    config = Config.objects.get(pk=config_id)

    if config.client != c:
        return HttpResponse("You are not permissioned.")

    context = {
        'config': config,
        'items': config.params.items()
    }

    return render(request, 'match/view.html', context)


@login_required
def run_match(request, config_id):

    c = request.user.client
    config = Config.objects.get(pk=config_id)

    if config.client != c:
        return HttpResponse("You are not permissioned.")

    
    context = {
        'config': config,
        'items': config.params.items()
    }

    return render(request, 'match/view.html', context)

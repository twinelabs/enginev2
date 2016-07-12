from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

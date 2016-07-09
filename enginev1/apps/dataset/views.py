from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def summary(request):

    c = request.user.client

    alpha_label = c.alpha_label if c.alpha_label != '' else "Dataset #1 Items"
    beta_label = c.beta_label if c.beta_label != '' else "Dataset #2 Items"

    alphas = c.alpha_set.all()
    betas = c.beta_set.all()

    context = {
        'alpha_label': alpha_label,
        'beta_label': beta_label,
        'alphas': alphas,
        'betas': betas,
    }

    return render(request, 'dataset/summary.html', context)


@login_required
def viewA(request):

    c = request.user.client

    alpha_label = c.alpha_label if c.alpha_label != '' else "Dataset #1 Items"
    alphas = c.alpha_set.all()

    context = {
        'dataset_label': alpha_label,
        'dataset': alphas,
    }

    return render(request, 'dataset/view.html', context)


@login_required
def viewB(request):

    c = request.user.client

    beta_label = c.beta_label if c.beta_label != '' else "Dataset #2 Items"
    betas = c.beta_set.all()

    context = {
        'dataset_label': beta_label,
        'dataset': betas,
    }

    return render(request, 'dataset/view.html', context)
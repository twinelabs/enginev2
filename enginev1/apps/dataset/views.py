from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import UserForm, ClientForm

@login_required
def dashboard(request):

    c = request.user.client

    alpha_label = c.alpha_label if c.alpha_label not null else "Dataset #1 Items"
    beta_label = c.beta_label if c.beta_label not null else "Dataset #1 Items"

    alphas = c.alphas
    betas = c.betas

    context = {
        'alpha_label': alpha_label,
        'beta_label': beta_label,
        'alphas': alphas,
        'betas': betas,
    }

    render(request, 'dataset/dashboard', context)
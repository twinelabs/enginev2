from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import DatasetObjectsToPandas as to_pandas_df

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
def view(request, alpha_or_beta):

    c = request.user.client

    if alpha_or_beta == 'alpha':
        label = c.alpha_label if c.alpha_label != '' else "Dataset #1 Items"
        objs = c.alpha_set.all()

    else:
        label = c.beta_label if c.beta_label != '' else "Dataset #2 Items"
        objs = c.beta_set.all()

    df = to_pandas_df(objs)
    df_html = df.to_html()

    context = {
        'label': label,
        'df_html': df_html
    }

    return render(request, 'dataset/view.html', context)

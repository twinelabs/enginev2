from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .utils import *
from .forms import UploadCSVForm


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

    df = dataset_objects_to_pandas_df(objs)
    df_html = df.to_html(classes=['table', 'table-striped', 'table-condensed'])

    context = {
        'label': label,
        'df_html': df_html
    }

    return render(request, 'dataset/view.html', context)


@login_required
def upload_csv(request):

    if request.method == 'POST':
        csv_form = UploadCSVForm(request.POST, request.FILES)

        if csv_form.is_valid():

            client = request.user.client
            alpha_or_beta = csv_form.cleaned_data['alpha_or_beta']
            csv_file = request.FILES['csv_file']

            import_csv_as_dataset(client, alpha_or_beta, csv_file)

            return HttpResponseRedirect('/dataset/view/' + alpha_or_beta)

    else:
        csv_form = UploadCSVForm()
        context = { 'csv_form': csv_form }

    return render(request, 'dataset/upload_csv.html', context)
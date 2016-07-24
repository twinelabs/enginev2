import csv
import xlwt

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

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
    df_html = df.to_html(classes=['dataset-table'])

    context = {
        'alpha_or_beta': alpha_or_beta,
        'label': label,
        'df_count': len(df),
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


@login_required
def export_csv(request, alpha_or_beta):

    c = request.user.client

    if alpha_or_beta == 'alpha':
        label = c.alpha_label if c.alpha_label != '' else "Dataset #1 Items"
        objs = c.alpha_set.all()

    else:
        label = c.beta_label if c.beta_label != '' else "Dataset #2 Items"
        objs = c.beta_set.all()

    df = dataset_objects_to_pandas_df(objs)
    csv_header = df.columns.values.tolist()
    csv_rows = df.values.tolist()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + label + '.csv"'

    writer = csv.writer(response)
    writer.writerows([csv_header] + csv_rows)

    return response


@login_required
def export_xls(request, alpha_or_beta):

    c = request.user.client

    if alpha_or_beta == 'alpha':
        label = c.alpha_label if c.alpha_label != '' else "Dataset #1 Items"
        objs = c.alpha_set.all()

    else:
        label = c.beta_label if c.beta_label != '' else "Dataset #2 Items"
        objs = c.beta_set.all()

    df = dataset_objects_to_pandas_df(objs)
    csv_header = df.columns.values.tolist()
    csv_rows = df.values.tolist()

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + label + '.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Data")

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    i_row = 0
    for i_col, colname in enumerate(df.columns.values.tolist()):
        ws.write(i_row, i_col, colname, font_style)
        ws.col(i_col).width = 4000

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for csv_row in csv_rows:
        i_row += 1
        for i_col, x in enumerate(csv_row):
            ws.write(i_row, i_col, x, font_style)

    wb.save(response)
    return response


@login_required
def delete(request, alpha_or_beta):

    c = request.user.client

    if alpha_or_beta == 'alpha':
        objs = c.alpha_set.all()

    else:
        objs = c.beta_set.all()

    objs.delete()

    context = {}

    return HttpResponseRedirect('/dataset/summary/')

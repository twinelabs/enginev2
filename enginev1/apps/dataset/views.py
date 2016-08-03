import csv
import xlwt
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from .utils import *
from .forms import UploadCSVForm
from .models import DataTable, DataColumn


@login_required
def view(request, data_table_id):

    c = request.user.client

    data_table = DataTable.objects.get(id=data_table_id)
    if data_table.client != c:
        return HttpResponse("You are not permissioned.")

    data_table_columns, data_table_values = data_table_to_lists(data_table)

    context = {
        'data_table_columns': data_table_columns
        'data_table_values': data_table_values
    }

    return render(request, 'dataset/view.html', context)


@login_required
def analytics(request, data_table_id):

    c = request.user.client

    data_table = DataTable.objects.get(id=data_table_id)
    if data_table.client != c:
        return HttpResponse("You are not permissioned.")

    df = data_table_to_df(data_table)
    dashboard = [df_to_dashboard(df, 1, "my table", True)]
    dashboard_s = json.dumps(dashboard)

    context = {
        'dashboard': dashboard,
        'dashboard_s': dashboard_s
    }

    return render(request, 'dataset/analytics.html', context)


@login_required
def upload_csv(request):

    c = request.user.client

    if request.method == 'POST':
        csv_form = UploadCSVForm(request.POST, request.FILES)

        if csv_form.is_valid():

            client = request.user.client
            csv_file = request.FILES['csv_file']
            data_table_id = import_csv_as_dataset(client, csv_file)

            return HttpResponseRedirect('/dataset/view/' + str(data_table_id))

    else:
        csv_form = UploadCSVForm()
        context = { 'csv_form': csv_form }

    return render(request, 'dataset/upload_csv.html', context)


@login_required
def export_csv(request, data_table_id):

    c = request.user.client

    data_table = DataTable.objects.get(id=data_table_id)
    if data_table.client != c:
        return HttpResponse("You are not permissioned.")

    df = data_table_to_df(data_table)
    csv_header = df.columns.values.tolist()
    csv_rows = df.values.tolist()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + label + '.csv"'

    writer = csv.writer(response)
    writer.writerows([csv_header] + csv_rows)

    return response


@login_required
def export_xls(request, data_table_id):

    c = request.user.client

    data_table = DataTable.objects.get(id=data_table_id)
    if data_table.client != c:
        return HttpResponse("You are not permissioned.")

    df = data_table_to_df(data_table)
    csv_header = df.columns.values.tolist()
    csv_rows = df.values.tolist()

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + data_table.name + '.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Data")

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    i_row = 0
    for i_col, colname in enumerate(csv_header):
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
def delete(request, data_table_id):

    c = request.user.client

    data_table = DataTable.objects.get(id=data_table_id)
    if data_table.client != c:
        return HttpResponse("You are not permissioned.")

    data_table.delete()
    context = {}

    return HttpResponseRedirect('/welcome/home/')

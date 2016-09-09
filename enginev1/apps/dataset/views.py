import csv
import xlwt
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from .utils import *
from .forms import UploadCSVForm
from .models import DataTable


@login_required
def upload_csv(request):
    """ Upload CSV into DataTable object.
    """

    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    if request.method == 'POST':
        csv_form = UploadCSVForm(request.POST, request.FILES)

        if csv_form.is_valid():
            client = request.user.client
            name = request.POST['name']
            csv_file = request.FILES['csv_file']
            data_table_id = import_csv_as_data_table(client, name, csv_file)

            return HttpResponseRedirect('/dataset/view/' + str(data_table_id))

        else:
            print csv_form.errors

    else:
        csv_form = UploadCSVForm()
        context = {
            'csv_form': csv_form,
            'c': c,
            'data_tables': data_tables,
            'matches': matches
        }

    return render(request, 'dataset/upload_csv.html', context)


@login_required
def view(request, data_table_id):

    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    data_table = DataTable.objects.get(id=data_table_id)
    if data_table.client != c:
        return HttpResponse("You are not permissioned.")

    # TODO: Figure out why ignores first column?

    data_table_columns, data_table_values = data_table_to_lists(data_table)
    data_table_count = len(data_table_values)

    context = {
        'c': c,
        'data_tables': data_tables,
        'matches': matches,
        'data_table': data_table,
        'data_table_columns': data_table_columns,
        'data_table_values': data_table_values,
        'data_table_count': data_table_count
    }

    return render(request, 'dataset/view.html', context)


@login_required
def analytics(request, data_table_id):

    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    data_table = DataTable.objects.get(id=data_table_id)
    if data_table.client != c:
        return HttpResponse("You are not permissioned.")

    df = data_table_to_df(data_table)
    dashboard = [df_to_dashboard(df, 1, "my table", True)]
    dashboard_s = json.dumps(dashboard)

    context = {
        'c': c,
        'data_tables': data_tables,
        'matches': matches,
        'data_table': data_table,
        'dashboard': dashboard,
        'dashboard_s': dashboard_s
    }

    return render(request, 'dataset/analytics.html', context)



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
    response['Content-Disposition'] = 'attachment; filename="' + data_table.name + ' - Export.csv"'

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
    response['Content-Disposition'] = 'attachment; filename="' + data_table.name + ' - Export.xls"'
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
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    data_table = DataTable.objects.get(id=data_table_id)
    if data_table.client != c:
        return HttpResponse("You are not permissioned.")

    data_table.delete()
    context = {
        'c': c,
        'data_tables': data_tables,
        'matches': matches
    }

    return HttpResponseRedirect('/welcome/home/')

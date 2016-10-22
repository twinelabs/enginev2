import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .utils import *
from .forms import UploadCSVForm
from .models import DataTable


@login_required
def upload_csv(request):
    """ Upload CSV into DataTable object.
    """

    context = {}

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
        }

    return render(request, 'dataset/upload_csv.html', context)


@login_required
def view(request, data_table_id):
    """ Pulls header and data values for viewing.
    """

    data_table = DataTable.objects.get(id=data_table_id)

    if data_table.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    (dt_header, dt_values, dt_count) = data_table.as_table_data()

    context = {
        'data_table': data_table,
        'dt_header': dt_header,
        'dt_values': dt_values,
        'dt_count': dt_count
    }

    return render(request, 'dataset/view.html', context)


@login_required
def analytics(request, data_table_id):
    """ Creates JSON used by data viz dashboard.
    """
    data_table = DataTable.objects.get(id=data_table_id)

    if data_table.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    viz_data = data_table.to_viz_data()
    viz_data_s = json.dumps(viz_data)

    context = {
        'data_table': data_table,
        'viz_data_s': viz_data_s
    }

    return render(request, 'dataset/analytics.html', context)


@login_required
def export_csv(request, data_table_id):

    data_table = DataTable.objects.get(id=data_table_id)

    if data_table.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    csv_response = export_data_table_as_csv(data_table)
    return csv_response


@login_required
def export_xls(request, data_table_id):

    data_table = DataTable.objects.get(id=data_table_id)

    if data_table.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    xls_response = export_data_table_as_xls(data_table)
    return xls_response


@login_required
def delete(request, data_table_id):

    data_table = DataTable.objects.get(id=data_table_id)

    if data_table.client != request.user.client:
        return HttpResponse("You are not permissioned.")

    data_table.delete()

    return HttpResponseRedirect('/welcome/home/')

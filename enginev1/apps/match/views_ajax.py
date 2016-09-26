from django.http import JsonResponse

from .models import *


def get_data_table_columns(request):

    data_table_id = request.GET.get('data_table_id', None)
    data_table = DataTable.objects.get(pk=data_table_id)

    data_columns = DataColumn.objects.filter(data_table=data_table)
    columns_data = [ (c.id, c.name) for c in data_columns]

    return JsonResponse(columns_data, safe=False)


# TODO: collapse into 1 function
def get_data_column(request):

    data_column_id = request.GET.get('data_column_id', None)
    data_column = DataColumn.objects.get(pk=data_column_id)

    column_data = [data_column.id, data_column.name, data_column.dtype]

    return JsonResponse(column_data, safe=False)


def get_two_data_columns(request):

    data_column_ids = request.GET.get('data_column_ids', None)

    d1 = DataColumn.objects.get(pk=data_column_ids[0])
    c1 = [d1.id, d1.name, d1.dtype]

    d2 = DataColumn.objects.get(pk=data_column_ids[1])
    c2 = [d2.id, d2.name, d2.dtype]

    column_data = [c1, c2]

    return JsonResponse(column_data, safe=False)


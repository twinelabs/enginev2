from django.http import JsonResponse

from .models import *


def get_data_table_columns(request):

    data_table_id = request.GET.get('data_table_id', None)
    data_table = DataTable.objects.get(pk=data_table_id)

    data_columns = DataColumn.objects.filter(data_table=data_table)
    columns_data = [ (c.id, c.name) for c in data_columns]

    return JsonResponse(columns_data, safe=False)


def get_data_column(request):

    data_column_id = request.GET.get('data_column_id', None)
    data_column = DataColumn.objects.get(pk=data_column_id)

    column_data = [data_column.id, data_column.name, data_column.dtype]

    return JsonResponse(column_data, safe=False)


import pandas as pd
import csv
import xlwt

from django.http import HttpResponse

import models
import pdb

def import_csv_as_data_table(client, name, csv_file):
    """ Loads csv file into DataTable object and creates DataColumn objects.
    Returns data_table_id if successfully saved.
    """

    df = pd.read_csv(csv_file, na_filter=False, encoding='latin-1')
    n_rows, n_cols = df.shape
    list_of_dicts = df.to_dict(orient='records')

    data_table = models.DataTable(client = client,
                                  name = name,
                                  data = { 'data': list_of_dicts },
                                  n_rows = n_rows,
                                  n_cols = n_cols)

    data_table.save()

    # Create columns
    for i, column_name in enumerate(list(df.columns.values)):
        dtype = str(df.dtypes[i])
        vals = list(df[column_name])
        n_unique = len(set(vals))
        n_nonblank = len([x for x in vals if x != ''])

        data_column = models.DataColumn(
            data_table = data_table,
            name = column_name,
            dtype = dtype,
            order_original = i,
            order_custom = i,
            n_unique = n_unique,
            n_nonblank = n_nonblank
        )
        data_column.save()

    return data_table.id


def export_data_table_as_csv(data_table):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + data_table.name + ' - Export.csv"'

    writer = csv.writer(response)
    writer.writerows([data_table.header()] + data_table.values())

    return response


def export_data_table_as_xls(data_table):

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + data_table.name + ' - Export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Data")

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    i_row = 0
    for i_col, colname in enumerate(data_table.header()):
        ws.write(i_row, i_col, colname, font_style)
        ws.col(i_col).width = 4000

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for csv_row in data_table.values():
        i_row += 1
        for i_col, x in enumerate(csv_row):
            ws.write(i_row, i_col, x, font_style)

    wb.save(response)

    return response


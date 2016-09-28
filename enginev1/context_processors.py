
def insert_client_data(request):

    u = request.user.id

    if u:
        c = request.user.client
        data_tables = c.datatable_set.all()
        matches = c.match_set.all()

        context = {
            'c': c,
            'data_tables': data_tables,
            'matches': matches
        }
    else:
        context = {}

    return context

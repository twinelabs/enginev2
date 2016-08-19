"""
matching.clustering.run_multiple
-------------------------

Functions to set up, run, and save clustering.
"""

def cluster_simple(data, df_master, cluster_params, print_results=True, save_tag=False):
    """
    Clusters data given distance functions in df_master, evaluates output on euclidean distance.
    """

    cc = closeness.Closeness(data, df_master)
    #cc.describe_distance(True)

    dd = cc.ds['master']
    kk = cluster.Cluster(cc.ds['master'], cluster_params)
    results = kk.data_by_clusters(data)

    df_euclid = distance_objects.df_cade_euclidean
    cc_euclid = closeness.Closeness(data, df_euclid)
#    print('> Average L2: ' + kk.goodness(cc_euclid.ds['master']))
    gofs = kk.goodness_all(cc_euclid.ds['master'])

    if print_results:
        for df_name in ['master']:
            print('> ' + df_name + ': ' + kk.goodness(cc.ds[df_name]))

    if save_tag:
        io.save_csv(data, save_tag + 'data.csv')
        io.save_csv(dd, save_tag + 'd.csv')
        io.save_csv(results, save_tag + 'results.csv')

#    return numpy.mean(gofs)
    return gofs


def run_cluster(n_people, m_columns, k_size, k_method, df_name):
    """
    Cluster randomly generated data and return gofs.
    """

    data = gen_data(n_people, m_columns)

    if df_name == 'euclidean_inv':
        df_master = distance_objects.df_cade_euclidean_inv
    elif df_name == "euclidean_neg":
        df_master = distance_objects.df_cade_euclidean_neg
    elif df_name == "euclidean":
        df_master = distance_objects.df_cade_euclidean

    cluster_params_greedy = { 'method': k_method, 'k_size': k_size}
    print_results = False
    save_tag = False #'./results/test/'

    print('\nn = ' + str(n_people) + ', m = ' + str(m_columns) + ', k_size = ' + str(k_size) + ', k_method = ' + k_method + ', df = ' + df_name)
    gofs = cluster_simple(data, df_master, cluster_params_greedy, print_results, save_tag)
    return gofs
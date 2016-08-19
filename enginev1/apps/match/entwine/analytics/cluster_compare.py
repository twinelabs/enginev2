"""
analytics.cluster_compare
-------------------------

Functions to run and compare different clustering methods.
"""


def run_experiment(data, n_control, df_master, print_results=True, save_tag=False):
    """ Run RANDOM control and GREEDY target clusters, and compare results.
    """

    n = len(data) - 1
    n_target = n - n_control

    d = data[1:]
    numpy.random.shuffle(d)

    data_control = [data[0]] + d[:n_control]
    data_target = [data[0]] + d[n_control:]

    c_control = closeness.Closeness(data_control, df_master)
    d_control = c_control.ds['master']
    k_control = cluster.Cluster(d_control, { 'method': 'random' })
    results_control = k_control.data_by_clusters(data_control)

    c_target = closeness.Closeness(data_target, df_master)
    d_target = c_target.ds['master']
    k_target = cluster.Cluster(d_target, { 'method': 'greedy' })
    results_target = k_target.data_by_clusters(data_target)

    if print_results:
        for df_name in ['master', 'Personality', 'Social', 'Structural', 'Professional']:
            print('> ' + df_name)
            print('Control: ' + k_control.goodness(c_control.ds[df_name]))
            print('Target: ' + k_target.goodness(c_target.ds[df_name]))

    if save_tag:
        subdirs = ['./data/', './experiment/', './results/']
        for subdir in subdirs:
            if not os.path.exists(sav_tag + subdir):
                os.makedirs(save_tag + subdir)

        io.save_csv(data, save_tag + './data/msd_r4_test.csv')

        io.save_csv(data_control, save_tag + './experiment/data_control.csv')
        io.save_csv(data_target, save_tag + './experiment/data_target.csv')

        io.save_csv(d_control, save_tag + './experiment/d_control.csv')
        io.save_csv(d_target, save_tag + './experiment/d_target.csv')

        io.save_csv(results_control, save_tag + './results/results_control.csv')
        io.save_csv(results_target, save_tag + './results/results_target.csv')


def basic_stats(res):
    stats = [[x[0], x[1], x[2], x[3], numpy.mean(x[4]), numpy.std(x[4])] for x in res]
    return stats



# ===
# Test Greedy v Cade
# ===

if False:

    m_columns = 3
    n_people = 48
    k_size = 4
    df_name = 'euclidean_inv'
    k_method = 'greedy'

    df_master = distance_objects.df_cade_euclidean_inv
    cluster_params= { 'method': k_method, 'k_size': k_size}

    means = []
    for i in range(10):
        data = gen_data(n_people, m_columns)
        gofs = cluster_simple(data, df_master, cluster_params, False, False)
        means += [numpy.mean(gofs)]

    print(k_method + ': ' + str(numpy.mean(means)) + '+/-' + str(numpy.std(means)))


    k_method = 'cade'

    df_master = distance_objects.df_cade_euclidean_inv
    cluster_params= { 'method': k_method, 'k_size': k_size}

    means = []
    for i in range(10):
        data = gen_data(n_people, m_columns)
        gofs = cluster_simple(data, df_master, cluster_params, False, False)
        means += [numpy.mean(gofs)]

    print(k_method + ': ' + str(numpy.mean(means)) + '+/-' + str(numpy.std(means)))


# ===
# Consider full search
# ===

if True:

    m_columns = 3
    n_people = 12
    k_size = 4
    df_name = 'euclidean_inv'
    k_method = 'fullsearch'

    df_master = distance_objects.df_cade_euclidean_inv
    cluster_params= { 'method': k_method, 'k_size': k_size}

    data = gen_data(n_people, m_columns)

    t0 = time.clock()
    gofs = cluster_simple(data, df_master, cluster_params, False, False)
    print(gofs)
    print time.clock() - t0, "sec"



# ===
# Run all params
# ===

if True:

    """
    Script to compare gofs across clustering methods, data size, and cluster size.
    """

    m_columns = 3

    n_peoples = [50, 200, 500]
    k_sizes = [2, 5, 10]
    df_names = ['euclidean_inv']
    k_methods = ['greedy', 'cade', 'random']

    res = []
    for n_people in n_peoples:
        for k_size in k_sizes:
            for df_name in df_names:
                for k_method in k_methods:
                    print ""
                    gofs = run_cluster(n_people, m_columns, k_size, k_method, df_name)
                    res += [(n_people, k_size, k_method, df_name, gofs)]

#    output = open('./results/sim/full_runs.pkl', 'wb')
#    pickle.dump(res, output)
#    output.close()

#    pkl_file = open('./results/sim/full_runs.pkl', 'rb')
#    res2 = pickle.load(pkl_file)
#    pkl_file.close()

    if True:
        gofs_split = [[x[4].tolist() for x in res[i:i+3]] for i in range(0, 27, 3)]
        io.save_csv(gofs_split[0], './results/diff_cade/gofs_n50_k2.csv')
        io.save_csv(gofs_split[1], './results/diff_cade/gofs_n50_k5.csv')
        io.save_csv(gofs_split[2], './results/diff_cade/gofs_n50_k10.csv')
        io.save_csv(gofs_split[3], './results/diff_cade/gofs_n200_k2.csv')
        io.save_csv(gofs_split[4], './results/diff_cade/gofs_n200_k5.csv')
        io.save_csv(gofs_split[5], './results/diff_cade/gofs_n200_k10.csv')
        io.save_csv(gofs_split[6], './results/diff_cade/gofs_n500_k2.csv')
        io.save_csv(gofs_split[7], './results/diff_cade/gofs_n500_k5.csv')
        io.save_csv(gofs_split[8], './results/diff_cade/gofs_n500_k10.csv')

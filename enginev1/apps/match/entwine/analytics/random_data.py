"""
analytics.random_data
-------------------------

Generates random data sets for analysis.
"""


def gen_d(n):
    """ Generates nxn matrix by sampling from [1, 2, 3, 4] with probability. """
    dd = [numpy.random.choice(4, n, p=[0.15, 0.35, 0.35, 0.15]) for i in range(n)]
    dd = [[x + 1 for x in row] for row in dd]
    return dd


def gen_data(n, m, mean=0.0, std=1.0):
    """
    Generates normally distributed numerical data for clustering.
    :param n: number of people (rows)
    :param m: number of factors (columns)
    :return: data array
    """
    col_headers = ['people'] + ['f' + str(i+1) for i in range(m)]
    body_t = [['p' + str(i+1) for i in range(n)]] + numpy.round(numpy.random.normal(mean, std, (m, n)), 2).tolist()
    body = [list(row) for row in zip(*body_t)]
    res = [col_headers] + body
    return res

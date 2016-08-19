"""
matching.distance.A_functions
-------------------------

Common functions to generate distance matrix from single data set (A).

Scenarios:
(n, f1) -> (n, n): feature vector to distance matrix
(n, n) -> (n, n): transformation of distance matrix

"""

import numpy as np
import math

import pdb

def distance_matrix(match_data_list, distance_config):
    if len(match_data_list) != 1:
        raise TypeError("Match data list must have 1 item for A_functions.distance_matrix")

    match_data = match_data_list[0]

    if 'cols' in distance_config:
        data_rows = match_data.select_cols_by_name(distance_config['cols'])
    else:
        data_rows = match_data.select_cols_by_index(range(1, match_data.n_cols))

    # if distance_config.get('to_float',False)
    if 'to_float' in distance_config and distance_config['to_float']:
        data_rows = [[ float(x) for x in row] for row in data_rows]
    if distance_config['f'] == "l2_norm":
        distance_matrix = l2_norm(data_rows) 
    elif distance_config['f'] == "binary_same":
        distance_matrix = binary_same(data_rows) 
    elif distance_config['f'] == "binary_diff":
        distance_matrix = binary_diff(data_rows)     
    elif distance_config['f'] == "d_exp_neg_l2_norm":
        distance_matrix = d_exp_neg_l2_norm(data_rows)
    elif distance_config['f'] == "d_exp_neg":
        distance_matrix = d_exp_neg(data_rows)
    elif distance_config['f'] == "d_vegas_school":
        distance_matrix = d_vegas_school(data_rows)
    elif distance_config['f'] == "binary_sames":
        distance_matrix = binary_sames(data_rows)
    else:
        raise TypeError("Unsupported distance function for clustering")


    return np.array(distance_matrix)


def neg(dd):
    """ -x for x in dd
    """
    res = [[ -x for x in row] for row in dd]
    return res


def exp(dd):
    """ exp(x) for x in dd
    """
    res = [[ math.exp(x) for x in row] for row in dd]
    return res


def l2(x, y):
    x2 = x if isinstance(x, list) else x.tolist()
    y2 = y if isinstance(y, list) else y.tolist()
    a = [float(i) for i in x2]
    b = [float(i) for i in y2]
    diff = np.subtract(a, b)
    return np.linalg.norm(diff)

def l2_norm(data_rows):
    """ l2_norm given data_rows
    """
    return [[l2(row_1, row_2) for row_1 in data_rows] for row_2 in data_rows]

def d_exp_neg_l2_norm(data_rows):
    """ exp(-L2(x_1, x_2))
    """

    l2_norms = [[l2(row_1, row_2) for row_1 in data_rows] for row_2 in data_rows]
    l2_norms_inv = exp(neg(l2_norms))

    dd = np.array(l2_norms_inv)
    return dd


def d_exp_neg(dd):
    """ exp(-x) for x in dd
    """

    res = np.array(exp(neg(dd)))
    return res


def binary_same2(x, y):
    same = [ 0 if x[i] == y[i] else 1 for i in range(len(x)) ]
    return sum(same)

def binary_sames(data_rows):
    n_sames = [[binary_same2(row_1, row_2) for row_1 in data_rows] for row_2 in data_rows]
    return np.array(n_sames)


def d_vegas_school(data_rows):

    same_school = [[ 1 if row_1 == row_2 else 0 for row_1 in data_rows] for row_2 in data_rows]
    dd = np.array(same_school)
    return dd


INDUSTRIES = ["Consulting", "CPGRetail", "EntrepreneurshipStartups", "GovtMilitaryNonprofit", "HealthcareBiotech", "InvestmentBanking", "InvestmentManagement", "MediaEntertainment", "PEVC", "RealEstate", "TechInternetEcommerce", "Other", "OtherText", "NoneInternship"]

def get_col(c, col_name):
    """ Returns single column (as list) with column name.
    """
    return c.data[:, c.col_names.index(col_name)].tolist()

def get_cols(c, col_names):
    """ Returns multiple columns (as array) matching column names.
    """
    cols_select = [i for i, col_name in enumerate(c.col_names)if col_name in col_names]
    return c.data[:, cols_select]

def strings_to_int(arr):
    """ Converts array of strings to 0 (empty) or 1 (non-empty)
    """
    arr[arr != ''] = 1
    arr[arr == ''] = 0
    return arr.astype(int)

def blanks_to_zero(arr):
    """ Converts zeros in array of strings to 0, converts to int
    """
    arr[arr == ''] = 0
    return arr.astype(int)

# ---
# DIST HELPERS
# ---

def binary_same(x):
    """ 0 if same entry, 1 if different
    :param x: list compared using ==
    :return: distance matrix
    """
    return [[0 if i == j else 1 for j in x] for i in x]

def binary_diff(x):
    """ 1 if same entry, 0 if different
    :param x: list compared using ==
    :return: distance matrix
    """
    return [[1 if i == j else 0 for j in x] for i in x]

def abs_diff(x):
    """ abs(i-j)
    :param x: numerical list
    :return: distance matrix
    """
    x = [float(x_i) for x_i in x]
    return [[abs(i-j) for j in x] for i in x]

def abs_diff_inv_exp(x):
    """ exp(-abs(i-j))
    :param x: numerical list
    :return: distance matrix
    """
    x = [float(x_i) for x_i in x]
    abs_diff = [[abs(i-j) for j in x] for i in x]
    abs_diff_inv_exp = [[math.exp(-x) for x in row] for row in abs_diff]
    return abs_diff_inv_exp

def abs_diff_inv_cap(x, cap=0.1):
    """ 1/abs(i-j), capped at cap
    :param x: numerical list
    :param cap: if 1/diff > cap, return cap
    :return: distance matrix
    """
    x = [float(x_i) for x_i in x]
    abs_diff = [[max(cap, abs(i-j)) for j in x] for i in x]
    abs_diff_inv_cap = [[1.0/x for x in row] for row in abs_diff]
    pdb.set_trace()
    return abs_diff_inv_cap

def scaled_abs_diff(x, default):
    """ Colname column is converted to float (default if blank),
    abs diff-ed, and scaled to one.
    :param x: numerical list, or blanks
    :param default: default value to insert for blank
    :return:
    """
    vals = [default if x_i == '' else float(x_i) for x_i in x]
    d = numpy.array(abs_diff(vals))
    d = d.astype(float)/d.max()
    return d

def separate(x, flag):
    """ Separates items in x that are both flag (1 if both flag, 0 otherwise)
    :param x: array of objects
    :return: distance matrix
    """
    return [[1 if (i == flag and j == flag) else 0 for j in x] for i in x]

def jaccard(arr):
    """ Calculates jaccard distance on membership array (0/1).
    If item has memberships, returns 0.2 for all distances.
    """
    zeros = [i for i,x in enumerate(arr.sum(axis=1)) if x == 0] # has no members

    n_groups = arr.shape[1]
    tarr = numpy.transpose(arr)
    intersect = numpy.dot(arr, tarr)
    union = n_groups - numpy.dot(1-arr, 1-tarr)
    union_nozero = numpy.copy(union)
    union_nozero[union == 0] = 1
    jaccard = intersect.astype(float)/union_nozero

    jaccard[:, zeros] = 0.2
    jaccard[zeros, :] = 0.2

    return jaccard

def d_separate_byfield(c, field, vals_to_separate):
    """ 1 if both ambassador, 0 otherwise
    :param field: column name to separate by
    :param vals: values to separate
    """
    vals = get_col(c, field)
    vals = ["SEPARATE" if val in vals_to_separate else val for val in vals]
    d = separate(vals, "SEPARATE")
    return numpy.array(d)

# ---
# DISTANCE FUNCTIONS - GOAL
# ---

d_goal = lambda c: d_scaled_abs_diff(c, 'Goal1to10', 6.8)


# ---
# DISTANCE FUNCTIONS - STRUCTURAL
# ---

def d_yearclustercohort(c):
    """ 0 if different year. within same year, 0.99 if same cohort,
    0.66 if same cluster, 0.33 if different cluster.
    Cleaning for clustercohort: downcase, remove dashes, treat blank and other as '5m'
    """
    grad_years = c.data[:, c.col_names.index('GraduationYear')]
    d1 = binary_diff(grad_years)

    cc = get_col(c, 'ClusterCohort')
    cc = [s.lower().replace('-','') for s in cc]
    cc = [s if len(s) == 2 else '5m' for s in cc]
    d_cluster = binary_diff([s[0] for s in cc])
    d_cohort = binary_diff([s[1] for s in cc])
    d2 = numpy.array(d_cluster) * 0.33 + numpy.array(d_cohort) * 0.33 + 0.33
    return numpy.multiply(d1, d2)

def d_clubs(c, selected_group):
    """ jaccard distance between club memberships of selected type
    """
    # get emails, map them
    emails = [email.lower() for email in get_col(c, "Email")]
    email_map = dict(io.load_csv('./other_data/email_map.csv'))
    emails = [email_map[e] if e in email_map and email_map[e] != '' else e for e in emails]

    # look up their memberships (set to 0 otherwise)
    memberships = io.load_csv('./other_data/memberships.csv')
    all_groups = memberships[0][1:]
    memberships = memberships[1:]
    memberships_emails = [m[0].lower() for m in memberships]

    # desired clubs
    groups = io.load_csv('./other_data/groups.csv')
    selected_groups = [0] + [i + 1 for i, g in enumerate(groups) if g[2] == selected_group]
    selected_memberships = [[x for i, x in enumerate(row) if i in selected_groups] for row in memberships]

    i_emails = [memberships_emails.index(e) if e in memberships_emails else -1 for e in emails]
    default = ['0'] * len(selected_memberships[0][1:])
    ms = [selected_memberships[i][1:] if i != -1 else default for i in i_emails]

    ms2 = numpy.array(ms).astype(int)
    d = jaccard(ms2)
    return d

def d_groupsize(c):
    gps = get_col(c, 'IdealGroupSize')
    gps2 = ['2' if gp == '1-on-1' else gp for gp in gps]
    gps3 = ['2' if gp == '2 (1-on-1)' else gp for gp in gps2]
    gps4 = ['7' if gp == '7+' else gp for gp in gps3]
    d = scaled_abs_diff(gps4, 5.0)
    return d

# ---
# DISTANCE FUNCTIONS - PROFESSIONAL
# ---

def d_workexperience(c):
    """ 1 for 5+yr diff, 0 for same yr.
    Treat blanks as 5yr
    """
    yrs = get_col(c, 'YearsWorkExperience')
    yrs_float = [5.0 if yr == '' else float(yr) for yr in yrs]
    d = numpy.array(abs_diff(yrs_float))
    d = numpy.clip(d, 0, 5)/5
    return d

def d_industryexperience(c):
    """ Jaccard distance on industries with experience.
    """
    col_names = ['IndustryExperienceMulti_' + industry for industry in INDUSTRIES]
    industry_cols = get_cols(c, col_names)
    memberships = strings_to_int(industry_cols)
    d = jaccard(memberships)
    return d

def d_industryintended(c):
    """ 1 minus Jaccard distance on industries intended.
    """
    col_names = ['IndustryIntendedMulti_' + industry for industry in INDUSTRIES]
    industry_cols = get_cols(c, col_names)
    memberships = strings_to_int(industry_cols)
    d = jaccard(memberships)
    d = 1 - d
    return d

# ---
# DISTANCE FUNCTIONS - SOCIAL
# ---

d_horrormovies = lambda c: numpy.array(binary_same(get_col(c, 'HorrorMovies')))
d_travelalone = lambda c: numpy.array(binary_same(get_col(c, 'TravelAlone')))
d_sailboat = lambda c: numpy.array(binary_same(get_col(c, 'Sailboat')))
d_favoritedrink = lambda c: numpy.array(binary_same(get_col(c, 'FavoriteDrink')))
d_favoritemusic = lambda c: numpy.array(binary_same(get_col(c, 'MusicGenre')))
d_favoritecuisine = lambda c: numpy.array(binary_same(get_col(c, 'CuisineLife')))

# ---
# DISTANCE FUNCTIONS - VALUES
# ---

d_scaled_abs_diff = lambda c, colname, default: scaled_abs_diff(get_col(c, colname), default)

d_introspective = lambda c: d_scaled_abs_diff(c, 'Introspective1to10', 7.0)

d_big5_o = lambda c: d_scaled_abs_diff(c, 'BigFiveOpenness', 3.6)
d_big5_c = lambda c: d_scaled_abs_diff(c, 'BigFiveConscientiousness', 3.7)
d_big5_e = lambda c: d_scaled_abs_diff(c, 'BigFiveExtraversion', 3.2)
d_big5_a = lambda c: d_scaled_abs_diff(c, 'BigFiveAgreeableness', 3.8)
d_big5_r = lambda c: d_scaled_abs_diff(c, 'BigFiveEmotionalReactivity', 2.8)
d_big5_p = lambda c: d_scaled_abs_diff(c, 'BigFivePositiveAffectivity', 3.8)

def d_motivation(c):
    """ Spearman's R of motivation rankings. Zero corr (0.5 distance) for blanks."""
    motivators = ['IntellectualStimulation', 'InfluencePower', 'PersonalRelationships', 'Achievement', 'Wealth']
    ranks = get_cols(c, ['MotivationBRank_' + s for s in motivators])
    ranks = blanks_to_zero(ranks) # 0 for no data
    zeros = numpy.amin(ranks, axis=1)

    rho = stats.spearmanr(ranks, axis=1)[0]
    rho = numpy.nan_to_num(rho)
    rho = rho*zeros
    rho = (rho.T * zeros).T
    dd = (1 - rho)/2
    return dd

# ---
# VEGAS
# ---

def d_values_vegas(c):
    """ Spearman's R of motivation rankings. Zero corr (0.5 distance) for blanks."""
    motivators = ['IntellectualStimulation', 'InfluencePower', 'PersonalRelationships', 'Achievement', 'Wealth']
    ranks = get_cols(c, ['ValuesRank_' + s for s in motivators])
    ranks = blanks_to_zero(ranks) # 0 for no data
    zeros = numpy.amin(ranks, axis=1)

    rho = stats.spearmanr(ranks, axis=1)[0]
    rho = numpy.nan_to_num(rho)
    rho = rho*zeros
    rho = (rho.T * zeros).T
    dd = (1 - rho)/2
    return dd

d_gender = lambda c: numpy.array(binary_diff(get_col(c, 'Gender')))
d_school = lambda c: numpy.array(binary_diff(get_col(c, 'School')))

def f_school(i, j):
    if i == 'Columbia' or i == 'University of Pennsylvania (Wharton)':
        res = 1 if i == j else 0
    else:
        res = 0 if i == j else 0.9

    return res

def d_school_custom(c):
    schools = get_col(c, 'School')
    x = [[f_school(i,j) for j in schools] for i in schools]
    return numpy.array(x)



# ---
# FIELDS
# ---

# goal

df_goal = {
    'name': 'Goal',
    'desc': 'Professional to Social (1-10)',
    'f': d_goal
}

# structural

df_yearclustercohort = {
    'name': 'Graduation Year',
    'desc': 'Diversifies grad years. In same year, diversifies clusters and cohorts',
    'f': d_yearclustercohort
}

df_athletic_clubs = {
    'name': 'Sports Club Memberships',
    'desc': 'prefers students with non-overlapping sports club memberships',
    'f': lambda c: d_clubs(c, 'athletic')
}

df_cultural_clubs = {
    'name': 'Cultural Club Memberships',
    'desc': 'prefers students with non-overlapping cultural club memberships',
    'f': lambda c: d_clubs(c, 'cultural')
}

lauder_emails = ['adomanis@wharton.upenn.edu','agordin@wharton.upenn.edu','akmandan@wharton.upenn.edu','alerhand@wharton.upenn.edu','alexnog@wharton.upenn.edu','andrader@wharton.upenn.edu','antmun@wharton.upenn.edu','apanza@sas.upenn.edu','argente@wharton.upenn.edu','aroonv@wharton.upenn.edu','asharc@wharton.upenn.edu','attiaa@wharton.upenn.edu','aziakou@wharton.upenn.edu','benjo@law.upenn.edu','biancaz@wharton.upenn.edu','birman@wharton.upenn.edu','Bouskela@wharton.upenn.edu','bouskela@wharton.upenn.edu','brka@wharton.upenn.edu','bvirdi@wharton.upenn.edu','caioguim@wharton.upenn.edu','cburq@wharton.upenn.edu','ccerezo@wharton.upenn.edu','chadwyer@wharton.upenn.edu','chakra@wharton.upenn.edu','chehe@wharton.upenn.edu','cjonesw@wharton.upenn.edu','cmccarr@wharton.upenn.edu','craigjon@wharton.upenn.edu','diegoh@wharton.upenn.edu','diwu1@wharton.upenn.edu','dmikhail@wharton.upenn.edu','dodette@wharton.upenn.edu','dsardi@wharton.upenn.edu','dsoloski@wharton.upenn.edu','duchp@wharton.upenn.edu','eduardoe@wharton.upenn.edu','ericdet@wharton.upenn.edu','erihall@wharton.upenn.edu','etung@wharton.upenn.edu','evanixon@wharton.upenn.edu','fballard@wharton.upenn.edu','feis@wharton.upenn.edu','gbabenko@wharton.upenn.edu','gbradt@wharton.upenn.edu','Gianchandani@wharton.upenn.edu','gnemi@wharton.upenn.edu','gpigoli@wharton.upenn.edu','hamillr@wharton.upenn.edu','hodae@wharton.upenn.edu','huik@wharton.upenn.edu','hyudkin@wharton.upenn.edu','imrank@wharton.upenn.edu','ivangk@wharton.upenn.edu','jamran@wharton.upenn.edu','jbaen@wharton.upenn.edu','jbirge@wharton.upenn.edu','jbmarek@wharton.upenn.edu','jdelikat@wharton.upenn.edu','jesskong@wharton.upenn.edu','jfilippi@wharton.upenn.edu','jlanners@wharton.upenn.edu','johnwit@wharton.upenn.edu','joshzhou@wharton.upenn.edu','junghayi@wharton.upenn.edu','juskys@wharton.upenn.edu','jvandyke@wharton.upenn.edu','kamgang@wharton.upenn.edu','katsun@wharton.upenn.edu','kbigott@wharton.upenn.edu','kbriceno@wharton.upenn.edu','kfackler@wharton.upenn.edu','kkeefe@wharton.upenn.edu','kseniyad@wharton.upenn.edu','lenorma@wharton.upenn.edu','lesloi@wharton.upenn.edu','liyae@wharton.upenn.edu','lorenzoz@wharton.upenn.edu','mabdel@wharton.upenn.edu','mcattani@wharton.upenn.edu','mdiehl@wharton.upenn.edu','medinab@wharton.upenn.edu','migon@wharton.upenn.edu','ming27x@gmail.com','mitcan@wharton.upenn.edu','mizuhoi@wharton.upenn.edu','mlohner@wharton.upenn.edu','mohanm@wharton.upenn.edu','mpareles@wharton.upenn.edu','mscheid@wharton.upenn.edu','nehagoel@wharton.upenn.edu','nghh@wharton.upenn.edu','nidhips@wharton.upenn.edu','owec@wharton.upenn.edu','paulmoss@wharton.upenn.edu','pdushku@wharton.upenn.edu','ppujari@wharton.upenn.edu','queenz@wharton.upenn.edu','racine@wharton.upenn.edu','rafp@wharton.upenn.edu','rallegra@wharton.upenn.edu','rbond@wharton.upenn.edu','rdrew@wharton.upenn.edu','rizwann@wharton.upenn.edu','rkeff@law.upenn.edu','robfried@wharton.upenn.edu','ruicheng@wharton.upenn.edu','ruihengw@wharton.upenn.edu','ryanca@wharton.upenn.edu','sabinak@wharton.upenn.edu','sapud@wharton.upenn.edu','sfisch@wharton.upenn.edu','shanisch@wharton.upenn.edu','shubai@wharton.upenn.edu','shuliu1@wharton.upenn.edu','smillar@wharton.upenn.edu','snyds@wharton.upenn.edu','sopht@wharton.upenn.edu','staa@wharton.upenn.edu','steyn@wharton.upenn.edu','taboadaf@wharton.upenn.edu','takusumi@wharton.upenn.edu','tmcelwee@wharton.upenn.edu','Toledo@wharton.upenn.edu','tpfander@wharton.upenn.edu','typhaine@wharton.upenn.edu','vallejoa@wharton.upenn.edu','vfrances@wharton.upenn.edu','Villaneuva@wharton.upenn.edu','vkukreja@wharton.upenn.edu','wilswong@wharton.upenn.edu','wwachter@wharton.upenn.edu','xiaoxi@wharton.upenn.edu','xilian@wharton.upenn.edu','xinlong@wharton.upenn.edu','yifli@wharton.upenn.edu','yingrui@wharton.upenn.edu','ymanibog@wharton.upenn.edu','yueli4@wharton.upenn.edu','ztan@wharton.upenn.edu']
df_lauder = {
    'name': 'Lauder Membership',
    'desc': 'separates Lauder members',
    'f': lambda d: d_separate_byfield(d, 'Email', lauder_emails)
}

df_groupsize = {
    'name': 'Group Size',
    'desc': 'Prefer similar group size preference',
    'f': d_groupsize
}

# professional

df_workexperience = {
    'name': 'Work Experience',
    'desc': 'prefers similar # of years work experience',
    'f': d_workexperience
}

df_industryexperience = {
    'name': 'Industry Experience',
    'desc': 'diversifies prior industries',
    'f': d_industryexperience
}

df_industryintended = {
    'name': 'Industry Interest',
    'desc': 'prefers similar industries of interest',
    'f': d_industryintended
}

# social

df_horrormovies = {
    'name': 'Horror Movies',
    'desc': 'prefers similar answer to horror movies (OKCupid)',
    'f': d_horrormovies
}

df_travelalone = {
    'name': 'Travel Alone',
    'desc': 'prefers similar answer to travel alone (OKCupid)',
    'f': d_travelalone
}

df_sailboat = {
    'name': 'Sailboat',
    'desc': 'prefers similar answer to sailboat (OKCupid)',
    'f': d_sailboat
}

df_favoritedrink = {
    'name': 'Favorite Drink',
    'desc': 'prefers similar answer to favorite drink',
    'f': d_favoritedrink
}

df_favoritemusic = {
    'name': 'Favorite Music',
    'desc': 'prefers similar answer to favorite music',
    'f': d_favoritemusic
}

df_favoritecuisine = {
    'name': 'Favorite Cuisine',
    'desc': 'prefers similar answer to favorite cuisine',
    'f': d_favoritecuisine
}

# personality

df_introspective = {
    'name': 'Introspective',
    'desc': 'prefers similar self-rating on introspection',
    'f': d_introspective
}

df_big5_o = {
    'name': 'Big 5_o',
    'desc': 'prefers similar answer to big 5_o',
    'f' : d_big5_o
}
df_big5_c = {
    'name': 'Big 5_c',
    'desc': 'prefers similar answer to big 5_c',
    'f' : d_big5_c
}
df_big5_e = {
    'name': 'Big 5_e',
    'desc': 'prefers similar answer to big 5_e',
    'f' : d_big5_e
}
df_big5_a = {
    'name': 'Big 5_a',
    'desc': 'prefers similar answer to big 5_a',
    'f' : d_big5_a
}
df_big5_r = {
    'name': 'Big 5_r',
    'desc': 'prefers similar answer to big 5_r',
    'f' : d_big5_r
}
df_big5_p = {
    'name': 'Big 5_p',
    'desc': 'prefers similar answer to big 5_p',
    'f' : d_big5_p
}

df_motivation = {
    'name': 'Motivation',
    'desc': 'prefers similar motivation rankings',
    'f': d_motivation
}


# ambassador

ambassador_emails = ["smessick@wharton.upenn.edu", "chiaoh@wharton.upenn.edu", "weirongc@wharton.upenn.edu", "anambiar@wharton.upenn.edu", "brandenw@wharton.upenn.edu", "ikwong@wharton.upenn.edu", "jasschew@wharton.upenn.edu", "jellin@wharton.upenn.edu", "jsoto@wharton.upenn.edu", "chunjohn@wharton.upenn.edu", "josephtq@wharton.upenn.edu", "jamesonk@wharton.upenn.edu", "luhussey@wharton.upenn.edu", "mijinkim@wharton.upenn.edu", "nsri@wharton.upenn.edu", "rbrazer@wharton.upenn.edu", "shayaan@wharton.upenn.edu"]
df_ambassador = {
    'name': 'Ambassador',
    'desc': 'diversifies ambassadors',
    'f': lambda d: d_separate_byfield(d, 'Email', ambassador_emails)
}

# ---
# SUB-COMBINATIONS
# ---

df_big5 = {
    'name': 'Big 5',
    'd_fns': [df_big5_o, df_big5_c, df_big5_e, df_big5_a, df_big5_r, df_big5_p],
    'ws': [0.16, 0.16, 0.16, 0.16, 0.16, 0.16],
    'desc': 'Equal-weighted Big 5 (actually 6) personality'
}

df_okc = {
    'name': 'OKCupid',
    'd_fns': [df_horrormovies, df_travelalone, df_sailboat],
    'ws': [0.33, 0.33, 0.33],
    'desc': 'Equal-weighted OK Cupid questions'
}

# ---
# META-FIELDS
# ---

df_structural = {
    'name': 'Structural',
    'desc': 'prefers different structural characteristics',
    'ws': [0.35, 0.15, 0.2, 0.2, 0.1],
    'd_fns': [df_yearclustercohort, df_athletic_clubs, df_cultural_clubs, df_lauder, df_groupsize]
}

df_professional = {
    'name': 'Professional',
    'desc': 'prefers compatible professional characteristics',
    'ws': [0.2, 0.4, 0.4],
    'd_fns': [df_workexperience, df_industryexperience, df_industryintended]
}

df_social = {
    'name': 'Social',
    'desc': 'prefers compatible social characteristics',
    'ws': [0.15, 0.4, 0.3, 0.15],
    'd_fns': [df_favoritedrink, df_okc, df_favoritemusic, df_favoritecuisine]
}

df_personality = {
    'name': 'Personality',
    'desc': 'prefers compatible personality and values',
    'ws': [0.2, 0.2, 0.6],
    'd_fns': [df_introspective, df_big5, df_motivation]
}

# ---
# MASTER METRICS
# ---

df_master = {
    'name': 'Master',
    'desc': 'master distance',
    'ws': [0.2, 0.2, 0.2, 0.2, 0.2],
    'd_fns': [df_goal, df_structural, df_professional, df_social, df_personality]
}


# ---
# VEGAS
# ---

df_school_custom = {
    'name': 'School',
    'desc': 'Prefer different school if Wharton/Columbia, same otherwise',
    'f': d_school_custom
}

df_gender = {
    'name': 'Gender',
    'desc': 'Prefer different gender',
    'f': d_gender
}

df_school = {
    'name': 'School',
    'desc': 'Prefer different school',
    'f': d_school
}

df_values_vegas = {
    'name': 'Value rankings',
    'desc': 'prefers similar value rankings',
    'f': d_values_vegas
}


df_structural_vegas = {
    'name': 'Structural Vegas',
    'desc': 'structural distance for vegas',
    'ws': [0.7, 0.3],
    'd_fns': [df_gender, df_school]
}

df_professional_vegas = {
    'name': 'Professional Vegas',
    'desc': 'professional distance for vegas',
    'ws': [0.8, 0.2],
    'd_fns': [df_workexperience, df_industryintended]
}

df_personal_vegas = {
    'name': 'Personal Vegas',
    'desc': 'personal distance for vegas',
    'ws': [0.3, 0.2, 0.2, 0.2, 0.1],
    'd_fns': [df_favoritemusic, df_okc, df_favoritecuisine, df_values_vegas, df_big5_e]
}

df_master_vegas = {
    'name': 'Master Vegas',
    'desc': 'master distance for vegas',
    'ws': [0.5, 0.2, 0.3],
    'd_fns': [df_structural_vegas, df_professional_vegas, df_personal_vegas]
}


# ---
# CADE
# ---

def e_dist(x, y):
    a = [float(i) for i in x.tolist()]
    b = [float(i) for i in y.tolist()]
    diff = numpy.subtract(a, b)
    return numpy.linalg.norm(diff)

def d_euclid(c):
    col_names = ['f1', 'f2', 'f3']
    cols = get_cols(c, col_names)
    euclids = [[e_dist(a, b) for a in cols] for b in cols]
    return euclids

def d_euclid_inv(c):
    euclids = d_euclid(c)
    euclids_inv = [[math.exp(-x) for x in row] for row in euclids]
    return numpy.array(euclids_inv)

def d_euclid_neg(c):
    euclids = d_euclid(c)
    euclids_neg = [[-x for x in row] for row in euclids]
    return numpy.array(euclids_neg)


df_cade_euclidean = {
    'name': 'L2',
    'desc': 'Euclidean distance (L2 norm) of f1, f2, f3',
    'ws': [1],
    'd_fns': [{'name': 'euclid', 'desc': 'euclid', 'f': d_euclid}]
}

df_cade_euclidean_inv = {
    'name': 'Exp(-L2)',
    'desc': 'e^(-L2) of f1, f2, f3',
    'f': d_euclid_inv
}

df_cade_euclidean_neg = {
    'name': '-L2',
    'desc': '-L2 of f1, f2, f3',
    'f': d_euclid_neg
}
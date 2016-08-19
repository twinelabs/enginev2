"""
etl.qualtrics_data
--------

Import module for Qualtrics survey data.

"""

import etl.match_data


class QualtricsData(etl.match_data.MatchData):

    def __init__(self, raw_data, desc='generic MatchData object from Qualtrics survey', skip_first_n=0):
        """ Constructs survey data object from Qualtrics export file.
        NOTE: export file has two rows of headers, we take just the second
        """
        raw_data_trimmed = raw_data[1:]
        etl.match_data.MatchData.__init__(self, raw_data_trimmed, desc)

        self.data = self.data[skip_first_n:]
        self.n_rows = self.n_rows - skip_first_n


class MultiSurveyData:
    def __init__(self, col_names, surveys):
        """ Object for data from multiple surveys.
        :param survey_tuple: [(name1, fname1, n_exclude1, col_map1), ...]
        """
        self.surveys = surveys
        self.col_names = col_names
        self.sds = [ SurveyData(s[0], s[1], s[2]) for s in surveys]
        self.combine()
        self.dedup()


    def combine(self):
        """ Selects columns and combines.
        """
        self.datas = [ sd.select_cols(self.surveys[i][3]) for i, sd in enumerate(self.sds) ]
        self.data = [row for data in self.datas for row in data]


    def dedup(self):
        """ Dedups by email (takes last i.e. most recent)"""
        emails = [x[8] for x in self.data]
        i_keep = [i for i, email in enumerate(emails) if email not in emails[(i + 1):]]
        self.data_dedup = [self.data[i] for i in i_keep]


    def describe(self):
        for sd in self.sds:
            n = len(sd.data)
            n_excl = sd.n_exclude
            print ''.join([sd.name, ": N = ", str(n), " (", str(n_excl), " excl)"])

        print ''.join(['   Total: N = ', str(len(self.data))])
        print ''.join(['   Dedup: N = ', str(len(self.data_dedup))])
        print ''.join(['   (', str(len(self.data) - len(self.data_dedup)), ' dups)'])


    def data_full(self):
        return [self.col_names] + self.data_dedup


class SimpleData:
    def __init__(self, name, fname):
        """ Constructs survey data object from simple CSV file, with headers
        :param fname: filename
        """
        self.name = name
        self.fname = fname
        self.raw_data = io.load_csv(fname)
        self.dim_orig = (len(self.raw_data), len(self.raw_data[0]))
        self.col_names = self.raw_data[0]
        self.data = self.raw_data[1:]

    def data_full(self):
        return [self.col_names] + self.data

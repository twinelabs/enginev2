"""
etl.match_data
--------

Class for generalized data to be used in matching.
Functions to access, reorder, and remap data.

"""

import pdb

def combine(match_data_list, new_col_names):
    """ Combines multiple match data objects into a single one
    (vertical concatenation). Also checks they have same columns.

    :param match_data_list: list of match data objects
    :return: single match data object with combined data
    """

    all_n_cols = map( lambda x: x.n_cols, match_data_list )
    if len(set(all_n_cols)) > 1:
        raise TypeError("All # of columns must be the same when combining match data objects.")

    all_data = map( lambda x: x.data, match_data_list )
    data_new = [elem for data in all_data for elem in data]

    match_data_new = MatchData([new_col_names] + data_new, "Combined MatchData object")

    return match_data_new

# df.iloc[:,col_nums]
# Filter row by index would just be df.iloc[row_nums]
# Filetr row by index name would be df.loc[row_names]
def filter_cols_by_index(match_data, selected_indices):
    """ Returns match data object that include only selected column indices.
    """

    new_col_names = [col_name for i, col_name in enumerate(match_data.col_names) if str(i) in selected_indices]
    new_data = match_data.select_cols_by_index(selected_indices)

    new_match_data = MatchData([new_col_names] + new_data, match_data.desc)

    return new_match_data

# df['col1'] or df[['col1','col2']]
# Could also do df.loc[:,col_names]
def filter_cols_by_name(match_data, selected_names):
    """ Returns match data object that include only selected column names.
    """

    new_data = match_data.select_cols_by_name(selected_names)
    new_match_data = MatchData(selected_names + new_data, match_data.desc)
    return new_match_data


class MatchData:

    # Should definitely use pandas http://pandas.pydata.org/pandas-docs/stable/10min.html
    def __init__(self, raw_data, desc='generic MatchData object', strip_data = True):
        """ Constructs match data object.
        :param fname: name of MatchData
        :param raw_data: list of lists, with first list = column names
        """

        self.desc = desc
        self.raw_data = raw_data
        self.col_names = self.raw_data[0]
        self.data = self.raw_data[1:]
        self.n_rows = len(self.data)
        self.n_cols = len(self.data[0])

        if strip_data:
            self.data = [[ val.strip() for val in row] for row in self.data]
    
    # Would print well as pandas df
    def __repr__(self):
        return str(self.raw_data)
        
    # df.values[0,0] or df.values[0][0]
    def grab_data_value(self, field, i):
        """ Grabs data value.
        :param field: column name
        :param i: data row
        :return: Data value
        """
        i_col = self.col_names.index(field)
        val = self.data[i][i_col]
        return val

    # df.values[i]
    def grab_data_row(self, i):
        """ Returns i_th data row.
        :param i: row #
        :return: data row as list
        """
        i_row = self.data[i]
        return i_row

    # df.values[:,i]
    def select_cols_by_index(self, selected_indices):
        """ Selects columns from data given indices

        :param selected_indices: column number
        :return: selected data (list of list)
        """

        f_select_cols = lambda row: ["" if ix == "NULL" else row[int(ix)] for ix in selected_indices]
        res = map(f_select_cols, self.data)
        # Flatten to a row if it's a single column
        if len(res[0]) == 1:
            return [x for sublist in res for x in sublist]
        return res

    # df['col1'] or df[['col1','col2']], then .values
    def select_cols_by_name(self, selected_names):
        """ Selects columns from data given column names, ignoring if not found.

        :param selected_names: list of column names
        :return: selected data (list of lists)
        """

        selected_indices = [self.col_names.index(name) for name in selected_names if name in self.col_names]
        res = self.select_cols_by_index(selected_indices)

        return res



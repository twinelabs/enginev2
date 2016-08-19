"""
utils.io.io_csv
--------

Load, save, manipulate CSV files.

"""

import csv


def load_csv(fname):
    """Loads csv file as list of lists"""

    with open(fname, "rb") as f:
        reader = csv.reader(f)
        res = list(reader)

    return res


def save_csv(data, fname):
    """Saves list of lists as CSV file"""

    with open(fname, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    return True

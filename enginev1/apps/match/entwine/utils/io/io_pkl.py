"""
utils.io.io_pkl
--------

Load, save, manipulate pickle (.pkl) files.

"""

import pickle

def load_pkl(fname):
    """Loads pickle object"""

    with open(fname, 'rb') as f:
        res = pickle.load(f)

    return res
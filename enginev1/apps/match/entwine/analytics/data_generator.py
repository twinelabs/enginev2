"""
analytics.data_generator
-------------------------

Create a csv file with random people and various features.
Will be used to test algorithms and goodness of clusters / assignments.

"""

import numpy as np
import pandas as pd
import string
from faker import Faker

alphabet = [char for char in string.ascii_uppercase]

def create_numeric_data(n=100, m=5, mean=10, std=2):
    # Fake Names
    fake = Faker()
    names = [str(fake.name()) for i in xrange(n)]
    # Create dictionary to be turned into a csv file
    d = {'Name': names}
    normal_data = np.round(np.random.normal(mean, std, (m, n)), 2).tolist()
    # Populate the dictionary with the normal data
    for i in xrange(len(normal_data)):
        d['f%s' % i] = normal_data[i]
    # Turn into a pandas df then save it
    df = pd.DataFrame.from_dict(d)
    df.to_csv('test_file.csv',index=False)
    
def create_category_data(n=100, m=2, probs=[]):  
    # Fake Names
    fake = Faker()
    names = [str(fake.name()) for i in xrange(n)]
    # Create dictionary to be turned into a csv file
    d = {'Name': names}
    # Create arbitrary classes, the letters of the alphabet
    classes = [alphabet[i] for i in xrange(m)]
    # Custom distribution can be specified, else even distribution
    if not probs:
        probs = [1.0 / m] * m
    d['class'] = np.random.choice(classes,n,p=probs)
    # Turn into a pandas df then save it
    df = pd.DataFrame.from_dict(d)
    df.to_csv('test_file.csv',index=False)

def create_cluster_example(n=100, m=5, mean=10, std=2):
    # Fake Names
    fake = Faker()
    names = [str(fake.name()) for i in xrange(n)]
    # Create dictionary to be turned into a csv file
    d = {'Name': names}
    normal_data = np.round(np.random.normal(mean, std, (m, n)), 2).tolist()
    # Populate the dictionary with the normal data
    for i in xrange(len(normal_data)):
        d['f%s' % i] = normal_data[i]
    # Create categorical data
    classes = [1,-1]
    probs = [0.5,0.5]
    d['class'] = np.random.choice(classes,n,p=probs)
    # Turn into a pandas df then save it
    df = pd.DataFrame.from_dict(d)
    df.to_csv('data/cluster_example.csv')
    
def create_assign_example(n=100, m=20):
    # Helper to create both files, A and B
    def create_sheet(n, filename):
        # Fake Names
        fake = Faker()
        names = [str(fake.name()) for i in xrange(n)]
        # Create dictionary to be turned into a csv file
        d = {'Name': names}
        # Create categorical data
        genders = ['M','F']
        veterans = ['Yes','No']
        ethnicities = ['White','Black','Asian']
        d['Gender'] = np.random.choice(genders, n)
        d['Veteran'] = np.random.choice(veterans, n)
        d['Ethnicity'] = np.random.choice(ethnicities, n)
        # Turn into a pandas df then save it
        df = pd.DataFrame.from_dict(d)
        df.to_csv(filename)
        
    create_sheet(n, 'data/assign_example_A.csv')
    create_sheet(m, 'data/assign_example_B.csv')
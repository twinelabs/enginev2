"""
yep_feedback
--------

Loads original data and feedback data for the Wharton Alumni matching program.
The goal is to see what meaningful conclusions we can draw from the feedback.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load in all csv files as pandas dataframes
alumni = pd.read_csv('YEP_Feedback/alumni_remapped.csv')
students = pd.read_csv('YEP_Feedback/students_remapped.csv')
matches = pd.read_csv('YEP_Feedback/matches.csv')
utils = pd.read_csv('YEP_Feedback/utils.csv')
feedback = pd.read_csv('YEP_Feedback/YEP_alumni_feedback.csv')

alumni_first_last = matches[['First Name','Last Name']].values
alumni_full = [' '.join(fl) for fl in alumni_first_last]
students_first_last = matches[['First Name.1','Last Name.1']].values
students_full = [' '.join(fl) for fl in students_first_last]

# Maps each alum to students
alumni_to_students = {alum:[] for alum in set(alumni_full)}

for i in xrange(len(matches)):
    alumni_to_students[alumni_full[i]].append(students_full[i])
    
# Maps each student to alum
students_to_alumni = {students_full[i]:alumni_full[i] for i in xrange(len(matches))}

# Maps student to matched on
students_matched_on = {students_full[i]:matches.iloc[i]['-- MATCHED ON --'].split(', ') for i in xrange(len(matches))}

# Maps matched criteria to weighting
criteria_weights = {
                    'Gender':128,
                    'Veteran':64,
                    'Time Zones':32,
                    'Ethnicity':16,
                    'Of Color':8,
                    'Locations':4,
                    'Program':2,
                    'Industry':1
                   }
# Maps students to utilities
students_utilities = {s:sum([criteria_weights[crit] for crit in students_matched_on[s]]) for s in students_full}

# Total utility of each group (or, alumni utility)
alumni_utilities = {a:sum([students_utilities[s] for s in alumni_to_students[a]]) for a in alumni_full }

# Feedback data

# Drop this row, as it ruins everything
feedback = feedback.drop(0)
# Turn these rows into numeric data
feedback[['Q2_1', 'Q4_1', 'Q6_1', 'Q8_1', 'Q10_1', 'Q12_1', 'Q13', 'Q14_1']] = \
    feedback[['Q2_1', 'Q4_1', 'Q6_1', 'Q8_1', 'Q10_1', 'Q12_1', 'Q13', 'Q14_1']].astype(float)

# Stats
Q2_Stats = feedback['Q2_1'].describe()
Q13_Stats = feedback['Q13'].describe()
Q14_Stats = feedback['Q14_1'].describe()

# Map each mentor to rating of each student
alumni_student_feedback = {a:{} for a in alumni_full}
for a in alumni_full:
    alumni_student_feedback


# Get map of alumni to student ratings (These are in questions 3,5,...11
# Find correlations / make graphs

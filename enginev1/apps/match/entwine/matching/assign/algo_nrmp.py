"""
matching.assign.run_new
-------------------------

FOR NEW SYNTAX OF MATCHING:
Function to run assignment algorithms.
"""

import numpy as np
import random
import pdb

def residency(utility_matrix, match_cfg, verbose=False):
    """ Solves residency matching program with symmetric utilities and multiple capacity.

    :param utility_matrix: np array of utilities, with N rows of individuals (applicants) and M columns of programs (residencies).
    :return: Assignments [(a_1, score, desc), (a_2, score, desc), ..., (a_N, score, desc)] for each individual, with a_i in [1, 2, ... M].
    """
    a_s = {}
    n, m = utility_matrix.shape
    capacity = match_cfg['algorithm']['params']['capacity']
    capacities = [capacity] * m
    
    for i in range(n):
        a_s[i] = { 'match': None, 'ranks': np.argsort(np.negative(utility_matrix[i, :])).tolist(), 'utilities': utility_matrix[i, :] }

    b_s = {}
    for j in range(m):
        b_s[j] = { 'matches': [], 'ranks': np.argsort(np.negative(utility_matrix[:, j])).tolist(), 'utilities': utility_matrix[:, j] }


    # while there exists an unmatched, still-proposing individual ...
    a_alive = [a for a in a_s.keys() if a_s[a]['match'] is None and not a_s[a]['ranks'] is None]

    while a_alive:
        a_i = random.choice(a_alive)    # rando individual
        a = a_s[a_i]
        b_i = a['ranks'].pop(0)         # highest-ranked program
        b = b_s[b_i]

        if verbose:
            print( '\n> a' + str(a_i) + ' tries b' + str(b_i) + ' (current: ' + ', '.join([str(m) for m in b['matches']]) + ')')

        # if program has capacity, add
        if len(b['matches']) < int(capacities[b_i]):
            if verbose:
                print( 'b' + str(b_i) + ' has capacity and accepts proposal')
            b['matches'].append(a_i)
            a['match'] = b_i

        else:
            # if program prefers _a_ to least-desired existing ...
            current_utils = [b['utilities'][i] for i in b['matches']]
            if b['utilities'][a_i] > min(current_utils):
                least_desired_i = np.argmin(current_utils)
                least_desired = b['matches'][least_desired_i]

                # ... replace least-desired with _a_
                if verbose:
                    print( 'b' + str(b_i) + ' bumps a' + str(least_desired) + ' and accepts proposal')
                b['matches'][least_desired_i] = a_i
                a['match'] = b_i
                a_s[least_desired]['match'] = None

            else:
                if verbose:
                    print( 'b' + str(b_i) + ' is full and rejects proposal')

        a_alive = [a for a in a_s.keys() if a_s[a]['match'] is None and a_s[a]['ranks']]

    assignments = [b_s[i]['matches'] for i in range(m)]

    return assignments


def residency_mod(utility_matrix, match_config, verbose=False):
    """ Solves residency matching program with symmetric utilities and multiple capacity.

    :param utility_matrix: np array of utilities, with N rows of individuals (applicants) and M columns of programs (residencies).
    :return: Assignments [(a_1, score, desc), (a_2, score, desc), ..., (a_N, score, desc)] for each individual, with a_i in [1, 2, ... M].
    """
    capacities = match_config['capacities']
    
    a_s = {}
    n,m = utility_matrix.shape
    capacity = match_config['algorithm']['params']['capacity']
    # For now, let all capacities be the same as the given capacity
    capacities = [capacity] * m
    
    for i in range(n):
        a_s[i] = { 'match': None, 'ranks': np.argsort(utility_matrix[i,:])[::-1].tolist(), 'utilities': utility_matrix[i,:] }

    b_s = {}
    for j in range(m):
        b_s[j] = { 'matches': [], 'ranks': np.argsort(utility_matrix[:,j])[::-1].tolist(), 'utilities': utility_matrix[:,j] }

    a_remaining = set(a_s.keys())
    # This algorithm should always terminate with a solution, but may take a while.
    # While there exists an unmatched, still-proposing individual ...
    while a_remaining:
        a_i = random.choice(tuple(a_remaining))
        a = a_s[a_i]
        b = ''
        for b_i in a['ranks']: # In order from the highest-ranked program...
            b = b_s[b_i]

            if verbose:
                print( '\n> a' + str(a_i) + ' tries b' + str(b_i) + ' (current: ' + ', '.join([str(m) for m in b['matches']]) + ')')

            # If program has capacity, add individual to program
            if len(b['matches']) < int(capacities[b_i]):
                b['matches'].append(a_i)
                a['match'] = b_i
                a_remaining.remove(a_i)
                if verbose:
                    print( 'b' + str(b_i) + ' has capacity and accepts proposal')
                # Exit for loop of programs  
                break
    
            else:
                # If program prefers _a_ to least-desired existing ...
                current_utils = [b['utilities'][i] for i in b['matches']]
                if b['utilities'][a_i] > min(current_utils):
                    least_desired_i = np.argmin(current_utils)
                    least_desired = b['matches'][least_desired_i]
    
                    # ... replace least-desired with _a_
                    b['matches'][least_desired_i] = a_i
                    a['match'] = b_i
                    a_remaining.remove(a_i)
                    a_s[least_desired]['match'] = None
                    a_remaining.add(least_desired_i)
                    if verbose:
                        print( 'b' + str(b_i) + ' bumps a' + str(least_desired) + ' and accepts proposal')
                    # Exit for loop of programs
                    break
                # Else, go on to the next highest ranked program
                else:
                    if verbose:
                        print( 'b' + str(b_i) + ' is full and rejects proposal')
        # Shorten the rank list of a, such that all programs before and including b are eliminated
        idx = a['ranks'].index(b)   
        a['ranks'] = a['ranks'][idx+1:] 
         
    assignments = [b_s[i]['matches'] for i in range(m)]

    return assignments


def find_assignments(utility_matrix, match_cfg, verbose=False):
    res = residency(utility_matrix, match_cfg, verbose=False)
    return res

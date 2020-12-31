#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

import numpy as np

def getinputdict(loglineareqs = True):
    inputdict = {}

    inputdict['paramssdict'] = {'GAMMA': 1, 'DELTA': 0.05, 'ALPHA': 0.3, 'RHO': 0.05}

    inputdict['states'] = ['K']
    inputdict['controls'] = ['q', 'C']
    inputdict['irfshocks'] = ['K']

    # equations:{{{
    inputdict['equations'] = []

    # Euler
    if loglineareqs is True:
        inputdict['equations'].append('-GAMMA * C = q')
    else:
        inputdict['equations'].append('C ** (-GAMMA) = q')

    # q definition
    if loglineareqs is True:
        inputdict['equations'].append('-q_dot = ALPHA * K_ss**(ALPHA-1) * (ALPHA - 1) * K')
    else:
        inputdict['equations'].append('-q_dot / q = ALPHA * K ** (ALPHA-1) - DELTA - RHO')

    # resource constraint
    if loglineareqs is True:
        inputdict['equations'].append('K_dot = (ALPHA - 1) * K_ss **(ALPHA-1) * K - C_ss / K_ss * (C - K)')
    else:
        inputdict['equations'].append('K_dot / K = K ** (ALPHA-1) - DELTA - C / K')


    # equations:}}}

    # steady state:{{{
    p = inputdict['paramssdict']

    p['K'] = (p['ALPHA'] / (p['DELTA'] + p['RHO'])) ** (1/(1-p['ALPHA']))
    p['C'] = p['K'] ** p['ALPHA'] - p['DELTA'] * p['K']
    p['q'] = p['C'] ** (-p['GAMMA'])

    # steady state:}}}

    if loglineareqs is True:
        inputdict['loglineareqs'] = True
    else:
        inputdict['logvars'] = inputdict['states'] + inputdict['controls']

    return(inputdict)


def check():
    inputdict_loglin = getinputdict(loglineareqs = True)
    inputdict_log = getinputdict(loglineareqs = False)
    sys.path.append(str(__projectdir__ / Path('submodules/dsge-perturbation/')))
    from dsge_continuous_func import checksame_inputdict_cont
    checksame_inputdict_cont(inputdict_loglin, inputdict_log)
    

def dsgefull():
    inputdict = getinputdict()

    sys.path.append(str(__projectdir__ / Path('submodules/dsge-perturbation/')))
    from dsge_continuous_func import continuouslineardsgefull
    continuouslineardsgefull(inputdict)


# Run:{{{1
check()
dsgefull()

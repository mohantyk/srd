#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:03:05 2020

@author: kaniska
"""

import numpy as np
from scipy import signal


def power(x):
    '''
    Calculate power of signal x
    '''
    fro = np.linalg.norm(x) # frobenius norm
    return (fro**2)/len(x) 


def detect_env(x):
    '''
    Detect envelope of signal
    Group delay = 49
    '''
    fbe = [0, 0.05, 0.1, 1]
    damps = [1, 1, 0, 0]
    b = signal.firls(99, fbe, damps)
    gd = 49 # Can be computed using signal.group_delay
    
    envx = (np.pi/2)*signal.lfilter(b, 1, np.abs(x))
    return envx, gd
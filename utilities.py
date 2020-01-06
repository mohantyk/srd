#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:03:05 2020

@author: kaniska
"""

import numpy as np

def power(x):
    '''
    Calculate power of signal x
    '''
    fro = np.linalg.norm(x) # frobenius norm
    return (fro**2)/len(x) 
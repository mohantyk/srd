#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 16:54:44 2019

@author: kaniska
"""

import numpy as np

def downsample_waveform(sig, n):
    '''
    inputs:
        sig: signal
        n: sample every nth sample e.g, n=2 skips one sample
    output:
        sampled waveform
    '''
    w = np.zeros_like(sig)
    w[::n] = sig[::n]
    return w
    
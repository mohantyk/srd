#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 16:54:44 2019

@author: kaniska
"""

import numpy as np

def sample_waveform(sig, fs, Ts):
    '''
    inputs:
        sig: signal
        fs: Sampling frequency
        Ts: Simulation timestep
    output:
        sampled waveform
    '''
    Fs = 1/Ts # Simulation sampling rate, not actual sampling rate
    sample_ratio = Fs/fs
    n = round(sample_ratio) # Number of samples to be skipped
    if n != sample_ratio:
        raise ValueError('1/Ts should be a multiple of fs')
        
    w = np.zeros_like(sig)
    w[::n] = sig[::n]
    return w
    
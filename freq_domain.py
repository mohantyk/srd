#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 19:15:10 2019

@author: kaniska
"""

import math
import numpy as np
from scipy.fftpack import fft, fftshift

import matplotlib.pyplot as plt

import global_params as G

def plotspec(sig, Ts, ax=None):
    '''
    Returns the spectrum centered at 0
    inputs:
        sig: signal
        Ts: sampling interval (in sec)
    '''
    N = len(sig)
    freq_range = np.arange(math.ceil(-N/2), math.ceil(N/2))/(Ts*N) # Frequency vector
    fx = fft(sig) # FFT
    freqs = np.abs(fftshift(fx)) # Shift it for plotting, take amplitude
    
    if ax is None:
        _, ax = plt.subplots( figsize=G.FIGSIZE )
    ax.plot(freq_range, freqs)
    ax.set_xlabel('frequency')
    ax.set_ylabel('magnitude')
    return ax

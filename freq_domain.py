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

def plotspec(sig, Ts):
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
    
    plt.figure( figsize=G.FIGSIZE )
    plt.plot(freq_range, freqs)
    plt.xlabel('frequency')
    plt.ylabel('magnitude')
    plt.show()

    
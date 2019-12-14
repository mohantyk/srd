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

def plotspec(sig, Ts, ax_spec=None):
    '''
    Returns the spectrum centered at 0
    inputs:
        sig: signal
        Ts: sampling interval (in sec)
        ax_spec: axis to plot spectrum
    '''
    N = len(sig)
    t = np.arange(0, N)*Ts

    freq_range = np.arange(math.ceil(-N/2), math.ceil(N/2))/(Ts*N) # Frequency vector
    fx = fft(sig) # FFT
    freqs = np.abs(fftshift(fx)) # Shift it for plotting, take amplitude

    if ax_spec is None:
        _, (ax_sig, ax_spec) = plt.subplots(1,2, figsize=G.FIGSIZE )
    else:
        ax_sig = None # If spectrum axis is given, no need to plot signal

    # Plot signal
    if ax_sig is not None: 
        ax_sig.plot(t, sig)
        ax_sig.set_xlabel('Seconds')
        ax_sig.set_ylabel('Amplitude')

    # Plot spectrum    
    ax_spec.plot(freq_range, freqs)
    ax_spec.set_xlabel('Frequency')
    ax_spec.set_ylabel('Magnitude')
    return ax_spec

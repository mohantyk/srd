#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 19:15:10 2019

@author: kaniska
"""

import math
import numpy as np
from scipy.fftpack import fft, fftshift

def plotspec(sig, Ts):
    '''
    Returns the spectrum centered at 0
    inputs:
        sig: signal
        Ts: sampling interval (in sec)
    '''
    N = len(sig)
    ssf = np.arange(math.ceil(-N/2), math.ceil(N/2))/(Ts*N) # Frequency vector
    fx = fft(sig) # FFT
    fxs = np.abs(fftshift(fx)) # Shift it for plotting, take amplitude
    return ssf, fxs
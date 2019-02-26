# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

def sine_wave(freq, duration=0.05, sampling=1/10000):
    '''
    inputs: 
        freq (Hz)
        duration (sec)
        sampling (Hz)
    outputs:
        timestep, sine waveform
    '''
    t = np.arange(0, duration, sampling)
    w = np.sin(2*np.pi*freq*t)
    return t, w
# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

import numpy as np
from scipy import signal

def sine_wave(freq, duration=0.05, Ts=1/10000):
    '''
    inputs: 
        freq (Hz)
        duration (sec)
        sampling duration (sec)
    outputs:
        timestep, sine waveform
    '''
    t = np.arange(0, duration, Ts)
    w = np.sin(2*np.pi*freq*t)
    return t, w


def cosine_wave(freq, duration=0.05, Ts=1/10000):
    '''
    inputs: 
        freq (Hz)
        duration (sec)
        sampling duration (sec)
    outputs:
        timestep, sine waveform
    '''
    t = np.arange(0, duration, Ts)
    w = np.cos(2*np.pi*freq*t)
    return t, w


def awgn(duration=0.05, Ts=1/10000):
    '''
    Returns an awgn waveform
    inputs:
        duration (sec)
        sampling duration
    '''
    return np.random.randn(int(duration/Ts))


def mysinc(freq, duration=0.05, Ts=1/10000):
    '''
    Returns a sinc wave with a single-sided bandwidth equal to freq
    '''
    t = np.arange(0, duration, Ts)
    w = np.sinc(2*freq*(t-duration/2))
    return t, w


def exp_pulse(duration=0.05, Ts=1/10000):
    '''
    Creates an exponential pulse e^-t
    '''
    t = np.arange(0, duration, Ts)
    pulse = np.exp(-t)
    return t, pulse


def gaussian_pulse(start, stop, Ts=1/10000):
    '''
    Creates an exponential pulse e^-(t^2)
    '''
    t = np.arange(start, stop, Ts)
    pulse = np.exp(-(t**2))
    return t, pulse


def bandlimited(F_start, F_stop, duration, Ts=1/10000):
    '''
    Creates a bandlimited signal
    '''
    Fs = 1/Ts
    f_start = F_start/(Fs/2)
    f_stop = F_stop/(Fs/2)
    # Design bandpass filter
    freqs = [0, f_start - 0.01, f_start, f_stop, f_stop + 0.01, 1]
    amps = [0, 0, 1, 1, 0, 0]
    b = signal.firls(99, freqs, amps)
    # Filter white noise through bandpass filter
    noise = awgn(duration, Ts)
    filtered_noise = signal.lfilter(b, 1, noise)
    return filtered_noise


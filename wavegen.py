# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

import numpy as np
from scipy import signal
import warnings

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
    if f_start == 0:
        # Design lowpass filter
        freqs = [0, f_stop, f_stop + 0.01, 1]
        amps = [1, 1, 0, 0]
    else:
        # Design bandpass filter
        freqs = [0, f_start - 0.01, f_start, f_stop, f_stop + 0.01, 1]
        amps = [0, 0, 1, 1, 0, 0]
    b = signal.firls(99, freqs, amps)
    # Filter white noise through bandpass filter
    noise = awgn(duration, Ts)
    filtered_noise = signal.lfilter(b, 1, noise)
    return filtered_noise


def rcosine(syms, osr, β):
    '''
    Raised cosine waveform
    inputs:
        syms: half the duration
        osr: oversampling rate
        β: roll off factor, 0 gives sinc
    '''
    # All calculations are normalized by T
    duration = (-syms, syms)
    N = osr*(duration[1] - duration[0]) + 1
    t = np.linspace(*duration, N)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore') # For Divide by zero
        rcos_filt = np.sinc(t) * np.cos(np.pi*β*t) / (1-(2*β*t)**2)

    if β != 0:
        rcos_filt[np.isinf(rcos_filt)] = (np.pi/4)*np.sinc(1/(2*β))

    #delay = duration[1]*osr # Delay of impulse peak in samples
    return rcos_filt



# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

import numpy as np
from numpy import pi
from scipy import signal
import warnings

from utilities import power

def sine_wave(freq, duration=0.05, Ts=1/10000, phase=0):
    '''
    inputs:
        freq (Hz)
        duration (sec)
        sampling duration (sec)
    outputs:
        timestep, sine waveform
    '''
    t = np.arange(0, duration, Ts)
    w = np.sin(2*np.pi*freq*t + phase)
    return t, w


def cosine_wave(freq, duration=0.05, Ts=1/10000, phase=0):
    '''
    inputs:
        freq (Hz)
        duration (sec)
        sampling duration (sec)
    outputs:
        timestep, sine waveform
    '''
    t = np.arange(0, duration, Ts)
    w = np.cos(2*np.pi*freq*t + phase)
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


def rcosine(syms, osr, β, T=1):
    '''
    Raised cosine waveform
    inputs:
        syms: half the duration
        osr: oversampling rate
        β: roll off factor, 0 gives sinc
        Ts: symbol period
    '''
    duration = (-syms*T, syms*T)
    N = osr*(duration[1] - duration[0]) + 1
    t = np.linspace(*duration, N)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore') # For Divide by zero
        rcos_filt = (1/T)*np.sinc(t/T) * np.cos(pi*β*t/T) / (1-(2*β*t/T)**2)

    if β != 0:
        rcos_filt[np.isinf(rcos_filt)] = (pi/(4*T))*np.sinc(1/(2*β))

    #delay = duration[1]*osr # Delay of impulse peak in samples
    return rcos_filt


def srrc(syms, osr, β, timing_offset=0, T=1):
    '''
    Square root raised cosine waveform
    inputs:
        syms: half the duration
        osr: oversampling rate
        β: roll off factor, 0 gives sinc
        timing_offset: timing offset
        T: symbol period
    '''
    # https://en.wikipedia.org/wiki/Root-raised-cosine_filter
    duration = (-syms*T, syms*T)
    N = osr*(duration[1] - duration[0]) + 1
    t = np.linspace(-syms+timing_offset, syms+timing_offset, N)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore') # For Divide by zero
        srrc_wave = ( (np.sin((1-β)*pi*t/T) + (4*β*t/T)*np.cos((1+β)*pi*t/T)) /
                        ((pi*t/T)*(1-(4*β*t/T)**2)) )/T

    try:
        zero_idx = np.where(t==0)[0][0]
        srrc_wave[zero_idx] = (1-β+4*β/pi)/T
    except IndexError:
        pass

    if β != 0:
        srrc_wave[np.isnan(srrc_wave)] = β/(np.sqrt(2)*pi*T)*(
                                    (pi+2)/np.sin(pi/(4*β)) + (pi-2)*np.cos(pi/(4*β)) )

    # Normalize the srrc by its energy
    # This enables us to get the raised cosine directly by doing
    # np.convolve(srrc, srrc, 'same')
    normalized_srrc = srrc_wave / np.sqrt(len(srrc_wave)*power(srrc_wave))
    return normalized_srrc


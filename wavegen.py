# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

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
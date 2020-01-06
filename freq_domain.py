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


def plot_signal(t, sig, ax_sig):
    # Plot signal
    ax_sig.plot(t, sig)
    ax_sig.set_xlabel('Seconds')
    ax_sig.set_ylabel('Amplitude')
    return ax_sig


def plot_amplitude(freq_range, amplitude, ax_spec):
    # Plot spectrum amplitude
    ax_spec.plot(freq_range, amplitude)
    ax_spec.set_xlabel('Frequency')
    ax_spec.set_ylabel('Magnitude')
    return ax_spec


def plot_phase(freq_range, phase, ax_spec):
    # Plot spectrum phase
    ax_spec.plot(freq_range, phase)
    ax_spec.set_xlabel('Frequency')
    ax_spec.set_ylabel('Phase')
    return ax_spec


def plotspec(sig, Ts, amp=True):
    '''
    Returns the spectrum centered at 0
    inputs:
        sig: signal
        Ts: sampling interval (in sec)
        amp: amplitude if True, else phase
    '''
    N = len(sig)
    t = np.arange(0, N)*Ts

    freq_range = np.arange(math.ceil(-N/2), math.ceil(N/2))/(Ts*N) # Frequency vector
    fx = fft(sig) # FFT

    spectrum = fftshift(fx) # Shift it for plotting
    amplitude = np.abs(spectrum)
    phase = np.unwrap( np.angle(spectrum) )

    fig, ax = plt.subplots(1,2, figsize=G.FIGSIZE )
    
    plot_signal(t, sig, ax[0])
    if amp:
        plot_amplitude(freq_range, amplitude, ax[1])
    else:
        plot_phase(freq_range, phase, ax[1])
    fig.subplots_adjust(wspace=0.3)
    return ax

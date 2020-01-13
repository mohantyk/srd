#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 06:52:48 2020

@author: kaniska
"""
from collections import namedtuple


import numpy as np
import matplotlib.pyplot as plt

        
Band = namedtuple('Band', ['start', 'stop'])

    
class Bands:
    def __init__(self, *bands, Ts=1e-4):
        '''
        input:
            bands : all the bands as (start, stop) tuples
            Ts : simulation sampling rate
        '''
        self.all_bands = []
        for band in bands:
            self.all_bands.append(Band(*band))
        self.Fs = 1/Ts
            
    def add_band(self, *bands):
        '''
        Adds new bands
        '''
        for band in bands:
            self.all_bands.append( Band(*band) )
        return self
    
    
    def plot(self):
        '''
        Plot the bands in frequency
        '''
        Fs = self.Fs
        freqs = np.arange(-Fs/2, Fs/2)
        amps = np.zeros_like(freqs)
        for band in self.all_bands:
            amps[(freqs>=band.start) & (freqs<=band.stop)] += 1
        plt.figure()
        plt.plot(freqs, amps)
        plt.show()
    
    
    def modulate(self, fc):
        '''
        Modulate with a real cosine wave
        input:
            fc: frequency of cosine wave
        '''
        new_bands = []
        for band in self.all_bands:
            new_bands.append( Band(band.start-fc, band.stop-fc))
            new_bands.append( Band(band.start+fc, band.stop+fc))
        self.all_bands = new_bands
        return self
    
    @property
    def min_freq(self):
        return min( band.start for band in self.all_bands )
    
    @property
    def max_freq(self):
        return max( band.stop for band in self.all_bands )
    
    def sample(self, fs):
        '''
        Sample at rate fs (different from simulation rate Fs)
        '''   
        Fs = self.Fs
        images = []
        for band in self.all_bands:
            k_min = np.floor((band.stop + Fs/2)/fs).astype(int)
            k_max = np.floor((Fs/2 - band.start)/fs).astype(int)
            for k in range(-k_min, k_max + 1):
                images.append( Band(band.start + k*fs, band.stop + k*fs) )
        self.all_bands = images
        return self
    
    def __repr__(self):
        return f'{[tuple(band) for band in sorted(self.all_bands)]}'
    
    
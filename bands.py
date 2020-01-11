#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 06:52:48 2020

@author: kaniska
"""
from dataclasses import dataclass

import numpy as np

@dataclass
class Band:
    start: float
    stop: float
    
    def as_freqs(self, Ts=1e-4):
        Fs = 1/Ts
        freqs = np.arange(-Fs/2, Fs/2)
        amps = np.zeros_like(freqs)
        amps[(freqs>=self.start) & (freqs<=self.stop)] = 1
        return freqs, amps
    
    def modulate(self, fc):
        pos = Band(self.start+fc, self.stop+fc)
        neg = Band(self.start-fc, self.stop-fc)
        return (pos, neg)
        
    

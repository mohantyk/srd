#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 18:01:37 2019

@author: kaniska
"""

class Quantizer:
    allowed_modes = ('ufixed')
    allowed_rounding = ('floor', 'ceil', 'nearest')
    allowed_overflow = ('saturate')
    
    @classmethod
    def check_arg(cls, arg, allowed_values):
        if arg not in allowed_values:
            raise ValueError(f'{arg} not supported. Only the following values are allowed {allowed_values}')
    

    def __init__(self, int_bits, frac_bits, mode='ufixed', round_mode='floor', overflow_mode='saturate'):
        self.check_arg(mode, self.allowed_modes)
        self.check_arg(round_mode, self.allowed_rounding)
        self.check_arg(overflow_mode, self.allowed_overflow)
        self.int_bits = int_bits
        self.frac_bits = frac_bits

    def quantize(self, inp):
        pass


if __name__ == '__main__':
        quantizer = Quantizer(12, 8)
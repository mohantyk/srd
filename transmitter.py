import numpy as np
from scipy import signal

# Helper functions
def pairwise(iterator):
    ''' Pairs up two elements at a time '''
    window = [iter(iterator)]*2
    for combo in zip(*window):
        yield combo

#-----------------
# Encoding
def letters2pam(msg):
    '''
    inputs:
        msg: str
    outputs:
        symbols: list of 4-PAM symbols
    '''
    msg_bin = ''.join('{:08b}'.format(ord(ch)) for ch in msg)
    symbol_map = {'11': 3, '10': 1, '01': -1, '00': -3}
    symbols = [symbol_map[''.join(pair)] for pair in pairwise(msg_bin)]
    return symbols

def pulse_shaped(symbols, oversample=10):
    '''
    inputs:
        symbols: list of symbols
        oversample: oversampling factor (to simulate analog signal)
    '''
    pulse = signal.hamming(oversample)
    num_symbols = len(symbols)
    oversampled_symbols = np.zeros(oversample * num_symbols)
    oversampled_symbols[::oversample] = symbols
    analog_signal = np.convolve(oversampled_symbols, pulse)
    analog_signal = analog_signal[:len(oversampled_symbols)] # Remove the trailing transit
    return analog_signal

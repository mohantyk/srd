import numpy as np
from scipy import signal

from wavegen import cosine_wave

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


#-----------------
# Ideal transmitter
def ideal_transmitter(msg):
    '''
    inputs:
        msg: message string
    outputs:
        time array
        transmitted signal
    '''
    # Convert to PAM symbols
    symbols = letters2pam(msg)
    # Pulse shaping
    oversampling_factor = 100
    analog_waveform = pulse_shaped(symbols, oversampling_factor)
    # Modulate with carrier wave
    Ts = 1/oversampling_factor
    carrier_freq = 20
    duration = len(symbols)
    t, carrier = cosine_wave(carrier_freq, duration, Ts)
    transmitted = carrier * analog_waveform
    return t, transmitted



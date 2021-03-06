import numpy as np
from scipy import signal

from wavegen import cosine_wave
from sampling import oversample

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

def pulse_shaped(symbols, oversample_factor=10, shape=signal.hamming):
    '''
    inputs:
        symbols: list of symbols
        oversample_factor: oversampling factor (to simulate analog signal)
    '''
    pulse = shape(oversample_factor)
    oversampled_symbols = oversample(symbols, oversample_factor)
    analog_signal = np.convolve(oversampled_symbols, pulse)
    analog_signal = analog_signal[:len(oversampled_symbols)] # Remove the trailing transit
    return analog_signal


def modulate(sig, fc, Ts, phase_offset=0):
    '''
    Modulate an analog signal with a carrier wave
    input:
        sig : analog signal
        fc: carrier frequency
        Ts: sampling duration of analog signal
    '''
    duration = Ts*len(sig)
    Fs = 1/Ts
    assert Fs/2 > fc + 5 # Should ideally be fc + signal bw
    t, carrier = cosine_wave(fc, duration, Ts, phase_offset)
    transmitted = carrier * sig
    return t, transmitted

#-----------------
# Ideal transmitter
def ideal_transmitter(msg, fc=20, M=100):
    '''
    inputs:
        msg: message string
        fc:  carrier frequency
         M:  oversampling factor (for simulating analog signal)
    outputs:
        time array
        transmitted signal
    '''
    # Convert to PAM symbols
    symbols = letters2pam(msg)
    # Pulse shaping
    analog_waveform = pulse_shaped(symbols, M)
    # Modulate with carrier wave
    t, transmitted = modulate(analog_waveform, fc, 1/M)
    return t, transmitted



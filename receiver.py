import numpy as np
from scipy import signal

from wavegen import cosine_wave
from utilities import power

#-------------------------
# Helper functions
def combine(iterator, num_elems):
    ''' Pairs up a fixed number of  elements at a time '''
    window = [iter(iterator)]*num_elems
    for combo in zip(*window):
        yield combo

#-------------------------
# Receiver blocks

def pam2letters(symbols):
    '''
    inputs:
        symbols: list of pam symbols
    outputs:
        msg as a str
    '''
    symbol_to_bits = {3: '11', 1: '10', -1: '01', -3: '00'}
    bits = ''.join(symbol_to_bits[symbol] for symbol in symbols)
    msg = []
    for eight_bits in combine(bits, 8):
        ascii = int(''.join(eight_bits), 2)
        ch = chr(ascii)
        msg.append(ch)
    return ''.join(msg)


def demodulate(sig, fc, Ts):
    '''
    Demodulate a carrier wave
    inputs:
        sig: analog signal
        fc : carrier wave frequency
        Ts : sampling duration of analog signal
    '''
    # Downconvert
    duration = len(sig)*Ts
    _, carrier = cosine_wave(fc, duration, Ts)
    downconverted = sig * carrier
    # Low pass filter the downconverted signal
    taps = 50
    Fs = 1/Ts
    band_edges = np.array([0, 0.1, 0.2, 1])*(Fs//2) # Cutoff at 0.2*Fs/2
    damps = [1, 0]
    b = signal.remez(taps, band_edges, damps, fs=Fs)
    # Scaling by 2 below to compensate for cos(x)**2 = (1/2)*[cos(2x) + 1]
    baseband = 2*signal.lfilter(b, 1, downconverted) # Baseband is still in 'analog' domain
    return baseband


def pulse_correlator(sig, M):
    '''
    inputs:
        sig: baseband signal
        M : oversampling factor
    '''
    pulse = signal.hamming(M)
    # Normalize pulse so that correlation with another pulse gives coeff = 1
    pulse_normalized = pulse/(power(pulse)*len(pulse))
    # In 'full' mode, correlation of a pulse with itself gives an array of 2*M-1 elements
    # The peak is at index M - 1
    correlated = np.correlate(sig, pulse_normalized, 'full')
    return correlated


def quantalph(sig, alphabet):
    '''
    Quantize sig to nearest symbol in alphabet
    '''
    dist = (sig.reshape(-1,1) - alphabet.reshape(1, -1))**2
    idx = np.argmin(dist, axis=1)
    hard_decisions = alphabet[idx]
    return hard_decisions


# Final receiver
def ideal_receiver(sig):
    '''
    inputs:
        sig: received signal (numpy array)
    '''
    fc = 20
    Ts = 1/100
    oversample_factor = 100
    # Demodulate the carrier wave
    baseband = demodulate(sig, fc, Ts)
    # Use correlation to extract pulse amplitudes
    correlated = pulse_correlator(baseband, oversample_factor)

    return correlated





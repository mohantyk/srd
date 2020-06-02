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


def demodulate(sig, fc, Ts, taps=50):
    '''
    Demodulate a carrier wave
    inputs:
        sig: analog signal
        fc : carrier wave frequency
        Ts : sampling duration of analog signal
        taps: number of taps for LPF
    '''
    # Downconvert
    duration = len(sig)*Ts
    _, carrier = cosine_wave(fc, duration, Ts)
    downconverted = sig * carrier
    # Low pass filter the downconverted signal
    Fs = 1/Ts
    band_edges = np.array([0, 0.1, 0.2, 1])*(Fs//2) # Cutoff at 0.2*Fs/2
    damps = [1, 0]
    b = signal.remez(taps, band_edges, damps, fs=Fs)
    # Scaling by 2 below to compensate for cos(x)**2 = (1/2)*[cos(2x) + 1]
    baseband = 2*signal.lfilter(b, 1, downconverted) # Baseband is still in 'analog' domain
    return baseband


def pulse_correlator(sig, M, shape=signal.hamming):
    '''
    inputs:
        sig: baseband signal
        M : oversampling factor
        shape: pulse shape function, should take a single parameter oversample_factor
    '''
    pulse = shape(M)
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


def eye_diag(analog, n_eye=5, oversample_factor=10):
    '''
    inputs:
        analog: analog signal
        n_eye: number of symbols for eye
        oversample_factor: oversampling factor for analog signal
    output:
        2D array, each row consists of n_eye symbols
    '''
    M = oversample_factor
    n_eye = 5 # Number of symbols in eye
    groups = len(analog)//(n_eye*M)
    eye_diag = analog[-n_eye*groups*M:].reshape(-1, n_eye*M)
    return eye_diag


# Final receiver
def ideal_receiver(sig, fc=20, Ts=1/100):
    '''
    inputs:
        sig: received signal (numpy array)
        fc: carrier frequency
        Ts: sampling frequency (for analog signal)
    output:
        decoded msg (str)
    '''
    oversample_factor = int(1/Ts)
    # Demodulate the carrier wave
    taps = 50
    baseband = demodulate(sig, fc, Ts, taps)
    # Use correlation to extract pulse amplitudes
    correlated = pulse_correlator(baseband, oversample_factor)
    # Downsample to get soft decisions
    filter_delay = taps//2 # taps // 2
    correlator_delay = oversample_factor
    sampling_start_idx = filter_delay + correlator_delay - 1
    soft_decisions = correlated[sampling_start_idx::oversample_factor]
    # Quantize to get hard decisions
    alphabet = np.array([-3, -1, 1, 3])
    hard_decisions = quantalph(soft_decisions, alphabet)
    # Decode message
    decoded_msg = pam2letters(hard_decisions)
    return decoded_msg





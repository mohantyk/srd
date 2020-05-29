import numpy as np
from scipy.fftpack import fft

def estimate_carrier_with_fft(sig, Ts):
    '''
    inputs:
        sig: modulated signal
        Ts: sampling interval
    outputs:
        freq: estimated carrier freq
        phase: estimated carrier phase
    '''
    sig_fft = fft(sig)
    max_idx = np.argmax(sig_fft[:len(sig_fft)//2])
    Fs = 1/Ts
    N = len(sig)
    freq_range = Fs*np.arange(0, N//2)/(N)
    freq = freq_range[max_idx]
    phase = np.angle(sig_fft[max_idx])
    return freq, phase
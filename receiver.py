import numpy as np
from scipy import signal

from wavegen import cosine_wave
from utilities import power

def ideal_receiver(sig, fc, Ts):
    '''
    inputs:
        sig: received signal (numpy array)
        fc:  carrier frequency
        Ts:  sampling duration (for simulated analog sig)
    '''
    duration = len(sig)*Ts
    t, carrier = cosine_wave(fc, duration, Ts)
    demodulated = sig * carrier
    # low pass filter
    taps = 50
    Fs = 1/Ts
    band_edges = np.array([0, 0.1, 0.2, 1])*(Fs//2) # Cutoff at 0.1*Fs/2
    damps = [1, 0]
    b = signal.remez(taps, band_edges, damps, fs=Fs)
    # Scaling by 2 below to compensate for cos(x)**2 = (1/2)*[cos(2x) + 1]
    baseband = 2*signal.lfilter(b, 1, demodulated) # Baseband is still in 'analog' domain
    # Use correlation to extract pulses
    oversample_factor = 100
    pulse = signal.hamming(oversample_factor)
    pulse_normalized = pulse/(power(pulse)*len(pulse))
    correlator = np.correlate(baseband, pulse_normalized, 'full')

    return correlator





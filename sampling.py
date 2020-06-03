import numpy as np
from wavegen import srrc

def sample_waveform(sig, fs, Ts):
    '''
    inputs:
        sig: signal
        fs: Sampling frequency
        Ts: Simulation timestep
    output:
        sampled waveform
    '''
    Fs = 1/Ts # Simulation sampling rate, not actual sampling rate
    sample_ratio = Fs/fs
    n = round(sample_ratio) # Number of samples to be skipped

    w = np.zeros_like(sig)
    w[::n] = sig[::n]
    return w


def oversample(sig, factor=10):
    '''
    Oversample a signal by factor. Insert zeros in between
    '''
    num_samples = len(sig)
    oversampled = np.zeros(factor * num_samples)
    oversampled[::factor] = sig
    return oversampled


def interpolate(samples, t, l, β=0):
    '''
    Interpolate to find a single point using a sinc (or srrc) waveform
    inputs:
        samples : sampled data
        t       : time at which value is desired
        l       : one sided length from which to interpolate
        β       : roll-off factor for srrc (0 is sinc)
    '''
    t_now = np.round(t)
    τ = t - t_now
    waveform = srrc(l, 1, β, τ)

    lmargin = max(0, t_now-l)
    rmargin = min(len(samples), t_now+l+1)
    x = np.convolve(samples[lmargin:rmargin], waveform, 'same')
    final = x[l]
    return final
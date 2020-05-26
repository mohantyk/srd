import numpy as np

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


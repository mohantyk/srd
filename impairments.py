import numpy as np
from scipy import signal

def time_varying_fading_channel(sig):
    '''Implements a time varying fading channel'''
    channel = np.ones_like(sig)
    fading_start = int(0.2*len(sig))
    channel[fading_start:] = 0.5
    faded_sig = sig*channel
    return faded_sig


def agc(sig, desired_power, learning_rate=0.0003):
    gains = np.zeros_like(sig)
    output = np.zeros_like(sig)
    gains[0] = 1
    for i, sample in enumerate(sig[:-1]):
        output[i] = gains[i] * sample
        gains[i+1] = gains[i] - learning_rate*(output[i]**2 - desired_power)
    output[-1] = gains[-1] * sig[-1]
    return output, gains


def add_noise(sig, noise_gain=1):
    noise = noise_gain * np.random.randn(*sig.shape)
    noisy_sig = sig + noise
    return noisy_sig


def create_multipath(sig, severity='none', oversample_factor=100):
    '''
    inputs:
        sig : input signal
        severity: none, mild, harsh
        oversample_factor: oversampling factor for analog signal
    outputs:
        output signal
        multipath channel taps
    '''
    M = oversample_factor
    if severity == 'none':
        channel = np.array([1, 0, 0])
    elif severity == 'mild':
        channel = np.zeros(1+M+1+int(2.3*M)+1)
        channel[0] = 1
        channel[M+1] = 0.28
        channel[-1] = 0.11
    elif severity == 'harsh':
        channel = np.zeros(1+M+1+int(1.8*M)+1)
        channel[0] = 1
        channel[M+1] = 0.28
        channel[-1] = 0.4
    else:
        raise ValueError('Unknown argument type')

    # Normalize channel energy, multipath copies can not exceed total input energy
    channel /= np.linalg.norm(channel)
    output = signal.lfilter(channel, 1, sig)
    return output, channel

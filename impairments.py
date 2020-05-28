import numpy as np

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

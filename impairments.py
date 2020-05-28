import numpy as np

def time_varying_fading_channel(sig):
    '''Implements a time varying fading channel'''
    channel = np.ones_like(sig)
    fading_start = int(0.2*len(sig))
    channel[fading_start:] = 0.5
    faded_sig = sig*channel
    return faded_sig
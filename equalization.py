import numpy as np
from scipy import signal

from receiver import quantalph

def evaluate_equalizer(channel, equalizer, alphabet=None, num_symbols=1000):
    '''
    Evaluates the quality of a equalizer by simulation with random samples
    parameters:
        channel : channel taps (numpy array)
        equalizer: linear equalizer (numpy array)
        alphabet: symbol alphabet (defaults to 4-PAM)
        num_symbols: number of test symbols to generate
    returns:
        numpy array with number of errors for every delay.
        errors[i] is the number of errors when delay = i
    '''
    if alphabet is None:
        alphabet = np.array([-3, -1, 1, 3]) # 4 - PAM
    symbols = np.random.choice(alphabet, num_symbols)
    received = signal.lfilter(channel, 1, symbols)
    equalized = signal.lfilter(equalizer, 1, received)
    decisions = quantalph(equalized, alphabet)

    errors = []
    n = len(equalizer)
    for delay in range(n):
        error = 0.5*np.sum( np.abs(decisions[delay:] - symbols[:num_symbols-delay]) )
        errors.append(error)

    return np.array(errors)
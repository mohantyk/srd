import numpy as np
from scipy import signal

from receiver import quantalph

def lms_equalizer(received, pilot, taps=4, mu=0.01):
    '''
    LMS equalizer
    parameters:
        received: received signal
        pilot: transmitted pilot symbols
        taps: number of filter taps
        mu: learning rate
    output:
        filter coefficients
    '''
    f = np.zeros(taps, float)
    delay = taps//2
    for i in range(taps, len(received)):
        window = received[i:i-taps:-1]
        predicted = np.dot(f, window)
        err = pilot[i-delay] - predicted
        f = f + mu*err*window
    return f


def dd_equalizer(received, alphabet, taps=4, mu=0.1):
    '''
    Decision directed equalizer
    parameters:
        received: received signal
        alphabet: decision alphabet
        taps: number of filter taps
        mu: learning rate
    output:
        filter coefficients
    '''
    f = np.zeros(taps, float)
    f[len(f)//2] = 1 # Center-spike initialization
    for i in range(taps, len(received)):
        window = received[i:i-taps:-1]
        predicted = np.dot(f, window)
        decision = quantalph(np.array(predicted), alphabet)
        err = decision[0] - predicted
        f = f + mu*err*window
    return f


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
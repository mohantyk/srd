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


def pll_sq_diff(sig, freq_estimate, Ts, mu=0.001, window=25, initial_ph_estimate=0):
    '''
    inputs:
        sig: signal at double the carrier frequency (and double the phase of carrier)
        freq_estimate: estimate of carrier frequency (assumed to be known perfectly)
        Ts: sampling duration
        mu: learning rate
        window: width of window over which averaging is done
    output:
        adaptive estimates of phase
    '''
    f0 = freq_estimate
    theta = np.zeros_like(sig)
    theta[0] = initial_ph_estimate
    avg_filter = np.ones(window)/window
    buffer = np.zeros_like(avg_filter)

    for k, sample in enumerate(sig[:-1]):
        tick = k*Ts
        deriv = (sample - np.cos(4*np.pi*f0*tick + 2*theta[k])) * np.sin(4*np.pi*f0*tick + 2*theta[k])
        buffer = np.roll(buffer, 1)
        buffer[0] = deriv
        theta[k+1] = theta[k] - mu*np.dot(avg_filter, buffer)
    return theta
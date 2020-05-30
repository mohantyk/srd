import numpy as np
from scipy import signal
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


def pll_sq_diff(sig, freq_estimate, Ts, mu=0.001, window=25, initial_phase=0):
    '''
    inputs:
        sig: signal at double the carrier frequency (and double the phase of carrier)
        freq_estimate: estimate of carrier frequency (assumed to be known perfectly)
        Ts: sampling duration
        mu: learning rate
        window: width of window over which averaging is done
        initial_phase: initial estimate of phase
    output:
        adaptive estimates of phase
    '''
    f0 = freq_estimate
    theta = np.zeros_like(sig)
    theta[0] = initial_phase
    avg_filter = np.ones(window)/window
    buffer = np.zeros_like(avg_filter)

    for k, sample in enumerate(sig[:-1]):
        tick = k*Ts
        deriv = (sample - np.cos(4*np.pi*f0*tick + 2*theta[k])) * np.sin(4*np.pi*f0*tick + 2*theta[k])
        buffer = np.roll(buffer, 1)
        buffer[0] = deriv
        theta[k+1] = theta[k] - mu*np.dot(avg_filter, buffer)
    return theta


def pll(sig, freq_estimate, Ts, mu=0.003, psi=0, initial_phase=0):
    '''
    inputs:
        sig: signal at double the carrier frequency (and double the phase of carrier)
        freq_estimate: estimate of carrier frequency (assumed to be known perfectly)
        Ts: sampling duration
        mu: learning rate
        initial_phase: initial estimate of phase
        psi: known constant phase
    output:
        adaptive estimates of phase
    '''
    f0 = freq_estimate
    theta = np.zeros_like(sig)
    theta[0] = initial_phase
    # LPF
    Fs = 1/Ts
    taps = 100
    band_edges = np.array([0, 0.01, 0.02, 1])*(Fs/2)
    damps = [1, 0]
    lpf = signal.remez(taps, band_edges, damps, fs=Fs)
    buffer = np.zeros_like(lpf)

    for k, sample in enumerate(sig[:-1]):
        tick = k*Ts
        deriv = np.sin(4*np.pi*f0*tick + 2*theta[k] + psi)*sample
        buffer = np.roll(buffer, 1)
        buffer[0] = deriv
        theta[k+1] = theta[k] - mu*np.dot(lpf, buffer)
    return theta


def costas(sig, freq_estimate, Ts, mu=0.003, initial_phase=0):
    '''
    inputs:
        sig: original signal (no need to process with non-linearity)
        freq_estimate: estimate of carrier frequency (assumed to be known perfectly)
        Ts: sampling duration
        mu: learning rate
        initial_phase: initial estimate of phase
    output:
        adaptive estimates of phase
    '''
    f0 = freq_estimate
    theta = np.zeros_like(sig)
    theta[0] = initial_phase
    # LPF
    Fs = 1/Ts
    taps = 500
    band_edges = np.array([0, 0.01, 0.02, 1])*(Fs/2)
    damps = [1, 0]
    lpf = signal.remez(taps, band_edges, damps, fs=Fs)
    # Two buffers, one each for the cosine path and sine path
    buffer_cosine = np.zeros_like(lpf)
    buffer_sine = np.zeros_like(lpf)

    for k, sample in enumerate(sig[:-1]):
        tick = k*Ts
        # Cosine path
        path_cosine = 2*np.cos(2*np.pi*f0*tick + theta[k])*sample
        buffer_cosine = np.roll(buffer_cosine, 1)
        buffer_cosine[0] = path_cosine
        # Sine path
        path_sine = 2*np.sin(2*np.pi*f0*tick + theta[k])*sample
        buffer_sine = np.roll(buffer_sine, 1)
        buffer_sine[0] = path_sine
        # Update theta
        theta[k+1] = theta[k] - mu*np.dot(lpf, buffer_cosine)*np.dot(lpf, buffer_sine)
    return theta

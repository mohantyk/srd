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


def dual_plls(sig, freq_estimate, Ts, mu1=0.01, mu2=0.003):
    '''
    inputs:
        sig: signal at double the carrier frequency (and double the phase of carrier)
        freq_estimate: estimate of carrier frequency
        Ts: sampling duration
        mu1: learning rate for frequency estimating pll
        mu2: learning rate for phase estimating pll
    output:
        (freq_est, phase_est), (theta1, theta2), est_carrier
        freq_est: carrier frequency estimate
        phase_est: carrier phase estimate
        theta1 : frequency estimating pll output (slope gives estimate of frequency difference)
        theta2 : phase estimating pll output
        est_carrier: final estimated squared carrier (at 2*f frequency and 2*phi phase)
    '''
    f0 = freq_estimate
    theta1 = np.zeros_like(sig)
    theta2 = np.zeros_like(sig)
    est_carrier = np.zeros_like(sig)
    # Note: skipping pll since the integrator already does a low pass filtering
    for k, sample in enumerate(sig[:-1]):
        tick = k*Ts
        # Top PLL
        error1 = np.sin(4*np.pi*f0*tick + 2*theta1[k])*sample
        theta1[k+1] = theta1[k] - mu1*error1
        # Bottom PLL
        error2 =  np.sin(4*np.pi*f0*tick + 2*theta1[k] + 2*theta2[k])*sample
        theta2[k+1] = theta2[k] - mu2*error2
        # Estimate carrier
        est_carrier[k] = np.cos(4*np.pi*f0*tick + 2*theta1[k] + 2*theta2[k])
    # Add the final sample of the estimated carrier
    k = len(sig) - 1
    est_carrier[k] = np.cos(4*np.pi*f0*k*Ts + 2*theta1[k] + 2*theta2[k])

    # Estimate frequency as slope of theta1
    t = np.arange(0, len(sig)*Ts, Ts)
    l = len(theta1)
    f_diff = (theta1[l//2] - theta1[l//4])/(2*np.pi*(t[l//2] - t[l//4]))
    freq_est = f0 + f_diff
    # Estimate phase from theta1 and theta2
    b = theta1[l//2] - 2*np.pi*f_diff # Intercept of theta1 line
    phase_est = theta2[-1] + b

    return (freq_est, phase_est), (theta1, theta2), est_carrier

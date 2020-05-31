def eye_diag(analog, n_eye=5, oversample_factor=10):
    '''
    inputs:
        analog: analog signal
        n_eye: number of symbols for eye
        oversample_factor: oversampling factor for analog signal
    output:
        2D array, each row consists of n_eye symbols
    '''
    M = oversample_factor
    n_eye = 5 # Number of symbols in eye
    groups = len(analog)//(n_eye*M)
    eye_diag = analog[-n_eye*groups*M:].reshape(-1, n_eye*M)
    return eye_diag

import numpy as np
from scipy import signal

from transmitter import *

from numpy.testing import assert_array_equal

class TestHelpers:
    def test_pairwise(self):
        nums = [1,2,3,4]
        paired = list(pairwise(nums))
        assert paired == [(1,2), (3,4)]

class TestEncoding:
    def test_letters2pam(self):
        msg = 'A'
        assert letters2pam(msg) == [-1, -3, -3, -1]

        msg = 'AI'
        assert letters2pam(msg) == [-1, -3, -3, -1, -1, -3, 1, -1]

    def test_pulse_shape(self):
        symbols = [1, -1]
        analog_signal = pulse_shaped(symbols)

        pulse = signal.hamming(10)
        expected_analog = np.concatenate((pulse, -pulse))
        assert_array_equal(analog_signal, expected_analog)
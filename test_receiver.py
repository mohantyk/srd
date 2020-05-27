from numpy.testing import assert_array_equal

from receiver import *


class TestDecoder:
    def test_pam2letters(self):
        symbols = [-1, -3, -3, -1]
        assert pam2letters(symbols) == 'A'
        symbols = [-1, -3, -3, -1, -1, -3, 1, -1]
        assert pam2letters(symbols) == 'AI'

    def test_quantalph(self):
        soft_decisions = np.array([-2.9, -3.2, 1.1])
        alphabet = np.array([-3, -1, 1, 3])
        symbols = quantalph(soft_decisions, alphabet)
        expected = np.array([-3, -3, 1])
        assert_array_equal(symbols, expected)

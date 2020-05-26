from receiver import *


class TestDecoder:
    def test_pam2letters(self):
        symbols = [-1, -3, -3, -1]
        assert pam2letters(symbols) == 'A'

        symbols = [-1, -3, -3, -1, -1, -3, 1, -1]
        assert pam2letters(symbols) == 'AI'
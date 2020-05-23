from transmitter import *

class TestHelpers:
    def test_pairwise(self):
        nums = [1,2,3,4]
        paired = list(pairwise(nums))
        assert paired == [(1,2), (3,4)]

class TestEncoding:
    def test_letters2pam(self):
        msg = 'A'
        assert letters2pam(msg) == [-1, -3, -3, -1]
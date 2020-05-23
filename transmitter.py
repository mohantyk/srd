# Helper functions
def pairwise(iterator):
    ''' Pairs up two elements at a time '''
    window = [iter(iterator)]*2
    for combo in zip(*window):
        yield combo

#-----------------
# Encoding
def letters2pam(msg):
    msg_bin = ''.join('{:08b}'.format(ord(ch)) for ch in msg)
    symbol_map = {'11': 3, '10': 1, '01': -1, '00': -3}
    symbols = [symbol_map[''.join(pair)] for pair in pairwise(msg_bin)]
    return symbols

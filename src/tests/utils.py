#!/usr/bin/env python3
# pylint: disable=C0111


def byte_bin_str_repr(byte):
    '''
    Returns (as a string) binary representation of byte filled with "0" to the full 8-bit length
    e.g.:   byte_bin_str_repr(4) == '00000100'
    '''
    assert byte.bit_length() <= 8
    return bin(byte)[2:].rjust(8, '0')


def bytes_bin_str_repr(data):
    '''
    Returns (as a string) binary representation of bytes array with each byte filled with "0" to the full 8-bit length
    e.g.:
        bytes_bin_str_repr(b'Z!') == '0101101000100001'
        # because b'Z!' <-> (90, 33) <-> (0b1011010, 0b100001) <-> 0_1011010_0_100001
    '''
    return ''.join([byte_bin_str_repr(byte) for byte in data])


def change_one_bit(data):
    '''Inverts one pseudo-random bit in given bytes object'''
    byte_no = data[0] % len(data)  # choose some "pseudo-random" byte
    byte = data[byte_no]
    bit_no = sum(data) % 8   # choose some "pseudo-random" bit
    changed_byte = byte ^ (1 << bit_no)
    ret = list(data)
    ret[byte_no] = changed_byte
    return bytes(ret)

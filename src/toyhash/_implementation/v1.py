#!/usr/bin/env python3
'''Algorithm implementation, version 1'''

# pylint: disable=missing-docstring, too-few-public-methods
class ToyHashImplementation:
    __slots__ = 'bit_length', 'bit_maximum', 'buffer', 'prime', 'seed', 'state'

    version = 1
    _default_prime = sum('There is always at least one prime number in cryptography!'.encode())  # it is 5503; and yes it is prime
    _default_seed = sum('ToyHash'.encode())

    # python implementation of bitwise rotation taken
    # from MartyMacGyver's code: https://bit.ly/2y4xaGI
    _rotate = [
        # rotate right
        lambda val, ro_bits, max_bits: ((val & (2**max_bits-1)) >> ro_bits%max_bits) \
                                        | (val << (max_bits-(ro_bits%max_bits)) & (2**max_bits-1)),
        # rotate left
        lambda val, ro_bits, max_bits: (val << ro_bits%max_bits) & (2**max_bits-1) \
                                        | ((val & (2**max_bits-1)) >> (max_bits-(ro_bits%max_bits)))
        ]

    def __init__(self, bit_length, prime=_default_prime, seed=_default_seed):
        assert bit_length % 8 == 0

        self.prime = prime
        self.seed = seed ** bit_length
        self.bit_length = bit_length
        self.bit_maximum = 2 ** bit_length
        self.state = 0

        self.buffer = self.seed * self.prime
        while self.bit_length > self.buffer.bit_length():
            part = self.seed * self.prime ^ self.buffer.bit_length()
            self.buffer <<= part.bit_length()
            self.buffer += part
        self.buffer = self.buffer % (self.bit_maximum - 1)

    def update(self, data=b''):
        for byte in data:
            self.state += (self.prime % byte) if byte else self.prime
            self.buffer = self._rotate[(byte+self.state) % 2](self.buffer, byte, self.bit_length)

            rotated_byte = self._rotate[self.state % 2](byte, self.state ^ self.prime, 8)
            power = pow(self.seed, rotated_byte, self.state)

            intermediate_res = pow(self.buffer, power, self.prime)

            self.buffer ^= intermediate_res
            self.buffer %= self.bit_maximum

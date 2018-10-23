#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Some simple hash function implementation.
Written for fun and self-education.
Remember the rule
    "Don't roll your own crypto!"
and don't use it in any real project please.
'''

from operator import itemgetter


ALGORITHM_VERSION = 1
VERSION = (ALGORITHM_VERSION, 0, 0)


class ToyHash:
    '''Some simple hash function implementation. Don't use it in real project.'''
    # pylint: disable=R0902
    __slots__ = ('_algorithm', '_bit_length', '_bit_maximum',
                 '_buffer', 'digest_size', '_storage', '_state')

    # python implementation of bitwise rotation taken
    # from MartyMacGyver's code: https://bit.ly/2y4xaGI
    _ro_op = [
        # rotate right
        lambda val, ro_bits, max_bits: ((val & (2**max_bits-1)) >> ro_bits%max_bits) \
                                        | (val << (max_bits-(ro_bits%max_bits)) & (2**max_bits-1)),
        # rotate left
        lambda val, ro_bits, max_bits: (val << ro_bits%max_bits) & (2**max_bits-1) \
                                        | ((val & (2**max_bits-1)) >> (max_bits-(ro_bits%max_bits)))
        ]

    def __init__(self, data=b'', bit_length=None, initials=None, algorithm_version=ALGORITHM_VERSION):
        if isinstance(data, (bytes, bytearray)):
            if not isinstance(bit_length, int) or bit_length % 8 != 0:
                raise ValueError('bit_length must be positive integer multiple of 8')

            # for possible backward compatibility. See comment near `_algo_ver_1` for details.
            if not hasattr(self.__class__, '_algo_ver_%d' % algorithm_version):
                raise ValueError('Implementation of algorithm version %d not found' % algorithm_version)
            self._algorithm = getattr(self, '_algo_ver_%d' % algorithm_version)

            self.digest_size = bit_length // 8
            self._bit_length = bit_length
            self._bit_maximum = 2 ** bit_length
            self._storage = initials or {}
            self._buffer = None

            self._algorithm('init')
            self.update(data)
        elif isinstance(data, self.__class__):
            # `self` should be copy of another instance
            for attr in self.__slots__:
                setattr(self, attr, getattr(data, '_buffer'))
        elif isinstance(data, str):
            raise TypeError("Unicode-objects must be encoded before hashing")
        else:
            raise TypeError("Input data should be bytes or bytearray")

    def update(self, data):
        '''Update this hash object's state with the provided data. Repeated calls
        are equivalent to a single call with the concatenation of all
        the arguments, i.e. toyhash_obj.update(b'foo'); toyhash_obj.update(b'bar')
        is equivalent to toyhash_obj.update(b'foobar').
        '''
        if isinstance(data, str):
            raise TypeError("Unicode strings must be encoded to bytes or bytearray array before hashing")
        self._algorithm('update', data=data)

    def digest(self):
        '''Return the digest of the data. This is a byte string'''
        # len of returned bytes will be self._bit_length // 8
        hd = self.hexdigest()
        d = []
        for i in range(0, len(hd), 2):
            d.append(int(hd[i:i+2], 16))
        return bytes(d)

    def hexdigest(self):
        '''Like digest() except the digest is returned as a string
        containing only hexadecimal digits.'''
        pattern = '%0'+'%d' % (self._bit_length//4) + 'x'
        return pattern % self._buffer

    def copy(self):
        '''Return a copy ('clone') of the hash object. This can be used
        to efficiently compute the digests of data that share a common
        initial subset.'''
        return self.__class__(data=self)

    # For backward compatibility:
    # Changes in hash function logic after publishing seems really HORRIBLE idea. Even if it is toy function.
    # But in case changing is absolutly inevitable, don't do it here (in already present `_algo_ver_<N>` method).
    # Create corresponding `_algo_ver_<N_PLUS_ONE>` method and switch ALGORITHM_VERSION at the top to <N_PLUS_ONE> value.

    def _algo_ver_1(self, operation, **kwargs):
        if operation == 'init':
            assert isinstance(self._storage, dict)

            default_prime = sum('There is always at least one prime number in cryptography!'.encode())
            # it is 5503; and yes it is prime

            prime = self._storage.get('prime', default_prime)
            seed = self._storage.get('seed', sum('ToyHash'.encode()) ** self._bit_length)
            state = 0

            self._storage = {'prime': prime, 'seed': seed, 'state': state}

            buffer = seed * prime
            while self._bit_length > buffer.bit_length():
                part = seed * prime ^ buffer.bit_length()
                buffer <<= part.bit_length()
                buffer += part
            self._buffer = buffer % (self._bit_maximum - 1)

        elif operation == 'update':
            data = kwargs.get('data', b'')
            seed, prime, state = itemgetter('seed', 'prime', 'state')(self._storage)
            for byte in data:
                state += (prime % byte) if byte else prime
                self._buffer = self._ro_op[(byte+state) % 2](self._buffer, byte, self._bit_length)

                rotated_byte = self._ro_op[state % 2](byte, state ^ prime, 8)
                power = pow(seed, rotated_byte, state)  # pylint: disable=W0621

                intermediate_res = pow(self._buffer, power, prime)

                self._buffer ^= intermediate_res
                self._buffer %= self._bit_maximum
            self._storage['state'] = state
        else:
            assert False, 'Unknown operation'


def toyhash(data=b'', bit_length=None):
    '''Some simple hash function. Don't use it in real project.'''
    if not isinstance(bit_length, int) or bit_length <= 0 or bit_length % 8 != 0:
        raise ValueError('bit_length must be positive integer multiple of 8, but %s given' % bit_length)
    return ToyHash(data, bit_length)

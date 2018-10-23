#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Some simple hash function implementation.
Written for fun and self-education.
Remember the rule
    "Don't roll your own crypto!"
and don't use it in any real project please.
'''

from copy import deepcopy


ALGORITHM_VERSION = 1
VERSION = (ALGORITHM_VERSION, 0, 1)


class ToyHash:
    '''Some simple hash function implementation. Don't use it in real project.'''
    __slots__ = '_bit_length', 'digest_size', '_implementation', '_initials'

    def __init__(self, data=b'', bit_length=None, initials=None, algorithm_version=ALGORITHM_VERSION):
        if isinstance(data, (bytes, bytearray)):
            if not isinstance(bit_length, int) or bit_length % 8 != 0:
                raise ValueError('bit_length must be positive integer multiple of 8')
            self.digest_size = bit_length // 8
            self._bit_length = bit_length
            self._initials = initials
            self._get_implementation(algorithm_version, initials=initials or {})
            self.update(data)
        elif isinstance(data, self.__class__):
            # `self` should be copy of another instance
            for attr_name in self.__slots__:
                attr = getattr(data, attr_name)
                if attr_name == '_implementation':
                    setattr(self, attr_name, deepcopy(attr))
                else:
                    setattr(self, attr_name, attr)
        elif isinstance(data, str):
            raise TypeError("Unicode-objects must be encoded before hashing")
        else:
            raise TypeError("Input data should be bytes or bytearray")

    # For backward compatibility:
    # Changes in hash function logic after publishing seems really HORRIBLE idea. Even if it is toy function.
    # However, if changing is absolutly inevitable, it must be done not in the current version of implementation
    # but in next one.
    # Implementation are searched in submodule `toyhash._implementation.v<VERSION>`.
    #   - it must be class named `ToyHashImplementation` with attribute `version` = <VERSION>
    #   - class `__init__` method
    #           - must accept mandatory `bit_length` argument
    #           - can accept any other necessary for implementation arguments, but they must be optional
    #   - class `update` method must accept bytes instance as first argument
    #   - class must provide `buffer` attribute containing hashing result as integer with bit length equal to initial `bit_length`
    #
    # See `toyhash._implementation.v1` as example
    def _get_implementation(self, version, initials):
        from importlib import import_module

        try:
            module = import_module('toyhash._implementation.v%s' % version)
            th_class = getattr(module, 'ToyHashImplementation')
        except (ImportError, AttributeError):
            raise ValueError('Implementation of algorithm version %s not found' % version)
        if getattr(th_class, 'version', float('Nan')) != version:  # float('Nan') is not equal to anything
            raise ValueError('Algorithm version %s expected, '
                             'but %s was found' % (version, getattr(th_class, 'version', 'unknown version')))
        self._implementation = th_class(bit_length=self._bit_length, **initials)

    def update(self, data):
        '''Update this hash object's state with the provided data. Repeated calls
        are equivalent to a single call with the concatenation of all
        the arguments, i.e. toyhash_obj.update(b'foo'); toyhash_obj.update(b'bar')
        is equivalent to toyhash_obj.update(b'foobar').
        '''
        if isinstance(data, str):
            raise TypeError("Unicode strings must be encoded to bytes or bytearray array before hashing")
        self._implementation.update(data)

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
        return pattern % self._implementation.buffer

    def copy(self):
        '''Return a copy ('clone') of the hash object. This can be used
        to efficiently compute the digests of data that share a common
        initial subset.'''
        return self.__class__(data=self)


def toyhash(data=b'', bit_length=None):
    '''Some simple hash function. Don't use it in real project.'''
    if not isinstance(bit_length, int) or bit_length <= 0 or bit_length % 8 != 0:
        raise ValueError('bit_length must be positive integer multiple of 8, but %s given' % bit_length)
    return ToyHash(data, bit_length)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111
import types
import sys

from toyhash.core import toyhash, VERSION, __doc__


assert isinstance(__doc__, object)  # pyflakes get lost plz!

__all__ = ['toyhash', 'VERSION']

# Dynamic creation of shortcut functions with fixed bit_length
def _generate(bl):
    def _boilerplate(data=b''):
        return toyhash(data, bl)
    return _boilerplate

for power in range(6, 10):
    # Питономешалка мешает питон! (Простите)
    bits = 2 ** power
    fname = 'toyhash%d' % bits

    func = _generate(bits)
    func.__doc__ = toyhash.__doc__.replace("hash", "%d-bit hash" % bits)
    func.__name__ = fname
    func.__qualname__ = fname

    setattr(sys.modules[__name__], fname, func)
    __all__.append(fname)

    del bits, func, fname, power
del sys, types, _generate

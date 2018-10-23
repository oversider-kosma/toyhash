#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111
import types
import sys

from toyhash.core import toyhash, VERSION, __doc__


assert isinstance(__doc__, object)  # pyflakes get lost plz!

__all__ = ['toyhash', 'VERSION']

# Dynamic creation of shortcut functions with fixed bit_length
for power in range(6, 10):
    # Питономешалка мешает питон! (Простите)
    bits = 2 ** power
    fname = 'toyhash%d' % bits

    def _boilerplate(data=b''):
        return toyhash(data, bit_length=0)
    _code = _boilerplate.__code__

    # Did you know that `types.CodeType.__doc__` says it is "Not for the faint of heart"?
    # Well... I hope I'm not.
    func_code = types.CodeType(_code.co_argcount, _code.co_kwonlyargcount, _code.co_nlocals,
                               _code.co_stacksize, _code.co_flags, _code.co_code,
                               (None, 'bit_length', bits),
                               _code.co_names, _code.co_varnames, _code.co_filename,
                               fname,
                               _code.co_firstlineno, _code.co_lnotab)

    func = types.FunctionType(func_code, _boilerplate.__globals__, fname)
    func.__doc__ = toyhash.__doc__.replace("hash", "%d-bit hash" % bits)
    func.__qualname__ = fname
    func.__defaults__ = _boilerplate.__defaults__

    setattr(sys.modules[__name__], fname, func)
    __all__.append(fname)

    del _code, _boilerplate, bits, func, func_code, fname, power
del sys, types

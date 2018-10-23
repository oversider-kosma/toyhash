#!/usr/bin/env python3
# pylint: disable=C0111
from hashlib import sha512

from toyhash import toyhash64, toyhash128, toyhash256, toyhash512  # pylint: disable=E0611
from toyhash.core import ToyHash

from tests.utils import bytes_bin_str_repr, change_one_bit


def test_determinacy():
    assert toyhash256(b'qwerty').digest() == toyhash256(b'qwerty').digest()


def test_update_idempotency():
    h = toyhash64()
    h.update(b'qwe')
    h.update(b'asd')
    h.update(b'zxc')

    assert h.hexdigest() == toyhash64(b'qweasdzxc').hexdigest()
    assert h.digest() == toyhash64(b'qweasdzxc').digest()


def test_avalanche_vs_sha():
    messages = (
        b'1', b'12', b'qwe', b'zazaza', b'foobarbaz', b'lorem ipsum', b'abracadabra',
        b'Klaatu barada nikto', b'not very random string', b'one more not very random string',
        b'Every even integer greater than 2 can be expressed as the sum of two primes.',

        b' S A T O R \n' +
        b' A R E P O \n' +
        b' T E N E T \n' +
        b' O P E R A \n' +
        b' R O T A S \n',)

    pairs = [(msg, change_one_bit(msg)) for msg in messages]

    avg_avalanche = {}

    for func in (toyhash512, sha512):
        diffs = []
        for pair in pairs:
            results = [func(msg).digest() for msg in pair]
            bits_repr = [bytes_bin_str_repr(digest) for digest in results]
            assert len(bits_repr[0]) == len(bits_repr[1]) == 512

            diffs.append(0)
            for bit1, bit2 in zip(*bits_repr):
                if bit1 != bit2:
                    diffs[-1] += 1
        avg_avalanche[func] = sum(diffs) // len(diffs)

    assert avg_avalanche[toyhash512] >= avg_avalanche[sha512]


def test_backward_compatibility():
    th = ToyHash(b'toyhash', bit_length=256, algorithm_version=1)
    assert th.hexdigest() == '81b9d20fb1ec32dbe0ca802a1f6d7aeff8099608244424e215e6bf309ee7c239'

def test_copy():
    hash1 = toyhash128(b'lasto beth lammen')
    hash2 = hash1.copy()

    assert hash1 is not hash2
    assert hash1._implementation is not hash2._implementation  # pylint: disable=W0212
    assert hash1.digest() == hash2.digest()

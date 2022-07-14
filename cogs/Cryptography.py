import discord
from discord.ext import commands
from discord import app_commands
import json
import requests
import aiohttp

import argparse
import pickle
import random
import hashlib
import functools as ft
import operator as op
import sys
import os
from typing import List, NamedTuple, Union
from random import randint, choice
from typing import Tuple, List, Optional, Any
from string import ascii_lowercase

"""
Encryption and decryption of messages
"""
def compress(a: bytes, b: bytes) -> bytes:
    """Given two length-32 byte sequences, compress them into a single
    length-32 byte sequences.

    This function is collision-resistent.

    Note: the implementation is based on SHA-256.

    >>> compress(b"0"*32, "a"*32)
    Traceback (most recent call last):
      ...
    ValueError: Non-bytes argument

    >>> compress(b"0"*32, b"0"*31)
    Traceback (most recent call last):
      ...
    ValueError: Non-length-32 argument

    >>> compress(b"0"*32, b"0"*32).hex()
    '60e05bd1b195af2f94112fa7197a5c88289058840ce7c6df9693756bc6250f55'
    """
    if not isinstance(a, bytes) or not isinstance(b, bytes):
        raise ValueError("Non-bytes argument")
    if len(a) != 32 or len(b) != 32:
        raise ValueError("Non-length-32 argument")
    return hashlib.sha256(a + b).digest()


class IntMod:
    value: int
    modulus: int

    def __init__(self, value: int, modulus: int):
        """
        Create an `IntMod`.

        You must reduce value modulo `modulus` before storing it.

        >>> IntMod(5, 7)
        IntMod(5, 7)

        >>> IntMod(11, 7)
        IntMod(4, 7)

        >>> IntMod(-1, 7)
        IntMod(6, 7)

        >>> IntMod(7, 7)
        IntMod(0, 7)

        """
        # Do not change.
        self.value = value % modulus
        self.modulus = modulus

    def __repr__(self) -> str:
        # Do not change.
        return f"IntMod({self.value}, {self.modulus})"

    def __add__(self, other: Union[int, "IntMod"]) -> "IntMod":
        """
        Add an `IntMod` and another `IntMod` or an integer.

        You should use:
            * `isinstance(other, int)` and
            * `isinstance(other, IntMod)`

        >>> IntMod(5, 7) + IntMod(2, 7)
        IntMod(0, 7)

        >>> IntMod(3, 7) + IntMod(3, 7)
        IntMod(6, 7)

        >>> IntMod(3, 7) + 3
        IntMod(6, 7)

        >>> 3 + IntMod(3, 7)
        IntMod(6, 7)
        """
        if isinstance(other, IntMod):
            assert self.modulus == other.modulus
            return IntMod(self.value + other.value, self.modulus)
        elif isinstance(other, int):
            return self + IntMod(other, self.modulus)
        else:
            assert False, f"Can't add {self} to {other}"

    def __neg__(self) -> "IntMod":
        return IntMod(-self.value, self.modulus)

    def __mul__(self, other: Union[int, "IntMod"]) -> "IntMod":
        """
        Multiply an `IntMod` and another `IntMod` or an integer.

        >>> IntMod(5, 7) * IntMod(2, 7)
        IntMod(3, 7)

        >>> IntMod(3, 7) * IntMod(3, 7)
        IntMod(2, 7)

        >>> IntMod(3, 7) * 3
        IntMod(2, 7)

        >>> 3 * IntMod(3, 7)
        IntMod(2, 7)
        """
        if isinstance(other, IntMod):
            assert self.modulus == other.modulus
            return IntMod(self.value * other.value, self.modulus)
        elif isinstance(other, int):
            return self * IntMod(other, self.modulus)
        else:
            assert False, f"Can't multiply {self} and {other}"

    def __truediv__(self, other: Union[int, "IntMod"]) -> "IntMod":
        """
        Multiply an `IntMod` and another `IntMod` or an integer.

        >>> IntMod(5, 7) / IntMod(2, 7)
        IntMod(6, 7)

        >>> IntMod(3, 7) / IntMod(3, 7)
        IntMod(1, 7)

        >>> IntMod(3, 7) / 3
        IntMod(1, 7)
        """
        if isinstance(other, IntMod):
            assert self.modulus == other.modulus
            return IntMod(self.value * pow(other.value, -1, self.modulus), self.modulus)
        elif isinstance(other, int):
            return self / IntMod(other, self.modulus)
        else:
            assert False, f"Can't divide {self} and {other}"

    def __pow__(self, other: int) -> "IntMod":
        """Raise an `IntMod` to the power `other`.

        >>> IntMod(2, 7) ** 1
        IntMod(2, 7)
        >>> IntMod(2, 7) ** 2
        IntMod(4, 7)
        >>> IntMod(2, 7) ** 3
        IntMod(1, 7)
        >>> IntMod(2, 7) ** 4
        IntMod(2, 7)
        >>> IntMod(2, 7) ** 5
        IntMod(4, 7)
        """
        return IntMod(pow(self.value, other, self.modulus), self.modulus)

    def __eq__(self, other: Union[int, "IntMod"]) -> bool:
        # Equality definition. Do not change.
        if isinstance(other, IntMod):
            assert self.modulus == other.modulus
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            assert False, f"Can't compare {self} == {other}"

    def __sub__(self, other: Union[int, "IntMod"]) -> "IntMod":
        # Subtraction definition. Do not change.
        return self + (-other)

    def __radd__(self, other: Union[int, "IntMod"]) -> "IntMod":
        # Addition is commutative. Do not change.
        return self + other

    def __rmul__(self, other: Union[int, "IntMod"]) -> "IntMod":
        # Multiplication is commutative. Do not change.
        return self * other

    def __req__(self, other: Union[int, "IntMod"]) -> bool:
        # Equality is commutative. Do not change.
        return self == other

    def __rsub__(self, other: Union[int, "IntMod"]) -> "IntMod":
        # Subtraction definition. Do not change.
        return -self + other


class Ed25519:
    """A point on the twisted edwards curve, "edwards25519".

    See [RFC7748](https://datatracker.ietf.org/doc/html/rfc7748#section-4.1) for a specification.
    """

    # base field (prime) order
    p = 2**255 - 19
    d = 37095705934669439343138083508754565189542113879843219016388785533085940283555
    order = 2**252 + int("14def9dea2f79cd65812631a5cf5d3ed", 16)

    def __init__(self, x: int, y: int):
        # check y*y - x*x = 1 + d*x*x*y*y (mod p)
        if (y * y - x * x - 1 - Ed25519.d * x * x * y * y) % Ed25519.p != 0:
            raise ValueError("Invalid x, y coordinate: does not satisfy curve equation")
        self.x = x % Ed25519.p
        self.y = y % Ed25519.p

    def __eq__(self, other) -> bool:
        if not isinstance(other, Ed25519):
            return False
        if self is other:
            return True
        return (self.x - other.x) % Ed25519.p == 0 and (
            self.y - other.y
        ) % Ed25519.p == 0

    def __repr__(self) -> str:
        if self.x == 0:
            return "Ed25519.identity()"
        elif self == Ed25519.generator():
            return "Ed25519.generator()"
        else:
            return f"Ed25519({self.x}, {self.y})"

    @classmethod
    def generator(cls) -> "Ed25519":
        """Get the generator of the group

        >>> Ed25519.identity() * Ed25519.generator()
        Ed25519.generator()
        """
        return cls(
            15112221349535400772501151409588531511454012693041857206046113283949847762202,
            46316835694926478169428394003475163141307993866256225615783033603165251855960,
        )

    @classmethod
    def identity(cls) -> "Ed25519":
        """Get the identity of the group

        >>> Ed25519.identity() * Ed25519.generator()
        Ed25519.generator()
        """
        return cls(0, 1)

    def __mul__(self, other: "Ed25519") -> "Ed25519":
        """Perform the group operation.

        >>> Ed25519.identity() * Ed25519.identity()
        Ed25519.identity()
        >>> Ed25519.identity() * Ed25519.generator()
        Ed25519.generator()
        >>> Ed25519.generator() * Ed25519.identity()
        Ed25519.generator()
        >>> g = Ed25519.generator()
        >>> (g * g) * g == g * (g * g)
        True
        >>> (g * g) * g != g * (g * g)
        False
        >>> (g * g) * g != g * g
        True
        """
        if not isinstance(other, Ed25519):
            raise ValueError(f"Cannot multiple curve point by {type(other)}")
        x1 = self.x
        y1 = self.y
        x2 = other.x
        y2 = other.y
        p = Ed25519.p
        d = Ed25519.d
        prod = d * x1 % p * x2 % p * y1 % p * y2 % p
        x = (x1 * y2 + y1 * x2) % p * pow(1 + prod, -1, p) % p
        y = (y1 * y2 + x1 * x2) % p * pow(p + 1 - prod, -1, p) % p
        return Ed25519(x, y)

    def inverse(self) -> "Ed25519":
        """Get the inverse of a group element

        >>> g = Ed25519.generator() ** 5
        >>> g * g.inverse()
        Ed25519.identity()
        """
        return Ed25519(-self.x, self.y)

    def __pow__(self, other: Union[int, IntMod]) -> "Ed25519":
        """Raise a group element to a power. The power can be an integer or an
        integer modulo the group order.

        >>> gen = Ed25519.generator()
        >>> ga = gen ** 3
        >>> ga ** 2 == gen ** 6
        True
        >>> gen ** -3 * gen ** 3
        Ed25519.identity()
        >>> neg_three_mod_order = IntMod(-3, Ed25519.order)
        >>> gen ** neg_three_mod_order * gen ** 3
        Ed25519.identity()
        """
        if isinstance(other, int):
            exp = other % self.order
        elif isinstance(other, IntMod):
            assert (
                other.modulus == self.order
            ), f"Cannot compute {self} ** {other} the modulus {other.modulus} is the group order {self.order}"
            exp = other.value
        else:
            assert False, f"Cannot compute {self} ** {other}"

        def helper(b, e):
            assert e >= 0
            if e == 0:
                return Ed25519.identity()
            elif e % 2 == 0:
                return helper(b * b, e // 2)
            else:
                return b * helper(b * b, e // 2)

        return helper(self, exp)

    def to_bytes(self) -> bytes:
        """Get this group element as bytes.

        >>> Ed25519.generator().to_bytes()
        b'Ed25519.generator()'
        >>> (Ed25519.generator() ** 2).to_bytes()
        b'Ed25519(24727413235106541002554574571675588834622768167397638456726423682521233608206, 15549675580280190176352668710449542251549572066445060580507079593062643049417)'
        """
        return repr(self).encode()


class ChaCha20State(NamedTuple):
    data: List[int]

    def add(self, dst: int, src: int):
        self.data[dst] = (self.data[dst] + self.data[src]) & 0xFFFF_FFFF

    def xor(self, dst: int, src: int):
        self.data[dst] = (self.data[dst] ^ self.data[src]) & 0xFFFF_FFFF

    def rot(self, dst: int, n: int):
        assert 0 <= n < 31
        self.data[dst] = ((self.data[dst] << n) & 0xFFFF_FFFF) | (
            (self.data[dst] >> (32 - n)) & 0xFFFF_FFFF
        )

    def qr(self, a: int, b: int, c: int, d: int):
        """Quarter round function

        Test case from RFC7539 section 2.1.1

        >>> st = ChaCha20State([0x11111111, 0x01020304, 0x9b8d6f43, 0x01234567])
        >>> st.qr(0, 1, 2, 3)
        >>> assert st.data == [0xea2a92f4, 0xcb1cf8ce, 0x4581472e, 0x5881c4bb]
        >>> st = ChaCha20State([0x879531e0, 0xc5ecf37d, 0x516461b1, 0xc9a62f8a, 0x44c20ef3, 0x3390af7f, 0xd9fc690b, 0x2a5f714c, 0x53372767, 0xb00a5631, 0x974c541a, 0x359e9963, 0x5c971061, 0x3d631689, 0x2098d9d6, 0x91dbd320])
        >>> st.qr(2, 7, 8, 13)
        """
        # fmt: off
        self.add(a, b); self.xor(d, a); self.rot(d, 16)
        self.add(c, d); self.xor(b, c); self.rot(b, 12)
        self.add(a, b); self.xor(d, a); self.rot(d,  8)
        self.add(c, d); self.xor(b, c); self.rot(b,  7)
        # fmt: on

    @classmethod
    def init(cls, key: bytes, counter: int, nonce: bytes) -> "ChaCha20State":
        """Initialize the ChaCha20 state

        >>> k = bytes.fromhex("00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f")
        >>> n = bytes.fromhex("00 00 00 09 00 00 00 4a 00 00 00 00")
        >>> c = 1
        >>> st = ChaCha20State.init(k, c, n)
        """
        consts = b"expand 32-byte k"
        if not isinstance(key, bytes) or len(key) != 32:
            raise ValueError("Expected 32 bytes of key")
        if not isinstance(counter, int) or not (0 <= counter < 2**32):
            raise ValueError("Expected 32-bit counter")
        if not isinstance(nonce, bytes) or len(nonce) != 12:
            raise ValueError("Expected 12 bytes of nonce")
        counter_bytes = counter.to_bytes(4, byteorder="little")
        data = consts + key + counter_bytes + nonce
        return cls(
            [
                int.from_bytes(data[i : i + 4], byteorder="little")
                for i in range(0, 64, 4)
            ]
        )

    def finish(self) -> bytes:
        return ft.reduce(op.add, [i.to_bytes(4, byteorder="little") for i in self.data])

    @staticmethod
    def get_block(key: bytes, ctr: int, nonce: bytes) -> bytes:
        """
        >>> k = bytes.fromhex("00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f")
        >>> n = bytes.fromhex("00 00 00 09 00 00 00 4a 00 00 00 00")
        >>> c = 1
        >>> out = ChaCha20State.get_block(k, c, n)
        >>> out.hex(" ")
        '10 f1 e7 e4 d1 3b 59 15 50 0f dd 1f a3 20 71 c4 c7 d1 f4 c7 33 c0 68 03 04 22 aa 9a c3 d4 6c 4e d2 82 64 46 07 9f aa 09 14 c2 d7 05 d9 8b 02 a2 b5 12 9c d1 de 16 4e b9 cb d0 83 e8 a2 50 3c 4e'
        """

        st = ChaCha20State.init(key, ctr, nonce)
        orig_st = st.data[:]
        for _ in range(10):
            # fmt: off
            st.qr( 0,  4,  8, 12)
            st.qr( 1,  5,  9, 13)
            st.qr( 2,  6, 10, 14)
            st.qr( 3,  7, 11, 15)
            st.qr( 0,  5, 10, 15)
            st.qr( 1,  6, 11, 12)
            st.qr( 2,  7,  8, 13)
            st.qr( 3,  4,  9, 14)
            # fmt: on
        st = ChaCha20State([(a + b) & 0xFFFF_FFFF for a, b in zip(orig_st, st.data)])
        return st.finish()


def prg(seed: bytes, n: int) -> bytes:
    """Generate `n` bytes from a PRG with `seed` (a length-32 byte sequence).

    Note: the implementation is based on ChaCha20, but this **is not** a secure
    stream cipher.


    >>> prg("a", 5)
    Traceback (most recent call last):
      ...
    ValueError: Seed is not a byte sequence

    >>> prg(b"0", 5)
    Traceback (most recent call last):
      ...
    ValueError: Seed has length 1. It should be 32.

    >>> prg(b"0" * 32, 5).hex()
    '5408783b02'

    >>> prg(b"0" * 32, 6).hex()
    '5408783b02a4'

    >>> for i in range(10):
    ...   assert len(prg(b"0" * 32, i)) == i
    ...   assert prg(b"0" * 32, i) == prg(b"0" * 32, i+1)[:i]
    """
    if not isinstance(seed, bytes):
        raise ValueError("Seed is not a byte sequence")
    if len(seed) != 32:
        raise ValueError(f"Seed has length {len(seed)}. It should be 32.")
    n_blocks = int(n / 16) + 1
    # not a real nonce because we want a stream cipher
    nonce = b"0" * 4 * 3
    return bytes().join(
        ChaCha20State.get_block(seed, i, nonce) for i in range(n_blocks)
    )[:n]


def random_bytes(n: int) -> bytes:
    """Generate n random bytes.

    Useful tools:
    * `random.randint`/`random.getrandbits`
    * the `bytes` constructor when given a list of numbers between 0 and 255

    >>> bytes([97, 98])
    b'ab'

    Actual tests:

    >>> 0 <= random_bytes(5)[0] < 256
    True
    >>> len(random_bytes(4))
    4
    >>> assert len(set(random_bytes(1000))) > 100
    """
    return bytes(random.getrandbits(8) for _ in range(n))


def bytes_to_bitstring(bs: bytes) -> str:
    """Return a bitstring that is equivalent to this byte-sequence.

    Each byte should be converted to an 8-bit binary string (that represents
    the binary number equal to the bytes), and those strings should be
    concatenated together.

    Thus, our bitstring is "little endian".

    To get the 8-bit binary number, try using a python format string like shown
    below:

    >>> n = 7
    >>> f'{n:b}'
    '111'
    >>> f'{n:6b}'
    '   111'
    >>> f'{n:06b}'
    '000111'

    Actual tests:

    >>> bytes_to_bitstring(b"a")
    '01100001'
    >>> bytes_to_bitstring(b"\x01\x02")
    '0000000100000010'
    >>> bytes_to_bitstring(b"\x01\x02a")
    '000000010000001001100001'
    """
    return "".join(f"{b:08b}" for b in bs)


def bitstring_to_bytes(bits: str) -> bytes:
    """Return a byte sequence that is equivalent to this bitstring.

    This should be an inverse function for bytes_to_bitstring.

    Each 8-bit binary sub-string should be converted to a number, and these
    numbers give the bytes.

    Useful tools:

    >>> int('11', 2)
    3
    >>> int('1001', 2)
    9
    >>> int('00001111', 2)
    15

    Actual tests:

    >>> bitstring_to_bytes(bytes_to_bitstring(b'a'))
    b'a'
    >>> bitstring_to_bytes(bytes_to_bitstring(b'ab'))
    b'ab'
    >>> bitstring_to_bytes('0111100101101111011101010010000001100111011011110111010000100000011010010111010000100001')
    b'you got it!'
    """
    assert len(bits) % 8 == 0
    return bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8))


def xor(bit0: str, bit1: str) -> str:
    """Given two bits (as strings), compute the xor:

    >>> xor('0', '0')
    '0'
    >>> xor('0', '1')
    '1'
    >>> xor('1', '0')
    '1'
    >>> xor('1', '1')
    '0'
    """
    assert bit0 in "01"
    assert bit1 in "01"
    return str(int(bit0) ^ int(bit1))


def bitstring_xor(bits0: str, bits1: str) -> str:
    """Given two bitstrings of equal length, compute the bit-wise xor (also a bitstring).

    >>> bitstring_xor('0', '0')
    '0'
    >>> bitstring_xor('0011', '0101')
    '0110'
    """
    assert all(b in "01" for b in bits0)
    assert all(b in "01" for b in bits1)
    return "".join(xor(a, b) for a, b in zip(bits0, bits1))


def one_time_pad_encrypt(msg: bytes, key: bytes) -> bytes:
    """Encrypt the msg using a one-time-pad with this key.

    Recall: the idea is to XOR the msg and key together...

    >>> one_time_pad_encrypt(b'hi', bytes([0, 0]))
    b'hi'
    >>> one_time_pad_encrypt(b'hi', b'\x50\x78') == b'8\x11'
    True
    >>> one_time_pad_encrypt(b'wow!', b'98sd') == b'NW\x04E'
    True
    """
    assert len(msg) == len(key)
    return bitstring_to_bytes(
        bitstring_xor(bytes_to_bitstring(msg), bytes_to_bitstring(key))
    )


def one_time_pad_decrypt(ct: bytes, key: bytes) -> bytes:
    """Decrypt the ciphertext using key.

    >>> k = random_bytes(5)
    >>> one_time_pad_decrypt(one_time_pad_encrypt(b"what!", k), k)
    b'what!'
    >>> k = random_bytes(9)
    >>> one_time_pad_decrypt(one_time_pad_encrypt(b"roundtrip", k), k)
    b'roundtrip'
    >>> k = random_bytes(15)
    >>> one_time_pad_decrypt(one_time_pad_encrypt(b"cancer symptoms", k), k)
    b'cancer symptoms'
    """
    assert len(ct) == len(key)
    return one_time_pad_encrypt(ct, key)


def stream_cipher_encrypt(msg: bytes, key: bytes) -> bytes:
    r"""Encrypt the msg using a one-time-pad with this key.

    Recall: the idea is to use `prg` to expand the key into a one-time
    pad key. You must use the first `len(msg)` bytes from the PRG for the test
    below to pass.

    >>> stream_cipher_encrypt(b'hi', b"0" * 32)
    b'<a'
    """
    assert len(key) == 32
    otp = prg(key, len(msg))
    return one_time_pad_encrypt(msg, otp)


def stream_cipher_decrypt(ct: bytes, key: bytes) -> bytes:
    r"""Decrypt the ciphertext using key.

    >>> k = random_bytes(32)
    >>> stream_cipher_decrypt(stream_cipher_encrypt(b"what!", k), k)
    b'what!'
    >>> k = random_bytes(32)
    >>> stream_cipher_decrypt(stream_cipher_encrypt(b"roundtrip", k), k)
    b'roundtrip'
    >>> k = random_bytes(32)
    >>> stream_cipher_decrypt(stream_cipher_encrypt(b"cancer symptoms", k), k)
    b'cancer symptoms'
    """
    assert len(key) == 32
    otp = prg(key, len(ct))
    return one_time_pad_decrypt(ct, otp)


def pad_with_length(data: bytes) -> bytes:
    r"""this function
    (1) adds 0 bytes to the end of `data` until its length is a multiple of 32.
    (2) formats the *original* length of `data` as a 256-bit binary string (use a format string)
    (3) converts that binary string to 32 bytes (use `bitstring_to_bytes`)
    (4) adds those to `data` too
    (5) returns the result.

    >>> pad_with_length(b'')
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    >>> pad_with_length(b'1')
    b'1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    >>> pad_with_length(b'1'*32)
    b'11111111111111111111111111111111\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 '
    """
    n = len(data)
    while len(data) % 32 != 0:
        data += b"\x00"
    data += bitstring_to_bytes(f"{n:0256b}")
    return data


def daisy_chain_hash(data: bytes) -> bytes:
    r"""do a daisy-chain hash.

    use `compress`.

    pseudo-code:

        function DaisyChainHash(data):
            data = pad_with_length(data)
            accumulator = 32 zero bytes
            for block in (data as 32-byte blocks):
                accumulator = compression(accumulator, block)
            return accumulator

    >>> daisy_chain_hash(b'')
    b"\xf5\xa5\xfdB\xd1j 0'\x98\xefn\xd3\t\x97\x9bC\x00=# \xd9\xf0\xe8\xea\x981\xa9'Y\xfbK"
    >>> daisy_chain_hash(b'hi there')
    b'\xc0|\xe1\xea\xa8\xbf\xbf\x0b\xa2\xce@\n`bw\x19{\xbe*O0\xb9Y\xaa\xe8u\x88\xc3\x81X\xb1\xa1'
    """

    a = b"\x00" * 32
    data = pad_with_length(data)
    for i in range(0, len(data), 32):
        a = compress(a, data[i : i + 32])
    return a


def diffie_hellman_key_gen() -> Tuple[int, Ed25519]:
    """
    Generate a Diffie-Hellman secret-key, public-key pair.
    The secret key (sk) is a random integer from {0, 1, ..., order-1}.
    The public key (pk) is the group generator raised to sk.

    Tests:
    The generator ** sk should be pk:
    >>> sk, pk = diffie_hellman_key_gen()
    >>> Ed25519.generator() ** sk == pk
    True
    100 runs should give 100 different secret keys:
    >>> len(set(diffie_hellman_key_gen()[0] for _ in range(100)))
    100
    """
    sk = randint(0, Ed25519.order - 1)
    pk = Ed25519.generator() ** sk
    return (sk, pk)


def diffie_hellman_derive_shared(sk: int, pk: Ed25519) -> bytes:
    r"""
    Generate a Diffie-Hellman shared key from your sk and their pk.
    This should be done by
    1. using Diffie-Hellman to derive a shared *group* element,
    2. convering that element to bytes using `Ed25519.to_bytes` and then
    3. hashing those bytes using `daisy_chain_hash`

    Tests:
    >>> sk1, pk1 = diffie_hellman_key_gen()
    >>> sk2, pk2 = diffie_hellman_key_gen()
    >>> k1 = diffie_hellman_derive_shared(sk1, pk2)
    >>> k2 = diffie_hellman_derive_shared(sk2, pk1)
    >>> k1 == k2
    True
    >>> daisy_chain_hash(Ed25519.identity().to_bytes())
    b'd\xc7T\xdd\x0e\xbf\xb4\xe6F\xd9\xa8\xac\x16\xa0\xbf\x1d\x15{*)\xaa\x19\xb1\x17\x03vs\xcb\x07\x9e\xbaQ'
    >>> diffie_hellman_derive_shared(0, Ed25519.generator())
    b'd\xc7T\xdd\x0e\xbf\xb4\xe6F\xd9\xa8\xac\x16\xa0\xbf\x1d\x15{*)\xaa\x19\xb1\x17\x03vs\xcb\x07\x9e\xbaQ'
    """
    return daisy_chain_hash((pk**sk).to_bytes())


def public_key_encrypt(pk: Ed25519, m: bytes) -> Tuple[Ed25519, bytes]:
    """Perform a Diffie-Hellman-based public key encryption.
    See the notes for the algorithm to implement.

    Use:
        * `Ed25519`
        * `daisy_chain_hash`
        * `stream_cipher_encrypt`

    Since encryption is randomized, different encryptions of the same message
    aren't equal!
    >>> sk, pk = diffie_hellman_key_gen()
    >>> public_key_encrypt(pk, b'hi') == public_key_encrypt(pk, b'hi')
    False
    It's hard to test this function any further on its own. One you've
    implemented `public_key_dec`, run its tests.
    """
    x = randint(0, Ed25519.order - 1)
    k = daisy_chain_hash((pk**x).to_bytes())
    c = stream_cipher_encrypt(m, k)
    return (Ed25519.generator() ** x, c)


def public_key_decrypt(sk: int, ct: Tuple[Ed25519, bytes]) -> bytes:
    """Perform a Diffie-Hellman-based public key decryption.

    See the notes for the algorithm to implement.

    Use:
        * `daisy_chain_hash`
        * `stream_cipher_decrypt`

    Testing and encryption and decryption:

    >>> sk, pk = diffie_hellman_key_gen()
    >>> ct = public_key_encrypt(pk, b'test message')
    >>> public_key_decrypt(sk, ct)
    b'test message'

    """
    pk, c = ct
    k = daisy_chain_hash((pk**sk).to_bytes())
    m = stream_cipher_decrypt(c, k)
    return m


def hash_to_ed25519_exp(i: bytes):
    """
    Hash some bytes to the set {0, 1, ..., Ed25519.order - 1}.

    You should do this by:
        * hashing the bytes using `daisy_chain_hash`
        * turning them into a bit-string using `bytes_to_bitstring`
        * parsing the bitstring as a binary number using `int(..., 2)`
        * wrapping that number modulo `Ed25519.order`.

    >>> hash_to_ed25519_exp(b"")
    2554841951840909954615001403685847680091511646998319114990040052939481059432
    >>> hash_to_ed25519_exp(b"ok")
    1763860046563134991747666434043362542916729735611754082581760026286200666356
    """
    return (
        int(bytes_to_bitstring(daisy_chain_hash(i)), 2)
        % Ed25519.order
    )


def schnorr_sign(msg: bytes, sk: int) -> Tuple[Ed25519, int]:
    """Sign a message using a schnorr signature.

    >>> sk, pk = diffie_hellman_key_gen()
    >>> R, z = schnorr_sign(b"ok", sk)
    >>> 0 <= z < Ed25519.order
    True
    """
    assert isinstance(sk, int)
    assert isinstance(msg, bytes)
    r = randint(0, Ed25519.order - 1)
    pk = Ed25519.generator() ** sk
    R = Ed25519.generator() ** r
    x = hash_to_ed25519_exp(msg + pk.to_bytes() + R.to_bytes())
    z = (sk * x + r) % Ed25519.order
    return (R, z)


def schnorr_verify(msg: bytes, pk: Ed25519, sig: Tuple[Ed25519, int]) -> bool:
    """
    >>> sk, pk = diffie_hellman_key_gen()
    >>> sig = schnorr_sign(b"ok", sk)
    >>> schnorr_verify(b"ok", pk, sig)
    True
    >>> schnorr_verify(b"o", pk, sig)
    False
    >>> schnorr_verify(b"ok", Ed25519.generator(), sig)
    False
    """
    assert isinstance(pk, Ed25519)
    R, z = sig
    x = hash_to_ed25519_exp(msg + pk.to_bytes() + R.to_bytes())
    return pk**x * R == Ed25519.generator() ** z


class Cryptography(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key_storage = {}
        
    @commands.command()
    async def keygen(self, ctx):
        sender = ctx.author
        keys = diffie_hellman_key_gen()
        #sk = keys[0]
        #pk = keys[1]
        self.key_storage[sender] = keys
        await ctx.send("Keys generated!")
    
    @app_commands.command(name = "encrypt", description = "Encrypt a message to send to someone!")
    async def encrypt(self, interaction: discord.Interaction, message: str, recipient: discord.Member):
        sender = interaction.user
        print(f'{sender} used encrypt')
        mykeys = self.key_storage[sender]
        theirkeys = self.key_storage[recipient]
        mysk = mykeys[0]
        theirpk = theirkeys[1]
        #sharedkey = diffie_hellman_derive_shared(mysk, theirpk)
        messagebytes = message.encode()
        ct = public_key_encrypt(theirpk, messagebytes)[1]
        ctstr = ct.decode()
        await interaction.response.send_message(f'{ctstr} is your ciphertext. Paste it into a channel for {recipient} to decrypt!', ephemeral=True)
      
    @app_commands.command(name = "decrypt", description = "Decrypt a message that send to someone!")
    async def decrypt(self, interaction: discord.Interaction, message: str):
        sender = interaction.user
        print(f'{sender} used decrypt')
        await interaction.response.send_message(f'Sender said {message} to you', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Cryptography(bot))

"""
The customised implementation of Keccak hash
TODO: Add comments
"""

from __future__ import annotations
import math
import operator
import copy
import functools
from typing import Callable, List


# fmt: off
RoundConstants = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
]

RotationConstants = [
    [0, 1, 62, 28, 27,],
    [36, 44, 6, 55, 20,],
    [3, 10, 43, 25, 39,],
    [41, 45, 15, 21, 8,],
    [18, 2, 61, 56, 14,]
]
# fmt: on


# 0000
# 0001
# 0011
# ...
Masks = [(1 << i) - 1 for i in range(65)]


def how_many_bytes(bits: int) -> int:
    """
    how_many_bytes calculates how many bytes are needed to to hold the given number of bits
    E.g.
    => how_many_bytes(bits=0) == 0
    => how_many_bytes(bits=8) == 1
    => how_many_bytes(bits=9) == 2

    Args:
        bits (int): The number of bits

    Returns:
        int: The number of bytes
    """
    return (bits + 7) // 8


def rol(value: int, left: int, bits: int) -> int:
    """
    rol is the bitwise operation that rotates the given value left
    E.g.
    rol(3, 1, 4)
    => Rotate "0011" (the 4-bit binary representation of 3) left by 1 bit
    => The result is "0110" (6 in decimal)

    Args:
        value (int): The value to rotate
        left (int): The number of bits to rotate
        bits (int): The total bits of the number

    Returns:
        int: The result of rotating
    """
    top = value >> (bits - left)
    bot = (value & Masks[bits - left]) << left
    return bot | top


def ror(value: int, right: int, bits: int) -> int:
    """
    ror is the bitwise operation that rotates the given value right
    E.g.
    ror(3, 1, 4)
    => Rotate "0011" (the 4-bit binary representation of 3) right by 1 bit
    => The result is "1001" (9 in decimal)

    Args:
        value (int): The value to rotate
        right (int): The number of bits to rotate
        bits (int): The total bits of the number

    Returns:
        int: The result of rotating
    """
    top = value >> right
    bot = (value & Masks[right]) << (bits - right)
    return bot | top


def multirate_padding(used_bytes: int, align_bytes: int):
    padlen = align_bytes - used_bytes
    if padlen == 0:
        padlen = align_bytes
    # note: padding done in 'internal bit ordering', wherein LSB is leftmost
    if padlen == 1:
        return [0x81]
    return [0x01] + ([0x00] * (int(padlen) - 2)) + [0x80]  # int() can be removed?


def keccak_f(state: KeccakState) -> None:
    def my_round(A, RC):
        W, H = state.W, state.H
        rangeW, rangeH = state.rangeW, state.rangeH
        lanew = state.lanew
        zero = state.zero

        # theta
        C = [functools.reduce(operator.xor, A[x]) for x in rangeW]
        D = [0] * W
        for x in rangeW:
            D[x] = C[(x - 1) % W] ^ rol(C[(x + 1) % W], 1, lanew)
            for y in rangeH:
                A[x][y] ^= D[x]

        # rho and pi
        B = zero()
        for x in rangeW:
            for y in rangeH:
                B[y % W][(2 * x + 3 * y) % H] = rol(
                    A[x][y], RotationConstants[y][x], lanew
                )

        # chi
        for x in rangeW:
            for y in rangeH:
                A[x][y] = B[x][y] ^ ((~B[(x + 1) % W][y]) & B[(x + 2) % W][y])

        # iota
        A[0][0] ^= RC

    l = int(math.log(state.lanew, 2))
    nr = 12 + 2 * l

    for ir in range(nr):
        my_round(state.s, RoundConstants[ir])


class KeccakState:
    W = 5
    H = 5

    # TODO: to be removed
    rangeW = range(W)
    rangeH = range(H)

    def __init__(self, bitrate: int, b: int) -> None:
        self.bitrate = bitrate
        self.b = b

        # only byte-aligned
        assert self.bitrate % 8 == 0
        self.bitrate_bytes = how_many_bytes(self.bitrate)

        assert self.b % 25 == 0
        self.lanew = self.b // 25

        self.s = self.zero()

    @classmethod
    def zero(cls) -> KeccakState:
        """
        zero returns a H * W 2d list

        Returns:
            [type]: [description]
        """
        return [[0] * cls.W for _ in range(cls.H)]

    @classmethod
    def format(cls, st: List[List[int]]):
        """
        format formats the given 2d list to a string

        Args:
            st (List[List[int]]): [description]

        Returns:
            [type]: [description]
        """
        rows = []

        def fmt(x: int) -> str:
            """
            # TODO:
            Finish comment
            E.g.
            >>> "%016x" % 4
            '0000000000000004'
            >>> "%016x" % 100
            '0000000000000064'
            Args:
                x ([type]): [description]

            Returns:
                [type]: [description]
            """
            return f"{x:016x}"

        for y in range(cls.H):
            row = []
            for x in range(cls.W):
                row.append(fmt(st[x][y]))
            rows.append(" ".join(row))
        return "\n".join(rows)

    @staticmethod
    def lane2bytes(s, w):
        o = []
        for b in range(0, w, 8):
            o.append((s >> b) & 0xFF)
        return o

    @staticmethod
    def bytes2lane(bb):
        r = 0
        for b in reversed(bb):
            r = r << 8 | b
        return r

    def __str__(self):
        return KeccakState.format(self.s)

    def absorb(self, bb):
        assert len(bb) == self.bitrate_bytes

        bb += [0] * int(how_many_bytes(self.b - self.bitrate))
        i = 0

        for y in self.rangeH:
            for x in self.rangeW:
                self.s[x][y] ^= KeccakState.bytes2lane(bb[i : i + 8])
                i += 8

    def squeeze(self):
        return self.get_bytes()[: self.bitrate_bytes]

    def get_bytes(self):
        out = [0] * int(how_many_bytes(self.b))
        i = 0
        for y in self.rangeH:
            for x in self.rangeW:
                v = KeccakState.lane2bytes(self.s[x][y], self.lanew)
                out[i : i + 8] = v
                i += 8
        return out

    def set_bytes(self, bb):
        i = 0
        for y in self.rangeH:
            for x in self.rangeW:
                self.s[x][y] = KeccakState.bytes2lane(bb[i : i + 8])
                i += 8


class KeccakSponge:
    def __init__(
        self,
        bitrate: int,
        width: int,
        padfn: Callable[[int, int], List[int]],
        permfn: Callable[["KeccakState"], None],
    ):
        """
        Args:
            bitrate (int): The bit rate
            width (int): The width
            padfn ([type]): The padding function
            permfn ([type]): The permutation function
        """
        self.state = KeccakState(bitrate, width)
        self.padfn = padfn
        self.permfn = permfn
        self.buffer = []

    def copy(self) -> KeccakSponge:
        return copy.deepcopy(self)

    def absorb_block(self, bb):
        self.state.bitrate_bytes = int(self.state.bitrate_bytes)
        assert len(bb) == self.state.bitrate_bytes
        self.state.absorb(bb)
        self.permfn(self.state)

    def absorb(self, s: str):
        self.buffer = [c for c in s]

        while len(self.buffer) >= self.state.bitrate_bytes:
            self.absorb_block(self.buffer[: self.state.bitrate_bytes])
            self.buffer = self.buffer[self.state.bitrate_bytes :]

    def absorb_final(self):
        padded = self.buffer + self.padfn(len(self.buffer), self.state.bitrate_bytes)
        self.absorb_block(padded)
        self.buffer = []

    def squeeze_once(self):
        rc = self.state.squeeze()
        self.permfn(self.state)
        return rc

    def squeeze(self, l):
        Z = self.squeeze_once()
        while len(Z) < l:
            Z += self.squeeze_once()
        return Z[: int(l)]


class KeccakHash:
    def __init__(self) -> None:
        bitrate_bits = 1088
        capacity_bits = 512
        output_bits = 256
        self.sponge = KeccakSponge(
            bitrate=bitrate_bits,
            width=(bitrate_bits + capacity_bits),
            padfn=multirate_padding,
            permfn=keccak_f,
            # bitrate_bits, bitrate_bits + capacity_bits, multirate_padding, keccak_f
        )
        self.digest_size = how_many_bytes(output_bits)
        self.block_size = how_many_bytes(bitrate_bits)

    def __repr__(self):
        inf = (
            self.sponge.state.bitrate,
            self.sponge.state.b - self.sponge.state.bitrate,
            self.digest_size * 8,
        )
        return "<KeccakHash with r=%d, c=%d, image=%d>" % inf

    # s can be bytes
    def digest(self, s) -> bytes:
        self.sponge.absorb(s)
        finalised = self.sponge.copy()
        finalised.absorb_final()
        digest = finalised.squeeze(self.digest_size)
        return bytes(digest)


keccak256 = KeccakHash()

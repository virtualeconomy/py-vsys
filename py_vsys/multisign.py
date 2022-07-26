"""
multisign contains the multisign logics.
For example usage, see test/test_multisign.py
"""

import hashlib
import functools
from typing import Tuple, List


BASE_FIELD_Z_P = 2**255 - 19


def modp_inv(x: int) -> int:
    return pow(x, BASE_FIELD_Z_P - 2, BASE_FIELD_Z_P)


CURVE_CONST_D = -121665 * modp_inv(121666) % BASE_FIELD_Z_P
GROUP_ORDER_Q = 2**252 + 27742317777372353535851937790883648493


def sha512(s):
    return hashlib.sha512(s).digest()


def sha512_modq(s: bytes) -> int:
    return int.from_bytes(sha512(s), "little") % GROUP_ORDER_Q


def sha512_modp(s: bytes) -> int:
    return int.from_bytes(sha512(s), "little") % BASE_FIELD_Z_P


# "Point" is represented as a 4-element-tuple for performance purposes.
Point = Tuple[int, int, int, int]


def point_add(P: "Point", Q: "Point") -> "Point":
    PX, PY, PZ, PT = P
    QX, QY, QZ, QT = Q

    A = (PY - PX) * (QY - QX) % BASE_FIELD_Z_P
    B = (PY + PX) * (QY + QX) % BASE_FIELD_Z_P

    C = 2 * PT * QT * CURVE_CONST_D % BASE_FIELD_Z_P
    D = 2 * PZ * QZ % BASE_FIELD_Z_P
    E = B - A
    F = D - C
    G = D + C
    H = B + A
    
    return (E * F, G * H, F * G, E * H)


def point_mul(s: int, P: "Point") -> "Point":
    Q = (0, 1, 1, 0)  # Neutral element
    while s > 0:
        if s & 1:
            Q = point_add(Q, P)
        P = point_add(P, P)
        s >>= 1
    return Q


def point_equals(P: "Point", Q: "Point") -> bool:
    PX, PY, PZ, PT = P
    QX, QY, QZ, QT = Q

    if (PX * QZ - QX * PZ) % BASE_FIELD_Z_P != 0:
        return False
    if (PY * QZ - QY * PZ) % BASE_FIELD_Z_P != 0:
        return False
    return True


def point_compress(P: "Point") -> bytes:
    PX, PY, PZ, PT = P
    zinv = modp_inv(PZ)
    x = PX * zinv % BASE_FIELD_Z_P
    y = PY * zinv % BASE_FIELD_Z_P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def point_decompress(b: bytes) -> "Point":
    if len(b) != 32:
        raise ValueError("Invalid input length for decompression")
    y = int.from_bytes(b, "little") 
    sign = y >> 255
    y &= (1 << 255) - 1

    x = point_recover_x(y, sign)
    return (
        x,
        y,
        1,
        (x * y) % BASE_FIELD_Z_P,
    )


def point_to_pub_key(P: "Point") -> bytes:
    PX, PY, PZ, PT = P
    zinv = modp_inv(PY)
    x = 0 * zinv % BASE_FIELD_Z_P
    y = PY * zinv % BASE_FIELD_Z_P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def point_recover_x(y: int, sign: int) -> int:
    """
    Compute corresponding x-coordinate, with low bit corresponding to
    sign, or raise ValueError on failure.
    """
    if y >= BASE_FIELD_Z_P:
        raise ValueError("Invalid y")

    x2 = (y * y - 1) * modp_inv(CURVE_CONST_D * y * y + 1)
    if x2 == 0:
        if sign:
            raise ValueError("Invalid x2 & sign")
        return 0
    
    # square root of -1 that mod 
    modp_sqrt_m1 = pow(2, (BASE_FIELD_Z_P - 1) // 4, BASE_FIELD_Z_P)

    x = pow(x2, (BASE_FIELD_Z_P + 3) // 8, BASE_FIELD_Z_P)
    if (x * x - x2) % BASE_FIELD_Z_P != 0:
        x = x * modp_sqrt_m1 % BASE_FIELD_Z_P

    if (x * x - x2) % BASE_FIELD_Z_P != 0:
        raise ValueError("Invalid x")
    
    if (x & 1) != sign:
        x = BASE_FIELD_Z_P - x
    
    return x


gy = 4 * modp_inv(5) % BASE_FIELD_Z_P
gx = point_recover_x(gy, 0)

G = (
    gx,
    gy,
    1,
    gx * gy % BASE_FIELD_Z_P,
)


class MultiSignPriKey:
    """
    MultiSignPriKey is the private key used by one party participated into the multi-sign procedure.
    """
    def __init__(self, pri_key: bytes) -> None:
        """
        Args:
            pri_key (bytes): The private key in bytes.
        """
        self.pri_key = pri_key
        self.a = self.get_a()
        self.A = self.get_A()
        self.pub_key = self.get_pub_key()

    def get_a(self) -> int:
        """
        a returns the variable a used in XEdDSA calculation. 
        """
        return int.from_bytes(self.pri_key, "little")
    
    def get_A(self) -> bytes:
        """
        A returns the variable A used in XEdDSA calculation.
        """
        return point_compress(point_mul(self.a, G))

    def get_pub_key(self) -> bytes:
        """
        pub_key returns the public key of the private key.
        """
        if (len(self.pri_key) != 32):
            raise ValueError("Bad size of private key")
        h = sha512(self.pri_key)
        a = int.from_bytes(h[:32], "little")
        a &= (1 << 254) - 8
        a |= (1 << 254)
        return point_compress(point_mul(a, G))

    def get_r(self, msg: bytes, rand: bytes) -> int:
        """
        get_r returns the variable r used in the XEdDSA calculation.

        Args:
            msg (bytes): The message to sign.
            rand (bytes): The 64-byte random bytes.
        
        Returns:
            int: The variable r.
        """
        prefix = 0xFE
        for _ in range(0, 31):
            prefix *= 256
            prefix += 0xFF
        prefix = int.to_bytes(prefix, 32, "big")
        return sha512_modq(prefix + self.pri_key + msg + rand)
    
    def get_R(self, msg: bytes, rand: bytes) -> "Point":
        """
        get_R returns the variable R used in XEdDSA calculation.

        Args:
            msg (bytes): The message to sign.
            rand (bytes): The 64-byte random bytes.
        
        Returns:
            Point: The variable R.
        """
        r = self.get_r(msg, rand)
        return point_mul(r, G)

    def get_x(self, *allAs: Tuple[bytes]) -> int:
        """
        get_x returns the variable x used in XEdDSA calculation.

        Args:
            allAs (Tuple[bytes]): A tuple of variable A of all MultiSignPriKey participated into the multisign procedure.
        
        Returns:
            int: The variable x.
        """
        if len(allAs) == 1:
            return 1

        prefix = 0xFD
        for _ in range(0, 31):
            prefix *= 256
            prefix += 0xFF
        prefix = int.to_bytes(prefix, 32, 'big')

        A = self.A
        b = prefix + A

        for Ai in allAs:
            b += Ai
        
        return sha512_modq(b)
    
    def get_bpA(self, *allAs: Tuple[bytes]) -> "Point":
        """
        get_bpA returns the variable point_mul((x * a) % GROUP_ORDER_Q, G)

        Args:
            allAs (Tuple[bytes]): A tuple of variable A of all MultiSignPriKey participated into the multisign procedure.
        
        Returns:
            Point: The variable bpA.
        """
        x = self.get_x(*allAs)
        return point_mul((x * self.a) % GROUP_ORDER_Q, G)

    def get_xA(self, *allAs: Tuple[bytes]) -> "Point":
        """
        get_xA returns the variable point_mul((x * a), G)

        Args:
            allAs (Tuple[bytes]): A tuple of variable A of all MultiSignPriKey participated into the multisign procedure.
        
        Returns:
            Point: The variable xA.
        """
        x = self.get_x(*allAs)
        return point_mul((x * self.a), G)

    def sign(self, msg: bytes, rand: bytes, unionA: bytes, unionR: "Point", allAs: Tuple[bytes]) -> int:
        """
        sign produces the sub-signature that can be used to compose the multi-signature.

        Args:
            msg (bytes): The message to sign.
            rand (bytes): The 64-byte random bytes.
            unionA (bytes): The union of a collection of variable xA.
            unionR (Point): The union of a collection of variable R.
            allAs (Tuple[bytes]): A tuple of variable A of all MultiSignPriKey participated into the multisign procedure.
        
        Returns:
            Point: The variable bpA.
        """
        r = self.get_r(msg, rand)
        x = self.get_x(*allAs)
        a = self.a
        h = sha512_modq(point_compress(unionR) + unionA + msg)
        return (r + (h * x * a) % GROUP_ORDER_Q) % GROUP_ORDER_Q


class MultiSign:
    """
    MultiSign is the multisign controller.
    """

    @staticmethod
    def get_unionA(*xAs: Tuple["Point"]) -> bytes:
        """
        get_unionA returns the union of a collection of variable xA.

        Args:
            xAs (Tuple[Point]): A tuple of variable xA of all MultiSignPriKey participated into the multisign procedure.
        
        Returns:
            bytes: The unionA.
        """
        return point_compress(
            functools.reduce(lambda a, b: point_add(a, b), xAs)
        )

    @staticmethod
    def get_unionR(*Rs: Tuple["Point"]) -> "Point":
        """
        get_unionR returns the union of a collection of R.

        Args:
            Rs (Tuple[Point]): A tuple of variable R of all MultiSignPriKey participated into the multisign procedure.
        
        Returns:
            Point: The unionR.
        """
        return functools.reduce(lambda a, b: point_add(a, b), Rs) 

    @staticmethod 
    def _transfer_sig(sig: int, A: bytes) -> List[int]:
        """
        _transfer_sig transfers the given signature.

        Args:
            sig (int): The signature to transfer.
            A (int): The variable A.

        Returns:
            List[int]: The transferred signature.
        """
        sl = list(int.to_bytes(sig, 32, "little"))
        sl[31] = (sl[31] & 0x7F) | (A[31] & 0x80)
        return sl 
    
    @staticmethod
    def get_sig(unionA: bytes, unionR: "Point", sigs: Tuple[int]) -> bytes:
        """
        get_sig composes the multisign signature from the sub-signatures.

        Args:
            unionA (bytes): The union of a collection of variable xA.
            unionR (Point): The union of a collection of variable R.
            sigs (Tuple[int]): Sub-signatures to compose the multisign signature.

        Returns:
            bytes: The multisign signature.
        """
        s = sum(sigs) % GROUP_ORDER_Q
        return point_compress(unionR) + bytes(MultiSign._transfer_sig(s, unionA))

    @staticmethod
    def get_pub(*bpAs: Tuple["Point"]) -> bytes:
        """
        get_pub returns the multisign publc key for the multisign signature.

        Args:
            bpAs (Tuple[Point]): A tuple of variable bpA of all MultiSignPriKey participated into the multisign procedure.
        
        Returns:
            bytes: The public key.
        """
        p = functools.reduce(lambda a, b: point_add(a, b), bpAs)

        zinv = modp_inv(p[2])
        py = p[1] * zinv % BASE_FIELD_Z_P

        return int.to_bytes((py + 1) * modp_inv(1  - py) % BASE_FIELD_Z_P, 32, 'little')


if __name__ == '__main__':
    import base58
    pks = "EV9ADJzYKZpk4MjxEkXxDSfRRSzBFnA9LEQNbepKZRFc"
    pk = base58.b58decode(pks)

    msp = MultiSignPriKey(pk)
    print(msp.a)
    print(list(msp.A))
    print(list(msp.pub_key))
    pass
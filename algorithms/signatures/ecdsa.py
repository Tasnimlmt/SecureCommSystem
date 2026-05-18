



"""
ECDSA (Elliptic Curve Digital Signature Algorithm)
Signs and verifies messages using elliptic curve cryptography.
Used in Bitcoin, Ethereum, TLS certificates.
"""
import hashlib
import random


class ECDSASignature:
    # secp256k1 parameters
    P  = 2**256 - 2**32 - 977
    A  = 0
    B  = 7
    GX = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    GY = 32670510020758816978083085130507043184471273380659243275938904335757337482424
    N  = 115792089237316195423570985008687907852837564279074904382605163141518161494337
    G  = (GX, GY)

    @classmethod
    def _point_add(cls, P_pt, Q_pt):
        p = cls.P
        if P_pt is None:
            return Q_pt
        if Q_pt is None:
            return P_pt
        x1, y1 = P_pt
        x2, y2 = Q_pt
        if x1 == x2 and (y1 + y2) % p == 0:
            return None
        if P_pt == Q_pt:
            slope = (3 * x1 * x1 + cls.A) * pow(2 * y1, -1, p) % p
        else:
            slope = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (slope * slope - x1 - x2) % p
        y3 = (slope * (x1 - x3) - y1) % p
        return x3, y3

    @classmethod
    def _scalar_mult(cls, k, point):
        result = None
        addend = point
        while k:
            if k & 1:
                result = cls._point_add(result, addend)
            addend = cls._point_add(addend, addend)
            k >>= 1
        return result

    @classmethod
    def generate_keypair(cls):
        """Generate ECDSA private/public key pair."""
        private = random.randint(1, cls.N - 1)
        public = cls._scalar_mult(private, cls.G)
        return private, public

    @classmethod
    def sign(cls, message: str, private_key: int) -> tuple:
        """
        Sign a message. Returns (r, s) signature pair.
        """
        if not message:
            raise ValueError("Message cannot be empty")
        z = int(hashlib.sha256(message.encode()).hexdigest(), 16)
        r = s = 0
        while r == 0 or s == 0:
            k = random.randint(1, cls.N - 1)
            point = cls._scalar_mult(k, cls.G)
            r = point[0] % cls.N
            if r == 0:
                continue
            k_inv = pow(k, -1, cls.N)
            s = (k_inv * (z + r * private_key)) % cls.N
        return r, s

    @classmethod
    def verify(cls, message: str, signature: tuple, public_key: tuple) -> bool:
        """Verify an ECDSA signature. Returns True if valid."""
        if not message:
            raise ValueError("Message cannot be empty")
        r, s = signature
        if not (1 <= r < cls.N and 1 <= s < cls.N):
            return False
        z = int(hashlib.sha256(message.encode()).hexdigest(), 16)
        w = pow(s, -1, cls.N)
        u1 = (z * w) % cls.N
        u2 = (r * w) % cls.N
        point = cls._point_add(
            cls._scalar_mult(u1, cls.G),
            cls._scalar_mult(u2, public_key)
        )
        if point is None:
            return False
        return point[0] % cls.N == r

    @staticmethod
    def get_info() -> str:
        return (
            "ECDSA (Elliptic Curve Digital Signature Algorithm)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Curve      : secp256k1 (y² = x³ + 7 mod p)\n"
            "Key size   : 256-bit private key\n"
            "Signature  : (r, s) pair – two 256-bit integers\n"
            "Security   : ECDLP (Elliptic Curve Discrete Log)\n"
            "Uses       : Bitcoin transactions, Ethereum, TLS certs\n"
            "Standard   : ANSI X9.62, FIPS 186-4"
        )
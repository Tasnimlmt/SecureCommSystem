# # # """
# # # Elliptic Curve Cryptography Implementation
# # # """
# # # from cryptography.hazmat.primitives.asymmetric import ec
# # # from cryptography.hazmat.primitives import hashes, serialization
# # # from cryptography.hazmat.primitives.kdf.hkdf import HKDF
# # # from cryptography.hazmat.backends import default_backend
# # # import base64

# # # class ECCCipher:
# # #     def __init__(self, curve='P-256'):
# # #         curves = {
# # #             'P-256': ec.SECP256R1(),
# # #             'P-384': ec.SECP384R1(),
# # #             'P-521': ec.SECP521R1()
# # #         }
# # #         self.curve = curves.get(curve, ec.SECP256R1())
# # #         self.private_key = None
# # #         self.public_key = None
    
# # #     def generate_keys(self):
# # #         """Generate ECC key pair"""
# # #         self.private_key = ec.generate_private_key(self.curve, backend=default_backend())
# # #         self.public_key = self.private_key.public_key()
# # #         return self.get_public_key_pem(), self.get_private_key_pem()
    
# # #     def get_public_key_pem(self):
# # #         return self.public_key.public_bytes(
# # #             encoding=serialization.Encoding.PEM,
# # #             format=serialization.PublicFormat.SubjectPublicKeyInfo
# # #         ).decode()
    
# # #     def get_private_key_pem(self):
# # #         return self.private_key.private_bytes(
# # #             encoding=serialization.Encoding.PEM,
# # #             format=serialization.PrivateFormat.PKCS8,
# # #             encryption_algorithm=serialization.NoEncryption()
# # #         ).decode()
    
# # #     def compute_shared_secret(self, peer_public_key_pem):
# # #         """Compute shared secret using ECDH"""
# # #         peer_key = serialization.load_pem_public_key(
# # #             peer_public_key_pem.encode(),
# # #             backend=default_backend()
# # #         )
# # #         shared_secret = self.private_key.exchange(ec.ECDH(), peer_key)
        
# # #         # Derive AES key
# # #         derived_key = HKDF(
# # #             algorithm=hashes.SHA256(),
# # #             length=32,
# # #             salt=None,
# # #             info=b'ecdh-key-derivation',
# # #             backend=default_backend()
# # #         ).derive(shared_secret)
        
# # #         return derived_key


# # import random

# # class ECCCipher:
# #     @staticmethod
# #     def get_curve():
# #         # secp256k1 (Bitcoin curve)
# #         p = 2**256 - 2**32 - 977
# #         a = 0
# #         b = 7
# #         Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
# #         Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
# #         n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
# #         return p, a, b, (Gx, Gy), n
    
# #     @staticmethod
# #     def mod_inverse(a, p):
# #         return pow(a, -1, p)
    
# #     @staticmethod
# #     def point_add(P, Q, p, a):
# #         if P is None:
# #             return Q
# #         if Q is None:
# #             return P
# #         x1, y1 = P
# #         x2, y2 = Q
# #         if x1 == x2 and y1 == y2:
# #             slope = ((3 * x1 * x1 + a) * ECCCipher.mod_inverse(2 * y1, p)) % p
# #         else:
# #             slope = ((y2 - y1) * ECCCipher.mod_inverse(x2 - x1, p)) % p
# #         x3 = (slope * slope - x1 - x2) % p
# #         y3 = (slope * (x1 - x3) - y1) % p
# #         return (x3, y3)
    
# #     @staticmethod
# #     def scalar_mult(k, P, p, a):
# #         result = None
# #         addend = P
# #         while k:
# #             if k & 1:
# #                 result = ECCCipher.point_add(result, addend, p, a)
# #             addend = ECCCipher.point_add(addend, addend, p, a)
# #             k >>= 1
# #         return result
    
# #     @staticmethod
# #     def generate_keypair():
# #         p, a, b, G, n = ECCCipher.get_curve()
# #         private = random.randint(1, n-1)
# #         public = ECCCipher.scalar_mult(private, G, p, a)
# #         return private, public


# """
# ECC — Elliptic Curve Cryptography (secp256k1)
# Asymmetric Cryptography | TP3

# Principle: Security based on the Elliptic Curve Discrete Logarithm Problem (ECDLP).
#   Given points G and Q = k·G on the curve, computing k is computationally infeasible.
#   Advantage: Same security as RSA but with much smaller keys:
#     ECC 256-bit ≈ RSA 3072-bit in security strength.

# Curve: secp256k1 (Koblitz curve — used in Bitcoin and Ethereum)
#   Equation : y² = x³ + 7 (mod p)
#   Prime p   : 2²⁵⁶ − 2³² − 977
#   Generator : G = (Gx, Gy)
#   Order n   : number of points on the curve

# Protocols implemented:
#   • Key generation (private scalar → public point)
#   • ECDH (Elliptic Curve Diffie-Hellman key exchange)
#   • ECDSA (Elliptic Curve Digital Signature Algorithm)
# """

# import hashlib
# import random
# import sympy


# class ECCPoint:
#     """A point on an elliptic curve, or the point at infinity."""

#     def __init__(self, x, y, curve=None):
#         self.x     = x
#         self.y     = y
#         self.curve = curve  # reference to curve for arithmetic

#     def is_infinity(self):
#         return self.x is None and self.y is None

#     def __eq__(self, other):
#         return self.x == other.x and self.y == other.y

#     def __repr__(self):
#         if self.is_infinity():
#             return "O (point at infinity)"
#         return f"({self.x}, {self.y})"


# class Secp256k1:
#     """
#     secp256k1 elliptic curve — the Bitcoin / Ethereum curve.
#     Equation: y² = x³ + 7 (mod p)
#     """
#     p  = 2**256 - 2**32 - 977   # prime field
#     a  = 0                       # curve parameter a
#     b  = 7                       # curve parameter b
#     Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
#     Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
#     n  = 115792089237316195423570985008687907852837564279074904382605163141518161494337

#     @classmethod
#     def G(cls) -> ECCPoint:
#         """Return the generator (base) point."""
#         return ECCPoint(cls.Gx, cls.Gy)

#     @classmethod
#     def add(cls, P: ECCPoint, Q: ECCPoint) -> ECCPoint:
#         """Add two points on the curve."""
#         INF = ECCPoint(None, None)
#         if P.is_infinity(): return Q
#         if Q.is_infinity(): return P
#         if P.x == Q.x and P.y != Q.y:
#             return INF  # P + (-P) = O
#         if P == Q:
#             if P.y == 0: return INF
#             lam = (3 * P.x**2 + cls.a) * pow(2 * P.y, -1, cls.p) % cls.p
#         else:
#             lam = (Q.y - P.y) * pow(Q.x - P.x, -1, cls.p) % cls.p
#         x3 = (lam**2 - P.x - Q.x) % cls.p
#         y3 = (lam * (P.x - x3) - P.y) % cls.p
#         return ECCPoint(x3, y3)

#     @classmethod
#     def scalar_mult(cls, k: int, P: ECCPoint) -> ECCPoint:
#         """Compute k·P using the double-and-add algorithm."""
#         result = ECCPoint(None, None)   # identity (point at infinity)
#         addend = P
#         while k:
#             if k & 1:
#                 result = cls.add(result, addend)
#             addend = cls.add(addend, addend)
#             k >>= 1
#         return result


# class ECCCipher:
#     """ECC key generation, ECDH, and ECDSA."""

#     # ── Key generation ────────────────────────────────────────────────────────

#     @staticmethod
#     def generate_keypair() -> tuple[int, ECCPoint]:
#         """
#         Generate an ECC key pair on secp256k1.

#         Returns:
#             (private_key, public_key)
#             private_key: Random integer d in [1, n-1]
#             public_key:  Point Q = d·G on the curve
#         """
#         d = random.randint(1, Secp256k1.n - 1)
#         Q = Secp256k1.scalar_mult(d, Secp256k1.G())
#         return d, Q

#     # ── ECDH ─────────────────────────────────────────────────────────────────

#     @staticmethod
#     def ecdh_shared_secret(my_private: int, their_public: ECCPoint) -> bytes:
#         """
#         Compute the ECDH shared secret.

#         Both parties arrive at the same point:
#           Alice: S = d_A · Q_B
#           Bob:   S = d_B · Q_A
#           S = d_A · d_B · G  (same for both)

#         Returns:
#             32-byte SHA-256 hash of the shared point's x-coordinate.
#         """
#         S = Secp256k1.scalar_mult(my_private, their_public)
#         return hashlib.sha256(str(S.x).encode()).digest()

#     @staticmethod
#     def simulate_ecdh() -> dict:
#         """Simulate a complete ECDH exchange between Alice and Bob."""
#         dA, QA = ECCCipher.generate_keypair()
#         dB, QB = ECCCipher.generate_keypair()
#         K_A    = ECCCipher.ecdh_shared_secret(dA, QB)
#         K_B    = ECCCipher.ecdh_shared_secret(dB, QA)
#         return {
#             "alice_private":   dA,
#             "alice_public_x":  QA.x,
#             "alice_public_y":  QA.y,
#             "bob_private":     dB,
#             "bob_public_x":    QB.x,
#             "bob_public_y":    QB.y,
#             "alice_secret":    K_A.hex(),
#             "bob_secret":      K_B.hex(),
#             "secrets_match":   K_A == K_B,
#         }

#     # ── ECDSA ─────────────────────────────────────────────────────────────────

#     @staticmethod
#     def ecdsa_sign(message: str, private_key: int) -> tuple[int, int]:
#         """
#         ECDSA signature.

#         Args:
#             message:     Message to sign
#             private_key: Signer's private key d

#         Returns:
#             Signature (r, s).
#         """
#         n    = Secp256k1.n
#         h    = int(hashlib.sha256(message.encode()).hexdigest(), 16)
#         while True:
#             k    = random.randint(1, n - 1)
#             R    = Secp256k1.scalar_mult(k, Secp256k1.G())
#             r    = R.x % n
#             if r == 0: continue
#             s    = pow(k, -1, n) * (h + private_key * r) % n
#             if s != 0: break
#         return r, s

#     @staticmethod
#     def ecdsa_verify(message: str, signature: tuple[int, int], public_key: ECCPoint) -> bool:
#         """
#         Verify an ECDSA signature.

#         Returns:
#             True if signature is valid.
#         """
#         r, s   = signature
#         n      = Secp256k1.n
#         if not (1 <= r < n and 1 <= s < n):
#             return False
#         h      = int(hashlib.sha256(message.encode()).hexdigest(), 16)
#         w      = pow(s, -1, n)
#         u1     = h * w % n
#         u2     = r * w % n
#         X      = Secp256k1.add(
#             Secp256k1.scalar_mult(u1, Secp256k1.G()),
#             Secp256k1.scalar_mult(u2, public_key),
#         )
#         return X.x % n == r


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     print("=" * 55)
#     print("ECC (secp256k1) DEMO — ECDH + ECDSA")
#     print("=" * 55)
#     print("Curve: y² = x³ + 7 (mod p)  [Bitcoin/Ethereum]")

#     print("\n── Key Generation ──")
#     d, Q = ECCCipher.generate_keypair()
#     print(f"Private key d : {d}")
#     print(f"Public key Qx : {Q.x}")
#     print(f"Public key Qy : {Q.y}")

#     print("\n── ECDH Key Exchange ──")
#     ecdh = ECCCipher.simulate_ecdh()
#     print(f"Alice secret  : {ecdh['alice_secret'][:32]}…")
#     print(f"Bob   secret  : {ecdh['bob_secret'][:32]}…")
#     print(f"Match         : {ecdh['secrets_match']}")

#     print("\n── ECDSA Signature ──")
#     msg = "Transfer 1 BTC to Alice"
#     sig = ECCCipher.ecdsa_sign(msg, d)
#     ok  = ECCCipher.ecdsa_verify(msg, sig, Q)
#     print(f"Message  : {msg}")
#     print(f"Sig (r)  : {sig[0]}")
#     print(f"Sig (s)  : {sig[1]}")
#     print(f"Valid    : {ok}")
#     bad = ECCCipher.ecdsa_verify("tampered", sig, Q)
#     print(f"Tampered : {bad}  (should be False)")


"""
ECC (Elliptic Curve Cryptography)
Uses the algebraic structure of elliptic curves over finite fields.
Implements secp256k1 (Bitcoin curve) for key generation,
and ECDH (Elliptic Curve Diffie-Hellman) for shared secret computation.
"""
import random


class ECCCipher:
    # secp256k1 curve parameters (Bitcoin / Ethereum)
    P  = 2**256 - 2**32 - 977
    A  = 0
    B  = 7
    GX = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    GY = 32670510020758816978083085130507043184471273380659243275938904335757337482424
    N  = 115792089237316195423570985008687907852837564279074904382605163141518161494337
    G  = (GX, GY)

    @staticmethod
    def _point_add(P_pt, Q_pt):
        """Add two elliptic curve points."""
        p, a = ECCCipher.P, ECCCipher.A
        if P_pt is None:
            return Q_pt
        if Q_pt is None:
            return P_pt
        x1, y1 = P_pt
        x2, y2 = Q_pt
        if x1 == x2 and (y1 + y2) % p == 0:
            return None  # Point at infinity
        if P_pt == Q_pt:
            slope = (3 * x1 * x1 + a) * pow(2 * y1, -1, p) % p
        else:
            slope = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (slope * slope - x1 - x2) % p
        y3 = (slope * (x1 - x3) - y1) % p
        return x3, y3

    @staticmethod
    def _scalar_mult(k: int, point: tuple) -> tuple:
        """Scalar multiplication: k * point using double-and-add."""
        result = None
        addend = point
        while k:
            if k & 1:
                result = ECCCipher._point_add(result, addend)
            addend = ECCCipher._point_add(addend, addend)
            k >>= 1
        return result

    @staticmethod
    def generate_keypair() -> tuple:
        """
        Generate an ECC key pair on secp256k1.
        Returns: (private_key: int, public_key: (x, y))
        """
        private = random.randint(1, ECCCipher.N - 1)
        public = ECCCipher._scalar_mult(private, ECCCipher.G)
        return private, public

    @staticmethod
    def ecdh_shared_secret(private_key: int, other_public: tuple) -> tuple:
        """
        Compute ECDH shared secret.
        Both parties compute: S = private * other_public
        Returns the shared point (x, y).
        """
        return ECCCipher._scalar_mult(private_key, other_public)

    @staticmethod
    def full_ecdh_exchange() -> dict:
        """Simulate a complete ECDH exchange between Alice and Bob."""
        a_priv, a_pub = ECCCipher.generate_keypair()
        b_priv, b_pub = ECCCipher.generate_keypair()
        S_alice = ECCCipher.ecdh_shared_secret(a_priv, b_pub)
        S_bob   = ECCCipher.ecdh_shared_secret(b_priv, a_pub)
        return {
            'alice_private': a_priv,
            'alice_public': a_pub,
            'bob_private': b_priv,
            'bob_public': b_pub,
            'shared_alice': S_alice,
            'shared_bob': S_bob,
            'match': S_alice == S_bob,
        }

    @staticmethod
    def get_info() -> str:
        return (
            "ECC – Elliptic Curve Cryptography (secp256k1)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Curve      : y² = x³ + 7  (mod p)\n"
            "Key size   : 256 bits ≈ RSA-3072 security\n"
            "Security   : Elliptic Curve Discrete Log Problem\n"
            "Uses       : Bitcoin, Ethereum, TLS 1.3, SSH\n"
            "ECDH       : Key agreement\n"
            "ECDSA      : Digital signatures"
        )
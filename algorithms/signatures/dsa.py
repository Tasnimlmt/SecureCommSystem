"""
DSA (Digital Signature Algorithm)
NIST standard for digital signatures based on discrete logarithm problem.
Similar to ElGamal signatures; standardized in FIPS 186.
"""
import hashlib
import sympy
import random


class DSASignature:
    @staticmethod
    def generate_params(bits: int = 128) -> tuple:
        """
        Generate DSA domain parameters (p, q, g).
        q is a prime, p = k*q + 1 for some k.
        """
        q = sympy.randprime(2**127, 2**128)
        # Find p = k*q + 1 such that p is prime
        p = None
        for _ in range(1000):
            k = random.randint(2, 2**4)
            candidate = k * q + 1
            if sympy.isprime(candidate):
                p = candidate
                break
        if p is None:
            # Fallback: use a simpler approach
            p = sympy.nextprime(2 * q + 1)
            while (p - 1) % q != 0:
                p = sympy.nextprime(p + 1)

        # Find generator g of order q subgroup
        h = 2
        g = pow(h, (p - 1) // q, p)
        while g == 1:
            h += 1
            g = pow(h, (p - 1) // q, p)
        return p, q, g

    @staticmethod
    def generate_keypair(p: int, q: int, g: int) -> tuple:
        """
        Generate DSA key pair given domain parameters.
        Returns: (private_key=x, public_key=y) where y = g^x mod p
        """
        x = random.randint(1, q - 1)
        y = pow(g, x, p)
        return x, y

    @staticmethod
    def sign(message: str, private_key: int, p: int, q: int, g: int) -> tuple:
        """
        Sign message. Returns (r, s) signature.
        """
        if not message:
            raise ValueError("Message cannot be empty")
        h = int(hashlib.sha256(message.encode()).hexdigest(), 16) % q
        r = s = 0
        while r == 0 or s == 0:
            k = random.randint(1, q - 1)
            r = pow(g, k, p) % q
            if r == 0:
                continue
            k_inv = pow(k, -1, q)
            s = (k_inv * (h + private_key * r)) % q
        return r, s

    @staticmethod
    def verify(message: str, signature: tuple, public_key: int,
               p: int, q: int, g: int) -> bool:
        """Verify a DSA signature."""
        if not message:
            raise ValueError("Message cannot be empty")
        r, s = signature
        if not (0 < r < q and 0 < s < q):
            return False
        h = int(hashlib.sha256(message.encode()).hexdigest(), 16) % q
        w = pow(s, -1, q)
        u1 = (h * w) % q
        u2 = (r * w) % q
        v = (pow(g, u1, p) * pow(public_key, u2, p)) % p % q
        return v == r

    @staticmethod
    def get_info() -> str:
        return (
            "DSA (Digital Signature Algorithm)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Basis      : Discrete logarithm problem\n"
            "Parameters : Prime p, prime q (q | p-1), generator g\n"
            "Signature  : (r, s) pair\n"
            "Hash used  : SHA-1 (original), SHA-256 (DSA2)\n"
            "Key sizes  : 1024/2048/3072 bits (p), 160/224/256 (q)\n"
            "Standard   : FIPS 186-4\n"
            "Note       : Only for signatures (not encryption)"
        )
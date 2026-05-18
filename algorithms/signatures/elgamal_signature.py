"""
ElGamal Digital Signature
Sign messages using ElGamal's signature scheme.
Different from ElGamal encryption; based on discrete logarithm problem.
"""
import hashlib
import sympy
import random


class ElGamalSignature:
    @staticmethod
    def generate_params(bits: int = 128) -> tuple:
        """Generate ElGamal domain parameters (p, g)."""
        p = sympy.randprime(2 ** (bits - 1), 2 ** bits)
        factors = sympy.factorint(p - 1)
        g = 2
        for candidate in range(2, min(p, 200)):
            if all(pow(candidate, (p - 1) // f, p) != 1 for f in factors):
                g = candidate
                break
        return p, g

    @staticmethod
    def generate_keypair(p: int, g: int) -> tuple:
        """
        Generate key pair. Returns (private_key=x, public_key=y).
        y = g^x mod p
        """
        x = random.randint(2, p - 2)
        y = pow(g, x, p)
        return x, y

    @staticmethod
    def sign(message: str, private_key: int, p: int, g: int) -> tuple:
        """
        Sign message. Returns (r, s) pair.
        Requires k coprime to p-1.
        """
        if not message:
            raise ValueError("Message cannot be empty")
        h = int(hashlib.sha256(message.encode()).hexdigest(), 16) % p
        r = s = 0
        while r == 0 or s == 0:
            k = random.randint(2, p - 2)
            if sympy.gcd(k, p - 1) != 1:
                continue
            r = pow(g, k, p)
            k_inv = pow(k, -1, p - 1)
            s = (k_inv * (h - private_key * r)) % (p - 1)
        return r, s

    @staticmethod
    def verify(message: str, signature: tuple, public_key: int,
               p: int, g: int) -> bool:
        """Verify ElGamal signature."""
        if not message:
            raise ValueError("Message cannot be empty")
        r, s = signature
        if not (0 < r < p):
            return False
        h = int(hashlib.sha256(message.encode()).hexdigest(), 16) % p
        lhs = pow(g, h, p)
        rhs = (pow(public_key, r, p) * pow(r, s, p)) % p
        return lhs == rhs

    @staticmethod
    def get_info() -> str:
        return (
            "ElGamal Digital Signature\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Basis      : Discrete logarithm problem\n"
            "Parameters : Prime p, generator g\n"
            "Signature  : (r, s) pair\n"
            "Key reuse  : k must NEVER be reused (breaks security)\n"
            "Relation   : Basis for DSA (DSA is an optimized variant)\n"
            "Uses       : Educational; DSA preferred in practice"
        )
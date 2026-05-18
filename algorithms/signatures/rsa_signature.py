"""
RSA Digital Signature
Sign a message with a private key; verify with the public key.
Uses SHA-256 for the message digest before signing.
"""
import hashlib
import sympy
import random


class RSASignature:
    @staticmethod
    def _generate_prime(bits: int = 256) -> int:
        return sympy.randprime(2 ** (bits - 1), 2 ** bits)

    @staticmethod
    def _mod_inverse(a: int, m: int) -> int:
        return pow(a, -1, m)

    @staticmethod
    def generate_keypair(bits: int = 256) -> tuple:
        """Generate RSA key pair for signing. Returns (public, private)."""
        p = RSASignature._generate_prime(bits)
        q = RSASignature._generate_prime(bits)
        while q == p:
            q = RSASignature._generate_prime(bits)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        d = RSASignature._mod_inverse(e, phi)
        return (n, e), (n, d)

    @staticmethod
    def sign(message: str, private_key: tuple) -> int:
        """
        Sign a message using RSA private key.
        Signature = H(message)^d mod n
        """
        if not message:
            raise ValueError("Message cannot be empty")
        n, d = private_key
        h = int(hashlib.sha256(message.encode()).hexdigest(), 16) % n
        return pow(h, d, n)

    @staticmethod
    def verify(message: str, signature: int, public_key: tuple) -> bool:
        """
        Verify RSA signature using public key.
        Valid if signature^e mod n == H(message)
        """
        if not message:
            raise ValueError("Message cannot be empty")
        n, e = public_key
        h_expected = int(hashlib.sha256(message.encode()).hexdigest(), 16) % n
        h_recovered = pow(signature, e, n)
        return h_expected == h_recovered

    @staticmethod
    def get_info() -> str:
        return (
            "RSA Digital Signature\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Operation  : Sign with private key, verify with public key\n"
            "Hash       : SHA-256 of message before signing\n"
            "Security   : Integer factorization problem\n"
            "Key sizes  : 2048–4096 bits recommended\n"
            "Standard   : PKCS#1 v1.5, RSA-PSS\n"
            "Uses       : TLS certificates, code signing, email (PGP)"
        )
# # # """
# # # RSA Cryptography Implementation
# # # """
# # # from cryptography.hazmat.primitives.asymmetric import rsa, padding
# # # from cryptography.hazmat.primitives import hashes, serialization
# # # from cryptography.hazmat.backends import default_backend
# # # import base64

# # # class RSACipher:
# # #     def __init__(self, key_size=2048):
# # #         self.key_size = key_size
# # #         self.private_key = None
# # #         self.public_key = None
    
# # #     def generate_keys(self):
# # #         """Generate RSA key pair"""
# # #         self.private_key = rsa.generate_private_key(
# # #             public_exponent=65537,
# # #             key_size=self.key_size,
# # #             backend=default_backend()
# # #         )
# # #         self.public_key = self.private_key.public_key()
# # #         return self.get_public_key_pem(), self.get_private_key_pem()
    
# # #     def get_public_key_pem(self):
# # #         """Get public key in PEM format"""
# # #         return self.public_key.public_bytes(
# # #             encoding=serialization.Encoding.PEM,
# # #             format=serialization.PublicFormat.SubjectPublicKeyInfo
# # #         ).decode()
    
# # #     def get_private_key_pem(self):
# # #         """Get private key in PEM format"""
# # #         return self.private_key.private_bytes(
# # #             encoding=serialization.Encoding.PEM,
# # #             format=serialization.PrivateFormat.PKCS8,
# # #             encryption_algorithm=serialization.NoEncryption()
# # #         ).decode()
    
# # #     def encrypt(self, message, public_key_pem=None):
# # #         """Encrypt message with RSA public key"""
# # #         if public_key_pem:
# # #             key = serialization.load_pem_public_key(public_key_pem.encode(), backend=default_backend())
# # #         else:
# # #             key = self.public_key
        
# # #         encrypted = key.encrypt(
# # #             message.encode(),
# # #             padding.OAEP(
# # #                 mgf=padding.MGF1(algorithm=hashes.SHA256()),
# # #                 algorithm=hashes.SHA256(),
# # #                 label=None
# # #             )
# # #         )
# # #         return base64.b64encode(encrypted).decode()
    
# # #     def decrypt(self, ciphertext_b64):
# # #         """Decrypt message with RSA private key"""
# # #         ciphertext = base64.b64decode(ciphertext_b64)
# # #         decrypted = self.private_key.decrypt(
# # #             ciphertext,
# # #             padding.OAEP(
# # #                 mgf=padding.MGF1(algorithm=hashes.SHA256()),
# # #                 algorithm=hashes.SHA256(),
# # #                 label=None
# # #             )
# # #         )
# # #         return decrypted.decode()


# # import sympy
# # import random

# # class RSACipher:
# #     @staticmethod
# #     def generate_prime(bits=256):
# #         return sympy.randprime(2**(bits-1), 2**bits)
    
# #     @staticmethod
# #     def extended_gcd(a, b):
# #         if a == 0:
# #             return b, 0, 1
# #         gcd, x1, y1 = RSACipher.extended_gcd(b % a, a)
# #         x = y1 - (b // a) * x1
# #         y = x1
# #         return gcd, x, y
    
# #     @staticmethod
# #     def mod_inverse(a, m):
# #         gcd, x, y = RSACipher.extended_gcd(a, m)
# #         if gcd != 1:
# #             return None
# #         return x % m
    
# #     @staticmethod
# #     def generate_keypair(bits=256):
# #         p = RSACipher.generate_prime(bits)
# #         q = RSACipher.generate_prime(bits)
# #         n = p * q
# #         phi = (p-1) * (q-1)
# #         e = 65537
# #         d = RSACipher.mod_inverse(e, phi)
# #         return (n, e), (n, d)
    
# #     @staticmethod
# #     def encrypt(message, public_key):
# #         n, e = public_key
# #         if isinstance(message, str):
# #             message = int.from_bytes(message.encode(), 'big')
# #         return pow(message, e, n)
    
# #     @staticmethod
# #     def decrypt(ciphertext, private_key):
# #         n, d = private_key
# #         decrypted = pow(ciphertext, d, n)
# #         byte_len = (decrypted.bit_length() + 7) // 8
# #         return decrypted.to_bytes(byte_len, 'big').decode()



# """
# RSA — Rivest–Shamir–Adleman (1977)
# Asymmetric (Public-Key) Cryptography | TP3

# Principle: Security based on the integer factorization problem.
#   Given n = p·q (product of two large primes), factoring n is computationally
#   infeasible for large p and q.

# Key generation:
#   1. Choose two large primes p and q
#   2. Compute n = p·q  (modulus)
#   3. Compute φ(n) = (p-1)·(q-1)  (Euler's totient)
#   4. Choose e such that gcd(e, φ(n)) = 1  (public exponent, typically 65537)
#   5. Compute d = e⁻¹ mod φ(n)  (private exponent)
#   Public key:  (n, e)
#   Private key: (n, d)

# Operations:
#   Encrypt : C = M^e mod n
#   Decrypt : M = C^d mod n
#   Sign    : S = hash(M)^d mod n
#   Verify  : hash(M) == S^e mod n

# Uses sympy for prime generation.
# """

# import hashlib
# import sympy
# import random


# class RSACipher:
#     """
#     Full RSA implementation: key generation, encryption, decryption,
#     signing, and verification.
#     """

#     # ── Key utilities ─────────────────────────────────────────────────────────

#     @staticmethod
#     def _extended_gcd(a: int, b: int) -> tuple[int, int, int]:
#         """Extended Euclidean algorithm → (gcd, x, y) such that a*x + b*y = gcd."""
#         if a == 0:
#             return b, 0, 1
#         gcd, x1, y1 = RSACipher._extended_gcd(b % a, a)
#         return gcd, y1 - (b // a) * x1, x1

#     @staticmethod
#     def mod_inverse(a: int, m: int) -> int:
#         """Compute a⁻¹ mod m using extended Euclidean algorithm."""
#         gcd, x, _ = RSACipher._extended_gcd(a % m, m)
#         if gcd != 1:
#             raise ValueError(f"gcd({a}, {m}) = {gcd} ≠ 1 — inverse does not exist")
#         return x % m

#     # ── Key generation ────────────────────────────────────────────────────────

#     @staticmethod
#     def generate_keypair(bits: int = 256) -> tuple[tuple, tuple]:
#         """
#         Generate an RSA key pair.

#         Args:
#             bits: Prime size in bits. Key strength ≈ 2×bits.
#                   Use 512+ for educational, 2048+ for real security.

#         Returns:
#             (public_key, private_key) where each is (n, exponent).

#         Example:
#             >>> pub, priv = RSACipher.generate_keypair(256)
#             >>> pub   # (n, e)
#             >>> priv  # (n, d)
#         """
#         p   = sympy.randprime(2**(bits-1), 2**bits)
#         q   = sympy.randprime(2**(bits-1), 2**bits)
#         n   = p * q
#         phi = (p - 1) * (q - 1)
#         e   = 65537   # standard public exponent
#         d   = RSACipher.mod_inverse(e, phi)
#         return (n, e), (n, d)

#     # ── Encryption / Decryption ───────────────────────────────────────────────

#     @staticmethod
#     def encrypt(message_int: int, public_key: tuple) -> int:
#         """
#         Encrypt an integer message: C = M^e mod n.

#         Args:
#             message_int: Integer representation of message (must be < n)
#             public_key:  (n, e) tuple

#         Returns:
#             Ciphertext integer.
#         """
#         n, e = public_key
#         if message_int >= n:
#             raise ValueError("Message integer must be less than n")
#         return pow(message_int, e, n)

#     @staticmethod
#     def decrypt(ciphertext: int, private_key: tuple) -> int:
#         """
#         Decrypt ciphertext: M = C^d mod n.

#         Args:
#             ciphertext:   Integer ciphertext
#             private_key:  (n, d) tuple

#         Returns:
#             Plaintext integer.
#         """
#         n, d = private_key
#         return pow(ciphertext, d, n)

#     @staticmethod
#     def encrypt_text(message: str, public_key: tuple) -> int:
#         """
#         Encrypt a short text string.

#         Args:
#             message:    Text string (limited by key size — use hybrid encryption for long messages)
#             public_key: (n, e)

#         Returns:
#             Ciphertext integer.
#         """
#         m_int = int.from_bytes(message.encode("utf-8"), "big")
#         return RSACipher.encrypt(m_int, public_key)

#     @staticmethod
#     def decrypt_text(ciphertext: int, private_key: tuple) -> str:
#         """Decrypt ciphertext back to a text string."""
#         m_int    = RSACipher.decrypt(ciphertext, private_key)
#         byte_len = (m_int.bit_length() + 7) // 8
#         return m_int.to_bytes(byte_len, "big").decode("utf-8")

#     # ── Digital signature ─────────────────────────────────────────────────────

#     @staticmethod
#     def sign(message: str, private_key: tuple) -> int:
#         """
#         Sign a message: S = hash(M)^d mod n.

#         Args:
#             message:     Message to sign
#             private_key: (n, d)

#         Returns:
#             Integer signature.
#         """
#         n, d      = private_key
#         hash_int  = int(hashlib.sha256(message.encode()).hexdigest(), 16) % n
#         return pow(hash_int, d, n)

#     @staticmethod
#     def verify(message: str, signature: int, public_key: tuple) -> bool:
#         """
#         Verify a signature: check that S^e mod n == hash(M) mod n.

#         Args:
#             message:    Original message
#             signature:  Signature integer
#             public_key: (n, e)

#         Returns:
#             True if signature is valid, False otherwise.
#         """
#         n, e      = public_key
#         hash_int  = int(hashlib.sha256(message.encode()).hexdigest(), 16) % n
#         recovered = pow(signature, e, n)
#         return hash_int == recovered


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     print("=" * 55)
#     print("RSA DEMO — key generation, encryption, signing")
#     print("=" * 55)
#     print("Generating 256-bit key pair…")
#     pub, priv = RSACipher.generate_keypair(128)
#     n, e = pub;  _, d = priv

#     print(f"  n = {n}")
#     print(f"  e = {e}  (public exponent)")
#     print(f"  d = {d}  (private exponent)")

#     msg = "RSA test"
#     ct  = RSACipher.encrypt_text(msg, pub)
#     pt  = RSACipher.decrypt_text(ct, priv)
#     print(f"\nEncrypt/Decrypt:")
#     print(f"  Plaintext  : {msg}")
#     print(f"  Ciphertext : {ct}")
#     print(f"  Decrypted  : {pt}")
#     print(f"  Match      : {msg == pt}")

#     sig   = RSACipher.sign(msg, priv)
#     valid = RSACipher.verify(msg, sig, pub)
#     print(f"\nDigital Signature:")
#     print(f"  Signature  : {sig}")
#     print(f"  Valid      : {valid}")
#     tampered = RSACipher.verify("tampered message", sig, pub)
#     print(f"  Tampered   : {tampered}  (should be False)")



"""
RSA (Rivest–Shamir–Adleman) - Asymmetric Public-Key Cryptosystem
Security relies on the difficulty of factoring large integers.
"""
import sympy
import random


class RSACipher:
    @staticmethod
    def _generate_prime(bits: int = 256) -> int:
        """Generate a random prime of given bit length."""
        return sympy.randprime(2 ** (bits - 1), 2 ** bits)

    @staticmethod
    def _extended_gcd(a: int, b: int) -> tuple:
        """Extended Euclidean algorithm; returns (gcd, x, y) where a*x + b*y = gcd."""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = RSACipher._extended_gcd(b % a, a)
        return gcd, y1 - (b // a) * x1, x1

    @staticmethod
    def _mod_inverse(a: int, m: int) -> int:
        """Modular multiplicative inverse of a mod m using extended GCD."""
        gcd, x, _ = RSACipher._extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError(f"Modular inverse does not exist (gcd={gcd})")
        return x % m

    @staticmethod
    def generate_keypair(bits: int = 256) -> tuple:
        """
        Generate RSA public/private key pair.
        Returns: (public_key=(n, e), private_key=(n, d))
        """
        p = RSACipher._generate_prime(bits)
        q = RSACipher._generate_prime(bits)
        while q == p:
            q = RSACipher._generate_prime(bits)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537  # Common public exponent
        d = RSACipher._mod_inverse(e, phi)
        return (n, e), (n, d)

    @staticmethod
    def encrypt(message: int, public_key: tuple) -> int:
        """Encrypt an integer message: C = M^e mod n."""
        n, e = public_key
        if message >= n:
            raise ValueError("Message too large for key size")
        return pow(message, e, n)

    @staticmethod
    def decrypt(ciphertext: int, private_key: tuple) -> int:
        """Decrypt an integer ciphertext: M = C^d mod n."""
        n, d = private_key
        return pow(ciphertext, d, n)

    @staticmethod
    def encrypt_text(text: str, public_key: tuple) -> int:
        """Encrypt a short string by converting to integer first."""
        if not text:
            raise ValueError("Text cannot be empty")
        msg_int = int.from_bytes(text.encode('utf-8'), 'big')
        return RSACipher.encrypt(msg_int, public_key)

    @staticmethod
    def decrypt_text(ciphertext: int, private_key: tuple) -> str:
        """Decrypt integer ciphertext back to string."""
        msg_int = RSACipher.decrypt(ciphertext, private_key)
        byte_len = (msg_int.bit_length() + 7) // 8
        return msg_int.to_bytes(byte_len, 'big').decode('utf-8')

    @staticmethod
    def get_info() -> str:
        return (
            "RSA (Rivest–Shamir–Adleman)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Type       : Asymmetric public-key cryptosystem\n"
            "Security   : Integer factorization problem\n"
            "Key sizes  : 2048–4096 bits recommended\n"
            "Uses       : Encryption, digital signatures, key exchange\n"
            "Note       : Vulnerable to quantum (Shor's algorithm)"
        )
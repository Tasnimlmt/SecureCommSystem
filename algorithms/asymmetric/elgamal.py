# # import sympy
# # import random

# # class ElGamalCipher:
# #     @staticmethod
# #     def generate_prime(bits=128):
# #         return sympy.randprime(2**(bits-1), 2**bits)
    
# #     @staticmethod
# #     def find_primitive_root(p):
# #         if p == 2:
# #             return 1
# #         factors = sympy.factorint(p-1)
# #         for g in range(2, min(p, 50)):
# #             valid = True
# #             for factor in factors.keys():
# #                 if pow(g, (p-1)//factor, p) == 1:
# #                     valid = False
# #                     break
# #             if valid:
# #                 return g
# #         return 2
    
# #     @staticmethod
# #     def generate_keypair(bits=128):
# #         p = ElGamalCipher.generate_prime(bits)
# #         g = ElGamalCipher.find_primitive_root(p)
# #         x = random.randint(2, p-2)
# #         y = pow(g, x, p)
# #         return (p, g, y), x
    
# #     @staticmethod
# #     def encrypt(message, public_key):
# #         p, g, y = public_key
# #         k = random.randint(2, p-2)
# #         c1 = pow(g, k, p)
# #         c2 = (message * pow(y, k, p)) % p
# #         return (c1, c2)
    
# #     @staticmethod
# #     def decrypt(ciphertext, private_key, p):
# #         c1, c2 = ciphertext
# #         s = pow(c1, private_key, p)
# #         s_inv = pow(s, -1, p)
# #         return (c2 * s_inv) % p



# """
# ElGamal Cryptosystem (1985)
# Asymmetric Cryptography | TP3

# Principle: Security based on the Discrete Logarithm Problem (DLP).
#   Probabilistic encryption — same plaintext produces different ciphertexts each time
#   (semantic security / IND-CPA).

# Key generation:
#   1. Choose prime p and generator g (primitive root mod p)
#   2. Choose private key x (random, 1 < x < p-1)
#   3. Compute public key y = g^x mod p
#   Public key:  (p, g, y)
#   Private key: x

# Encryption:
#   Choose random k, compute:
#     c1 = g^k mod p
#     c2 = M · y^k mod p
#   Ciphertext: (c1, c2)

# Decryption:
#   s  = c1^x mod p
#   M  = c2 · s⁻¹ mod p
# """

# import sympy
# import random
# import hashlib


# class ElGamalCipher:
#     """ElGamal public-key cryptosystem — encryption, decryption, and signature."""

#     @staticmethod
#     def _find_primitive_root(p: int) -> int:
#         """Find a primitive root (generator) of the multiplicative group mod p."""
#         factors = sympy.factorint(p - 1)
#         for g in range(2, min(p, 1000)):
#             if all(pow(g, (p-1)//f, p) != 1 for f in factors):
#                 return g
#         return 2  # fallback

#     @staticmethod
#     def generate_keypair(bits: int = 128) -> tuple[tuple, int]:
#         """
#         Generate an ElGamal key pair.

#         Args:
#             bits: Prime size in bits

#         Returns:
#             (public_key, private_key)
#             public_key  = (p, g, y)
#             private_key = x (integer)
#         """
#         p = sympy.randprime(2**(bits-1), 2**bits)
#         g = ElGamalCipher._find_primitive_root(p)
#         x = random.randint(2, p - 2)   # private key
#         y = pow(g, x, p)               # public key component
#         return (p, g, y), x

#     @staticmethod
#     def encrypt(message_int: int, public_key: tuple) -> tuple[int, int]:
#         """
#         Encrypt an integer message.

#         Args:
#             message_int: Integer M (must satisfy 1 ≤ M < p)
#             public_key:  (p, g, y)

#         Returns:
#             Ciphertext pair (c1, c2).

#         Note: Each call produces a DIFFERENT ciphertext (probabilistic encryption).
#         """
#         p, g, y = public_key
#         if not (1 <= message_int < p):
#             raise ValueError(f"Message must satisfy 1 ≤ M < p={p}")
#         k  = random.randint(2, p - 2)  # ephemeral key (fresh each call)
#         c1 = pow(g, k, p)
#         c2 = (message_int * pow(y, k, p)) % p
#         return c1, c2

#     @staticmethod
#     def decrypt(ciphertext: tuple[int, int], private_key: int, p: int) -> int:
#         """
#         Decrypt an ElGamal ciphertext.

#         Args:
#             ciphertext:  (c1, c2) pair
#             private_key: Integer x
#             p:           Prime modulus

#         Returns:
#             Plaintext integer M.
#         """
#         c1, c2 = ciphertext
#         s      = pow(c1, private_key, p)     # s = c1^x = g^(kx) mod p
#         s_inv  = pow(s, -1, p)              # s⁻¹ mod p
#         return (c2 * s_inv) % p

#     # ── Signature ─────────────────────────────────────────────────────────────

#     @staticmethod
#     def sign(message: str, private_key: int, public_key: tuple) -> tuple[int, int]:
#         """
#         ElGamal digital signature.

#         Returns:
#             Signature (r, s).
#         """
#         p, g, y = public_key
#         h       = int(hashlib.sha256(message.encode()).hexdigest(), 16) % (p - 1)
#         while True:
#             k = random.randint(2, p - 2)
#             if sympy.gcd(k, p - 1) == 1:
#                 break
#         r   = pow(g, k, p)
#         k_inv = pow(k, -1, p - 1)
#         s   = (k_inv * (h - private_key * r)) % (p - 1)
#         return r, s

#     @staticmethod
#     def verify_signature(message: str, signature: tuple[int, int], public_key: tuple) -> bool:
#         """
#         Verify an ElGamal signature.

#         Returns:
#             True if signature is valid.
#         """
#         p, g, y   = public_key
#         r, s      = signature
#         if not (0 < r < p) or not (0 < s < p - 1):
#             return False
#         h         = int(hashlib.sha256(message.encode()).hexdigest(), 16) % (p - 1)
#         lhs       = pow(g, h, p)
#         rhs       = (pow(y, r, p) * pow(r, s, p)) % p
#         return lhs == rhs

#     @staticmethod
#     def homomorphic_multiply(ct1: tuple, ct2: tuple, p: int) -> tuple:
#         """
#         ElGamal is multiplicatively homomorphic:
#         E(m1) ⊗ E(m2) = E(m1 · m2)
#         i.e. (c1_1·c1_2 mod p, c2_1·c2_2 mod p) decrypts to m1·m2.
#         """
#         c1_1, c2_1 = ct1
#         c1_2, c2_2 = ct2
#         return (c1_1 * c1_2) % p, (c2_1 * c2_2) % p


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     print("=" * 55)
#     print("ELGAMAL CRYPTOSYSTEM DEMO")
#     print("=" * 55)
#     print("Generating 128-bit key pair…")
#     pub, priv = ElGamalCipher.generate_keypair(128)
#     p, g, y   = pub

#     print(f"  p (prime)  : {p}")
#     print(f"  g (gen)    : {g}")
#     print(f"  y=g^x mod p: {y}")
#     print(f"  x (private): {priv}")

#     M  = 42000
#     ct = ElGamalCipher.encrypt(M, pub)
#     pt = ElGamalCipher.decrypt(ct, priv, p)
#     print(f"\nEncrypt/Decrypt:")
#     print(f"  M  = {M}")
#     print(f"  c1 = {ct[0]}")
#     print(f"  c2 = {ct[1]}")
#     print(f"  M' = {pt}  →  Match: {M == pt}")

#     # Same M, different ciphertext (probabilistic)
#     ct2 = ElGamalCipher.encrypt(M, pub)
#     print(f"\nProbabilistic: re-encrypt M={M}")
#     print(f"  New c1 = {ct2[0]}  (different!)")

#     # Homomorphic
#     ct_a  = ElGamalCipher.encrypt(6, pub)
#     ct_b  = ElGamalCipher.encrypt(7, pub)
#     ct_ab = ElGamalCipher.homomorphic_multiply(ct_a, ct_b, p)
#     prod  = ElGamalCipher.decrypt(ct_ab, priv, p)
#     print(f"\nHomomorphic: E(6)⊗E(7) → decrypt → {prod}  (expect 42)")


"""
ElGamal Cryptosystem - Asymmetric Public-Key Encryption
Based on Diffie-Hellman key exchange; provides probabilistic encryption
(same plaintext → different ciphertexts each time).
"""
import sympy
import random


class ElGamalCipher:
    @staticmethod
    def generate_prime(bits: int = 128) -> int:
        """Generate a random prime of given bit length."""
        return sympy.randprime(2 ** (bits - 1), 2 ** bits)

    @staticmethod
    def find_primitive_root(p: int) -> int:
        """Find the smallest primitive root modulo prime p."""
        if p == 2:
            return 1
        factors = sympy.factorint(p - 1)
        for g in range(2, min(p, 1000)):
            valid = all(pow(g, (p - 1) // f, p) != 1 for f in factors)
            if valid:
                return g
        return 2

    @staticmethod
    def generate_keypair(bits: int = 128) -> tuple:
        """
        Generate ElGamal key pair.
        Returns: (public_key=(p, g, y), private_key=x)
        where y = g^x mod p
        """
        p = ElGamalCipher.generate_prime(bits)
        g = ElGamalCipher.find_primitive_root(p)
        x = random.randint(2, p - 2)       # private key
        y = pow(g, x, p)                   # public key component
        return (p, g, y), x

    @staticmethod
    def encrypt(message: int, public_key: tuple) -> tuple:
        """
        Encrypt an integer message.
        Returns: (c1, c2) ciphertext pair.
        c1 = g^k mod p,  c2 = M * y^k mod p
        """
        p, g, y = public_key
        if message >= p:
            raise ValueError("Message must be smaller than prime p")
        k = random.randint(2, p - 2)       # ephemeral key (random each call)
        c1 = pow(g, k, p)
        c2 = (message * pow(y, k, p)) % p
        return c1, c2

    @staticmethod
    def decrypt(ciphertext: tuple, private_key: int, p: int) -> int:
        """
        Decrypt ciphertext pair (c1, c2).
        M = c2 * (c1^x)^(-1) mod p
        """
        c1, c2 = ciphertext
        s = pow(c1, private_key, p)
        s_inv = pow(s, -1, p)
        return (c2 * s_inv) % p

    @staticmethod
    def get_info() -> str:
        return (
            "ElGamal Cryptosystem\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Type       : Asymmetric public-key encryption\n"
            "Security   : Discrete logarithm problem (like DH)\n"
            "Property   : Probabilistic – same message ≠ same ciphertext\n"
            "Ciphertext : 2× size of plaintext\n"
            "Uses       : PGP encryption, key encapsulation\n"
            "Note       : Vulnerable to quantum (Shor's algorithm)"
        )
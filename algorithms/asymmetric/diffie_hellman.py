# # import sympy
# # import random

# # class DiffieHellman:
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
# #     def generate_keypair(p, g):
# #         private = random.randint(2, p-2)
# #         public = pow(g, private, p)
# #         return private, public
    
# #     @staticmethod
# #     def compute_shared_secret(private, other_public, p):
# #         return pow(other_public, private, p)



# """
# Diffie-Hellman Key Exchange (1976)
# Asymmetric Cryptography | TP3

# Principle: Two parties agree on a shared secret over a PUBLIC channel
#   without ever transmitting the secret itself.
#   Security based on the Discrete Logarithm Problem (DLP):
#   Given g, p, and g^a mod p — computing 'a' is computationally infeasible.

# Protocol:
#   Public params: prime p, generator g (primitive root mod p)
#   Alice: chooses secret a, sends A = g^a mod p
#   Bob:   chooses secret b, sends B = g^b mod p
#   Alice: computes K = B^a mod p
#   Bob:   computes K = A^b mod p
#   Both arrive at K = g^(a·b) mod p — the shared secret.

# Vulnerability: Vulnerable to Man-in-the-Middle (MITM) attack without
#   authentication. Use Authenticated DH (STS, TLS) in practice.
# """

# import sympy
# import random
# import hashlib


# class DiffieHellman:
#     """Diffie-Hellman key exchange — full protocol simulation."""

#     @staticmethod
#     def generate_params(bits: int = 128) -> tuple[int, int]:
#         """
#         Generate a safe prime p and a primitive root g mod p.

#         Args:
#             bits: Size of the prime in bits (use 2048+ for real security)

#         Returns:
#             (p, g) — prime modulus and generator
#         """
#         p       = sympy.randprime(2**(bits-1), 2**bits)
#         factors = sympy.factorint(p - 1)
#         # Find a primitive root g: g^((p-1)/q) ≠ 1 mod p for all prime factors q of p-1
#         g = 2
#         for candidate in range(2, min(p, 1000)):
#             if all(pow(candidate, (p-1)//f, p) != 1 for f in factors):
#                 g = candidate
#                 break
#         return p, g

#     @staticmethod
#     def generate_keypair(p: int, g: int) -> tuple[int, int]:
#         """
#         Generate a DH key pair given public parameters.

#         Args:
#             p: Prime modulus
#             g: Generator

#         Returns:
#             (private_key, public_key) where public_key = g^private mod p
#         """
#         private = random.randint(2, p - 2)
#         public  = pow(g, private, p)
#         return private, public

#     @staticmethod
#     def compute_shared_secret(my_private: int, their_public: int, p: int) -> int:
#         """
#         Compute the shared secret K = their_public^my_private mod p.

#         Args:
#             my_private:   This party's private key
#             their_public: The other party's public key
#             p:            Prime modulus

#         Returns:
#             Shared secret integer K.
#         """
#         return pow(their_public, my_private, p)

#     @staticmethod
#     def derive_aes_key(shared_secret: int) -> bytes:
#         """
#         Derive a 256-bit AES key from the DH shared secret using SHA-256.

#         Args:
#             shared_secret: Integer shared secret

#         Returns:
#             32-byte AES key.
#         """
#         return hashlib.sha256(str(shared_secret).encode()).digest()

#     @staticmethod
#     def simulate_exchange(bits: int = 128) -> dict:
#         """
#         Simulate a complete DH key exchange between Alice and Bob.

#         Returns:
#             Dictionary with all exchange parameters and the shared secret.
#         """
#         p, g             = DiffieHellman.generate_params(bits)
#         a, A             = DiffieHellman.generate_keypair(p, g)   # Alice
#         b, B             = DiffieHellman.generate_keypair(p, g)   # Bob
#         K_alice          = DiffieHellman.compute_shared_secret(a, B, p)
#         K_bob            = DiffieHellman.compute_shared_secret(b, A, p)
#         assert K_alice == K_bob, "Shared secrets do not match!"
#         return {
#             "prime_p":         p,
#             "generator_g":     g,
#             "alice_private":   a,
#             "alice_public":    A,
#             "bob_private":     b,
#             "bob_public":      B,
#             "shared_secret":   K_alice,
#             "aes_key":         DiffieHellman.derive_aes_key(K_alice).hex(),
#             "secrets_match":   K_alice == K_bob,
#         }


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     print("=" * 55)
#     print("DIFFIE-HELLMAN KEY EXCHANGE DEMO")
#     print("=" * 55)
#     print("Generating parameters…")
#     result = DiffieHellman.simulate_exchange(bits=128)

#     print(f"Prime p         : {result['prime_p']}")
#     print(f"Generator g     : {result['generator_g']}")
#     print(f"\nAlice private a : {result['alice_private']}")
#     print(f"Alice public  A : {result['alice_public']}")
#     print(f"\nBob   private b : {result['bob_private']}")
#     print(f"Bob   public  B : {result['bob_public']}")
#     print(f"\nShared secret K : {result['shared_secret']}")
#     print(f"AES-256 key     : {result['aes_key']}")
#     print(f"Secrets match   : {result['secrets_match']}")
#     print()
#     print("Public channel revealed: p, g, A, B")
#     print("Secret:                  a, b, K  (never transmitted)")


"""
Diffie-Hellman Key Exchange
Allows two parties to establish a shared secret over an insecure channel.
Security relies on the discrete logarithm problem.
"""
import sympy
import random


class DiffieHellman:
    @staticmethod
    def generate_prime(bits: int = 128) -> int:
        """Generate a random prime of given bit length."""
        return sympy.randprime(2 ** (bits - 1), 2 ** bits)

    @staticmethod
    def find_primitive_root(p: int) -> int:
        """
        Find the smallest primitive root (generator) modulo p.
        p should be prime for a guaranteed result.
        """
        if p == 2:
            return 1
        factors = sympy.factorint(p - 1)
        for g in range(2, min(p, 1000)):
            valid = all(pow(g, (p - 1) // f, p) != 1 for f in factors)
            if valid:
                return g
        return 2  # Fallback

    @staticmethod
    def generate_keypair(p: int, g: int) -> tuple:
        """
        Generate a DH private/public key pair.
        Returns: (private_key, public_key)
        """
        private = random.randint(2, p - 2)
        public = pow(g, private, p)
        return private, public

    @staticmethod
    def compute_shared_secret(private: int, other_public: int, p: int) -> int:
        """Compute the shared secret: K = other_public^private mod p."""
        return pow(other_public, private, p)

    @staticmethod
    def full_exchange(bits: int = 128) -> dict:
        """
        Simulate a complete Diffie-Hellman exchange between Alice and Bob.
        Returns all parameters and keys for display.
        """
        p = DiffieHellman.generate_prime(bits)
        g = DiffieHellman.find_primitive_root(p)

        a, A = DiffieHellman.generate_keypair(p, g)   # Alice
        b, B = DiffieHellman.generate_keypair(p, g)   # Bob

        K_alice = DiffieHellman.compute_shared_secret(a, B, p)
        K_bob = DiffieHellman.compute_shared_secret(b, A, p)

        return {
            'p': p, 'g': g,
            'alice_private': a, 'alice_public': A,
            'bob_private': b, 'bob_public': B,
            'shared_secret_alice': K_alice,
            'shared_secret_bob': K_bob,
            'match': K_alice == K_bob,
        }

    @staticmethod
    def get_info() -> str:
        return (
            "Diffie-Hellman Key Exchange\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Type       : Key agreement protocol\n"
            "Security   : Discrete logarithm problem\n"
            "Key sizes  : 2048+ bits recommended\n"
            "Uses       : TLS, SSH, IPsec key establishment\n"
            "Note       : Provides no authentication by itself"
        )
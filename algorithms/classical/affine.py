
# # class AffineCipher:
# #     """Affine cipher: y = (ax + b) mod 26"""
    
# #     @staticmethod
# #     def _mod_inverse(a, m=26):
# #         for x in range(1, m):
# #             if (a * x) % m == 1:
# #                 return x
# #         return None
    
# #     @staticmethod
# #     def _validate_a(a):
# #         if a < 1 or a > 25:
# #             raise ValueError("'a' must be between 1 and 25")
# #         inv = AffineCipher._mod_inverse(a)
# #         if inv is None:
# #             raise ValueError(f"'a'={a} is not coprime with 26. Allowed values: 1,3,5,7,9,11,15,17,19,21,23,25")
# #         return inv
    
# #     @staticmethod
# #     def encrypt(text, a, b):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         inv = AffineCipher._validate_a(a)
# #         if b < 0 or b > 25:
# #             raise ValueError("'b' must be between 0 and 25")
        
# #         result = []
# #         for char in text.upper():
# #             if char.isalpha():
# #                 x = ord(char) - 65
# #                 y = (a * x + b) % 26
# #                 result.append(chr(y + 65))
# #             else:
# #                 result.append(char)
# #         return ''.join(result)
    
# #     @staticmethod
# #     def decrypt(text, a, b):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         a_inv = AffineCipher._validate_a(a)
# #         if b < 0 or b > 25:
# #             raise ValueError("'b' must be between 0 and 25")
        
# #         result = []
# #         for char in text.upper():
# #             if char.isalpha():
# #                 y = ord(char) - 65
# #                 x = (a_inv * (y - b)) % 26
# #                 result.append(chr(x + 65))
# #             else:
# #                 result.append(char)
# #         return ''.join(result)


# """
# Affine Cipher — Linear transformation monoalphabetic cipher
# Classical Cryptography | TP1

# Principle: Uses the linear function y = (a·x + b) mod 26
#   Encrypt: C = (a·P + b) mod 26
#   Decrypt: P = a⁻¹·(C - b) mod 26

# Constraint: gcd(a, 26) = 1 — 'a' must be coprime with 26.
#   Valid values of 'a': 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
#   (12 valid keys × 26 values of b = 312 total keys)
# """

# import math


# class AffineCipher:
#     """Affine cipher with full encryption, decryption, and key validation."""

#     # All valid values of 'a' (coprime with 26)
#     VALID_A = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

#     @staticmethod
#     def mod_inverse(a: int, m: int = 26) -> int | None:
#         """
#         Compute the modular inverse of a mod m using brute force.

#         Returns:
#             Integer x such that (a * x) % m == 1, or None if not invertible.
#         """
#         if math.gcd(a, m) != 1:
#             return None
#         for x in range(1, m):
#             if (a * x) % m == 1:
#                 return x
#         return None

#     @staticmethod
#     def encrypt(text: str, a: int, b: int) -> str:
#         """
#         Encrypt using the Affine cipher.

#         Args:
#             text: Plaintext (any characters)
#             a:    Multiplicative key — must be coprime with 26
#             b:    Additive key — integer 0-25

#         Returns:
#             Ciphertext (uppercase, non-alpha unchanged)

#         Raises:
#             ValueError: If 'a' is not coprime with 26.

#         Example:
#             >>> AffineCipher.encrypt("Hello", 5, 8)
#             'RCLLA'
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         if AffineCipher.mod_inverse(a) is None:
#             raise ValueError(
#                 f"'a'={a} is not valid — must be coprime with 26.\n"
#                 f"Valid values: {AffineCipher.VALID_A}"
#             )
#         result = []
#         for char in text.upper():
#             if char.isalpha():
#                 x = ord(char) - 65
#                 y = (a * x + b) % 26
#                 result.append(chr(y + 65))
#             else:
#                 result.append(char)
#         return "".join(result)

#     @staticmethod
#     def decrypt(text: str, a: int, b: int) -> str:
#         """
#         Decrypt Affine ciphertext.

#         Args:
#             text: Ciphertext string
#             a:    Same multiplicative key used during encryption
#             b:    Same additive key used during encryption

#         Returns:
#             Recovered plaintext (uppercase).

#         Raises:
#             ValueError: If 'a' has no modular inverse mod 26.

#         Example:
#             >>> AffineCipher.decrypt("RCLLA", 5, 8)
#             'HELLO'
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         a_inv = AffineCipher.mod_inverse(a)
#         if a_inv is None:
#             raise ValueError(f"'a'={a} not invertible mod 26")
#         result = []
#         for char in text.upper():
#             if char.isalpha():
#                 y = ord(char) - 65
#                 x = (a_inv * (y - b)) % 26
#                 result.append(chr(x + 65))
#             else:
#                 result.append(char)
#         return "".join(result)

#     @staticmethod
#     def brute_force(ciphertext: str) -> list[tuple[int, int, str]]:
#         """
#         Try all 312 valid (a, b) key pairs.

#         Returns:
#             List of (a, b, plaintext) for every possible key.
#         """
#         results = []
#         for a in AffineCipher.VALID_A:
#             for b in range(26):
#                 pt = AffineCipher.decrypt(ciphertext, a, b)
#                 results.append((a, b, pt))
#         return results


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     plaintext = "CRYPTOGRAPHY"
#     a, b      = 5, 8   # classic example

#     ciphertext = AffineCipher.encrypt(plaintext, a, b)
#     recovered  = AffineCipher.decrypt(ciphertext, a, b)

#     print("=" * 50)
#     print("AFFINE CIPHER DEMO")
#     print("=" * 50)
#     print(f"Plaintext  : {plaintext}")
#     print(f"Key        : a={a}, b={b}  → y = ({a}x + {b}) mod 26")
#     print(f"a⁻¹ mod 26 : {AffineCipher.mod_inverse(a)}")
#     print(f"Ciphertext : {ciphertext}")
#     print(f"Decrypted  : {recovered}")
#     print(f"Match      : {plaintext == recovered}")
#     print(f"\nTotal key space: {len(AffineCipher.VALID_A) * 26} combinations")


"""
Affine Cipher - Classical Mathematical Substitution Cipher
Encrypts using: E(x) = (a*x + b) mod 26
Decrypts using: D(y) = a_inv * (y - b) mod 26
'a' must be coprime with 26; valid values: 1,3,5,7,9,11,15,17,19,21,23,25
"""


class AffineCipher:
    VALID_A = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

    @staticmethod
    def mod_inverse(a: int, m: int = 26) -> int | None:
        """Find modular multiplicative inverse of a mod m."""
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    @staticmethod
    def encrypt(text: str, a: int, b: int) -> str:
        """Encrypt text using Affine cipher: E(x) = (a*x + b) mod 26."""
        if not text:
            raise ValueError("Text cannot be empty")
        if AffineCipher.mod_inverse(a) is None:
            raise ValueError(
                f"'a'={a} must be coprime with 26.\nValid values: {AffineCipher.VALID_A}"
            )
        b = b % 26
        result = []
        for char in text:
            if char.isalpha():
                x = ord(char.upper()) - 65
                y = (a * x + b) % 26
                enc = chr(y + 65)
                result.append(enc if char.isupper() else enc.lower())
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, a: int, b: int) -> str:
        """Decrypt text using Affine cipher: D(y) = a_inv*(y - b) mod 26."""
        if not text:
            raise ValueError("Text cannot be empty")
        a_inv = AffineCipher.mod_inverse(a)
        if a_inv is None:
            raise ValueError(
                f"'a'={a} has no modular inverse mod 26.\nValid values: {AffineCipher.VALID_A}"
            )
        b = b % 26
        result = []
        for char in text:
            if char.isalpha():
                y = ord(char.upper()) - 65
                x = (a_inv * (y - b)) % 26
                dec = chr(x + 65)
                result.append(dec if char.isupper() else dec.lower())
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def show_mapping(a: int, b: int) -> str:
        """Display the full affine substitution mapping."""
        if AffineCipher.mod_inverse(a) is None:
            return f"Invalid 'a'={a}. Must be coprime with 26."
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        encrypted = AffineCipher.encrypt(alphabet, a, b)
        lines = [
            f"Affine Cipher Mapping (a={a}, b={b}):",
            "Plain:  " + ' '.join(alphabet),
            "Cipher: " + ' '.join(encrypted),
        ]
        return '\n'.join(lines)
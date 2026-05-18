# # class CaesarCipher:
# #     """Caesar cipher - monoalphabetic shift"""
    
# #     @staticmethod
# #     def encrypt(text, shift):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         if shift < 1 or shift > 25:
# #             raise ValueError("Shift must be between 1 and 25")
        
# #         shift = shift % 26
# #         result = []
# #         for char in text:
# #             if char.isalpha():
# #                 if char.isupper():
# #                     result.append(chr((ord(char) - 65 + shift) % 26 + 65))
# #                 else:
# #                     result.append(chr((ord(char) - 97 + shift) % 26 + 97))
# #             else:
# #                 result.append(char)
# #         return ''.join(result)
    
# #     @staticmethod
# #     def decrypt(text, shift):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         if shift < 1 or shift > 25:
# #             raise ValueError("Shift must be between 1 and 25")
# #         return CaesarCipher.encrypt(text, -shift)



# """
# Caesar Cipher — Monoalphabetic shift cipher
# Classical Cryptography | TP1

# Principle: Each letter is shifted by a fixed amount (key) in the alphabet.
#   Encrypt: C = (P + key) mod 26
#   Decrypt: P = (C - key) mod 26
# """


# class CaesarCipher:
#     """Caesar cipher with support for uppercase, lowercase, and non-alpha characters."""

#     @staticmethod
#     def encrypt(text: str, shift: int) -> str:
#         """
#         Encrypt plaintext using Caesar cipher.

#         Args:
#             text:  Plaintext string (any characters)
#             shift: Integer shift key (e.g. 3 for classic Caesar)

#         Returns:
#             Ciphertext with letters shifted, non-alpha characters unchanged.

#         Example:
#             >>> CaesarCipher.encrypt("Hello, World!", 3)
#             'Khoor, Zruog!'
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         shift = shift % 26  # normalise negative or large shifts
#         result = []
#         for char in text:
#             if char.isalpha():
#                 base = 65 if char.isupper() else 97
#                 result.append(chr((ord(char) - base + shift) % 26 + base))
#             else:
#                 result.append(char)
#         return "".join(result)

#     @staticmethod
#     def decrypt(text: str, shift: int) -> str:
#         """
#         Decrypt Caesar ciphertext.

#         Args:
#             text:  Ciphertext string
#             shift: Same integer shift key used during encryption

#         Returns:
#             Recovered plaintext.

#         Example:
#             >>> CaesarCipher.decrypt("Khoor, Zruog!", 3)
#             'Hello, World!'
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         return CaesarCipher.encrypt(text, -shift)

#     @staticmethod
#     def brute_force(ciphertext: str) -> list[tuple[int, str]]:
#         """
#         Try all 25 possible shifts (cryptanalysis).

#         Args:
#             ciphertext: Encrypted text

#         Returns:
#             List of (shift, plaintext) tuples for all 25 possible keys.
#         """
#         return [
#             (shift, CaesarCipher.decrypt(ciphertext, shift))
#             for shift in range(1, 26)
#         ]


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     plaintext = "The quick brown fox jumps over the lazy dog"
#     shift     = 13   # ROT13 is Caesar with shift=13

#     ciphertext = CaesarCipher.encrypt(plaintext, shift)
#     recovered  = CaesarCipher.decrypt(ciphertext, shift)

#     print("=" * 50)
#     print("CAESAR CIPHER DEMO")
#     print("=" * 50)
#     print(f"Plaintext  : {plaintext}")
#     print(f"Shift      : {shift}")
#     print(f"Ciphertext : {ciphertext}")
#     print(f"Decrypted  : {recovered}")
#     print(f"Match      : {plaintext == recovered}")
#     print()
#     print("Brute-force (first 5 shifts):")
#     for s, pt in CaesarCipher.brute_force(ciphertext)[:5]:
#         print(f"  shift={s:2d} → {pt}")



"""
Caesar Cipher - Classical Cipher
Shifts each letter by a fixed number of positions in the alphabet.
"""


class CaesarCipher:
    @staticmethod
    def encrypt(text: str, shift: int) -> str:
        """Encrypt text using Caesar cipher with given shift."""
        if not text:
            raise ValueError("Text cannot be empty")
        shift = shift % 26
        result = []
        for char in text:
            if char.isalpha():
                base = 65 if char.isupper() else 97
                result.append(chr((ord(char) - base + shift) % 26 + base))
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, shift: int) -> str:
        """Decrypt text using Caesar cipher with given shift."""
        return CaesarCipher.encrypt(text, -shift)

    @staticmethod
    def brute_force(text: str) -> list:
        """Try all 25 possible shifts and return results."""
        results = []
        for shift in range(1, 26):
            decrypted = CaesarCipher.decrypt(text, shift)
            results.append((shift, decrypted))
        return results
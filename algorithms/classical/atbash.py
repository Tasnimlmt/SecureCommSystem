# # class AtbashCipher:
# #     """Atbash cipher - Hebrew substitution (A->Z, B->Y, etc.)"""
    
# #     @staticmethod
# #     def encrypt(text):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         result = []
# #         for char in text:
# #             if char.isupper():
# #                 result.append(chr(155 - ord(char)))
# #             elif char.islower():
# #                 result.append(chr(219 - ord(char)))
# #             else:
# #                 result.append(char)
# #         return ''.join(result)
    
# #     @staticmethod
# #     def decrypt(text):
# #         return AtbashCipher.encrypt(text)\\\



# """
# Atbash Cipher — Hebrew substitution cipher
# Classical Cryptography | TP1

# Principle: Mirror the alphabet. A↔Z, B↔Y, C↔X, …
#   Encrypt: C = 25 - (P - 'A')  (for uppercase)
#   This cipher is its own inverse — encrypt == decrypt.

# Historical note: Originally used with the Hebrew alphabet.
# """


# class AtbashCipher:
#     """Atbash cipher — self-inverse monoalphabetic substitution."""

#     @staticmethod
#     def encrypt(text: str) -> str:
#         """
#         Encrypt (or decrypt) text using Atbash.
#         Since Atbash is its own inverse, this method serves both directions.

#         Args:
#             text: Input string (any characters)

#         Returns:
#             Transformed string — uppercase and lowercase handled separately,
#             non-alpha characters are passed through unchanged.

#         Example:
#             >>> AtbashCipher.encrypt("Hello")
#             'Svool'
#             >>> AtbashCipher.encrypt("Svool")
#             'Hello'
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         result = []
#         for char in text:
#             if char.isupper():
#                 # A(65)↔Z(90): 65 + 90 = 155
#                 result.append(chr(155 - ord(char)))
#             elif char.islower():
#                 # a(97)↔z(122): 97 + 122 = 219
#                 result.append(chr(219 - ord(char)))
#             else:
#                 result.append(char)
#         return "".join(result)

#     # Alias — decrypt is identical to encrypt for Atbash
#     decrypt = encrypt

#     @staticmethod
#     def show_mapping() -> dict:
#         """Return the full substitution alphabet mapping (uppercase)."""
#         return {chr(i): chr(155 - i) for i in range(65, 91)}


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     plaintext = "Attack At Dawn"

#     ciphertext = AtbashCipher.encrypt(plaintext)
#     recovered  = AtbashCipher.decrypt(ciphertext)

#     print("=" * 50)
#     print("ATBASH CIPHER DEMO")
#     print("=" * 50)
#     print(f"Plaintext  : {plaintext}")
#     print(f"Ciphertext : {ciphertext}")
#     print(f"Decrypted  : {recovered}")
#     print(f"Self-inverse confirmed: {plaintext == recovered}")
#     print()
#     print("Substitution mapping (A-M):")
#     mapping = AtbashCipher.show_mapping()
#     for k, v in list(mapping.items())[:13]:
#         print(f"  {k} ↔ {v}", end="   ")
#     print()


"""
Atbash Cipher - Classical Substitution Cipher
Reverses the alphabet: A↔Z, B↔Y, C↔X, etc.
Originally used for the Hebrew alphabet; self-inverse (encrypt = decrypt).
"""


class AtbashCipher:
    @staticmethod
    def encrypt(text: str) -> str:
        """Encrypt (or decrypt) text using Atbash cipher."""
        if not text:
            raise ValueError("Text cannot be empty")
        result = []
        for char in text:
            if char.isupper():
                result.append(chr(90 - (ord(char) - 65)))   # Z - offset from A
            elif char.islower():
                result.append(chr(122 - (ord(char) - 97)))  # z - offset from a
            else:
                result.append(char)
        return ''.join(result)

    # Atbash is its own inverse
    decrypt = encrypt

    @staticmethod
    def show_mapping() -> str:
        """Display the full Atbash substitution mapping."""
        forward = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        backward = forward[::-1]
        lines = [
            "Atbash Substitution Table:",
            "Plain:  " + ' '.join(forward),
            "Cipher: " + ' '.join(backward),
        ]
        return '\n'.join(lines)
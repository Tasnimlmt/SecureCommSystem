
# # class OneTimePad:
# #     """One-Time Pad (Vernam cipher) - theoretically unbreakable"""
    
# #     @staticmethod
# #     def encrypt(text, key):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         if not key:
# #             raise ValueError("Key cannot be empty")
# #         if len(key) < len(text):
# #             raise ValueError(f"Key must be at least {len(text)} characters long")
        
# #         result = []
# #         for i, char in enumerate(text):
# #             result.append(chr(ord(char) ^ ord(key[i])))
# #         return ''.join(result)
    
# #     @staticmethod
# #     def decrypt(cipher, key):
# #         if not cipher:
# #             raise ValueError("Ciphertext cannot be empty")
# #         if not key:
# #             raise ValueError("Key cannot be empty")
# #         if len(key) < len(cipher):
# #             raise ValueError(f"Key must be at least {len(cipher)} characters long")
        
# #         return OneTimePad.encrypt(cipher, key)


# """
# One-Time Pad (OTP) / Vernam Cipher — Theoretically Unbreakable
# Classical Cryptography | TP1

# Principle: XOR each byte of the plaintext with a truly random key of equal length.
#   Encrypt: C_i = P_i XOR K_i
#   Decrypt: P_i = C_i XOR K_i  (identical operation — XOR is self-inverse)

# Security conditions (Shannon, 1949):
#   1. Key must be truly random.
#   2. Key must be at least as long as the message.
#   3. Key must never be reused (hence "One-Time").
#   4. Key must be kept completely secret.

# If all conditions are met, the cipher is information-theoretically secure
# (provably unbreakable even with unlimited computing power).
# """

# import os
# import secrets


# class OneTimePad:
#     """One-Time Pad (Vernam cipher) — byte-level XOR encryption."""

#     @staticmethod
#     def generate_key(length: int) -> bytes:
#         """
#         Generate a cryptographically secure random key.

#         Args:
#             length: Key length in bytes (must equal message length)

#         Returns:
#             Random bytes of the specified length.
#         """
#         return secrets.token_bytes(length)

#     @staticmethod
#     def encrypt(plaintext: bytes | str, key: bytes | str) -> bytes:
#         """
#         Encrypt plaintext using XOR with the key.

#         Args:
#             plaintext: Message as bytes or string
#             key:       Key as bytes or string — must be at least len(plaintext)

#         Returns:
#             Ciphertext as bytes.

#         Raises:
#             ValueError: If key is shorter than plaintext.

#         Example:
#             >>> key = OneTimePad.generate_key(5)
#             >>> ct  = OneTimePad.encrypt("Hello", key)
#             >>> OneTimePad.decrypt(ct, key)
#             b'Hello'
#         """
#         if isinstance(plaintext, str):
#             plaintext = plaintext.encode("utf-8")
#         if isinstance(key, str):
#             key = key.encode("utf-8")
#         if not plaintext:
#             raise ValueError("Plaintext cannot be empty")
#         if len(key) < len(plaintext):
#             raise ValueError(
#                 f"Key must be at least {len(plaintext)} bytes "
#                 f"(got {len(key)} bytes). OTP requires key ≥ message length."
#             )
#         return bytes(p ^ k for p, k in zip(plaintext, key))

#     @staticmethod
#     def decrypt(ciphertext: bytes, key: bytes | str) -> bytes:
#         """
#         Decrypt OTP ciphertext (identical to encrypt — XOR is self-inverse).

#         Args:
#             ciphertext: Encrypted bytes
#             key:        Same key used during encryption

#         Returns:
#             Recovered plaintext as bytes.
#         """
#         return OneTimePad.encrypt(ciphertext, key)

#     @staticmethod
#     def encrypt_text(plaintext: str, key: str = None) -> tuple[str, str]:
#         """
#         Convenience wrapper for text encryption.

#         Args:
#             plaintext: Plain text message
#             key:       Optional key string (auto-generated if None)

#         Returns:
#             (ciphertext_hex, key_hex) — both as hex strings for display.
#         """
#         pt_bytes  = plaintext.encode("utf-8")
#         key_bytes = key.encode("utf-8") if key else OneTimePad.generate_key(len(pt_bytes))
#         if len(key_bytes) < len(pt_bytes):
#             raise ValueError(f"Key must be at least {len(pt_bytes)} characters")
#         ct        = OneTimePad.encrypt(pt_bytes, key_bytes)
#         return ct.hex(), key_bytes.hex()

#     @staticmethod
#     def decrypt_text(ciphertext_hex: str, key_hex: str) -> str:
#         """
#         Convenience wrapper to decrypt hex-encoded OTP ciphertext.

#         Args:
#             ciphertext_hex: Hex string of ciphertext
#             key_hex:        Hex string of key

#         Returns:
#             Recovered plaintext string.
#         """
#         ct  = bytes.fromhex(ciphertext_hex)
#         key = bytes.fromhex(key_hex)
#         pt  = OneTimePad.decrypt(ct, key)
#         return pt.decode("utf-8")


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     plaintext = "TOP SECRET MESSAGE"

#     key_bytes = OneTimePad.generate_key(len(plaintext.encode()))
#     pt_bytes  = plaintext.encode("utf-8")
#     ct_bytes  = OneTimePad.encrypt(pt_bytes, key_bytes)
#     recovered = OneTimePad.decrypt(ct_bytes, key_bytes)

#     print("=" * 55)
#     print("ONE-TIME PAD (VERNAM CIPHER) DEMO")
#     print("=" * 55)
#     print(f"Plaintext  : {plaintext}")
#     print(f"Key (hex)  : {key_bytes.hex()}")
#     print(f"Ciphertext : {ct_bytes.hex()}")
#     print(f"Decrypted  : {recovered.decode()}")
#     print(f"Match      : {pt_bytes == recovered}")
#     print()
#     print("Security note:")
#     print("  ✓ Key is randomly generated (os.urandom / secrets)")
#     print("  ✓ Key length == message length")
#     print("  ✗ Reusing this key would destroy security!")


"""
One-Time Pad (OTP) - Theoretically Unbreakable Cipher
XORs each character with a corresponding key character.
The key must be at least as long as the message and truly random.
"""
import os


class OneTimePad:
    @staticmethod
    def generate_key(length: int) -> str:
        """Generate a cryptographically secure random key of given length."""
        return ''.join(chr(b % 95 + 32) for b in os.urandom(length))

    @staticmethod
    def encrypt(text: str, key: str) -> tuple:
        """
        Encrypt text using One-Time Pad (XOR).
        Returns (ciphertext_bytes, hex_representation).
        """
        if not text:
            raise ValueError("Text cannot be empty")
        if not key or len(key) < len(text):
            raise ValueError(f"Key must be at least {len(text)} characters long")
        cipher_bytes = bytes(ord(text[i]) ^ ord(key[i]) for i in range(len(text)))
        hex_repr = cipher_bytes.hex()
        return cipher_bytes, hex_repr

    @staticmethod
    def decrypt(cipher_bytes: bytes, key: str) -> str:
        """Decrypt bytes using One-Time Pad (XOR)."""
        if not cipher_bytes:
            raise ValueError("Ciphertext cannot be empty")
        if not key or len(key) < len(cipher_bytes):
            raise ValueError(f"Key must be at least {len(cipher_bytes)} characters long")
        return ''.join(chr(cipher_bytes[i] ^ ord(key[i])) for i in range(len(cipher_bytes)))

    @staticmethod
    def encrypt_hex(text: str, key: str) -> str:
        """Encrypt and return hex string."""
        _, hex_repr = OneTimePad.encrypt(text, key)
        return hex_repr

    @staticmethod
    def decrypt_hex(hex_str: str, key: str) -> str:
        """Decrypt from hex string."""
        cipher_bytes = bytes.fromhex(hex_str)
        return OneTimePad.decrypt(cipher_bytes, key)
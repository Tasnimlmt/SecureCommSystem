
# """
# AES (Advanced Encryption Standard) - Symmetric Block Cipher
# Winner of the NIST AES competition (Rijndael algorithm).
# Supports CBC and GCM modes with 256-bit keys.
# """
# import hashlib
# import base64
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# from Crypto.Random import get_random_bytes


# class AESCipher:
#     KEY_SIZE = 32       # 256-bit key
#     BLOCK_SIZE = 16     # 128-bit block

#     @staticmethod
#     def _derive_key(key: str) -> bytes:
#         """Derive a 256-bit key from a string using SHA-256."""
#         return hashlib.sha256(key.encode()).digest()

#     # ── CBC Mode ──────────────────────────────────────────────────────────

#     @staticmethod
#     def encrypt_cbc(text: str, key: str) -> str:
#         """Encrypt text using AES-256-CBC. Returns Base64-encoded string."""
#         if not text:
#             raise ValueError("Text cannot be empty")
#         if not key:
#             raise ValueError("Key cannot be empty")
#         k = AESCipher._derive_key(key)
#         iv = get_random_bytes(AESCipher.BLOCK_SIZE)
#         cipher = AES.new(k, AES.MODE_CBC, iv)
#         encrypted = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
#         return base64.b64encode(iv + encrypted).decode()

#     @staticmethod
#     def decrypt_cbc(encrypted_b64: str, key: str) -> str:
#         """Decrypt AES-256-CBC ciphertext from Base64."""
#         if not encrypted_b64:
#             raise ValueError("Ciphertext cannot be empty")
#         if not key:
#             raise ValueError("Key cannot be empty")
#         k = AESCipher._derive_key(key)
#         data = base64.b64decode(encrypted_b64)
#         iv, ciphertext = data[:16], data[16:]
#         cipher = AES.new(k, AES.MODE_CBC, iv)
#         return unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

#     # ── GCM Mode (authenticated encryption) ──────────────────────────────

#     @staticmethod
#     def encrypt_gcm(text: str, key: str) -> str:
#         """Encrypt text using AES-256-GCM (authenticated). Returns Base64."""
#         if not text:
#             raise ValueError("Text cannot be empty")
#         if not key:
#             raise ValueError("Key cannot be empty")
#         k = AESCipher._derive_key(key)
#         cipher = AES.new(k, AES.MODE_GCM)
#         ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
#         # Pack: nonce (16) + tag (16) + ciphertext
#         packed = cipher.nonce + tag + ciphertext
#         return base64.b64encode(packed).decode()

#     @staticmethod
#     def decrypt_gcm(encrypted_b64: str, key: str) -> str:
#         """Decrypt AES-256-GCM ciphertext; raises ValueError if tampered."""
#         if not encrypted_b64:
#             raise ValueError("Ciphertext cannot be empty")
#         if not key:
#             raise ValueError("Key cannot be empty")
#         k = AESCipher._derive_key(key)
#         data = base64.b64decode(encrypted_b64)
#         nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
#         cipher = AES.new(k, AES.MODE_GCM, nonce=nonce)
#         return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')

#     @staticmethod
#     def get_info() -> str:
#         """Return a summary of the AES algorithm."""
#         return (
#             "AES-256 (Advanced Encryption Standard)\n"
#             "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
#             "Block size : 128 bits\n"
#             "Key size   : 256 bits\n"
#             "Rounds     : 14\n"
#             "Modes      : CBC (confidentiality), GCM (auth. encryption)\n"
#             "Security   : ~2¹²⁸ brute-force resistance\n"
#             "Standard   : FIPS 197, ISO/IEC 18033-3"
#         )







"""
AES (Advanced Encryption Standard) - Symmetric Block Cipher
Winner of the NIST AES competition (Rijndael algorithm).
Supports ECB, CBC and GCM modes with 256-bit keys.
"""
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class AESCipher:
    KEY_SIZE = 32       # 256-bit key
    BLOCK_SIZE = 16     # 128-bit block

    @staticmethod
    def _derive_key(key: str) -> bytes:
        """Derive a 256-bit key from a string using SHA-256."""
        return hashlib.sha256(key.encode()).digest()

    # ── ECB Mode (WARNING: Insecure for most uses) ──────────────────────────

    @staticmethod
    def encrypt_ecb(text: str, key: str) -> str:
        """Encrypt text using AES-256-ECB (INSECURE - for educational use only)."""
        if not text:
            raise ValueError("Text cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        k = AESCipher._derive_key(key)
        cipher = AES.new(k, AES.MODE_ECB)
        encrypted = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
        return base64.b64encode(encrypted).decode()

    @staticmethod
    def decrypt_ecb(encrypted_b64: str, key: str) -> str:
        """Decrypt AES-256-ECB ciphertext."""
        if not encrypted_b64:
            raise ValueError("Ciphertext cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        k = AESCipher._derive_key(key)
        ciphertext = base64.b64decode(encrypted_b64)
        cipher = AES.new(k, AES.MODE_ECB)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

    # ── CBC Mode ──────────────────────────────────────────────────────────

    @staticmethod
    def encrypt_cbc(text: str, key: str) -> str:
        """Encrypt text using AES-256-CBC. Returns Base64-encoded string."""
        if not text:
            raise ValueError("Text cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        k = AESCipher._derive_key(key)
        iv = get_random_bytes(AESCipher.BLOCK_SIZE)
        cipher = AES.new(k, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
        return base64.b64encode(iv + encrypted).decode()

    @staticmethod
    def decrypt_cbc(encrypted_b64: str, key: str) -> str:
        """Decrypt AES-256-CBC ciphertext from Base64."""
        if not encrypted_b64:
            raise ValueError("Ciphertext cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        k = AESCipher._derive_key(key)
        data = base64.b64decode(encrypted_b64)
        iv, ciphertext = data[:16], data[16:]
        cipher = AES.new(k, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

    # ── GCM Mode (authenticated encryption) ──────────────────────────────

    @staticmethod
    def encrypt_gcm(text: str, key: str) -> str:
        """Encrypt text using AES-256-GCM (authenticated). Returns Base64."""
        if not text:
            raise ValueError("Text cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        k = AESCipher._derive_key(key)
        cipher = AES.new(k, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
        packed = cipher.nonce + tag + ciphertext
        return base64.b64encode(packed).decode()

    @staticmethod
    def decrypt_gcm(encrypted_b64: str, key: str) -> str:
        """Decrypt AES-256-GCM ciphertext; raises ValueError if tampered."""
        if not encrypted_b64:
            raise ValueError("Ciphertext cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        k = AESCipher._derive_key(key)
        data = base64.b64decode(encrypted_b64)
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        cipher = AES.new(k, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')

    @staticmethod
    def get_info() -> str:
        """Return a summary of the AES algorithm."""
        return (
            "AES-256 (Advanced Encryption Standard)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Block size : 128 bits\n"
            "Key size   : 256 bits\n"
            "Rounds     : 14\n"
            "Modes      : ECB (⚠ insecure), CBC, GCM (auth. encryption)\n"
            "Security   : ~2¹²⁸ brute-force resistance\n"
            "Standard   : FIPS 197, ISO/IEC 18033-3\n\n"
            "⚠ ECB MODE WARNING: Encrypts identical plaintext blocks to\n"
            "  identical ciphertext blocks. Do NOT use for real encryption!"
        )
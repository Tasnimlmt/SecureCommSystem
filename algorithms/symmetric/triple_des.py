# # import hashlib
# # import base64
# # from Crypto.Cipher import DES3
# # from Crypto.Util.Padding import pad, unpad
# # from Crypto.Random import get_random_bytes

# # class TripleDESCipher:
# #     """Triple DES block cipher (168-bit key)"""
    
# #     @staticmethod
# #     def encrypt(text, key):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         if not key:
# #             raise ValueError("Key cannot be empty")
        
# #         key = hashlib.sha256(key.encode()).digest()[:24]
# #         iv = get_random_bytes(8)
# #         cipher = DES3.new(key, DES3.MODE_CBC, iv)
# #         padded = pad(text.encode(), DES3.block_size)
# #         encrypted = cipher.encrypt(padded)
# #         return base64.b64encode(iv + encrypted).decode()
    
# #     @staticmethod
# #     def decrypt(encrypted_b64, key):
# #         if not encrypted_b64:
# #             raise ValueError("Ciphertext cannot be empty")
# #         if not key:
# #             raise ValueError("Key cannot be empty")
        
# #         key = hashlib.sha256(key.encode()).digest()[:24]
# #         data = base64.b64decode(encrypted_b64)
# #         iv = data[:8]
# #         ciphertext = data[8:]
# #         cipher = DES3.new(key, DES3.MODE_CBC, iv)
# #         decrypted = unpad(cipher.decrypt(ciphertext), DES3.block_size)
# #         return decrypted.decode()

# """
# Triple DES (3DES / TDEA) — Triple Data Encryption Algorithm
# Modern Symmetric Cryptography | TP2

# Principle: Apply DES three times with two or three independent keys.
#   Two-key 3DES   (112-bit effective): C = E_K1(D_K2(E_K1(P)))
#   Three-key 3DES (168-bit effective): C = E_K3(D_K2(E_K1(P)))

# Specification:
#   Block size : 64 bits (8 bytes) — same as DES
#   Key sizes  : 128-bit (2-key) or 192-bit (3-key)
#   Rounds     : 48 (3 × 16 DES rounds)
#   Status     : Deprecated by NIST (2023) — use AES instead.
#                Still found in legacy banking (EMV cards, ATMs).

# The EDE (Encrypt-Decrypt-Encrypt) structure ensures backward compatibility:
#   Setting K1 = K2 = K3 reduces 3DES to single DES.

# Uses PyCryptodome (pip install pycryptodome).
# """

# import hashlib
# import base64
# from Crypto.Cipher import DES3
# from Crypto.Util.Padding import pad, unpad
# from Crypto.Random import get_random_bytes


# class TripleDESCipher:
#     """Triple DES (3DES) — CBC and ECB modes, two-key and three-key variants."""

#     @staticmethod
#     def _derive_key(password: str, three_key: bool = True) -> bytes:
#         """
#         Derive a 3DES key from a password.

#         Args:
#             password:  Key password
#             three_key: True → 24-byte (192-bit) key; False → 16-byte (128-bit) key
#         """
#         raw = hashlib.sha256(password.encode()).digest()  # 32 bytes
#         if three_key:
#             return DES3.adjust_key_parity(raw[:24])   # 3-key variant
#         else:
#             return DES3.adjust_key_parity(raw[:16])   # 2-key variant

#     # ── ECB mode ─────────────────────────────────────────────────────────────

#     @staticmethod
#     def encrypt_ecb(plaintext: str, password: str, three_key: bool = True) -> str:
#         """
#         Encrypt with 3DES-ECB.

#         Args:
#             plaintext: Input text
#             password:  Key password
#             three_key: Use 3-key (True) or 2-key (False) variant

#         Returns:
#             Base64-encoded ciphertext.
#         """
#         if not plaintext: raise ValueError("Plaintext cannot be empty")
#         key    = TripleDESCipher._derive_key(password, three_key)
#         cipher = DES3.new(key, DES3.MODE_ECB)
#         ct     = cipher.encrypt(pad(plaintext.encode(), DES3.block_size))
#         return base64.b64encode(ct).decode()

#     @staticmethod
#     def decrypt_ecb(ciphertext_b64: str, password: str, three_key: bool = True) -> str:
#         """Decrypt 3DES-ECB ciphertext."""
#         if not ciphertext_b64: raise ValueError("Ciphertext cannot be empty")
#         key    = TripleDESCipher._derive_key(password, three_key)
#         cipher = DES3.new(key, DES3.MODE_ECB)
#         return unpad(cipher.decrypt(base64.b64decode(ciphertext_b64)), DES3.block_size).decode()

#     # ── CBC mode ─────────────────────────────────────────────────────────────

#     @staticmethod
#     def encrypt_cbc(plaintext: str, password: str, three_key: bool = True) -> str:
#         """
#         Encrypt with 3DES-CBC (recommended mode).
#         A random 8-byte IV is prepended.

#         Args:
#             plaintext: Input text
#             password:  Key password
#             three_key: Use 3-key (192-bit) or 2-key (112-bit) variant

#         Returns:
#             Base64-encoded (IV || ciphertext).

#         Example:
#             >>> ct = TripleDESCipher.encrypt_cbc("Legacy system data", "bankkey")
#             >>> TripleDESCipher.decrypt_cbc(ct, "bankkey")
#             'Legacy system data'
#         """
#         if not plaintext: raise ValueError("Plaintext cannot be empty")
#         key    = TripleDESCipher._derive_key(password, three_key)
#         iv     = get_random_bytes(8)
#         cipher = DES3.new(key, DES3.MODE_CBC, iv)
#         ct     = cipher.encrypt(pad(plaintext.encode(), DES3.block_size))
#         return base64.b64encode(iv + ct).decode()

#     @staticmethod
#     def decrypt_cbc(ciphertext_b64: str, password: str, three_key: bool = True) -> str:
#         """Decrypt 3DES-CBC ciphertext."""
#         if not ciphertext_b64: raise ValueError("Ciphertext cannot be empty")
#         key    = TripleDESCipher._derive_key(password, three_key)
#         data   = base64.b64decode(ciphertext_b64)
#         iv, ct = data[:8], data[8:]
#         cipher = DES3.new(key, DES3.MODE_CBC, iv)
#         return unpad(cipher.decrypt(ct), DES3.block_size).decode()


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     plaintext = "Banking transaction data"
#     password  = "legacykey"

#     print("=" * 55)
#     print("TRIPLE DES (3DES) DEMO")
#     print("=" * 55)
#     for variant, three_key in [("3-key (168-bit effective)", True), ("2-key (112-bit effective)", False)]:
#         print(f"\n── {variant} ──")
#         for mode, enc, dec in [
#             ("ECB", TripleDESCipher.encrypt_ecb, TripleDESCipher.decrypt_ecb),
#             ("CBC", TripleDESCipher.encrypt_cbc, TripleDESCipher.decrypt_cbc),
#         ]:
#             ct = enc(plaintext, password, three_key)
#             pt = dec(ct, password, three_key)
#             print(f"  {mode}: {ct[:40]}…  ✓" if pt == plaintext else f"  {mode}: MISMATCH ✗")


"""
Triple DES (3DES / TDEA) - Symmetric Block Cipher
Applies DES three times with two or three independent keys.
168-bit key (112-bit effective security due to meet-in-the-middle).
"""
import hashlib
import base64
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class TripleDESCipher:
    BLOCK_SIZE = 8    # 64-bit block (same as DES)
    KEY_SIZE = 24     # 192-bit key (168 effective)

    @staticmethod
    def _derive_key(key: str) -> bytes:
        """Derive a 24-byte 3DES key from a string using SHA-256."""
        return hashlib.sha256(key.encode()).digest()[:24]

    @staticmethod
    def encrypt(text: str, key: str) -> str:
        """Encrypt text using 3DES-CBC. Returns Base64-encoded string."""
        if not text:
            raise ValueError("Text cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        k = TripleDESCipher._derive_key(key)
        iv = get_random_bytes(TripleDESCipher.BLOCK_SIZE)
        cipher = DES3.new(k, DES3.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(text.encode('utf-8'), DES3.block_size))
        return base64.b64encode(iv + encrypted).decode()

    @staticmethod
    def decrypt(encrypted_b64: str, key: str) -> str:
        """Decrypt 3DES-CBC ciphertext from Base64."""
        if not encrypted_b64:
            raise ValueError("Ciphertext cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        k = TripleDESCipher._derive_key(key)
        data = base64.b64decode(encrypted_b64)
        iv, ciphertext = data[:8], data[8:]
        cipher = DES3.new(k, DES3.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), DES3.block_size).decode('utf-8')

    @staticmethod
    def get_info() -> str:
        return (
            "Triple DES (3DES / TDEA)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Block size     : 64 bits\n"
            "Key size       : 168 effective bits (3 × 56)\n"
            "Rounds         : 48 Feistel rounds (16 × 3)\n"
            "Security       : ~112-bit (meet-in-the-middle)\n"
            "Status         : ⚠ Deprecated (NIST 2023) – use AES\n"
            "Still used in  : legacy banking / payment systems"
        )
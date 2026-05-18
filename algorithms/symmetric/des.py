# # import hashlib
# # import base64
# # from Crypto.Cipher import DES
# # from Crypto.Util.Padding import pad, unpad
# # from Crypto.Random import get_random_bytes

# # class DESCipher:
# #     """DES block cipher (56-bit key, legacy)"""
    
# #     @staticmethod
# #     def encrypt(text, key):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         if not key:
# #             raise ValueError("Key cannot be empty")
        
# #         key = hashlib.md5(key.encode()).digest()[:8]
# #         iv = get_random_bytes(8)
# #         cipher = DES.new(key, DES.MODE_CBC, iv)
# #         padded = pad(text.encode(), DES.block_size)
# #         encrypted = cipher.encrypt(padded)
# #         return base64.b64encode(iv + encrypted).decode()
    
# #     @staticmethod
# #     def decrypt(encrypted_b64, key):
# #         if not encrypted_b64:
# #             raise ValueError("Ciphertext cannot be empty")
# #         if not key:
# #             raise ValueError("Key cannot be empty")
        
# #         key = hashlib.md5(key.encode()).digest()[:8]
# #         data = base64.b64decode(encrypted_b64)
# #         iv = data[:8]
# #         ciphertext = data[8:]
# #         cipher = DES.new(key, DES.MODE_CBC, iv)
# #         decrypted = unpad(cipher.decrypt(ciphertext), DES.block_size)
# #         return decrypted.decode()


# """
# DES — Data Encryption Standard
# Modern Symmetric Cryptography | TP2

# Specification:
#   Block size : 64 bits (8 bytes)
#   Key size   : 56 bits effective (64-bit input, 8 parity bits discarded)
#   Rounds     : 16 rounds using a Feistel network
#   Status     : BROKEN — vulnerable to exhaustive key search (EFF DES Cracker, 1998)
#                Replaced by 3DES and then AES.

# Feistel network structure (each round):
#   1. Split 64-bit block into L (left 32 bits) and R (right 32 bits)
#   2. L_new = R
#   3. R_new = L XOR F(R, round_key)
#   Where F = Expansion → XOR round key → S-box substitution → Permutation

# Uses PyCryptodome (pip install pycryptodome).
# """

# import hashlib
# import base64
# from Crypto.Cipher import DES
# from Crypto.Util.Padding import pad, unpad
# from Crypto.Random import get_random_bytes


# class DESCipher:
#     """DES block cipher — CBC and ECB modes."""

#     @staticmethod
#     def _derive_key(password: str) -> bytes:
#         """Derive an 8-byte DES key from a password string."""
#         return hashlib.md5(password.encode()).digest()[:8]

#     # ── ECB mode ─────────────────────────────────────────────────────────────

#     @staticmethod
#     def encrypt_ecb(plaintext: str, password: str) -> str:
#         """
#         Encrypt with DES-ECB.
#         ⚠️ ECB mode is insecure — identical 8-byte blocks produce identical output.

#         Args:
#             plaintext: Input text
#             password:  Key password (derived to 8 bytes)

#         Returns:
#             Base64-encoded ciphertext.
#         """
#         if not plaintext: raise ValueError("Plaintext cannot be empty")
#         key    = DESCipher._derive_key(password)
#         cipher = DES.new(key, DES.MODE_ECB)
#         ct     = cipher.encrypt(pad(plaintext.encode(), DES.block_size))
#         return base64.b64encode(ct).decode()

#     @staticmethod
#     def decrypt_ecb(ciphertext_b64: str, password: str) -> str:
#         """Decrypt DES-ECB ciphertext."""
#         if not ciphertext_b64: raise ValueError("Ciphertext cannot be empty")
#         key    = DESCipher._derive_key(password)
#         cipher = DES.new(key, DES.MODE_ECB)
#         return unpad(cipher.decrypt(base64.b64decode(ciphertext_b64)), DES.block_size).decode()

#     # ── CBC mode ─────────────────────────────────────────────────────────────

#     @staticmethod
#     def encrypt_cbc(plaintext: str, password: str) -> str:
#         """
#         Encrypt with DES-CBC.
#         A random 8-byte IV is prepended to the ciphertext.

#         Args:
#             plaintext: Input text
#             password:  Key password

#         Returns:
#             Base64-encoded (IV || ciphertext).

#         Example:
#             >>> ct = DESCipher.encrypt_cbc("Hello DES!", "secret")
#             >>> DESCipher.decrypt_cbc(ct, "secret")
#             'Hello DES!'
#         """
#         if not plaintext: raise ValueError("Plaintext cannot be empty")
#         key    = DESCipher._derive_key(password)
#         iv     = get_random_bytes(8)
#         cipher = DES.new(key, DES.MODE_CBC, iv)
#         ct     = cipher.encrypt(pad(plaintext.encode(), DES.block_size))
#         return base64.b64encode(iv + ct).decode()

#     @staticmethod
#     def decrypt_cbc(ciphertext_b64: str, password: str) -> str:
#         """Decrypt DES-CBC ciphertext."""
#         if not ciphertext_b64: raise ValueError("Ciphertext cannot be empty")
#         key    = DESCipher._derive_key(password)
#         data   = base64.b64decode(ciphertext_b64)
#         iv, ct = data[:8], data[8:]
#         cipher = DES.new(key, DES.MODE_CBC, iv)
#         return unpad(cipher.decrypt(ct), DES.block_size).decode()

#     @staticmethod
#     def key_info(password: str) -> dict:
#         """Return information about the derived DES key."""
#         key = DESCipher._derive_key(password)
#         return {
#             "key_hex":        key.hex(),
#             "key_bits":       len(key) * 8,
#             "effective_bits": 56,   # 8 parity bits removed
#             "block_size":     64,
#             "rounds":         16,
#             "status":         "BROKEN — do not use for new systems",
#         }


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     plaintext = "Secret DES message"
#     password  = "testkey"

#     print("=" * 55)
#     print("DES (DATA ENCRYPTION STANDARD) DEMO")
#     print("=" * 55)
#     info = DESCipher.key_info(password)
#     for k, v in info.items():
#         print(f"  {k:<18}: {v}")
#     print()

#     for mode, enc, dec in [
#         ("ECB", DESCipher.encrypt_ecb, DESCipher.decrypt_ecb),
#         ("CBC", DESCipher.encrypt_cbc, DESCipher.decrypt_cbc),
#     ]:
#         ct = enc(plaintext, password)
#         pt = dec(ct, password)
#         print(f"DES-{mode}:")
#         print(f"  Plaintext  : {plaintext}")
#         print(f"  Ciphertext : {ct}")
#         print(f"  Decrypted  : {pt}")
#         print(f"  Match      : {pt == plaintext}")
#         print()


"""
DES (Data Encryption Standard) - Symmetric Block Cipher
56-bit effective key size; considered BROKEN for modern use.
Included for educational/historical purposes only.
"""
import hashlib
import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class DESCipher:
    BLOCK_SIZE = 8   # 64-bit block
    KEY_SIZE = 8     # 64-bit key (56 effective bits)

    @staticmethod
    def _derive_key(key: str) -> bytes:
        """Derive an 8-byte DES key from a string using MD5."""
        return hashlib.md5(key.encode()).digest()[:8]

    @staticmethod
    def encrypt(text: str, key: str) -> str:
        """Encrypt text using DES-CBC. Returns Base64-encoded string."""
        if not text:
            raise ValueError("Text cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        k = DESCipher._derive_key(key)
        iv = get_random_bytes(DESCipher.BLOCK_SIZE)
        cipher = DES.new(k, DES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(text.encode('utf-8'), DES.block_size))
        return base64.b64encode(iv + encrypted).decode()

    @staticmethod
    def decrypt(encrypted_b64: str, key: str) -> str:
        """Decrypt DES-CBC ciphertext from Base64."""
        if not encrypted_b64:
            raise ValueError("Ciphertext cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        k = DESCipher._derive_key(key)
        data = base64.b64decode(encrypted_b64)
        iv, ciphertext = data[:8], data[8:]
        cipher = DES.new(k, DES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), DES.block_size).decode('utf-8')

    @staticmethod
    def get_info() -> str:
        return (
            "DES (Data Encryption Standard)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Block size     : 64 bits\n"
            "Key size       : 56 effective bits\n"
            "Rounds         : 16 Feistel rounds\n"
            "Status         : ⚠ BROKEN – do NOT use in production\n"
            "Broken by      : EFF DES Cracker (1998) in < 3 days\n"
            "Replacement    : AES or 3DES"
        )
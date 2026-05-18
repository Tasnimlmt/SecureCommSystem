# # import base64
# # from Crypto.Cipher import ARC4

# # class RC4Cipher:
# #     """RC4 stream cipher"""
    
# #     @staticmethod
# #     def encrypt(text, key):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         if not key:
# #             raise ValueError("Key cannot be empty")
        
# #         cipher = ARC4.new(key.encode())
# #         encrypted = cipher.encrypt(text.encode())
# #         return base64.b64encode(encrypted).decode()
    
# #     @staticmethod
# #     def decrypt(encrypted_b64, key):
# #         if not encrypted_b64:
# #             raise ValueError("Ciphertext cannot be empty")
# #         if not key:
# #             raise ValueError("Key cannot be empty")
        
# #         data = base64.b64decode(encrypted_b64)
# #         cipher = ARC4.new(key.encode())
# #         return cipher.decrypt(data).decode()\



# """
# RC4 — Rivest Cipher 4 (Stream Cipher)
# Modern Symmetric Cryptography | TP2

# Principle: Generates a pseudo-random keystream using a variable-length key
#   and XORs it byte-by-byte with the plaintext.
#   Encrypt/Decrypt: C_i = P_i XOR KS_i  (XOR is self-inverse)

# Algorithm:
#   1. Key Scheduling Algorithm (KSA):
#      Initialize S = [0..255], then permute using the key.
#   2. Pseudo-Random Generation Algorithm (PRGA):
#      Generate keystream bytes from S; update S on each byte.

# Key size: 1 to 256 bytes (typically 40-2048 bits)
# Status  : BROKEN — multiple vulnerabilities discovered:
#   • Fluhrer-Mantin-Shamir attack (WEP key recovery)
#   • RC4 NOMORE attack (HTTPS/TLS session cookie recovery)
#   Removed from TLS 1.3. Do NOT use in new systems.
# Historical use: WEP, WPA-TKIP, SSL/TLS (deprecated), Bluetooth E0.
# """

# import base64
# from Crypto.Cipher import ARC4


# class RC4Cipher:
#     """
#     RC4 stream cipher — encrypt and decrypt using XOR keystream.
#     Uses PyCryptodome's ARC4 implementation.
#     """

#     @staticmethod
#     def encrypt(plaintext: str, key: str) -> str:
#         """
#         Encrypt plaintext with RC4.

#         Args:
#             plaintext: Input text (UTF-8)
#             key:       Key string (any length; longer is better)

#         Returns:
#             Base64-encoded ciphertext.

#         Example:
#             >>> ct = RC4Cipher.encrypt("Hello RC4!", "secretkey")
#             >>> RC4Cipher.decrypt(ct, "secretkey")
#             'Hello RC4!'
#         """
#         if not plaintext: raise ValueError("Plaintext cannot be empty")
#         if not key:       raise ValueError("Key cannot be empty")
#         cipher = ARC4.new(key.encode())
#         ct     = cipher.encrypt(plaintext.encode())
#         return base64.b64encode(ct).decode()

#     @staticmethod
#     def decrypt(ciphertext_b64: str, key: str) -> str:
#         """
#         Decrypt RC4 ciphertext.

#         Args:
#             ciphertext_b64: Base64-encoded ciphertext
#             key:            Same key used during encryption

#         Returns:
#             Recovered plaintext string.
#         """
#         if not ciphertext_b64: raise ValueError("Ciphertext cannot be empty")
#         if not key:            raise ValueError("Key cannot be empty")
#         data   = base64.b64decode(ciphertext_b64)
#         cipher = ARC4.new(key.encode())
#         return cipher.decrypt(data).decode()

#     @staticmethod
#     def generate_keystream(key: str, length: int) -> bytes:
#         """
#         Generate the raw RC4 keystream (educational — shows the PRGA output).

#         Args:
#             key:    Key string
#             length: Number of keystream bytes to generate

#         Returns:
#             Keystream as bytes.
#         """
#         cipher = ARC4.new(key.encode())
#         return cipher.encrypt(bytes(length))   # XOR with zeros = raw keystream

#     @staticmethod
#     def encrypt_raw(key: str) -> tuple:
#         """
#         Manual RC4 implementation (educational — shows KSA + PRGA explicitly).

#         Returns:
#             (S_initial, S_after_KSA, first_16_keystream_bytes)
#         """
#         key_bytes = key.encode()
#         # KSA
#         S = list(range(256))
#         j = 0
#         for i in range(256):
#             j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
#             S[i], S[j] = S[j], S[i]
#         S_ksa = list(S)
#         # PRGA — generate 16 keystream bytes
#         i = j = 0
#         ks = []
#         for _ in range(16):
#             i = (i + 1) % 256
#             j = (j + S[i]) % 256
#             S[i], S[j] = S[j], S[i]
#             ks.append(S[(S[i] + S[j]) % 256])
#         return S_ksa[:8], bytes(ks)


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     plaintext = "This is encrypted with RC4"
#     key       = "SecretKey123"

#     ct = RC4Cipher.encrypt(plaintext, key)
#     pt = RC4Cipher.decrypt(ct, key)

#     print("=" * 55)
#     print("RC4 STREAM CIPHER DEMO")
#     print("=" * 55)
#     print(f"Key        : {key}")
#     print(f"Plaintext  : {plaintext}")
#     print(f"Ciphertext : {ct}")
#     print(f"Decrypted  : {pt}")
#     print(f"Match      : {pt == plaintext}")
#     print()
#     ks = RC4Cipher.generate_keystream(key, 16)
#     print(f"First 16 keystream bytes: {ks.hex()}")
#     print()
#     print("⚠️  SECURITY NOTE:")
#     print("  RC4 is cryptographically broken.")
#     print("  Known attacks: FMS, RC4 NOMORE, Fluhrer-Mantin-Shamir.")
#     print("  Removed from TLS 1.3. Use AES-GCM or ChaCha20 instead.")


"""
RC4 (Rivest Cipher 4) - Symmetric Stream Cipher
Generates a pseudo-random keystream XORed with the plaintext.
Fast but BROKEN; do NOT use in production (WEP, SSL/TLS deprecated it).
"""
import base64
from Crypto.Cipher import ARC4


class RC4Cipher:
    @staticmethod
    def _ksa(key: bytes) -> list:
        """Key Scheduling Algorithm (KSA) – returns the initial S-box."""
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    @staticmethod
    def _prga(S: list, length: int) -> bytes:
        """Pseudo-Random Generation Algorithm (PRGA) – generates keystream."""
        i = j = 0
        keystream = []
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            keystream.append(S[(S[i] + S[j]) % 256])
        return bytes(keystream)

    @staticmethod
    def encrypt(text: str, key: str) -> str:
        """Encrypt text using RC4 stream cipher. Returns Base64 string."""
        if not text:
            raise ValueError("Text cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        cipher = ARC4.new(key.encode('utf-8'))
        encrypted = cipher.encrypt(text.encode('utf-8'))
        return base64.b64encode(encrypted).decode()

    @staticmethod
    def decrypt(encrypted_b64: str, key: str) -> str:
        """Decrypt RC4 ciphertext from Base64."""
        if not encrypted_b64:
            raise ValueError("Ciphertext cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        data = base64.b64decode(encrypted_b64)
        cipher = ARC4.new(key.encode('utf-8'))
        return cipher.decrypt(data).decode('utf-8')

    @staticmethod
    def show_keystream(key: str, length: int = 16) -> str:
        """Show first N bytes of the keystream (educational)."""
        key_bytes = key.encode('utf-8')
        S = RC4Cipher._ksa(key_bytes)
        keystream = RC4Cipher._prga(S, length)
        return ' '.join(f'{b:02X}' for b in keystream)

    @staticmethod
    def get_info() -> str:
        return (
            "RC4 (Rivest Cipher 4) – Stream Cipher\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Type       : Stream cipher (byte-oriented)\n"
            "Key size   : 40–2048 bits (variable)\n"
            "Speed      : Very fast (software)\n"
            "Status     : ⚠ BROKEN – forbidden in TLS since RFC 7465\n"
            "Weaknesses : Biased keystream, WEP attacks, BEAST/POODLE\n"
            "Replacement: AES-GCM or ChaCha20-Poly1305"
        )
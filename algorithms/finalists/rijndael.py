"""
Rijndael – AES Competition Winner (became AES / FIPS 197)
Designed by Joan Daemen and Vincent Rijmen (Belgium).
"""
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class RijndaelInfo:
    NAME = "Rijndael (AES Winner)"
    DESIGNERS = "Joan Daemen & Vincent Rijmen (Belgium)"
    ROUNDS = {128: 10, 192: 12, 256: 14}
    BLOCK_SIZE = 128   # bits
    KEY_SIZES = [128, 192, 256]

    @staticmethod
    def encrypt(text: str, key: str, key_bits: int = 256) -> str:
        """Encrypt using Rijndael (AES) in CBC mode."""
        if not text or not key:
            raise ValueError("Text and key cannot be empty")
        key_bytes = hashlib.sha256(key.encode()).digest()
        if key_bits == 128:
            key_bytes = key_bytes[:16]
        elif key_bits == 192:
            key_bytes = key_bytes[:24]
        iv = get_random_bytes(16)
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(text.encode(), AES.block_size))
        return base64.b64encode(iv + encrypted).decode()

    @staticmethod
    def decrypt(ciphertext_b64: str, key: str, key_bits: int = 256) -> str:
        """Decrypt Rijndael (AES) CBC ciphertext."""
        if not ciphertext_b64 or not key:
            raise ValueError("Ciphertext and key cannot be empty")
        key_bytes = hashlib.sha256(key.encode()).digest()
        if key_bits == 128:
            key_bytes = key_bytes[:16]
        elif key_bits == 192:
            key_bytes = key_bytes[:24]
        data = base64.b64decode(ciphertext_b64)
        iv, ct = data[:16], data[16:]
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()

    @staticmethod
    def get_info() -> str:
        return (
            "Rijndael (AES – Advanced Encryption Standard)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Designers  : Joan Daemen & Vincent Rijmen (Belgium)\n"
            "Rounds     : 10 (128-bit key), 12 (192), 14 (256)\n"
            "Block size : 128 bits\n"
            "Key sizes  : 128 / 192 / 256 bits\n"
            "Structure  : Substitution-Permutation Network (SPN)\n"
            "Operations : SubBytes, ShiftRows, MixColumns, AddRoundKey\n"
            "Status     : ✓ AES WINNER – FIPS 197 standard\n"
            "Why it won : Fast on hardware AND software, elegant math,\n"
            "             no IP restrictions, flexible key/block sizes"
        )
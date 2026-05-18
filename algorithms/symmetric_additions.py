"""
Symmetric additions: AES-ECB mode
Drop this into algorithms/symmetric.py (append to existing file)
"""
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESECBCipher:
    """
    AES-256 in ECB (Electronic Codebook) mode.

    ⚠  ECB is deterministic and does NOT hide data patterns.
    Identical plaintext blocks always produce identical ciphertext blocks.
    It is included here for educational / comparison purposes only.
    """

    @staticmethod
    def _make_key(key: str, bits: int = 256) -> bytes:
        h = hashlib.sha512(key.encode()).digest()
        return h[: bits // 8]

    @staticmethod
    def encrypt(plaintext: str, key: str, bits: int = 256) -> str:
        """
        Encrypt *plaintext* with AES-ECB.
        Returns Base64-encoded ciphertext (no IV – ECB has none).
        """
        k = AESECBCipher._make_key(key, bits)
        cipher = AES.new(k, AES.MODE_ECB)
        ct = cipher.encrypt(pad(plaintext.encode("utf-8"), 16))
        return base64.b64encode(ct).decode()

    @staticmethod
    def decrypt(b64_ciphertext: str, key: str, bits: int = 256) -> str:
        """
        Decrypt a Base64 AES-ECB ciphertext.
        """
        k = AESECBCipher._make_key(key, bits)
        ct = base64.b64decode(b64_ciphertext)
        cipher = AES.new(k, AES.MODE_ECB)
        return unpad(cipher.decrypt(ct), 16).decode("utf-8")

    @staticmethod
    def get_info() -> str:
        return (
            "AES-ECB (Electronic Codebook Mode)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Block size : 128 bits (16 bytes)\n"
            "Key sizes  : 128 / 192 / 256 bits\n"
            "IV         : None (ECB has no IV)\n\n"
            "How it works:\n"
            "  Each 16-byte plaintext block is independently encrypted:\n"
            "    C_i = AES_K(P_i)\n\n"
            "⚠  SECURITY WARNING:\n"
            "  • ECB does NOT provide semantic security.\n"
            "  • Identical plaintext blocks → identical ciphertext blocks.\n"
            "  • Never use ECB for real data — use CBC or GCM instead.\n"
            "  • The 'ECB penguin' is the classic demonstration of this flaw.\n\n"
            "Educational use: compare ECB vs CBC on repeated-block plaintexts\n"
            "to see the pattern-leakage problem clearly."
        )
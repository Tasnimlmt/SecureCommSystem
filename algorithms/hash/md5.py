# # import hashlib

# # class MD5Hash:
# #     """MD5 hash function (128-bit, broken for collisions)"""
    
# #     @staticmethod
# #     def hash(data):
# #         if not data:
# #             raise ValueError("Data cannot be empty")
# #         return hashlib.md5(data.encode()).hexdigest()\\\


# """
# MD5 — Message Digest 5 (Ron Rivest, 1991)
# Hash Functions | TP4

# Output : 128-bit (32 hex chars)
# Status : BROKEN — collision attacks demonstrated (Wang et al., 2004)
#          Two different inputs can produce the same MD5 hash.
#          Do NOT use for security-critical applications.
# Use for: Non-security checksums, legacy system compatibility.

# Structure (Merkle-Damgård):
#   • Message padded to multiple of 512 bits
#   • Processed in 512-bit blocks
#   • 4 rounds × 16 operations = 64 operations per block
#   • State: four 32-bit words (A, B, C, D)
# """

# import hashlib
# import struct


# class MD5:
#     """MD5 hash — wraps Python's hashlib for correctness, shows internals."""

#     @staticmethod
#     def hash(data: str | bytes) -> str:
#         """
#         Compute MD5 hash.

#         Args:
#             data: Input string or bytes

#         Returns:
#             32-character hexadecimal digest.

#         Example:
#             >>> MD5.hash("hello")
#             '5d41402abc4b2a76b9719d911017c592'
#         """
#         if isinstance(data, str):
#             data = data.encode("utf-8")
#         return hashlib.md5(data).hexdigest()

#     @staticmethod
#     def hash_file(filepath: str) -> str:
#         """Compute MD5 of a file (for integrity checking only, NOT security)."""
#         h = hashlib.md5()
#         with open(filepath, "rb") as f:
#             for chunk in iter(lambda: f.read(8192), b""):
#                 h.update(chunk)
#         return h.hexdigest()

#     @staticmethod
#     def demonstrate_avalanche(text: str) -> dict:
#         """
#         Show the avalanche effect: changing 1 bit produces a completely different hash.

#         Returns:
#             Dict with original and modified hash, and bit difference count.
#         """
#         h1       = MD5.hash(text)
#         modified = text[:-1] + chr(ord(text[-1]) ^ 1) if text else "x"
#         h2       = MD5.hash(modified)
#         bits1    = bin(int(h1, 16))[2:].zfill(128)
#         bits2    = bin(int(h2, 16))[2:].zfill(128)
#         diff     = sum(a != b for a, b in zip(bits1, bits2))
#         return {
#             "original":      text,
#             "modified":      modified,
#             "hash_original": h1,
#             "hash_modified": h2,
#             "bits_different": diff,
#             "percentage":    f"{diff/128*100:.1f}%",
#         }


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     print("=" * 55)
#     print("MD5 HASH DEMO")
#     print("=" * 55)
#     for msg in ["", "hello", "Hello", "The quick brown fox"]:
#         print(f"MD5({repr(msg)}) = {MD5.hash(msg)}")
#     print()
#     av = MD5.demonstrate_avalanche("hello")
#     print(f"Avalanche effect:")
#     print(f"  '{av['original']}' → {av['hash_original']}")
#     print(f"  '{av['modified']}' → {av['hash_modified']}")
#     print(f"  Bits changed: {av['bits_different']}/128 ({av['percentage']})")
#     print("\n⚠️  MD5 is BROKEN — collision attacks exist since 2004.")


"""
MD5 (Message Digest 5) - Cryptographic Hash Function
128-bit (16-byte) output. BROKEN – collision attacks found in 1996.
Do NOT use for security; included for educational/legacy purposes.
"""
import hashlib


class MD5Hash:
    DIGEST_SIZE = 16     # bytes
    DIGEST_BITS = 128

    @staticmethod
    def hash(data: str) -> str:
        """Return MD5 hex digest of the input string."""
        if not data:
            raise ValueError("Input cannot be empty")
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_bytes(data: bytes) -> str:
        """Return MD5 hex digest of raw bytes."""
        return hashlib.md5(data).hexdigest()

    @staticmethod
    def verify(data: str, expected_hash: str) -> bool:
        """Verify data against an expected MD5 hash."""
        return MD5Hash.hash(data) == expected_hash.lower()

    @staticmethod
    def get_info() -> str:
        return (
            "MD5 (Message Digest 5)\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Output     : 128 bits (32 hex chars)\n"
            "Designed   : Ronald Rivest, 1991\n"
            "Status     : ⚠ BROKEN – collision found (Wang & Yu, 2004)\n"
            "Weaknesses : Collision attacks, preimage speed\n"
            "Safe uses  : Non-security checksums, file deduplication\n"
            "Replacement: SHA-256 or SHA-3"
        )
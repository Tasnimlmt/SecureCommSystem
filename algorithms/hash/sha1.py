# # import hashlib

# # class SHA1Hash:
# #     """SHA-1 hash function (160-bit, weak)"""
    
# #     @staticmethod
# #     def hash(data):
# #         if not data:
# #             raise ValueError("Data cannot be empty")
# #         return hashlib.sha1(data.encode()).hexdigest()

# """
# SHA-1 — Secure Hash Algorithm 1 (NIST, 1995)
# Hash Functions | TP4

# Output : 160-bit (40 hex chars)
# Status : BROKEN — SHAttered collision attack (Google/CWI, 2017)
#          Two different PDF files were produced with the same SHA-1 hash.
#          Deprecated by NIST in 2011; removed from TLS in 2019.
# Use for: Legacy compatibility only. Use SHA-256 or SHA-3 for new systems.

# Structure (Merkle-Damgård):
#   • Message padded to multiple of 512 bits
#   • Processed in 512-bit blocks with 80 rounds
#   • State: five 32-bit words (H0..H4)
# """

# import hashlib


# class SHA1:
#     """SHA-1 hash — wraps hashlib."""

#     @staticmethod
#     def hash(data: str | bytes) -> str:
#         """
#         Compute SHA-1 hash.

#         Args:
#             data: Input string or bytes

#         Returns:
#             40-character hexadecimal digest.

#         Example:
#             >>> SHA1.hash("hello")
#             'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
#         """
#         if isinstance(data, str):
#             data = data.encode("utf-8")
#         return hashlib.sha1(data).hexdigest()

#     @staticmethod
#     def compare(data1: str, data2: str) -> dict:
#         """Compare SHA-1 hashes of two inputs."""
#         h1, h2 = SHA1.hash(data1), SHA1.hash(data2)
#         return {
#             "input1": data1, "hash1": h1,
#             "input2": data2, "hash2": h2,
#             "equal":  h1 == h2,
#         }


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     print("=" * 55)
#     print("SHA-1 HASH DEMO")
#     print("=" * 55)
#     for msg in ["hello", "Hello", "The quick brown fox jumps over the lazy dog"]:
#         print(f"SHA1({repr(msg[:20])}) = {SHA1.hash(msg)}")
#     print("\n⚠️  SHA-1 is BROKEN — SHAttered attack (2017) found a collision.")
#     print("   Replace with SHA-256, SHA-3, or BLAKE2.")

"""
SHA-1 (Secure Hash Algorithm 1) - Cryptographic Hash Function
160-bit (20-byte) output. BROKEN – practical collision found (SHAttered, 2017).
Do NOT use for security; use SHA-256 or SHA-3 instead.
"""
import hashlib


class SHA1Hash:
    DIGEST_SIZE = 20     # bytes
    DIGEST_BITS = 160

    @staticmethod
    def hash(data: str) -> str:
        """Return SHA-1 hex digest of the input string."""
        if not data:
            raise ValueError("Input cannot be empty")
        return hashlib.sha1(data.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_bytes(data: bytes) -> str:
        """Return SHA-1 hex digest of raw bytes."""
        return hashlib.sha1(data).hexdigest()

    @staticmethod
    def verify(data: str, expected_hash: str) -> bool:
        """Verify data against an expected SHA-1 hash."""
        return SHA1Hash.hash(data) == expected_hash.lower()

    @staticmethod
    def get_info() -> str:
        return (
            "SHA-1 (Secure Hash Algorithm 1)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Output     : 160 bits (40 hex chars)\n"
            "Designed   : NSA / NIST, 1993\n"
            "Status     : ⚠ BROKEN – SHAttered collision (Google, 2017)\n"
            "Weaknesses : Collision attack with 2⁶³·¹ operations\n"
            "Safe uses  : Git commit IDs (non-security context)\n"
            "Replacement: SHA-256, SHA-384, SHA-3"
        )
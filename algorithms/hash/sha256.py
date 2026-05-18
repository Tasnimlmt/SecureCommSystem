# # import hashlib

# # class SHA256Hash:
# #     """SHA-256 hash function (256-bit, secure)"""
    
# #     @staticmethod
# #     def hash(data):
# #         if not data:
# #             raise ValueError("Data cannot be empty")
# #         return hashlib.sha256(data.encode()).hexdigest()


# """
# SHA-256 — Secure Hash Algorithm 256 (NIST FIPS 180-4, 2001)
# Hash Functions | TP4

# Output : 256-bit (64 hex chars)
# Status : SECURE — no known practical attacks as of 2025.
# Use for: Password hashing (with salt), HMAC, digital certificates,
#          blockchain (Bitcoin PoW), file integrity, TLS 1.3.

# Structure (Merkle-Damgård with Davies-Meyer compression):
#   • Message padded to multiple of 512 bits
#   • Processed in 512-bit blocks with 64 rounds
#   • State: eight 32-bit words (H0..H7) initialised from √prime constants
#   • Operations per round: Ch, Maj, Σ0, Σ1, σ0, σ1 (bitwise + modular addition)

# SHA-2 family: SHA-224, SHA-256, SHA-384, SHA-512 (and truncated variants)
# """

# import hashlib


# class SHA256:
#     """SHA-256 and SHA-224 hash functions."""

#     @staticmethod
#     def hash(data: str | bytes) -> str:
#         """
#         Compute SHA-256 hash.

#         Args:
#             data: Input string or bytes

#         Returns:
#             64-character hexadecimal digest.

#         Example:
#             >>> SHA256.hash("hello")
#             '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
#         """
#         if isinstance(data, str):
#             data = data.encode("utf-8")
#         return hashlib.sha256(data).hexdigest()

#     @staticmethod
#     def hash_224(data: str | bytes) -> str:
#         """Compute SHA-224 hash (truncated SHA-256 with different IV)."""
#         if isinstance(data, str):
#             data = data.encode("utf-8")
#         return hashlib.sha224(data).hexdigest()

#     @staticmethod
#     def hash_file(filepath: str) -> str:
#         """Compute SHA-256 of a file for integrity verification."""
#         h = hashlib.sha256()
#         with open(filepath, "rb") as f:
#             for chunk in iter(lambda: f.read(8192), b""):
#                 h.update(chunk)
#         return h.hexdigest()

#     @staticmethod
#     def verify_integrity(data: str | bytes, expected_hash: str) -> bool:
#         """Check if data matches an expected SHA-256 hash."""
#         return SHA256.hash(data) == expected_hash

#     @staticmethod
#     def demonstrate_avalanche(text: str) -> dict:
#         """Show avalanche effect: 1-bit input change → ~50% output bits change."""
#         h1       = SHA256.hash(text)
#         modified = text + "x" if text else "x"
#         h2       = SHA256.hash(modified)
#         bits1    = bin(int(h1, 16))[2:].zfill(256)
#         bits2    = bin(int(h2, 16))[2:].zfill(256)
#         diff     = sum(a != b for a, b in zip(bits1, bits2))
#         return {
#             "original":       text,
#             "modified":       modified,
#             "hash_original":  h1,
#             "hash_modified":  h2,
#             "bits_different": diff,
#             "percentage":     f"{diff/256*100:.1f}%",
#         }


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     print("=" * 65)
#     print("SHA-256 (SHA-2 FAMILY) DEMO")
#     print("=" * 65)
#     test_vectors = [
#         ("", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
#         ("hello", "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"),
#         ("The quick brown fox jumps over the lazy dog",
#          "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"),
#     ]
#     print("Known test vectors:")
#     for msg, expected in test_vectors:
#         result  = SHA256.hash(msg)
#         status  = "✓" if result == expected else "✗"
#         print(f"  {status} SHA256({repr(msg[:30])}) = {result[:32]}…")
#     print()
#     av = SHA256.demonstrate_avalanche("hello")
#     print(f"Avalanche effect (add 'x'):")
#     print(f"  Bits changed: {av['bits_different']}/256 ({av['percentage']})")
#     print(f"  (ideal ≈ 50%)")


"""
SHA-256 (Secure Hash Algorithm 256-bit) - Cryptographic Hash Function
Part of the SHA-2 family; 256-bit (32-byte) output.
Current standard for digital signatures, certificates, and Bitcoin mining.
"""
import hashlib
import hmac


class SHA256Hash:
    DIGEST_SIZE = 32     # bytes
    DIGEST_BITS = 256

    @staticmethod
    def hash(data: str) -> str:
        """Return SHA-256 hex digest of the input string."""
        if not data:
            raise ValueError("Input cannot be empty")
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_bytes(data: bytes) -> str:
        """Return SHA-256 hex digest of raw bytes."""
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def verify(data: str, expected_hash: str) -> bool:
        """Verify data against an expected SHA-256 hash."""
        return SHA256Hash.hash(data) == expected_hash.lower()

    @staticmethod
    def double_hash(data: str) -> str:
        """SHA-256 applied twice (used in Bitcoin)."""
        first = hashlib.sha256(data.encode('utf-8')).digest()
        return hashlib.sha256(first).hexdigest()

    @staticmethod
    def get_info() -> str:
        return (
            "SHA-256 (Secure Hash Algorithm 256-bit)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Output     : 256 bits (64 hex chars)\n"
            "Designed   : NSA / NIST, 2001 (SHA-2 family)\n"
            "Status     : ✓ SECURE – no known practical attacks\n"
            "Security   : 2¹²⁸ collision resistance\n"
            "Uses       : TLS, code signing, Bitcoin, JWT\n"
            "Standard   : FIPS 180-4"
        )
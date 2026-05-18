# import hashlib

# class SHA512Hash:
#     """SHA-512 hash function (512-bit, secure)"""
    
#     @staticmethod
#     def hash(data):
#         if not data:
#             raise ValueError("Data cannot be empty")
#         return hashlib.sha512(data.encode()).hexdigest()

"""
SHA-512 (Secure Hash Algorithm 512-bit) - Cryptographic Hash Function
Part of the SHA-2 family; 512-bit (64-byte) output.
Preferred over SHA-256 on 64-bit platforms due to wider internal state.
"""
import hashlib


class SHA512Hash:
    DIGEST_SIZE = 64     # bytes
    DIGEST_BITS = 512

    @staticmethod
    def hash(data: str) -> str:
        """Return SHA-512 hex digest of the input string."""
        if not data:
            raise ValueError("Input cannot be empty")
        return hashlib.sha512(data.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_bytes(data: bytes) -> str:
        """Return SHA-512 hex digest of raw bytes."""
        return hashlib.sha512(data).hexdigest()

    @staticmethod
    def verify(data: str, expected_hash: str) -> bool:
        """Verify data against an expected SHA-512 hash."""
        return SHA512Hash.hash(data) == expected_hash.lower()

    @staticmethod
    def sha512_256(data: str) -> str:
        """SHA-512/256 truncated variant (faster on 64-bit, same security as SHA-256)."""
        return hashlib.new('sha512_256', data.encode('utf-8')).hexdigest()

    @staticmethod
    def get_info() -> str:
        return (
            "SHA-512 (Secure Hash Algorithm 512-bit)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Output     : 512 bits (128 hex chars)\n"
            "Designed   : NSA / NIST, 2001 (SHA-2 family)\n"
            "Status     : ✓ SECURE – 2²⁵⁶ collision resistance\n"
            "Speed      : Faster than SHA-256 on 64-bit CPUs\n"
            "Uses       : Password hashing, high-security signing\n"
            "Standard   : FIPS 180-4"
        )
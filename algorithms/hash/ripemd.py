# import hashlib

# class RIPEMDHash:
#     """RIPEMD-160 hash function"""
    
#     @staticmethod
#     def hash160(data):
#         if not data:
#             raise ValueError("Data cannot be empty")
#         return hashlib.new('ripemd160', data.encode()).hexdigest()

"""
RIPEMD-160 (RACE Integrity Primitives Evaluation Message Digest)
160-bit hash function developed in Europe as an alternative to SHA.
Used in Bitcoin address generation (combined with SHA-256).
"""
import hashlib


class RIPEMDHash:
    @staticmethod
    def hash(data: str) -> str:
        """Return RIPEMD-160 hex digest of the input string."""
        if not data:
            raise ValueError("Input cannot be empty")
        h = hashlib.new('ripemd160')
        h.update(data.encode('utf-8'))
        return h.hexdigest()

    @staticmethod
    def hash_bytes(data: bytes) -> str:
        """Return RIPEMD-160 hex digest of raw bytes."""
        h = hashlib.new('ripemd160')
        h.update(data)
        return h.hexdigest()

    @staticmethod
    def verify(data: str, expected_hash: str) -> bool:
        """Verify data against an expected RIPEMD-160 hash."""
        return RIPEMDHash.hash(data) == expected_hash.lower()

    @staticmethod
    def bitcoin_address_hash(sha256_hash: bytes) -> str:
        """
        Compute RIPEMD-160(SHA-256(data)) – used in Bitcoin P2PKH addresses.
        Pass already-SHA256-hashed bytes.
        """
        h = hashlib.new('ripemd160')
        h.update(sha256_hash)
        return h.hexdigest()

    @staticmethod
    def get_info() -> str:
        return (
            "RIPEMD-160 (RACE Integrity Primitives Evaluation MD)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Output     : 160 bits (40 hex chars)\n"
            "Designed   : Hans Dobbertin et al., 1996 (Europe)\n"
            "Status     : ✓ No known practical attacks\n"
            "Uses       : Bitcoin address derivation (HASH160)\n"
            "Bitcoin    : Address = RIPEMD160(SHA256(pubkey))\n"
            "Note       : Slower than SHA-2 but European alternative"
        )
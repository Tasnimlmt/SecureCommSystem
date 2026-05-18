# import hmac
# import hashlib

# class HMACFunction:
#     """HMAC - Hash-based Message Authentication Code"""
    
#     @staticmethod
#     def hmac_sha256(key, message):
#         if not key:
#             raise ValueError("Key cannot be empty")
#         if not message:
#             raise ValueError("Message cannot be empty")
#         return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()


"""
HMAC (Hash-based Message Authentication Code)
Combines a secret key with a hash function to provide message authentication.
Provides both integrity and authenticity verification.
"""
import hmac
import hashlib


class HMACAuth:
    @staticmethod
    def sign(message: str, key: str, algorithm: str = 'sha256') -> str:
        """
        Create an HMAC tag for a message.
        algorithm: 'sha256' | 'sha512' | 'sha1' | 'md5'
        """
        if not message:
            raise ValueError("Message cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        h = hmac.new(key.encode('utf-8'), message.encode('utf-8'), algorithm)
        return h.hexdigest()

    @staticmethod
    def verify(message: str, key: str, tag: str, algorithm: str = 'sha256') -> bool:
        """
        Verify an HMAC tag in constant time (resistant to timing attacks).
        Returns True if valid, False otherwise.
        """
        expected = HMACAuth.sign(message, key, algorithm)
        return hmac.compare_digest(expected, tag.lower())

    @staticmethod
    def sign_sha256(message: str, key: str) -> str:
        """Shorthand: HMAC-SHA256."""
        return HMACAuth.sign(message, key, 'sha256')

    @staticmethod
    def sign_sha512(message: str, key: str) -> str:
        """Shorthand: HMAC-SHA512."""
        return HMACAuth.sign(message, key, 'sha512')

    @staticmethod
    def get_info() -> str:
        return (
            "HMAC (Hash-based Message Authentication Code)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Formula    : HMAC(K, M) = H((K⊕opad) ∥ H((K⊕ipad) ∥ M))\n"
            "Provides   : Integrity + Authenticity (not confidentiality)\n"
            "Algorithms : HMAC-SHA256 (recommended), HMAC-SHA512\n"
            "Security   : As strong as the underlying hash\n"
            "Uses       : JWT signatures, API authentication, TLS MACs\n"
            "Standard   : FIPS 198-1, RFC 2104"
        )
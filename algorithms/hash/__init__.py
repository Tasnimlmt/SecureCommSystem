# from algorithms.hash.md5 import MD5Hash
# from algorithms.hash.sha1 import SHA1Hash
# from algorithms.hash.sha256 import SHA256Hash
# from algorithms.hash.sha512 import SHA512Hash
# from algorithms.hash.ripemd import RIPEMDHash
# from algorithms.hash.hmac import HMACFunction
# from algorithms.hash.index_of_coincidence import IndexOfCoincidence


"""
Hash Functions Package
Contains: MD5, SHA-1, SHA-256, SHA-512, RIPEMD-160, HMAC,
          Index of Coincidence
"""
from .md5 import MD5Hash
from .sha1 import SHA1Hash
from .sha256 import SHA256Hash
from .sha512 import SHA512Hash
from .ripemd import RIPEMDHash
from .hmac import HMACAuth
from .index_of_coincidence import IndexOfCoincidence

__all__ = [
    'MD5Hash', 'SHA1Hash', 'SHA256Hash', 'SHA512Hash',
    'RIPEMDHash', 'HMACAuth', 'IndexOfCoincidence',
]
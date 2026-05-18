"""
Configuration for Secure Communication System
"""

# Network Configuration
DEFAULT_PORT = 8443
DEFAULT_HOST = 'localhost'

# Cryptographic Configuration
RSA_KEY_SIZES = [1024, 2048, 3072, 4096]
DEFAULT_RSA_SIZE = 2048
AES_KEY_SIZES = [128, 192, 256]
DEFAULT_AES_SIZE = 256
DH_PRIME_BITS = 2048

# Protocol Versions
TLS_VERSION = '1.3'
SIGNATURE_SCHEME = 'PSS'  # PKCS1v15 or PSS
HASH_ALGORITHM = 'SHA-256'

# Security Parameters
PERFECT_FORWARD_SECRECY = True
SESSION_TIMEOUT = 3600  # seconds
MAX_MESSAGE_SIZE = 65536  # bytes

# Voting Configuration
HOMOMORPHIC_SCHEME = 'Paillier'  # or 'ElGamal'
PAILLIER_KEY_SIZE = 2048

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/secure_comm.log'

# AES Finalists Configuration
FINALISTS = {
    'Rijndael': {'winner': True, 'rounds': 10, 'priority': 1},
    'Twofish': {'winner': False, 'rounds': 16, 'priority': 2},
    'Serpent': {'winner': False, 'rounds': 32, 'priority': 3},
    'RC6': {'winner': False, 'rounds': 20, 'priority': 4},
    'MARS': {'winner': False, 'rounds': 32, 'priority': 5}
}
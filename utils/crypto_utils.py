# """
# Cryptographic Utilities - Integration of all algorithms
# """
# import base64
# import hashlib
# import os
# import json
# from Crypto.Cipher import AES, DES, DES3, ARC4
# from Crypto.PublicKey import RSA
# from Crypto.Random import get_random_bytes
# from Crypto.Util.Padding import pad, unpad

# class CryptoUtils:
#     """Utility class integrating all cryptographic algorithms"""
    
#     @staticmethod
#     def generate_aes_key(key_size=256):
#         """Generate AES key of specified size"""
#         return get_random_bytes(key_size // 8)
    
#     @staticmethod
#     def generate_rsa_keypair(key_size=2048):
#         """Generate RSA key pair"""
#         key = RSA.generate(key_size)
#         return key.export_key().decode(), key.publickey().export_key().decode()
    
#     @staticmethod
#     def rsa_encrypt(message, public_key_pem):
#         """Encrypt with RSA public key"""
#         key = RSA.import_key(public_key_pem)
#         cipher = PKCS1_OAEP.new(key)
#         return base64.b64encode(cipher.encrypt(message.encode())).decode()
    
#     @staticmethod
#     def rsa_decrypt(ciphertext_b64, private_key_pem):
#         """Decrypt with RSA private key"""
#         key = RSA.import_key(private_key_pem)
#         cipher = PKCS1_OAEP.new(key)
#         return cipher.decrypt(base64.b64decode(ciphertext_b64)).decode()
    
#     @staticmethod
#     def aes_encrypt(plaintext, key, mode='CBC'):
#         """AES encryption with multiple modes"""
#         if mode == 'ECB':
#             cipher = AES.new(key, AES.MODE_ECB)
#             return cipher.encrypt(pad(plaintext.encode(), AES.block_size))
#         elif mode == 'CBC':
#             iv = get_random_bytes(AES.block_size)
#             cipher = AES.new(key, AES.MODE_CBC, iv)
#             return iv + cipher.encrypt(pad(plaintext.encode(), AES.block_size))
#         elif mode == 'CTR':
#             nonce = get_random_bytes(8)
#             cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
#             return nonce + cipher.encrypt(plaintext.encode())
    
#     @staticmethod
#     def aes_decrypt(ciphertext, key, mode='CBC'):
#         """AES decryption"""
#         if mode == 'ECB':
#             cipher = AES.new(key, AES.MODE_ECB)
#             return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
#         elif mode == 'CBC':
#             iv = ciphertext[:AES.block_size]
#             cipher = AES.new(key, AES.MODE_CBC, iv)
#             return unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size).decode()
#         elif mode == 'CTR':
#             nonce = ciphertext[:8]
#             cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
#             return cipher.decrypt(ciphertext[8:]).decode()
    
#     @staticmethod
#     def des_encrypt(plaintext, key):
#         """DES encryption (legacy)"""
#         cipher = DES.new(key, DES.MODE_CBC)
#         iv = cipher.iv
#         encrypted = cipher.encrypt(pad(plaintext.encode(), DES.block_size))
#         return iv + encrypted
    
#     @staticmethod
#     def triple_des_encrypt(plaintext, key):
#         """3DES encryption"""
#         cipher = DES3.new(key, DES3.MODE_CBC)
#         iv = cipher.iv
#         encrypted = cipher.encrypt(pad(plaintext.encode(), DES3.block_size))
#         return iv + encrypted
    
#     @staticmethod
#     def rc4_encrypt(plaintext, key):
#         """RC4 stream cipher (legacy, insecure)"""
#         cipher = ARC4.new(key)
#         return cipher.encrypt(plaintext.encode())
    
#     @staticmethod
#     def sha256_hash(data):
#         """SHA-256 hash"""
#         return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()
    
#     @staticmethod
#     def sha512_hash(data):
#         """SHA-512 hash"""
#         return hashlib.sha512(data.encode() if isinstance(data, str) else data).hexdigest()
    
#     @staticmethod
#     def md5_hash(data):
#         """MD5 hash (insecure, for checksum only)"""
#         return hashlib.md5(data.encode() if isinstance(data, str) else data).hexdigest()
    
#     @staticmethod
#     def hmac_sha256(key, message):
#         """HMAC for message authentication"""
#         import hmac
#         return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

# class ClassicalCiphers:
#     @staticmethod
#     def caesar(text, shift):
#         result = []
#         for c in text.upper():
#             if c.isalpha():
#                 result.append(chr(((ord(c) - ord('A') + shift) % 26) + ord('A')))
#             else:
#                 result.append(c)
#         return ''.join(result)
    
#     @staticmethod
#     def vigenere(text, key, decrypt=False):
#         key = key.upper()
#         result = []
#         key_idx = 0
#         for c in text.upper():
#             if c.isalpha():
#                 shift = ord(key[key_idx % len(key)]) - ord('A')
#                 if decrypt:
#                     shift = -shift
#                 result.append(chr(((ord(c) - ord('A') + shift) % 26) + ord('A')))
#                 key_idx += 1
#             else:
#                 result.append(c)
#         return ''.join(result)

# class AESFinalistsComparison:
#     @staticmethod
#     def compare_all(data_size=1024*1024):
#         """Compare all 5 AES finalists"""
#         import time
#         from algorithms.symmetric.aes import AESFinalistComparison
        
#         comparator = AESFinalistComparison()
#         results = comparator.benchmark_all(data_size)
        
#         print("\n" + "="*70)
#         print("🏆 AES FINALISTS PERFORMANCE COMPARISON 🏆")
#         print("="*70)
#         print(f"{'Algorithm':<20} {'Time (s)':<12} {'Throughput (MB/s)':<15}")
#         print("-"*70)
        
#         for name, data in sorted(results.items(), key=lambda x: x[1]['time']):
#             winner = "🥇 WINNER" if name == 'Rijndael (AES)' else ""
#             print(f"{name:<20} {data['time']:<12.3f} {data['throughput']:<15.2f} {winner}")
        
#         return results


"""
Cryptographic Utilities - Integration of all algorithms
"""
import hashlib
import hmac
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class CryptoUtils:
    @staticmethod
    def generate_aes_key(key_size=256):
        return os.urandom(key_size // 8)
    
    @staticmethod
    def sha256_hash(data):
        return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()
    
    @staticmethod
    def sha512_hash(data):
        return hashlib.sha512(data.encode() if isinstance(data, str) else data).hexdigest()
    
    @staticmethod
    def md5_hash(data):
        return hashlib.md5(data.encode() if isinstance(data, str) else data).hexdigest()
    
    @staticmethod
    def hmac_sha256(key, message):
        if isinstance(key, str):
            key = key.encode()
        return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()
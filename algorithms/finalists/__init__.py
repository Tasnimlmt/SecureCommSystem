# # algorithms/finalists/__init__.py
# """
# AES Finalists - NIST Competition 1997-2000
# Rijndael (Winner), Twofish, Serpent, RC6, MARS
# """

# class Rijndael:
#     """Rijndael - Winner of AES competition"""
#     name = "Rijndael (AES)"
#     rounds = 10
#     block_size = 128
#     key_sizes = [128, 192, 256]
    
#     @staticmethod
#     def encrypt(block, key):
#         # Simplified simulation - actual implementation would be full AES
#         return f"Rijndael_encrypted_{block}_{key[:8]}"

# class Twofish:
#     """Twofish - Bruce Schneier's algorithm"""
#     name = "Twofish"
#     rounds = 16
#     block_size = 128
#     key_sizes = [128, 192, 256]

# class Serpent:
#     """Serpent - Most secure but slowest"""
#     name = "Serpent"
#     rounds = 32
#     block_size = 128
#     key_sizes = [128, 192, 256]

# class RC6:
#     """RC6 - Ron Rivest's algorithm"""
#     name = "RC6"
#     rounds = 20
#     block_size = 128
#     key_sizes = [128, 192, 256]

# class MARS:
#     """MARS - IBM's algorithm"""
#     name = "MARS"
#     rounds = 32
#     block_size = 128
#     key_sizes = [128, 192, 256]


"""
AES Finalists Package (NIST Competition 1997–2000)
Five algorithms competed; Rijndael won and became AES.
Contains: Rijndael (AES), Twofish, Serpent, RC6, MARS
"""
from .rijndael import RijndaelInfo
from .twofish import TwofishInfo
from .serpent import SerpentInfo
from .rc6 import RC6Info
from .mars import MARSInfo

__all__ = ['RijndaelInfo', 'TwofishInfo', 'SerpentInfo', 'RC6Info', 'MARSInfo']

COMPARISON_TABLE = """
╔══════════════╦════════╦════════════╦══════════╦══════════╦═══════════════╗
║  Algorithm   ║ Rounds ║  Block     ║ Key Size ║  Speed   ║ Security      ║
╠══════════════╬════════╬════════════╬══════════╬══════════╬═══════════════╣
║ Rijndael✓   ║ 10/12/ ║ 128 bits   ║ 128/192/ ║ Fast     ║ High          ║
║  (AES)       ║   14   ║            ║  256 bit ║          ║               ║
╠══════════════╬════════╬════════════╬══════════╬══════════╬═══════════════╣
║ Twofish      ║   16   ║ 128 bits   ║ 128/192/ ║ Fast     ║ High          ║
║              ║        ║            ║  256 bit ║          ║               ║
╠══════════════╬════════╬════════════╬══════════╬══════════╬═══════════════╣
║ Serpent      ║   32   ║ 128 bits   ║ 128/192/ ║ Slow     ║ Highest       ║
║              ║        ║            ║  256 bit ║          ║ margin        ║
╠══════════════╬════════╬════════════╬══════════╬══════════╬═══════════════╣
║ RC6          ║   20   ║ 128 bits   ║ 128/192/ ║ Fast     ║ High          ║
║              ║        ║            ║  256 bit ║          ║               ║
╠══════════════╬════════╬════════════╬══════════╬══════════╬═══════════════╣
║ MARS         ║   32   ║ 128 bits   ║ 128–448  ║ Moderate ║ High          ║
║              ║        ║            ║   bits   ║          ║               ║
╚══════════════╩════════╩════════════╩══════════╩══════════╩═══════════════╝
"""
"""
RC6 – AES Finalist
Designed by Ron Rivest, Matt Robshaw, Ray Sidney, and Yiqun Lisa Yin (RSA Security, USA).
Evolution of RC5 with data-dependent rotations and multiplication.
"""


class RC6Info:
    NAME = "RC6"
    DESIGNERS = "Ron Rivest, Matt Robshaw, Ray Sidney, Yiqun Lisa Yin (RSA Security)"
    ROUNDS = 20
    BLOCK_SIZE = 128    # bits (uses four 32-bit registers)
    KEY_SIZES = [128, 192, 256]

    @staticmethod
    def get_info() -> str:
        return (
            "RC6 – AES Finalist (4th place)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Designers  : Ron Rivest et al. (RSA Security, USA)\n"
            "Rounds     : 20\n"
            "Block size : 128 bits (4 × 32-bit registers A, B, C, D)\n"
            "Key sizes  : 128 / 192 / 256 bits\n"
            "Structure  : Feistel-like with 4 registers\n"
            "Features   :\n"
            "  • Data-dependent rotations (key feature of RC5)\n"
            "  • Integer multiplication for fast diffusion\n"
            "  • Very fast on 32-bit platforms\n"
            "  • Evolved from RC5 (adding 4-register structure)\n"
            "Status     : No known practical attacks; not selected\n"
            "Why not AES: IP concerns (RSA Security held patents)\n"
            "             Rijndael had no IP restrictions"
        )

    @staticmethod
    def get_structure_description() -> str:
        return (
            "RC6 Structure (r=20 rounds):\n"
            "  Input split into: A, B, C, D (each 32 bits)\n"
            "     ↓ Pre-whitening: B += S[0],  D += S[1]\n"
            "  20 × rounds:\n"
            "     ├── t = (B * (2B+1)) <<< lg_w\n"
            "     ├── u = (D * (2D+1)) <<< lg_w\n"
            "     ├── A = ((A⊕t) <<< u) + S[2i]\n"
            "     ├── C = ((C⊕u) <<< t) + S[2i+1]\n"
            "     └── (A,B,C,D) = (B,C,D,A)\n"
            "     ↓ Post-whitening: A += S[2r+2],  C += S[2r+3]\n"
            "  Output: A, B, C, D\n"
        )
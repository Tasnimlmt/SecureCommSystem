"""
Serpent – AES Finalist
Designed by Ross Anderson, Eli Biham, and Lars Knudsen.
Most conservative security margin of all five finalists (32 rounds).
"""


class SerpentInfo:
    NAME = "Serpent"
    DESIGNERS = "Ross Anderson, Eli Biham, Lars Knudsen"
    ROUNDS = 32
    BLOCK_SIZE = 128    # bits
    KEY_SIZES = [128, 192, 256]

    @staticmethod
    def get_info() -> str:
        return (
            "Serpent – AES Finalist (3rd place, highest security margin)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Designers  : Ross Anderson, Eli Biham, Lars Knudsen\n"
            "Rounds     : 32 (most of any finalist)\n"
            "Block size : 128 bits\n"
            "Key sizes  : 128 / 192 / 256 bits\n"
            "Structure  : Substitution-Permutation Network (SPN)\n"
            "Features   :\n"
            "  • 8 fixed S-boxes (4-bit), applied 4 times per round\n"
            "  • Designed for bitsliced implementation\n"
            "  • Extremely conservative security margin\n"
            "  • Simple, easy-to-analyze structure\n"
            "Status     : No known attacks; not selected\n"
            "Why not AES: Too slow (2× slower than Rijndael in software)\n"
            "Supporters : Those who preferred security over speed"
        )

    @staticmethod
    def get_structure_description() -> str:
        return (
            "Serpent Structure:\n"
            "  Input (128 bits)\n"
            "     ↓ IP (Initial Permutation)\n"
            "  32 × rounds:\n"
            "     ├── Key mixing (XOR with 128-bit subkey)\n"
            "     ├── S-box layer (32 × 4-bit S-boxes in parallel)\n"
            "     └── Linear transformation (diffusion)\n"
            "  Final round: key mixing, no linear transform\n"
            "     ↓ FP (Final Permutation)\n"
            "  Output (128 bits)\n"
        )
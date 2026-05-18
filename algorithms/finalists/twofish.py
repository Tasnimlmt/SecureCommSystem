"""
Twofish – AES Finalist
Designed by Bruce Schneier et al. (Counterpane Internet Security, USA).
A Feistel cipher with key-dependent S-boxes and MDS matrix.
"""


class TwofishInfo:
    NAME = "Twofish"
    DESIGNERS = "Bruce Schneier et al. (Counterpane, USA)"
    ROUNDS = 16
    BLOCK_SIZE = 128    # bits
    KEY_SIZES = [128, 192, 256]

    @staticmethod
    def get_info() -> str:
        return (
            "Twofish – AES Finalist (2nd place)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Designers  : Bruce Schneier et al. (Counterpane, USA)\n"
            "Rounds     : 16\n"
            "Block size : 128 bits\n"
            "Key sizes  : 128 / 192 / 256 bits\n"
            "Structure  : Feistel network\n"
            "Features   :\n"
            "  • Key-dependent S-boxes (based on Maximum Distance\n"
            "    Separable / MDS matrices)\n"
            "  • Highly efficient on 32-bit CPUs\n"
            "  • Pre-whitening and post-whitening\n"
            "  • Pseudo-Hadamard Transform (PHT)\n"
            "Status     : No known practical attacks; not selected\n"
            "Why not AES: Rijndael was faster on embedded/hardware"
        )

    @staticmethod
    def get_structure_description() -> str:
        return (
            "Twofish Structure:\n"
            "  Input (128 bits)\n"
            "     ↓ Input whitening (XOR with 4 key words)\n"
            "  16 × Feistel rounds:\n"
            "     ├── Left half → g() function (key-dep. S-boxes + MDS)\n"
            "     ├── Right half → g() function (rotated 8 bits)\n"
            "     ├── PHT + round subkeys\n"
            "     └── Swap halves (except last round)\n"
            "     ↓ Output whitening (XOR with 4 key words)\n"
            "  Output (128 bits)\n"
        )
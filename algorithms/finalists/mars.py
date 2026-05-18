"""
MARS – AES Finalist
Designed by a team at IBM Research (USA).
Complex heterogeneous cipher combining multiple operations.
"""


class MARSInfo:
    NAME = "MARS"
    DESIGNERS = "IBM Research Team (USA)"
    ROUNDS = 32
    BLOCK_SIZE = 128    # bits (four 32-bit words)
    KEY_SIZES = list(range(128, 449, 32))   # 128 to 448 bits

    @staticmethod
    def get_info() -> str:
        return (
            "MARS – AES Finalist (5th place)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Designers  : IBM Research (Coppersmith, Grover, et al.)\n"
            "Rounds     : 32 (8 forward mixing + 16 cryptographic core\n"
            "             + 8 backward mixing)\n"
            "Block size : 128 bits (four 32-bit words)\n"
            "Key sizes  : 128 to 448 bits (variable, in 32-bit steps)\n"
            "Structure  : Heterogeneous (unique, complex design)\n"
            "Features   :\n"
            "  • Three distinct phases: forward mixing,\n"
            "    cryptographic core, backward mixing\n"
            "  • Data-dependent rotations\n"
            "  • Large fixed S-boxes (4KB)\n"
            "  • Key-dependent addition and XOR\n"
            "Status     : No known practical attacks; not selected\n"
            "Why not AES: Overly complex design; harder to analyze;\n"
            "             slower key schedule"
        )

    @staticmethod
    def get_structure_description() -> str:
        return (
            "MARS Structure:\n"
            "  Input: 4 × 32-bit words (A, B, C, D)\n"
            "     ↓ Phase 1 – Forward Mixing (8 rounds)\n"
            "       Add key words, XOR, rotate, use E-box\n"
            "     ↓ Phase 2 – Cryptographic Core (16 rounds)\n"
            "       Alternating forward and backward keyed\n"
            "       transformations with S-boxes\n"
            "     ↓ Phase 3 – Backward Mixing (8 rounds)\n"
            "       Inverse of forward mixing\n"
            "  Output: 4 × 32-bit words\n"
        )
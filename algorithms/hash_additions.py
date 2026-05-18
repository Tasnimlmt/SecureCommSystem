"""
Hash / theory additions:
  - Merkle–Damgård Construction  (visual demonstration)
  - Kerckhoffs' Principle         (informational + quiz)
  - Kasiski Test                  (Vigenère key-length attack)
"""

import hashlib
import math
import struct
from collections import Counter


# ════════════════════════════════════════════════════════════════
#  1. Merkle–Damgård Construction
# ════════════════════════════════════════════════════════════════

class MerkleDamgard:
    """
    Demonstrates the Merkle–Damgård (MD) construction used by MD5, SHA-1,
    SHA-256, etc.

    A *toy* 64-bit hash is implemented step-by-step so every compression
    round is visible; real SHA-256 is also run in parallel for comparison.
    """

    # ── Toy compression function (Davies-Meyer style, 64-bit) ──────────────
    _IV64 = 0x6A09E667F3BCC908  # truncated SHA-256 IV word

    @staticmethod
    def _compress64(h: int, block_bytes: bytes) -> int:
        """Very simplified 64-bit compression: XOR + rotate + add."""
        val = int.from_bytes(block_bytes[:8], "big")
        h = ((h ^ val) + 0xBB67AE8584CAA73B) & 0xFFFFFFFFFFFFFFFF
        h = ((h << 13) | (h >> 51)) & 0xFFFFFFFFFFFFFFFF
        h = (h ^ int.from_bytes(block_bytes[8:], "big")) & 0xFFFFFFFFFFFFFFFF
        return h

    @staticmethod
    def _md_pad(message: bytes) -> bytes:
        """
        Merkle–Damgård strengthening:
          append 0x80, then 0x00 bytes, then 64-bit big-endian bit-length.
        Block size = 16 bytes (toy).
        """
        length = len(message)
        message += b"\x80"
        # pad to 8 bytes short of next 16-byte boundary
        while (len(message) % 16) != 8:
            message += b"\x00"
        message += struct.pack(">Q", length * 8)
        return message

    @staticmethod
    def hash_toy(message: str) -> tuple[str, list[dict]]:
        """
        Run the toy MD construction.
        Returns (hex_digest, list_of_round_dicts).
        Each round dict has: block_index, block_hex, h_in, h_out.
        """
        msg = message.encode("utf-8")
        padded = MerkleDamgard._md_pad(msg)
        h = MerkleDamgard._IV64
        rounds = []
        for i in range(0, len(padded), 16):
            block = padded[i : i + 16]
            h_in = h
            h = MerkleDamgard._compress64(h, block)
            rounds.append(
                {
                    "block_index": i // 16,
                    "block_hex": block.hex(),
                    "h_in": f"{h_in:016x}",
                    "h_out": f"{h:016x}",
                }
            )
        return f"{h:016x}", rounds

    @staticmethod
    def hash_sha256(message: str) -> str:
        return hashlib.sha256(message.encode()).hexdigest()

    @staticmethod
    def get_full_report(message: str) -> str:
        toy_digest, rounds = MerkleDamgard.hash_toy(message)
        sha256_digest = MerkleDamgard.hash_sha256(message)

        lines = [
            "=" * 60,
            "MERKLE–DAMGÅRD CONSTRUCTION – STEP-BY-STEP",
            "=" * 60,
            "",
            f"Input message : {message!r}",
            f"Length        : {len(message)} bytes",
            "",
            "─" * 60,
            "PHASE 1 – Padding (MD Strengthening)",
            "─" * 60,
            "  Append 0x80 (binary 1 bit)",
            "  Append 0x00 bytes until len ≡ 8 (mod 16)   [toy block=16]",
            "  Append 64-bit big-endian bit-count",
            "",
            "─" * 60,
            "PHASE 2 – Compression Rounds",
            "─" * 60,
            f"  IV (H₀) = {MerkleDamgard._IV64:016x}",
            "",
        ]

        for r in rounds:
            lines.append(
                f"  Block {r['block_index']:2d} | {r['block_hex']}\n"
                f"          H_in  = {r['h_in']}\n"
                f"          H_out = {r['h_out']}"
            )
        lines += [
            "",
            "─" * 60,
            "RESULTS",
            "─" * 60,
            f"  Toy 64-bit digest : {toy_digest}",
            f"  Real SHA-256      : {sha256_digest}",
            "",
            "─" * 60,
            MerkleDamgard.get_info(),
        ]
        return "\n".join(lines)

    @staticmethod
    def get_info() -> str:
        return (
            "MERKLE–DAMGÅRD CONSTRUCTION\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Invented independently by Ralph Merkle and Ivan Damgård (1989).\n"
            "Underlies MD4, MD5, SHA-1, SHA-256, SHA-512.\n\n"
            "Core idea:\n"
            "  H(m) = f( f( f(IV, b₁), b₂ ), … bₙ )\n"
            "  where f is a one-way compression function and\n"
            "  bᵢ are fixed-size blocks of the padded message.\n\n"
            "Security property:\n"
            "  If f is collision-resistant, so is H.\n\n"
            "Known weakness – length-extension attack:\n"
            "  An attacker who knows H(m) can compute H(m ‖ padding ‖ extra)\n"
            "  without knowing m.  SHA-3 (Keccak sponge) is immune to this."
        )


# ════════════════════════════════════════════════════════════════
#  2. Kerckhoffs' Principle
# ════════════════════════════════════════════════════════════════

class KerckhoffsPrinciple:
    """
    Informational class covering Kerckhoffs' Principle and its modern
    implications.  Includes a self-test quiz.
    """

    PRINCIPLES = [
        ("1", "The system must be practically, if not mathematically, indecipherable."),
        ("2", "The system must not require secrecy, and can be stolen by the enemy without causing trouble."),
        ("3", "The key must be communicable and retainable without the help of written notes."),
        ("4", "The system must be compatible with telegraph communication."),
        ("5", "The apparatus must be portable, and its use must not require several persons."),
        ("6", "The system must be easy to use, without requiring stress of mind."),
    ]

    QUIZ = [
        {
            "q": "What does Kerckhoffs' 2nd principle state?",
            "options": [
                "A) The key must be secret, but the algorithm may be public.",
                "B) The algorithm must be secret even if the key is known.",
                "C) The system should use a one-time pad.",
                "D) Security through obscurity is sufficient.",
            ],
            "answer": "A",
            "explanation": (
                "Kerckhoffs stated that security should rest solely in the key, "
                "not in keeping the algorithm secret.  This is the foundation of "
                "modern public cryptographic standards (AES, RSA, etc.)."
            ),
        },
        {
            "q": "Shannon's maxim rephrases Kerckhoffs as:",
            "options": [
                "A) 'Trust but verify'",
                "B) 'The enemy knows the system'",
                "C) 'A chain is only as strong as its weakest link'",
                "D) 'Security lies in complexity'",
            ],
            "answer": "B",
            "explanation": (
                "Claude Shannon restated the principle as "
                "'The enemy knows the system' — design under the assumption "
                "that the adversary fully understands your algorithm."
            ),
        },
        {
            "q": "Which approach VIOLATES Kerckhoffs' principle?",
            "options": [
                "A) Publishing AES source code openly.",
                "B) Using a proprietary, secret cipher and keeping the algorithm hidden.",
                "C) Protecting only the encryption key.",
                "D) Open peer review of a new hash function.",
            ],
            "answer": "B",
            "explanation": (
                "Hiding the algorithm ('security through obscurity') violates "
                "Kerckhoffs.  History shows that secret algorithms are frequently "
                "broken once reverse-engineered (e.g., A5/1 in GSM)."
            ),
        },
    ]

    @staticmethod
    def get_info() -> str:
        lines = [
            "=" * 60,
            "KERCKHOFFS' PRINCIPLE  (Auguste Kerckhoffs, 1883)",
            "=" * 60,
            "",
            'Published in "La Cryptographie militaire", Journal des sciences',
            "militaires, January 1883.  Six design principles for military",
            "ciphers:",
            "",
        ]
        for num, text in KerckhoffsPrinciple.PRINCIPLES:
            lines.append(f"  {num}. {text}")
        lines += [
            "",
            "─" * 60,
            "MODERN INTERPRETATION",
            "─" * 60,
            "  The algorithm may be public knowledge.",
            "  Security must depend ONLY on the secrecy of the key.",
            "",
            "  Shannon's maxim: 'The enemy knows the system.'",
            "",
            "  Implications for today:",
            "  • AES, RSA, ECC – all fully published; security = key secrecy.",
            "  • 'Security through obscurity' is not real security.",
            "  • Public algorithms withstand peer review and cryptanalysis.",
            "",
            "  Counter-argument (limited):",
            "  • Some argue adding obscurity as an extra layer (defence-in-depth)",
            "    can raise the cost of attack slightly — but it is never a",
            "    substitute for a strong, key-based system.",
        ]
        return "\n".join(lines)

    @staticmethod
    def get_quiz() -> list[dict]:
        return KerckhoffsPrinciple.QUIZ


# ════════════════════════════════════════════════════════════════
#  3. Kasiski Test
# ════════════════════════════════════════════════════════════════

class KasiskiTest:
    """
    Kasiski Examination – determine the key length of a Vigenère cipher.

    Method:
      1. Find all repeated n-grams (n ≥ 3) in the ciphertext.
      2. Record the distances between each pair of repetitions.
      3. Compute GCD of all distances.
      4. Likely key length = most common factor of those GCDs.
    """

    @staticmethod
    def find_repeats(ciphertext: str, ngram_size: int = 3) -> dict[str, list[int]]:
        """Return {ngram: [positions]} for repeated ngrams."""
        ct = ciphertext.upper().replace(" ", "").replace("\n", "")
        ct = "".join(c for c in ct if c.isalpha())
        ngrams: dict[str, list[int]] = {}
        for i in range(len(ct) - ngram_size + 1):
            ng = ct[i : i + ngram_size]
            ngrams.setdefault(ng, []).append(i)
        return {ng: pos for ng, pos in ngrams.items() if len(pos) > 1}

    @staticmethod
    def compute_distances(repeats: dict[str, list[int]]) -> list[int]:
        """All pairwise distances between occurrences."""
        distances = []
        for positions in repeats.values():
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    distances.append(positions[j] - positions[i])
        return distances

    @staticmethod
    def factor_counts(distances: list[int], max_key: int = 20) -> dict[int, int]:
        """Count how many distances each factor (2..max_key) divides."""
        counts: dict[int, int] = {}
        for d in distances:
            for f in range(2, max_key + 1):
                if d % f == 0:
                    counts[f] = counts.get(f, 0) + 1
        return counts

    @staticmethod
    def analyse(ciphertext: str, ngram_size: int = 3, max_key: int = 20) -> str:
        """Full Kasiski report."""
        ct_clean = "".join(
            c for c in ciphertext.upper() if c.isalpha()
        )
        repeats = KasiskiTest.find_repeats(ciphertext, ngram_size)
        distances = KasiskiTest.compute_distances(repeats)
        factors = KasiskiTest.factor_counts(distances, max_key)
        sorted_factors = sorted(factors.items(), key=lambda x: -x[1])

        lines = [
            "=" * 60,
            "KASISKI EXAMINATION",
            "=" * 60,
            f"Ciphertext length  : {len(ct_clean)} letters",
            f"N-gram size        : {ngram_size}",
            f"Repeated n-grams   : {len(repeats)}",
            f"Total distances    : {len(distances)}",
            "",
            "─" * 60,
            "Top repeated n-grams (first 10):",
            "─" * 60,
        ]

        for ng, pos in list(repeats.items())[:10]:
            dists = [pos[j] - pos[j - 1] for j in range(1, len(pos))]
            g = dists[0]
            for d in dists[1:]:
                g = math.gcd(g, d)
            lines.append(f"  '{ng}'  positions={pos}  GCD={g}")

        lines += [
            "",
            "─" * 60,
            "Factor frequency (likely key lengths):",
            "─" * 60,
        ]

        for factor, count in sorted_factors[:10]:
            bar = "█" * count
            lines.append(f"  Key len {factor:3d}: {count:3d} hits  {bar}")

        if sorted_factors:
            best = sorted_factors[0][0]
            lines += [
                "",
                f"  ► Most likely key length: {best}",
                "",
                "─" * 60,
                KasiskiTest.get_info(),
            ]
        else:
            lines += ["", "  No repeated n-grams found – try a longer ciphertext."]

        return "\n".join(lines)

    @staticmethod
    def get_info() -> str:
        return (
            "KASISKI TEST\n"
            "━━━━━━━━━━━━\n"
            "Invented by Friedrich Kasiski (1863).\n\n"
            "Breaks polyalphabetic (Vigenère) ciphers by exploiting repeated\n"
            "plaintext words encrypted at the same key-stream position.\n\n"
            "Steps:\n"
            "  1. Locate all repeated trigrams (or longer) in the ciphertext.\n"
            "  2. Record the spacing (distance) between each repeated group.\n"
            "  3. The key length most likely divides those distances.\n"
            "  4. GCD of distances → probable key length candidates.\n"
            "  5. Confirm with Index of Coincidence on each column.\n\n"
            "Historical note:\n"
            "  Before Kasiski, Vigenère was called 'le chiffre indéchiffrable'.\n"
            "  Babbage independently discovered the same attack ~1846 but never published."
        )
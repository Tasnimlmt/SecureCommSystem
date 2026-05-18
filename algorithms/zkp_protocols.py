"""
Zero-Knowledge Identification Protocols:
  - Schnorr Identification Protocol
  - Feige–Fiat–Shamir (FFS) Identification Protocol
"""

import hashlib
import random
import sympy


# ════════════════════════════════════════════════════════════════
#  1. Schnorr Identification Protocol
# ════════════════════════════════════════════════════════════════

class SchnorrIdentification:
    """
    Schnorr's interactive zero-knowledge proof of knowledge of a discrete log.

    Setup (public):  prime p, prime q | (p-1), generator g of order q in Z*_p
    Prover secret:   x  (private key, 1 ≤ x < q)
    Prover public:   y = g^x mod p

    Three-move (Σ-protocol) transcript:
      1. Prover  → commitment  r = g^k mod p      (k random in [1, q-1])
      2. Verifier→ challenge   e ∈ {0, …, 2^t-1}  (t-bit random)
      3. Prover  → response    s = (k - x·e) mod q
      Verifier checks: g^s · y^e ≡ r  (mod p)
    """

    @staticmethod
    def generate_params(bits: int = 256, q_bits: int = 128) -> tuple[int, int, int]:
        """
        Generate (p, q, g) for Schnorr.
        p = safe-prime style: p = k·q + 1  with p and q prime.
        For speed, bits are kept small (256/128 by default).
        Returns (p, q, g).
        """
        while True:
            q = sympy.randprime(2 ** (q_bits - 1), 2 ** q_bits)
            # find k so p = k*q+1 is prime
            for _ in range(200):
                k = random.randint(2, 2 ** (bits - q_bits))
                p = k * q + 1
                if sympy.isprime(p):
                    # find generator of order q
                    while True:
                        h = random.randint(2, p - 2)
                        g = pow(h, (p - 1) // q, p)
                        if g > 1:
                            return p, q, g

    @staticmethod
    def generate_keypair(p: int, q: int, g: int) -> tuple[int, int]:
        """
        Returns (x, y):  x = private key,  y = g^x mod p (public key).
        """
        x = random.randint(1, q - 1)
        y = pow(g, x, p)
        return x, y

    @staticmethod
    def run_protocol(
        p: int, q: int, g: int, x: int, y: int, t_bits: int = 80
    ) -> dict:
        """
        Run one full Schnorr proof round.
        Returns a dict with all transcript values and verification result.
        """
        # Step 1 – Commitment
        k = random.randint(1, q - 1)
        r = pow(g, k, p)

        # Step 2 – Challenge (simulated verifier)
        e = random.randint(0, 2**t_bits - 1)

        # Step 3 – Response
        s = (k - x * e) % q

        # Verification
        lhs = (pow(g, s, p) * pow(y, e, p)) % p
        valid = lhs == r

        return {
            "p": p, "q": q, "g": g,
            "private_x": x, "public_y": y,
            "commitment_k": k, "commitment_r": r,
            "challenge_e": e,
            "response_s": s,
            "lhs_verify": lhs,
            "valid": valid,
        }

    @staticmethod
    def full_report(p: int, q: int, g: int, x: int, y: int, rounds: int = 3) -> str:
        lines = [
            "=" * 60,
            "SCHNORR IDENTIFICATION PROTOCOL",
            "=" * 60,
            "",
            "PUBLIC PARAMETERS",
            f"  p (prime)            : {p}",
            f"  q (prime, q | p-1)   : {q}",
            f"  g (generator ord q)  : {g}",
            "",
            "KEYS",
            f"  Private key x        : {x}",
            f"  Public  key y=g^x    : {y}",
            "",
            "─" * 60,
        ]

        for rnd in range(1, rounds + 1):
            res = SchnorrIdentification.run_protocol(p, q, g, x, y)
            lines += [
                f"ROUND {rnd}",
                f"  k (random nonce)     : {res['commitment_k']}",
                f"  r = g^k mod p        : {res['commitment_r']}",
                f"  e (challenge)        : {res['challenge_e']}",
                f"  s = k - x·e  mod q   : {res['response_s']}",
                "",
                f"  VERIFY: g^s · y^e mod p = {res['lhs_verify']}",
                f"          r             = {res['commitment_r']}",
                f"  ✓ Valid              : {res['valid']}",
                "─" * 60,
            ]

        lines.append(SchnorrIdentification.get_info())
        return "\n".join(lines)

    @staticmethod
    def get_info() -> str:
        return (
            "SCHNORR IDENTIFICATION PROTOCOL\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Proposed by Claus-Peter Schnorr (1989).\n\n"
            "Properties:\n"
            "  • Completeness  – honest prover always convinces verifier.\n"
            "  • Soundness     – cheating prover succeeds with prob ≤ 2^{-t}.\n"
            "  • Zero-Knowledge– verifier learns nothing about x beyond y=g^x.\n\n"
            "Three-move Σ-protocol:\n"
            "  Prover  → r = g^k         (commitment)\n"
            "  Verifier→ e               (random challenge)\n"
            "  Prover  → s = k - x·e    (response)\n"
            "  Verifier checks g^s · y^e ≡ r  (mod p)\n\n"
            "Security: Based on hardness of Discrete Logarithm Problem (DLP).\n"
            "Non-interactive version (Fiat-Shamir transform): used in Schnorr signatures."
        )


# ════════════════════════════════════════════════════════════════
#  2. Feige–Fiat–Shamir Identification Protocol
# ════════════════════════════════════════════════════════════════

class FeigeFiatShamir:
    """
    Feige–Fiat–Shamir (FFS) zero-knowledge identification.

    Setup (Trusted Authority):
      Choose n = p·q  (product of two secret primes, kept by TA).
      Publish n.

    Prover (Peggy):
      Secret s ∈ Z*_n,  gcd(s, n) = 1.
      Public v = s^{-2} mod n   (or v = s² mod n depending on variant).
      We use the original: v ≡ s² mod n,  secret = modular sqrt of v.

    Three-move Σ-protocol (t parallel repetitions):
      1. Prover  → x = r² mod n        (r random)
      2. Verifier→ b ∈ {0, 1}
      3. Prover  → y = r · s^b mod n
      Verifier checks y² ≡ x · v^b  (mod n)
    """

    @staticmethod
    def setup(bits: int = 256) -> tuple[int, int, int]:
        """
        Generate n = p·q.  Returns (p, q, n).
        For speed, uses sympy primes of length bits//2.
        """
        half = bits // 2
        p = sympy.randprime(2 ** (half - 1), 2 ** half)
        q = sympy.randprime(2 ** (half - 1), 2 ** half)
        while q == p:
            q = sympy.randprime(2 ** (half - 1), 2 ** half)
        return p, q, p * q

    @staticmethod
    def generate_keypair(n: int) -> tuple[int, int]:
        """
        Returns (s, v): secret s coprime to n, public v = s² mod n.
        """
        while True:
            s = random.randint(2, n - 1)
            if math.gcd(s, n) == 1:
                v = pow(s, 2, n)
                return s, v

    @staticmethod
    def run_protocol(n: int, s: int, v: int, rounds: int = 10) -> dict:
        """
        Simulate 'rounds' parallel FFS rounds.
        Returns transcript and overall verification result.
        """
        transcript = []
        all_valid = True
        for _ in range(rounds):
            r = random.randint(2, n - 1)
            x = pow(r, 2, n)
            b = random.randint(0, 1)
            y = (r * pow(s, b, n)) % n
            lhs = pow(y, 2, n)
            rhs = (x * pow(v, b, n)) % n
            ok = lhs == rhs
            if not ok:
                all_valid = False
            transcript.append({"x": x, "b": b, "y": y, "lhs": lhs, "rhs": rhs, "ok": ok})
        return {"transcript": transcript, "all_valid": all_valid, "rounds": rounds}

    @staticmethod
    def full_report(n: int, s: int, v: int, rounds: int = 5) -> str:
        res = FeigeFiatShamir.run_protocol(n, s, v, rounds)
        lines = [
            "=" * 60,
            "FEIGE–FIAT–SHAMIR IDENTIFICATION PROTOCOL",
            "=" * 60,
            "",
            f"n (public modulus) : {n}",
            f"s (private secret) : {s}",
            f"v = s² mod n       : {v}",
            "",
            "─" * 60,
            f"Running {rounds} parallel rounds …",
            "─" * 60,
        ]
        for i, t in enumerate(res["transcript"], 1):
            lines += [
                f"Round {i}:",
                f"  x = r² mod n      : {t['x']}",
                f"  b (challenge)      : {t['b']}",
                f"  y = r·s^b mod n   : {t['y']}",
                f"  y² mod n          : {t['lhs']}",
                f"  x·v^b mod n       : {t['rhs']}",
                f"  ✓ Valid            : {t['ok']}",
                "",
            ]
        cheat_prob = (1 / 2) ** rounds
        lines += [
            "─" * 60,
            f"Overall valid      : {res['all_valid']}",
            f"Cheating prob      : (1/2)^{rounds} = {cheat_prob:.2e}",
            "",
            "─" * 60,
            FeigeFiatShamir.get_info(),
        ]
        return "\n".join(lines)

    @staticmethod
    def get_info() -> str:
        return (
            "FEIGE–FIAT–SHAMIR (FFS) IDENTIFICATION PROTOCOL\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Proposed by Feige, Fiat & Shamir (1987 / published 1988).\n\n"
            "Based on the hardness of computing modular square roots\n"
            "(equivalent to integer factoring).\n\n"
            "Protocol (one round):\n"
            "  1. Peggy picks random r, sends  x = r² mod n\n"
            "  2. Victor sends challenge bit  b ∈ {0,1}\n"
            "  3. Peggy sends  y = r · s^b mod n\n"
            "  Victor checks:  y² ≡ x · v^b  (mod n)\n\n"
            "Security:\n"
            "  • Cheating prover succeeds in one round with prob 1/2.\n"
            "  • After t rounds: prob ≤ (1/2)^t  (t=40 → prob ≈ 10^{-12}).\n"
            "  • Zero-knowledge: Victor learns only that Peggy knows sqrt(v).\n\n"
            "Applications:\n"
            "  • Smart-card authentication.\n"
            "  • Precursor to modern ZK proofs (zk-SNARKs in blockchains)."
        )


# resolve missing import
import math
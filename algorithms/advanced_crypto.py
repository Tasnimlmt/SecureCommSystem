"""
Advanced crypto algorithms:
  - Shamir's Secret Sharing  (threshold scheme)
  - Paillier Cryptosystem    (additively homomorphic encryption)
"""

import math
import random
import sympy
import functools


# ════════════════════════════════════════════════════════════════
#  1. Shamir's Secret Sharing
# ════════════════════════════════════════════════════════════════

class ShamirSecretSharing:
    """
    (k, n)-threshold secret sharing (Adi Shamir, 1979).

    A secret S is split into n shares so that:
      • Any k shares can reconstruct S (Lagrange interpolation).
      • Any k-1 or fewer shares reveal NOTHING about S.

    All arithmetic is done in Z_p (prime field) with p > max(S, n).
    """

    @staticmethod
    def _coerce_prime(secret: int, n: int) -> int:
        """Pick a prime larger than both secret and n."""
        candidate = max(secret, n) + 1
        while not sympy.isprime(candidate):
            candidate += 1
        return candidate

    @staticmethod
    def split(secret: int, k: int, n: int, prime: int | None = None) -> tuple[int, list[tuple[int, int]]]:
        """
        Split *secret* into *n* shares, requiring *k* to reconstruct.

        Returns (prime, [(x1, y1), …, (xn, yn)]).
        """
        if k > n:
            raise ValueError("Threshold k must be ≤ n.")
        if secret < 0:
            raise ValueError("Secret must be a non-negative integer.")

        if prime is None:
            prime = ShamirSecretSharing._coerce_prime(secret, n)
        if secret >= prime:
            raise ValueError(f"Secret ({secret}) must be < prime ({prime}).")

        # Build random polynomial of degree k-1: f(x) = secret + a1*x + … + a_{k-1}*x^{k-1}
        coeffs = [secret] + [random.randint(1, prime - 1) for _ in range(k - 1)]

        def _poly(x: int) -> int:
            return sum(c * pow(x, i, prime) for i, c in enumerate(coeffs)) % prime

        shares = [(i, _poly(i)) for i in range(1, n + 1)]
        return prime, shares

    @staticmethod
    def reconstruct(shares: list[tuple[int, int]], prime: int) -> int:
        """
        Reconstruct the secret from *any k* shares using Lagrange interpolation.
        shares = [(x1,y1), (x2,y2), …]
        """
        secret = 0
        k = len(shares)
        for i, (xi, yi) in enumerate(shares):
            num = 1
            den = 1
            for j, (xj, _) in enumerate(shares):
                if i != j:
                    num = (num * (-xj)) % prime
                    den = (den * (xi - xj)) % prime
            lagrange = (yi * num * pow(den, -1, prime)) % prime
            secret = (secret + lagrange) % prime
        return secret

    @staticmethod
    def full_report(secret: int, k: int, n: int) -> str:
        prime, shares = ShamirSecretSharing.split(secret, k, n)
        lines = [
            "=" * 60,
            "SHAMIR'S SECRET SHARING",
            "=" * 60,
            "",
            f"Secret           : {secret}",
            f"Threshold k      : {k}  (need k shares to reconstruct)",
            f"Total shares n   : {n}",
            f"Field prime p    : {prime}",
            "",
            "─" * 60,
            "SHARES  (x, y)",
            "─" * 60,
        ]
        for x, y in shares:
            lines.append(f"  Share {x:2d} : ({x}, {y})")

        # Demo: reconstruct with exactly k shares
        test_shares = shares[:k]
        recovered = ShamirSecretSharing.reconstruct(test_shares, prime)
        lines += [
            "",
            "─" * 60,
            f"RECONSTRUCTION using shares {[s[0] for s in test_shares]}:",
            "─" * 60,
            "  Lagrange interpolation at x=0…",
            f"  Recovered secret : {recovered}",
            f"  ✓ Matches        : {recovered == secret}",
            "",
            "─" * 60,
        ]

        # Try k-1 shares (should NOT recover – produces a different value)
        if k > 1:
            partial = shares[: k - 1]
            partial_val = ShamirSecretSharing.reconstruct(partial, prime)
            lines += [
                f"  With only {k-1} shares → gets {partial_val}  (WRONG – information-theoretically secure)",
                "",
                "─" * 60,
            ]

        lines.append(ShamirSecretSharing.get_info())
        return "\n".join(lines)

    @staticmethod
    def get_info() -> str:
        return (
            "SHAMIR'S SECRET SHARING\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Proposed by Adi Shamir (1979).\n\n"
            "Mathematical basis: Polynomial interpolation over a finite field.\n\n"
            "Key properties:\n"
            "  • Perfect secrecy – fewer than k shares leak zero information.\n"
            "  • Threshold flexibility – any k-of-n subset works.\n"
            "  • Additive structure – shares can be combined (useful in MPC).\n\n"
            "How it works:\n"
            "  1. Build f(x) = S + a₁x + a₂x² + … + a_{k-1}x^{k-1}  (in Z_p)\n"
            "  2. Give share (i, f(i)) to party i.\n"
            "  3. Any k parties perform Lagrange interpolation to find f(0) = S.\n\n"
            "Applications:\n"
            "  • Multi-signature cryptocurrency wallets.\n"
            "  • Distributed key management (HSMs, cloud KMS).\n"
            "  • Secure multi-party computation (MPC).\n"
            "  • Certificate authority private-key protection."
        )


# ════════════════════════════════════════════════════════════════
#  2. Paillier Cryptosystem (Additively Homomorphic)
# ════════════════════════════════════════════════════════════════

class PaillierCryptosystem:
    """
    Paillier public-key cryptosystem (Pascal Paillier, 1999).

    Additively homomorphic:
      D( E(m1) · E(m2) mod n² ) = m1 + m2  (mod n)
      D( E(m)^k        mod n² ) = k · m    (mod n)

    Key generation:
      1. Choose primes p, q  with gcd(pq, (p-1)(q-1)) = 1.
      2. n = p·q,  λ = lcm(p-1, q-1)
      3. g = n+1  (simplified variant)
      4. μ = λ⁻¹ mod n
      5. Public key  = (n, g)
         Private key = (λ, μ)

    Encryption of m ∈ [0, n-1]:
      Pick random r, 0 < r < n, gcd(r,n)=1.
      c = g^m · r^n  mod n²

    Decryption:
      m = L(c^λ mod n²) · μ  mod n
      where L(u) = (u-1)/n
    """

    @staticmethod
    def _L(u: int, n: int) -> int:
        return (u - 1) // n

    @staticmethod
    def generate_keypair(bits: int = 256) -> tuple[tuple, tuple]:
        """
        Returns ( (n, g), (lam, mu) ) = (public_key, private_key).
        """
        half = bits // 2
        while True:
            p = sympy.randprime(2 ** (half - 1), 2 ** half)
            q = sympy.randprime(2 ** (half - 1), 2 ** half)
            if p == q:
                continue
            n = p * q
            lam = (p - 1) * (q - 1) // math.gcd(p - 1, q - 1)  # lcm
            if math.gcd(n, lam) == 1:
                break
        g = n + 1          # Simplified variant
        mu = pow(lam, -1, n)
        return (n, g), (lam, mu)

    @staticmethod
    def encrypt(message: int, public_key: tuple) -> int:
        n, g = public_key
        n2 = n * n
        if not (0 <= message < n):
            raise ValueError(f"Message must be in [0, n-1].  n={n}")
        while True:
            r = random.randint(1, n - 1)
            if math.gcd(r, n) == 1:
                break
        c = (pow(g, message, n2) * pow(r, n, n2)) % n2
        return c

    @staticmethod
    def decrypt(ciphertext: int, public_key: tuple, private_key: tuple) -> int:
        n, g = public_key
        lam, mu = private_key
        n2 = n * n
        m = (PaillierCryptosystem._L(pow(ciphertext, lam, n2), n) * mu) % n
        return m

    @staticmethod
    def add_encrypted(c1: int, c2: int, n: int) -> int:
        """Homomorphic addition: E(m1+m2) = E(m1)·E(m2) mod n²"""
        return (c1 * c2) % (n * n)

    @staticmethod
    def scalar_multiply(c: int, k: int, n: int) -> int:
        """Homomorphic scalar multiplication: E(k·m) = E(m)^k mod n²"""
        return pow(c, k, n * n)

    @staticmethod
    def full_report(m1: int, m2: int, scalar: int = 3, bits: int = 128) -> str:
        pub, priv = PaillierCryptosystem.generate_keypair(bits)
        n, g = pub
        lam, mu = priv

        c1 = PaillierCryptosystem.encrypt(m1, pub)
        c2 = PaillierCryptosystem.encrypt(m2, pub)

        # Homomorphic addition
        c_add = PaillierCryptosystem.add_encrypted(c1, c2, n)
        m_add = PaillierCryptosystem.decrypt(c_add, pub, priv)

        # Homomorphic scalar multiply
        c_mul = PaillierCryptosystem.scalar_multiply(c1, scalar, n)
        m_mul = PaillierCryptosystem.decrypt(c_mul, pub, priv)

        lines = [
            "=" * 60,
            "PAILLIER CRYPTOSYSTEM  (Fully Homomorphic Addition)",
            "=" * 60,
            "",
            "KEY GENERATION",
            f"  n = p·q              : {n}",
            f"  g = n+1              : {g}",
            f"  λ = lcm(p-1,q-1)    : {lam}",
            f"  μ = λ⁻¹ mod n       : {mu}",
            "",
            "─" * 60,
            "ENCRYPTION",
            f"  m₁ = {m1}",
            f"  m₂ = {m2}",
            f"  E(m₁) = {c1}",
            f"  E(m₂) = {c2}",
            "",
            "─" * 60,
            "HOMOMORPHIC ADDITION",
            f"  E(m₁) · E(m₂) mod n² = {c_add}",
            f"  D( E(m₁)·E(m₂) )    = {m_add}",
            f"  Expected m₁+m₂       = {m1 + m2}",
            f"  ✓ Correct            : {m_add == (m1 + m2) % n}",
            "",
            "─" * 60,
            "HOMOMORPHIC SCALAR MULTIPLY",
            f"  k = {scalar}",
            f"  E(m₁)^k mod n²      = {c_mul}",
            f"  D( E(m₁)^k )        = {m_mul}",
            f"  Expected k·m₁        = {scalar * m1}",
            f"  ✓ Correct            : {m_mul == (scalar * m1) % n}",
            "",
            "─" * 60,
            PaillierCryptosystem.get_info(),
        ]
        return "\n".join(lines)

    @staticmethod
    def get_info() -> str:
        return (
            "PAILLIER CRYPTOSYSTEM\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "Proposed by Pascal Paillier (1999).\n"
            "Based on the Decisional Composite Residuosity (DCR) assumption.\n\n"
            "Additively homomorphic operations:\n"
            "  E(m₁)·E(m₂) mod n²  →  decrypts to  m₁+m₂  (mod n)\n"
            "  E(m)^k      mod n²  →  decrypts to  k·m    (mod n)\n\n"
            "Applications:\n"
            "  • Electronic voting (sum ballots without revealing individual votes).\n"
            "  • Privacy-preserving machine learning (federated learning).\n"
            "  • Secure multi-party computation.\n"
            "  • Private information retrieval.\n\n"
            "Note on 'Full Homomorphic Encryption' (FHE):\n"
            "  Paillier is *partially* homomorphic (addition only).\n"
            "  True FHE (Gentry 2009) supports both addition AND multiplication,\n"
            "  enabling arbitrary computations on encrypted data, but at much\n"
            "  higher computational cost.  Paillier is practical today.\n\n"
            "Security: Semantic security under the IND-CPA game.\n"
            "Key size recommendation: ≥ 2048-bit n for production use."
        )
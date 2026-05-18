"""
Advanced Cryptographic Concepts
Includes: Merkle-Damgård, Kerckhoffs' Principle, Kasiski Test,
Schnorr Protocol, Feige-Fiat-Shamir, Shamir's Secret Sharing, Paillier
"""
import random
import math
from typing import List, Tuple
import hashlib


class MerkleDamgard:
    """Merkle-Damgård construction demonstration"""
    
    @staticmethod
    def demonstrate(message: str) -> str:
        """Demonstrate Merkle-Damgård construction with padding"""
        # Simple demonstration of MD construction
        block_size = 64  # bytes
        msg_bytes = message.encode('utf-8')
        
        # Step 1: Padding
        original_len = len(msg_bytes)
        padding_len = block_size - (original_len % block_size) - 9
        if padding_len < 0:
            padding_len += block_size
        
        padded = msg_bytes + b'\x80' + b'\x00' * padding_len + original_len.to_bytes(8, 'big')
        
        # Step 2: Process blocks with compression function
        h = hashlib.sha256(b'').digest()  # Initialization vector
        for i in range(0, len(padded), block_size):
            block = padded[i:i+block_size]
            # Compression function: h = hash(h + block)
            h = hashlib.sha256(h + block).digest()
        
        result = h.hex()
        
        return (
            "═══════════════════════════════════════════════════════════════\n"
            "MERKLE-DAMGÅRD CONSTRUCTION\n"
            "═══════════════════════════════════════════════════════════════\n\n"
            "How it works:\n"
            "  1. Pad message to multiple of block size (MD padding)\n"
            "  2. Split into blocks: M₁, M₂, ..., Mₙ\n"
            "  3. Initialize H₀ = IV (initialization vector)\n"
            "  4. For each block: Hᵢ = f(Hᵢ₋₁, Mᵢ)\n"
            "  5. Final hash = Hₙ\n\n"
            f"Message: {message}\n"
            f"Original size: {original_len} bytes\n"
            f"Padded size: {len(padded)} bytes\n"
            f"Number of blocks: {len(padded) // block_size}\n"
            f"Final hash (SHA-256): {result}\n\n"
            "Used in: MD5, SHA-1, SHA-2 families\n"
            "Vulnerability: Length extension attacks"
        )
    
    @staticmethod
    def get_info() -> str:
        return (
            "Merkle-Damgård Construction\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Purpose: Build collision-resistant hash functions\n"
            "Structure: Iterated compression function f\n"
            "Properties:\n"
            "  • If f is collision-resistant → hash is collision-resistant\n"
            "  • Uses MD padding (append length at end)\n"
            "  • Vulnerable to length extension attacks\n"
            "Hash functions using MD: MD5, SHA-1, SHA-256, SHA-512"
        )


class KerckhoffsPrinciple:
    """Kerckhoffs' Principle demonstration"""
    
    @staticmethod
    def demonstrate() -> str:
        return (
            "═══════════════════════════════════════════════════════════════\n"
            "KERCKHOFFS' PRINCIPLE\n"
            "═══════════════════════════════════════════════════════════════\n\n"
            "Auguste Kerckhoffs (1883):\n"
            "  'A cryptographic system should be secure even if everything\n"
            "   about the system, except the key, is public knowledge.'\n\n"
            "Modern interpretation:\n"
            "  • Security through obscurity is NOT security\n"
            "  • The algorithm should be public\n"
            "  • Only the key must be kept secret\n\n"
            "Example - Caesar cipher violates this:\n"
            "  • If you know it's Caesar, you can break it easily\n"
            "  • Security depends on hiding the shift (obscurity)\n\n"
            "Example - AES respects this:\n"
            "  • Algorithm is public and well-studied\n"
            "  • Only the key needs to be secret\n"
            "  • Even knowing everything else, can't decrypt without key\n\n"
            "Why it matters:\n"
            "  • Allows public scrutiny and analysis\n"
            "  • Standardization of algorithms\n"
            "  • Keys can be changed, algorithms cannot\n"
            "  • Open design leads to stronger security"
        )
    
    @staticmethod
    def get_info() -> str:
        return "Kerckhoffs' Principle: The system must be secure even if everything except the key is public."


class KasiskiTest:
    """Kasiski test for finding Vigenère cipher key length"""
    
    @staticmethod
    def find_repeated_sequences(text: str, min_len: int = 3) -> dict:
        """Find repeated sequences and their positions"""
        text = text.upper().replace(" ", "")
        sequences = {}
        
        for length in range(min_len, min(min_len + 3, len(text) // 2)):
            for i in range(len(text) - length + 1):
                seq = text[i:i+length]
                if seq in sequences:
                    sequences[seq].append(i)
                else:
                    sequences[seq] = [i]
        
        # Filter sequences that appear at least twice
        return {k: v for k, v in sequences.items() if len(v) >= 2}
    
    @staticmethod
    def calculate_distances(positions: list) -> list:
        """Calculate distances between positions"""
        distances = []
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                distances.append(positions[j] - positions[i])
        return distances
    
    @staticmethod
    def gcd_of_distances(distances: list) -> int:
        """Calculate GCD of all distances"""
        if not distances:
            return 0
        result = distances[0]
        for d in distances[1:]:
            result = math.gcd(result, d)
        return result
    
    @staticmethod
    def analyze(text: str) -> str:
        """Run Kasiski test on ciphertext"""
        sequences = KasiskiTest.find_repeated_sequences(text)
        
        if not sequences:
            return "No repeated sequences found. Try longer text or smaller minimum length."
        
        all_distances = []
        for seq, positions in sequences.items():
            distances = KasiskiTest.calculate_distances(positions)
            all_distances.extend(distances)
        
        gcd_result = KasiskiTest.gcd_of_distances(all_distances)
        
        output = (
            "═══════════════════════════════════════════════════════════════\n"
            "KASISKI TEST - Finding Vigenère Key Length\n"
            "═══════════════════════════════════════════════════════════════\n\n"
            f"Analyzed text length: {len(text)} characters\n\n"
            "Repeated sequences found:\n"
        )
        
        for seq, positions in list(sequences.items())[:10]:
            output += f"  • '{seq}' at positions: {positions[:5]}\n"
        
        output += f"\nAll distances GCD: {gcd_result}\n\n"
        
        if gcd_result > 1:
            output += f"Suggested key length: {gcd_result} (or factors: "
            factors = []
            for i in range(2, gcd_result + 1):
                if gcd_result % i == 0:
                    factors.append(i)
            output += ", ".join(map(str, factors)) + ")\n"
        else:
            output += "No clear key length found. Try different text or min sequence length.\n"
        
        output += "\nHow it works:\n"
        output += "  • Repeated sequences in ciphertext suggest same plaintext\n"
        output += "  • Distance between repeats = multiple of key length\n"
        output += "  • GCD of all distances gives likely key length\n"
        
        return output
    
    @staticmethod
    def get_info() -> str:
        return "Kasiski Test: Cryptanalysis method to find Vigenère cipher key length by finding repeated sequences."


class SchnorrProtocol:
    """Schnorr Identification Protocol - Zero-Knowledge Proof"""
    
    @staticmethod
    def demonstrate() -> str:
        # Simple demonstration parameters
        p = 23  # prime
        q = 11  # prime divisor of p-1
        g = 2   # generator
        
        # Prover's private key
        private_key = 7
        
        # Prover's public key
        public_key = pow(g, private_key, p)
        
        # Commitment
        r = 5
        commitment = pow(g, r, p)
        
        # Challenge
        challenge = 4  # e in {0, 1}
        
        # Response
        response = (r + challenge * private_key) % q
        
        # Verification
        verify_left = pow(g, response, p)
        verify_right = (commitment * pow(public_key, challenge, p)) % p
        verified = verify_left == verify_right
        
        return (
            "═══════════════════════════════════════════════════════════════\n"
            "SCHNORR IDENTIFICATION PROTOCOL\n"
            "═══════════════════════════════════════════════════════════════\n\n"
            "Zero-Knowledge Proof Protocol (1989)\n\n"
            "Setup:\n"
            f"  • Prime p = {p}\n"
            f"  • Prime q = {q} (where q | p-1)\n"
            f"  • Generator g = {g}\n\n"
            "Prover (knows private key x):\n"
            f"  • Private key x = {private_key}\n"
            f"  • Public key y = g^x mod p = {public_key}\n\n"
            "Round 1 - Commitment:\n"
            f"  • Choose random r = {r}\n"
            f"  • Send commitment t = g^r mod p = {commitment}\n\n"
            "Round 2 - Challenge:\n"
            f"  • Verifier sends challenge e = {challenge}\n\n"
            "Round 3 - Response:\n"
            f"  • Prover sends s = r + e*x mod q = {response}\n\n"
            "Verification:\n"
            f"  • Check g^s ≡ t * y^e (mod p)\n"
            f"  • g^s mod p = {verify_left}\n"
            f"  • t * y^e mod p = {verify_right}\n"
            f"  • Verified: {verified}\n\n"
            "Properties:\n"
            "  • Zero-knowledge: verifier learns nothing about x\n"
            "  • Complete: honest prover always convinces\n"
            "  • Sound: dishonest prover cannot cheat\n"
            "Used in: Digital signatures (Schnorr signature scheme)"
        )
    
    @staticmethod
    def get_info() -> str:
        return "Schnorr Protocol: Zero-knowledge proof of discrete logarithm knowledge."


class FeigeFiatShamir:
    """Feige-Fiat-Shamir Identification Protocol"""
    
    @staticmethod
    def demonstrate() -> str:
        # Simple demonstration
        n = 7 * 11  # modulus (product of two primes)
        s = 5       # secret
        v = (s * s) % n  # public key
        
        # Round demonstration
        r = 3
        x = (r * r) % n
        challenge = 1  # 0 or 1
        y = (r * pow(s, challenge, n)) % n
        
        # Verification
        verify = (y * y) % n
        expected = (x * pow(v, challenge, n)) % n
        verified = verify == expected
        
        return (
            "═══════════════════════════════════════════════════════════════\n"
            "FEIGE-FIAT-SHAMIR IDENTIFICATION PROTOCOL\n"
            "═══════════════════════════════════════════════════════════════\n\n"
            "Zero-Knowledge Proof using Quadratic Residues (1988)\n\n"
            "Setup:\n"
            f"  • Modulus n = p*q = {n}\n"
            f"  • Secret s = {s}\n"
            f"  • Public v = s² mod n = {v}\n\n"
            "Round:\n"
            f"  • Choose random r = {r}\n"
            f"  • Send x = r² mod n = {x}\n"
            f"  • Challenge e = {challenge}\n"
            f"  • Send y = r * s^e mod n = {y}\n\n"
            "Verification:\n"
            f"  • Check y² ≡ x * v^e (mod n)\n"
            f"  • y² mod n = {verify}\n"
            f"  • x * v^e mod n = {expected}\n"
            f"  • Verified: {verified}\n\n"
            "Security: Based on factoring problem"
        )
    
    @staticmethod
    def get_info() -> str:
        return "Feige-Fiat-Shamir: Zero-knowledge identification using quadratic residues."


class ShamirSecretSharing:
    """Shamir's Secret Sharing - (k, n) threshold scheme"""
    
    @staticmethod
    def _horner_eval(coefficients: List[int], x: int, p: int) -> int:
        """Evaluate polynomial at x using Horner's method"""
        result = 0
        for coeff in reversed(coefficients):
            result = (result * x + coeff) % p
        return result
    
    @staticmethod
    def split_secret(secret: int, n: int, k: int, prime: int = 2**31 - 1) -> List[Tuple[int, int]]:
        """Split secret into n shares with threshold k"""
        if k > n:
            raise ValueError("Threshold k cannot be greater than number of shares n")
        
        # Generate random coefficients for polynomial of degree k-1
        coefficients = [secret] + [random.randint(1, prime - 1) for _ in range(k - 1)]
        
        # Generate n shares
        shares = []
        for i in range(1, n + 1):
            x = i
            y = ShamirSecretSharing._horner_eval(coefficients, x, prime)
            shares.append((x, y))
        
        return shares
    
    @staticmethod
    def reconstruct_secret(shares: List[Tuple[int, int]], prime: int = 2**31 - 1) -> int:
        """Reconstruct secret from k shares using Lagrange interpolation"""
        secret = 0
        k = len(shares)
        
        for i in range(k):
            xi, yi = shares[i]
            # Lagrange basis polynomial
            numerator = 1
            denominator = 1
            for j in range(k):
                if i != j:
                    xj, _ = shares[j]
                    numerator = (numerator * (-xj)) % prime
                    denominator = (denominator * (xi - xj)) % prime
            
            # Lagrange coefficient
            li = (numerator * pow(denominator, -1, prime)) % prime
            secret = (secret + yi * li) % prime
        
        return secret
    
    @staticmethod
    def demonstrate(secret: int = 42, n: int = 5, k: int = 3) -> str:
        """Demonstrate Shamir's Secret Sharing"""
        prime = 2**31 - 1  # Mersenne prime
        
        shares = ShamirSecretSharing.split_secret(secret, n, k, prime)
        reconstructed = ShamirSecretSharing.reconstruct_secret(shares[:k], prime)
        
        output = (
            "═══════════════════════════════════════════════════════════════\n"
            "SHAMIR'S SECRET SHARING (k, n) THRESHOLD SCHEME\n"
            "═══════════════════════════════════════════════════════════════\n\n"
            f"Secret: {secret}\n"
            f"Threshold: {k} shares needed to reconstruct\n"
            f"Total shares: {n}\n"
            f"Prime modulus: {prime}\n\n"
            "Generated shares:\n"
        )
        
        for x, y in shares:
            output += f"  • Share {x}: ({x}, {y})\n"
        
        output += f"\nReconstructing with {k} shares:\n"
        for i, (x, y) in enumerate(shares[:k]):
            output += f"  • Using share {i+1}: ({x}, {y})\n"
        
        output += f"\nReconstructed secret: {reconstructed}\n"
        output += f"✓ Success: {reconstructed == secret}\n\n"
        output += "Properties:\n"
        output += "  • Any k shares → reconstruct secret\n"
        output += "  • Any k-1 shares → no information about secret\n"
        output += "  • Perfect secrecy for < k shares\n"
        output += "Uses: Key management, distributed systems, Byzantine fault tolerance"
        
        return output
    
    @staticmethod
    def get_info() -> str:
        return "Shamir's Secret Sharing: (k,n) threshold scheme using polynomial interpolation."


class PaillierCryptosystem:
    """Paillier Cryptosystem - Partial Homomorphic Encryption"""
    
    @staticmethod
    def generate_keys(bits: int = 32) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Generate Paillier key pair"""
        # Simplified for demonstration (use larger primes in practice)
        from sympy import randprime
        
        p = randprime(2**(bits//2 - 1), 2**(bits//2))
        q = randprime(2**(bits//2 - 1), 2**(bits//2))
        while q == p:
            q = randprime(2**(bits//2 - 1), 2**(bits//2))
        
        n = p * q
        g = n + 1  # Standard choice for Paillier
        
        # λ = lcm(p-1, q-1)
        lambda_val = (p - 1) * (q - 1) // math.gcd(p - 1, q - 1)
        
        # μ = (L(g^λ mod n^2))⁻¹ mod n
        n_sq = n * n
        x = pow(g, lambda_val, n_sq)
        L = (x - 1) // n
        mu = pow(L, -1, n)
        
        return ((n, g), (lambda_val, mu))
    
    @staticmethod
    def encrypt(m: int, public_key: Tuple[int, int]) -> int:
        """Encrypt message with Paillier public key"""
        n, g = public_key
        n_sq = n * n
        r = random.randint(1, n - 1)
        while math.gcd(r, n) != 1:
            r = random.randint(1, n - 1)
        
        ciphertext = (pow(g, m, n_sq) * pow(r, n, n_sq)) % n_sq
        return ciphertext
    
    @staticmethod
    def decrypt(c: int, private_key: Tuple[int, int], public_key: Tuple[int, int]) -> int:
        """Decrypt ciphertext with Paillier private key"""
        n, g = public_key
        lambda_val, mu = private_key
        n_sq = n * n
        
        x = pow(c, lambda_val, n_sq)
        L = (x - 1) // n
        m = (L * mu) % n
        return m
    
    @staticmethod
    def add_encrypted(c1: int, c2: int, n: int) -> int:
        """Homomorphic addition of two ciphertexts"""
        n_sq = n * n
        return (c1 * c2) % n_sq
    
    @staticmethod
    def multiply_encrypted(c: int, scalar: int, n: int) -> int:
        """Homomorphic multiplication of ciphertext by scalar"""
        n_sq = n * n
        return pow(c, scalar, n_sq)
    
    @staticmethod
    def demonstrate() -> str:
        """Demonstrate Paillier homomorphic properties"""
        pub_key, priv_key = PaillierCryptosystem.generate_keys(32)
        n, g = pub_key
        
        # Encrypt two numbers
        m1 = 15
        m2 = 10
        c1 = PaillierCryptosystem.encrypt(m1, pub_key)
        c2 = PaillierCryptosystem.encrypt(m2, pub_key)
        
        # Homomorphic operations
        c_sum = PaillierCryptosystem.add_encrypted(c1, c2, n)
        decrypted_sum = PaillierCryptosystem.decrypt(c_sum, priv_key, pub_key)
        
        c_mul = PaillierCryptosystem.multiply_encrypted(c1, 3, n)
        decrypted_mul = PaillierCryptosystem.decrypt(c_mul, priv_key, pub_key)
        
        return (
            "═══════════════════════════════════════════════════════════════\n"
            "PAILLIER CRYPTOSYSTEM - Homomorphic Encryption\n"
            "═══════════════════════════════════════════════════════════════\n\n"
            "Properties: Additive homomorphism\n"
            "  • E(m₁) × E(m₂) = E(m₁ + m₂)\n"
            "  • E(m)ᵏ = E(k × m)\n\n"
            f"Public key (n): {n}\n\n"
            f"Message 1: {m1}\n"
            f"Ciphertext 1: {c1}\n\n"
            f"Message 2: {m2}\n"
            f"Ciphertext 2: {c2}\n\n"
            "Homomorphic Addition:\n"
            f"  • E({m1}) × E({m2}) = {c_sum}\n"
            f"  • Decrypted: {decrypted_sum}\n"
            f"  • Expected: {m1 + m2}\n"
            f"  ✓ Result: {decrypted_sum == m1 + m2}\n\n"
            "Homomorphic Multiplication by Scalar:\n"
            f"  • E({m1})³ = {c_mul}\n"
            f"  • Decrypted: {decrypted_mul}\n"
            f"  • Expected: {m1 * 3}\n"
            f"  ✓ Result: {decrypted_mul == m1 * 3}\n\n"
            "Uses:\n"
            "  • Electronic voting\n"
            "  • Private information retrieval\n"
            "  • Secure multi-party computation"
        )
    
    @staticmethod
    def get_info() -> str:
        return "Paillier Cryptosystem: Additive homomorphic encryption based on composite residuosity."


class CryptographicConcepts:
    """Container for cryptographic concept info"""
    
    @staticmethod
    def get_merkle_damgard_info() -> str:
        return MerkleDamgard.get_info()
    
    @staticmethod
    def get_kerckhoffs_info() -> str:
        return KerckhoffsPrinciple.get_info()
    
    @staticmethod
    def get_kasiski_info() -> str:
        return KasiskiTest.get_info()
    
    @staticmethod
    def get_schnorr_info() -> str:
        return SchnorrProtocol.get_info()
    
    @staticmethod
    def get_feige_fiat_shamir_info() -> str:
        return FeigeFiatShamir.get_info()
    
    @staticmethod
    def get_shamir_info() -> str:
        return ShamirSecretSharing.get_info()
    
    @staticmethod
    def get_paillier_info() -> str:
        return PaillierCryptosystem.get_info()
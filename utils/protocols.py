import random

class ShamirSecretSharing:
    """Shamir's Secret Sharing - (k,n) threshold scheme"""
    
    @staticmethod
    def split_secret(secret, n, k):
        """Split secret into n shares, need k to reconstruct"""
        if secret < 0:
            raise ValueError("Secret must be positive")
        if n < 1 or k < 1:
            raise ValueError("n and k must be positive")
        if k > n:
            raise ValueError("k cannot be greater than n")
        
        coefficients = [secret] + [random.randint(1, 1000) for _ in range(k-1)]
        shares = []
        for i in range(1, n+1):
            value = sum(coeff * (i ** idx) for idx, coeff in enumerate(coefficients))
            shares.append((i, value))
        return shares
    
    @staticmethod
    def reconstruct(shares):
        """Reconstruct secret from k shares using Lagrange interpolation"""
        if len(shares) < 2:
            raise ValueError("Need at least 2 shares to reconstruct")
        
        x_coords = [s[0] for s in shares]
        y_coords = [s[1] for s in shares]
        secret = 0
        for i in range(len(shares)):
            numerator = 1
            denominator = 1
            for j in range(len(shares)):
                if i != j:
                    numerator *= (-x_coords[j])
                    denominator *= (x_coords[i] - x_coords[j])
            secret += (y_coords[i] * numerator) // denominator
        return secret


class VigenereKasiski:
    """Kasiski test for Vigenère cipher"""
    
    @staticmethod
    def find_repeated_sequences(ciphertext, min_length=3):
        if not ciphertext:
            return []
        
        ciphertext = ciphertext.upper()
        sequences = {}
        for i in range(len(ciphertext) - min_length + 1):
            seq = ciphertext[i:i+min_length]
            if seq in sequences:
                sequences[seq].append(i)
            else:
                sequences[seq] = [i]
        
        distances = []
        for positions in sequences.values():
            if len(positions) >= 2:
                for j in range(len(positions)):
                    for k in range(j+1, len(positions)):
                        distances.append(positions[k] - positions[j])
        return distances
# # class VigenereCipher:
# #     """Vigenère cipher - polyalphabetic substitution"""
    
# #     @staticmethod
# #     def _validate_key(key):
# #         if not key:
# #             raise ValueError("Key cannot be empty")
# #         if not key.isalpha():
# #             raise ValueError("Key must contain only letters")
# #         return key.upper()
    
# #     @staticmethod
# #     def encrypt(text, key):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         key = VigenereCipher._validate_key(key)
        
# #         result = []
# #         key_len = len(key)
# #         key_idx = 0
        
# #         for char in text:
# #             if char.isalpha():
# #                 shift = ord(key[key_idx % key_len]) - 65
# #                 if char.isupper():
# #                     result.append(chr((ord(char) - 65 + shift) % 26 + 65))
# #                 else:
# #                     result.append(chr((ord(char) - 97 + shift) % 26 + 97))
# #                 key_idx += 1
# #             else:
# #                 result.append(char)
# #         return ''.join(result)
    
# #     @staticmethod
# #     def decrypt(text, key):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         key = VigenereCipher._validate_key(key)
        
# #         result = []
# #         key_len = len(key)
# #         key_idx = 0
        
# #         for char in text:
# #             if char.isalpha():
# #                 shift = ord(key[key_idx % key_len]) - 65
# #                 if char.isupper():
# #                     result.append(chr((ord(char) - 65 - shift) % 26 + 65))
# #                 else:
# #                     result.append(chr((ord(char) - 97 - shift) % 26 + 97))
# #                 key_idx += 1
# #             else:
# #                 result.append(char)
# #         return ''.join(result)
    
# #     @staticmethod
# #     def kasiski_test(ciphertext, min_length=3):
# #         """Find repeated sequences to estimate key length"""
# #         if not ciphertext:
# #             return []
        
# #         ciphertext = ciphertext.upper()
# #         sequences = {}
# #         for i in range(len(ciphertext) - min_length + 1):
# #             seq = ciphertext[i:i+min_length]
# #             if seq in sequences:
# #                 sequences[seq].append(i)
# #             else:
# #                 sequences[seq] = [i]
        
# #         distances = []
# #         for positions in sequences.values():
# #             if len(positions) >= 2:
# #                 for j in range(len(positions)):
# #                     for k in range(j+1, len(positions)):
# #                         distances.append(positions[k] - positions[j])
# #         return distances



# """
# Vigenère Cipher — Polyalphabetic substitution cipher (1553)
# Classical Cryptography | TP1

# Principle: Uses a repeating keyword. Each letter of the keyword determines
#   the Caesar shift applied to the corresponding plaintext letter.
#   Encrypt: C_i = (P_i + K_{i mod len(K)}) mod 26
#   Decrypt: P_i = (C_i - K_{i mod len(K)}) mod 26

# Cryptanalysis: Kasiski test + Index of Coincidence reveal key length,
#   then frequency analysis breaks each Caesar sub-cipher.
# """

# from collections import Counter
# import math


# class VigenereCipher:
#     """Vigenère polyalphabetic substitution cipher."""

#     @staticmethod
#     def encrypt(text: str, key: str) -> str:
#         """
#         Encrypt plaintext with Vigenère cipher.

#         Args:
#             text: Plaintext (any characters; non-alpha passed through)
#             key:  Keyword — letters only, any length ≥ 1

#         Returns:
#             Ciphertext with same case structure as input.

#         Raises:
#             ValueError: If text is empty or key contains non-letters.

#         Example:
#             >>> VigenereCipher.encrypt("ATTACKATDAWN", "LEMON")
#             'LXFOPVEFRNHR'
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         if not key or not key.isalpha():
#             raise ValueError("Key must contain only letters")
#         key     = key.upper()
#         result  = []
#         key_idx = 0
#         for char in text:
#             if char.isalpha():
#                 shift = ord(key[key_idx % len(key)]) - 65
#                 base  = 65 if char.isupper() else 97
#                 result.append(chr((ord(char) - base + shift) % 26 + base))
#                 key_idx += 1
#             else:
#                 result.append(char)
#         return "".join(result)

#     @staticmethod
#     def decrypt(text: str, key: str) -> str:
#         """
#         Decrypt Vigenère ciphertext.

#         Args:
#             text: Ciphertext string
#             key:  Same keyword used during encryption

#         Returns:
#             Recovered plaintext.

#         Example:
#             >>> VigenereCipher.decrypt("LXFOPVEFRNHR", "LEMON")
#             'ATTACKATDAWN'
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         if not key or not key.isalpha():
#             raise ValueError("Key must contain only letters")
#         key     = key.upper()
#         result  = []
#         key_idx = 0
#         for char in text:
#             if char.isalpha():
#                 shift = ord(key[key_idx % len(key)]) - 65
#                 base  = 65 if char.isupper() else 97
#                 result.append(chr((ord(char) - base - shift) % 26 + base))
#                 key_idx += 1
#             else:
#                 result.append(char)
#         return "".join(result)

#     # ── Cryptanalysis tools ──────────────────────────────────────────────────

#     @staticmethod
#     def index_of_coincidence(text: str) -> float:
#         """
#         Compute the Index of Coincidence (IC) of a text.
#         IC ≈ 0.065 for English, ≈ 0.038 for random text.
#         Used in the Friedman test to estimate key length.

#         Args:
#             text: Uppercase letters only (non-alpha ignored)

#         Returns:
#             Float IC value.
#         """
#         text  = "".join(c for c in text.upper() if c.isalpha())
#         n     = len(text)
#         if n < 2:
#             return 0.0
#         freqs = Counter(text)
#         total = sum(f * (f - 1) for f in freqs.values())
#         return total / (n * (n - 1))

#     @staticmethod
#     def kasiski_key_length(ciphertext: str, max_key_len: int = 20) -> list[int]:
#         """
#         Kasiski test: find repeated trigrams and compute GCDs of their distances.
#         Returns probable key lengths, sorted by likelihood.

#         Args:
#             ciphertext:  Ciphertext (letters only)
#             max_key_len: Maximum key length to consider

#         Returns:
#             List of probable key lengths (most likely first).
#         """
#         text    = "".join(c for c in ciphertext.upper() if c.isalpha())
#         repeats = {}
#         for i in range(len(text) - 2):
#             trigram = text[i:i+3]
#             if trigram in repeats:
#                 repeats[trigram].append(i)
#             else:
#                 repeats[trigram] = [i]

#         distances = []
#         for positions in repeats.values():
#             if len(positions) > 1:
#                 for j in range(1, len(positions)):
#                     distances.append(positions[j] - positions[j-1])

#         if not distances:
#             return list(range(2, max_key_len + 1))

#         factor_counts = Counter()
#         for d in distances:
#             for f in range(2, min(d + 1, max_key_len + 1)):
#                 if d % f == 0:
#                     factor_counts[f] += 1

#         return [k for k, _ in factor_counts.most_common()]


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     plaintext = "ATTACKATDAWN"
#     key       = "LEMON"

#     ciphertext = VigenereCipher.encrypt(plaintext, key)
#     recovered  = VigenereCipher.decrypt(ciphertext, key)

#     print("=" * 50)
#     print("VIGENÈRE CIPHER DEMO")
#     print("=" * 50)
#     print(f"Plaintext  : {plaintext}")
#     print(f"Key        : {key}  (repeated: {(key * (len(plaintext)//len(key)+1))[:len(plaintext)]})")
#     print(f"Ciphertext : {ciphertext}")
#     print(f"Decrypted  : {recovered}")
#     print(f"Match      : {plaintext == recovered}")
#     print()
#     # Longer message for IC demonstration
#     long_msg   = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
#     long_ct    = VigenereCipher.encrypt(long_msg, key)
#     ic         = VigenereCipher.index_of_coincidence(long_ct)
#     print(f"Index of Coincidence (ciphertext): {ic:.4f}")
#     print(f"  (English ≈ 0.065, random ≈ 0.038)")


"""
Vigenère Cipher - Classical Polyalphabetic Cipher
Uses a keyword to apply different Caesar shifts to each letter.
"""


class VigenereCipher:
    @staticmethod
    def encrypt(text: str, key: str) -> str:
        """Encrypt text using Vigenère cipher."""
        if not text:
            raise ValueError("Text cannot be empty")
        if not key or not key.isalpha():
            raise ValueError("Key must contain only letters")
        key = key.upper()
        result = []
        key_idx = 0
        for char in text:
            if char.isalpha():
                shift = ord(key[key_idx % len(key)]) - 65
                base = 65 if char.isupper() else 97
                result.append(chr((ord(char) - base + shift) % 26 + base))
                key_idx += 1
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, key: str) -> str:
        """Decrypt text using Vigenère cipher."""
        if not text:
            raise ValueError("Text cannot be empty")
        if not key or not key.isalpha():
            raise ValueError("Key must contain only letters")
        key = key.upper()
        result = []
        key_idx = 0
        for char in text:
            if char.isalpha():
                shift = ord(key[key_idx % len(key)]) - 65
                base = 65 if char.isupper() else 97
                result.append(chr((ord(char) - base - shift) % 26 + base))
                key_idx += 1
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def index_of_coincidence(text: str) -> float:
        """Calculate index of coincidence for cryptanalysis."""
        text = ''.join(c.upper() for c in text if c.isalpha())
        n = len(text)
        if n < 2:
            return 0.0
        freq = {}
        for c in text:
            freq[c] = freq.get(c, 0) + 1
        ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
        return ic
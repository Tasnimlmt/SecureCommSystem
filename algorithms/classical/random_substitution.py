# # import random
# # import string

# # class RandomSubstitutionCipher:
# #     """Random monoalphabetic substitution cipher"""
    
# #     def __init__(self, key=None):
# #         self.alphabet = list(string.ascii_uppercase)
# #         if key:
# #             self.shuffled = list(key.upper())
# #             if len(self.shuffled) != 26:
# #                 raise ValueError("Key must be 26 unique letters")
# #         else:
# #             self.shuffled = self.alphabet.copy()
# #             random.shuffle(self.shuffled)
        
# #         self.encrypt_map = dict(zip(self.alphabet, self.shuffled))
# #         self.decrypt_map = dict(zip(self.shuffled, self.alphabet))
    
# #     def encrypt(self, text):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         result = []
# #         for char in text.upper():
# #             if char in self.encrypt_map:
# #                 result.append(self.encrypt_map[char])
# #             else:
# #                 result.append(char)
# #         return ''.join(result)
    
# #     def decrypt(self, text):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         result = []
# #         for char in text.upper():
# #             if char in self.decrypt_map:
# #                 result.append(self.decrypt_map[char])
# #             else:
# #                 result.append(char)
# #         return ''.join(result)


# """
# Random Substitution Cipher — Monoalphabetic substitution
# Classical Cryptography | TP1

# Principle: Each letter of the alphabet is mapped to a unique, randomly chosen
#   letter. The mapping (key) is a permutation of the 26-letter alphabet.
#   Key space: 26! ≈ 4 × 10²⁶ — far larger than Caesar or Affine.
#   Weakness: Vulnerable to frequency analysis (letter frequencies are preserved).
# """

# import random
# import string


# class RandomSubstitutionCipher:
#     """
#     Monoalphabetic substitution cipher with a randomly generated or user-supplied key.

#     The key is a 26-character permutation of A-Z representing the substitution alphabet.
#     Example: key = "QWERTYUIOPASDFGHJKLZXCVBNM"
#       means A→Q, B→W, C→E, D→R, E→T, …
#     """

#     ALPHABET = string.ascii_uppercase  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#     def __init__(self, key: str = None):
#         """
#         Initialise the cipher.

#         Args:
#             key: Optional 26-character substitution key (uppercase A-Z, all unique).
#                  If None, a random permutation is generated.

#         Raises:
#             ValueError: If key is provided but invalid.
#         """
#         if key is not None:
#             key = key.upper()
#             if len(key) != 26 or set(key) != set(self.ALPHABET):
#                 raise ValueError(
#                     "Key must be a 26-character permutation of A-Z (no repeats)."
#                 )
#             self.key = key
#         else:
#             shuffled = list(self.ALPHABET)
#             random.shuffle(shuffled)
#             self.key = "".join(shuffled)

#         # Build lookup tables for O(1) encrypt/decrypt
#         self._enc_map = str.maketrans(self.ALPHABET, self.key)
#         self._dec_map = str.maketrans(self.key, self.ALPHABET)

#     def encrypt(self, text: str) -> str:
#         """
#         Encrypt plaintext using the substitution key.

#         Args:
#             text: Plaintext string (case-insensitive; non-alpha unchanged)

#         Returns:
#             Ciphertext (uppercase).

#         Example:
#             cipher = RandomSubstitutionCipher("QWERTYUIOPASDFGHJKLZXCVBNM")
#             cipher.encrypt("Hello")  →  "ITSSG"
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         return text.upper().translate(self._enc_map)

#     def decrypt(self, text: str) -> str:
#         """
#         Decrypt substitution ciphertext using the inverse key.

#         Args:
#             text: Ciphertext string (uppercase)

#         Returns:
#             Recovered plaintext (uppercase).
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         return text.upper().translate(self._dec_map)

#     def show_key_table(self) -> str:
#         """Return a formatted display of the substitution alphabet."""
#         plain  = "Plain  : " + " ".join(self.ALPHABET)
#         cipher = "Cipher : " + " ".join(self.key)
#         return plain + "\n" + cipher

#     @staticmethod
#     def frequency_analysis(text: str) -> list[tuple[str, int, float]]:
#         """
#         Count letter frequencies in text (tool for cryptanalysis).

#         Returns:
#             Sorted list of (letter, count, percentage) tuples, most frequent first.
#         """
#         text   = text.upper()
#         total  = sum(1 for c in text if c.isalpha())
#         counts = {c: text.count(c) for c in string.ascii_uppercase if c in text}
#         return sorted(
#             [(c, n, 100 * n / total) for c, n in counts.items()],
#             key=lambda x: -x[1],
#         )


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     # Use a fixed key for reproducibility
#     key    = "QWERTYUIOPASDFGHJKLZXCVBNM"
#     cipher = RandomSubstitutionCipher(key)

#     plaintext  = "The quick brown fox jumps over the lazy dog"
#     ciphertext = cipher.encrypt(plaintext)
#     recovered  = cipher.decrypt(ciphertext)

#     print("=" * 55)
#     print("RANDOM SUBSTITUTION CIPHER DEMO")
#     print("=" * 55)
#     print(cipher.show_key_table())
#     print()
#     print(f"Plaintext  : {plaintext}")
#     print(f"Ciphertext : {ciphertext}")
#     print(f"Decrypted  : {recovered}")
#     print(f"Match      : {plaintext.upper() == recovered}")
#     print()
#     print("Frequency analysis of ciphertext:")
#     for letter, count, pct in cipher.frequency_analysis(ciphertext)[:5]:
#         print(f"  '{letter}' appears {count:2d} times ({pct:.1f}%)")


"""
Random Substitution Cipher - Classical Monoalphabetic Cipher
Each letter of the alphabet is replaced by a randomly shuffled letter.
The key is the 26-character shuffled alphabet.
"""
import random
import string


class RandomSubstitutionCipher:
    def __init__(self, key: str = None):
        """
        Initialize with an optional key (26-letter substitution alphabet).
        If no key is provided, a random one is generated.
        """
        self.alphabet = list(string.ascii_uppercase)
        if key:
            key = key.upper()
            if len(key) != 26 or not key.isalpha() or len(set(key)) != 26:
                raise ValueError("Key must be 26 unique uppercase letters")
            self.shuffled = list(key)
        else:
            self.shuffled = self.alphabet.copy()
            random.shuffle(self.shuffled)

        self.encrypt_map = dict(zip(self.alphabet, self.shuffled))
        self.decrypt_map = dict(zip(self.shuffled, self.alphabet))

    def get_key(self) -> str:
        """Return the current substitution key as a string."""
        return ''.join(self.shuffled)

    def encrypt(self, text: str) -> str:
        """Encrypt text using random substitution."""
        if not text:
            raise ValueError("Text cannot be empty")
        result = []
        for char in text:
            upper = char.upper()
            if upper in self.encrypt_map:
                enc = self.encrypt_map[upper]
                result.append(enc if char.isupper() else enc.lower())
            else:
                result.append(char)
        return ''.join(result)

    def decrypt(self, text: str) -> str:
        """Decrypt text using random substitution."""
        if not text:
            raise ValueError("Text cannot be empty")
        result = []
        for char in text:
            upper = char.upper()
            if upper in self.decrypt_map:
                dec = self.decrypt_map[upper]
                result.append(dec if char.isupper() else dec.lower())
            else:
                result.append(char)
        return ''.join(result)

    def show_mapping(self) -> str:
        """Display the substitution mapping."""
        lines = [
            "Substitution Mapping:",
            "Plain:  " + ' '.join(self.alphabet),
            "Cipher: " + ' '.join(self.shuffled),
            f"\nKey: {''.join(self.shuffled)}",
        ]
        return '\n'.join(lines)

    @staticmethod
    def from_key(key: str) -> 'RandomSubstitutionCipher':
        """Create cipher from an existing 26-letter key."""
        return RandomSubstitutionCipher(key)
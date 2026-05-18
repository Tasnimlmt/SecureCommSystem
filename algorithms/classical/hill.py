# # class HillCipher:
# #     """Hill cipher - matrix-based polygraphic substitution (2x2)"""
    
# #     @staticmethod
# #     def _mod_inverse(a, m=26):
# #         a = a % m
# #         for x in range(1, m):
# #             if (a * x) % m == 1:
# #                 return x
# #         return None
    
# #     @staticmethod
# #     def _validate_matrix(matrix):
# #         if len(matrix) != 2 or len(matrix[0]) != 2 or len(matrix[1]) != 2:
# #             raise ValueError("Matrix must be 2x2")
        
# #         for row in matrix:
# #             for val in row:
# #                 if val < 0 or val > 25:
# #                     raise ValueError("Matrix values must be between 0 and 25")
        
# #         det = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 26
# #         det_inv = HillCipher._mod_inverse(det)
# #         if det_inv is None:
# #             raise ValueError(f"Matrix determinant {det} is not coprime with 26. Matrix not invertible!")
# #         return det_inv
    
# #     @staticmethod
# #     def encrypt(text, matrix):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
        
# #         det_inv = HillCipher._validate_matrix(matrix)
        
# #         # Clean text: keep only letters and convert to uppercase
# #         text = ''.join([c.upper() for c in text if c.isalpha()])
# #         if not text:
# #             raise ValueError("Text must contain at least one letter")
        
# #         # Pad with 'X' if odd length
# #         if len(text) % 2 != 0:
# #             text += 'X'
        
# #         result = []
# #         for i in range(0, len(text), 2):
# #             p1 = ord(text[i]) - 65
# #             p2 = ord(text[i+1]) - 65
# #             c1 = (matrix[0][0] * p1 + matrix[0][1] * p2) % 26
# #             c2 = (matrix[1][0] * p1 + matrix[1][1] * p2) % 26
# #             result.append(chr(c1 + 65))
# #             result.append(chr(c2 + 65))
# #         return ''.join(result)
    
# #     @staticmethod
# #     def decrypt(ciphertext, matrix):
# #         if not ciphertext:
# #             raise ValueError("Ciphertext cannot be empty")
        
# #         det_inv = HillCipher._validate_matrix(matrix)
        
# #         # Clean text
# #         ciphertext = ''.join([c.upper() for c in ciphertext if c.isalpha()])
# #         if len(ciphertext) % 2 != 0:
# #             raise ValueError("Ciphertext length must be even")
        
# #         # Calculate inverse matrix
# #         inv = [
# #             [(matrix[1][1] * det_inv) % 26, (-matrix[0][1] * det_inv) % 26],
# #             [(-matrix[1][0] * det_inv) % 26, (matrix[0][0] * det_inv) % 26]
# #         ]
        
# #         result = []
# #         for i in range(0, len(ciphertext), 2):
# #             c1 = ord(ciphertext[i]) - 65
# #             c2 = ord(ciphertext[i+1]) - 65
# #             p1 = (inv[0][0] * c1 + inv[0][1] * c2) % 26
# #             p2 = (inv[1][0] * c1 + inv[1][1] * c2) % 26
# #             result.append(chr(p1 + 65))
# #             result.append(chr(p2 + 65))
# #         return ''.join(result)


# """
# Hill Cipher — Polygraphic substitution using matrix multiplication
# Classical Cryptography | TP1

# Principle: Groups plaintext into blocks of n letters, represents each as a
#   vector mod 26, then multiplies by an n×n key matrix mod 26.
#   Encrypt: C = K · P  (mod 26)
#   Decrypt: P = K⁻¹ · C (mod 26)

# This implementation uses 2×2 matrices (digraph substitution).
# Requirement: det(K) must be coprime with 26 for K to be invertible mod 26.
# """

# import math


# class HillCipher:
#     """
#     Hill cipher with 2×2 integer matrix key.
#     Matrix entries must be integers 0-25.
#     """

#     @staticmethod
#     def mod_inverse(a: int, m: int = 26) -> int | None:
#         """Return a⁻¹ mod m, or None if not invertible."""
#         a = a % m
#         for x in range(1, m):
#             if (a * x) % m == 1:
#                 return x
#         return None

#     @staticmethod
#     def determinant_mod26(matrix: list[list[int]]) -> int:
#         """Return det(matrix) mod 26 for a 2×2 matrix."""
#         return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 26

#     @staticmethod
#     def is_valid_key(matrix: list[list[int]]) -> bool:
#         """Check if the 2×2 matrix is a valid Hill cipher key (det coprime with 26)."""
#         det = HillCipher.determinant_mod26(matrix)
#         return HillCipher.mod_inverse(det) is not None

#     @staticmethod
#     def inverse_matrix_mod26(matrix: list[list[int]]) -> list[list[int]]:
#         """
#         Compute the modular inverse of a 2×2 matrix mod 26.

#         Raises:
#             ValueError: If the matrix is not invertible mod 26.
#         """
#         det     = HillCipher.determinant_mod26(matrix)
#         det_inv = HillCipher.mod_inverse(det)
#         if det_inv is None:
#             raise ValueError(
#                 f"det={det} is not coprime with 26 — matrix is not invertible mod 26.\n"
#                 f"gcd({det}, 26) = {math.gcd(det, 26)}"
#             )
#         # Adjugate of 2×2: [[d, -b], [-c, a]]
#         return [
#             [(matrix[1][1] * det_inv) % 26,  (-matrix[0][1] * det_inv) % 26],
#             [(-matrix[1][0] * det_inv) % 26,  (matrix[0][0] * det_inv) % 26],
#         ]

#     @staticmethod
#     def _multiply_block(block: tuple[int, int], matrix: list[list[int]]) -> tuple[int, int]:
#         """Multiply a 2-element column vector by the 2×2 matrix mod 26."""
#         p1, p2 = block
#         c1 = (matrix[0][0] * p1 + matrix[0][1] * p2) % 26
#         c2 = (matrix[1][0] * p1 + matrix[1][1] * p2) % 26
#         return c1, c2

#     @staticmethod
#     def encrypt(text: str, matrix: list[list[int]]) -> str:
#         """
#         Encrypt plaintext with the Hill cipher (2×2 key matrix).

#         Args:
#             text:   Plaintext string (letters only used; others stripped)
#             matrix: 2×2 key matrix, e.g. [[3, 3], [2, 5]]

#         Returns:
#             Ciphertext (uppercase).

#         Raises:
#             ValueError: If the matrix is not invertible or text is empty.

#         Example:
#             >>> HillCipher.encrypt("ACT", [[6,24],[13,16],[20,17]])  # 3×3 example
#             # For 2×2: HillCipher.encrypt("HELP", [[3,3],[2,5]])
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         if not HillCipher.is_valid_key(matrix):
#             raise ValueError("Key matrix is not invertible mod 26")

#         letters = "".join(c.upper() for c in text if c.isalpha())
#         if len(letters) % 2 != 0:
#             letters += "X"   # pad with 'X'

#         result = []
#         for i in range(0, len(letters), 2):
#             p1 = ord(letters[i])   - 65
#             p2 = ord(letters[i+1]) - 65
#             c1, c2 = HillCipher._multiply_block((p1, p2), matrix)
#             result.append(chr(c1 + 65))
#             result.append(chr(c2 + 65))
#         return "".join(result)

#     @staticmethod
#     def decrypt(ciphertext: str, matrix: list[list[int]]) -> str:
#         """
#         Decrypt Hill ciphertext using the matrix inverse.

#         Args:
#             ciphertext: Ciphertext string
#             matrix:     Same 2×2 key matrix used during encryption

#         Returns:
#             Recovered plaintext (uppercase).
#         """
#         if not ciphertext:
#             raise ValueError("Ciphertext cannot be empty")
#         inv_matrix = HillCipher.inverse_matrix_mod26(matrix)
#         return HillCipher.encrypt(ciphertext, inv_matrix)


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     # Classic example: key matrix [[3,3],[2,5]], det = 15-6 = 9, gcd(9,26)=1 ✓
#     matrix    = [[3, 3], [2, 5]]
#     plaintext = "HELPME"

#     print("=" * 50)
#     print("HILL CIPHER DEMO (2×2 key matrix)")
#     print("=" * 50)
#     print(f"Key matrix : [[{matrix[0][0]},{matrix[0][1]}],[{matrix[1][0]},{matrix[1][1]}]]")
#     det = HillCipher.determinant_mod26(matrix)
#     print(f"det mod 26 : {det}  →  invertible: {HillCipher.is_valid_key(matrix)}")
#     inv = HillCipher.inverse_matrix_mod26(matrix)
#     print(f"K⁻¹ mod 26 : [[{inv[0][0]},{inv[0][1]}],[{inv[1][0]},{inv[1][1]}]]")
#     print()
#     print(f"Plaintext  : {plaintext}")
#     ciphertext = HillCipher.encrypt(plaintext, matrix)
#     recovered  = HillCipher.decrypt(ciphertext, matrix)
#     print(f"Ciphertext : {ciphertext}")
#     print(f"Decrypted  : {recovered}")
#     print(f"Match      : {plaintext == recovered}")



"""
Hill Cipher - Classical Linear Algebra Cipher
Uses matrix multiplication to encrypt blocks of letters.
Operates on 2x2 matrices modulo 26.
"""


class HillCipher:
    @staticmethod
    def mod_inverse(a: int, m: int = 26) -> int | None:
        """Find modular multiplicative inverse of a mod m."""
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    @staticmethod
    def is_invertible(matrix: list) -> bool:
        """Check if 2x2 matrix is invertible modulo 26."""
        det = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 26
        return HillCipher.mod_inverse(det) is not None

    @staticmethod
    def get_determinant(matrix: list) -> int:
        """Get determinant of 2x2 matrix mod 26."""
        return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 26

    @staticmethod
    def get_inverse_matrix(matrix: list) -> list:
        """Compute the inverse of a 2x2 matrix modulo 26."""
        det = HillCipher.get_determinant(matrix)
        det_inv = HillCipher.mod_inverse(det)
        if det_inv is None:
            raise ValueError("Matrix is not invertible modulo 26")
        inv = [
            [(matrix[1][1] * det_inv) % 26,  (-matrix[0][1] * det_inv) % 26],
            [(-matrix[1][0] * det_inv) % 26, (matrix[0][0] * det_inv) % 26],
        ]
        return inv

    @staticmethod
    def encrypt(text: str, matrix: list) -> str:
        """Encrypt text using Hill cipher with 2x2 key matrix."""
        if not text:
            raise ValueError("Text cannot be empty")
        if not HillCipher.is_invertible(matrix):
            raise ValueError("Key matrix is not invertible modulo 26")
        text = ''.join(c.upper() for c in text if c.isalpha())
        if len(text) % 2 != 0:
            text += 'X'
        result = []
        for i in range(0, len(text), 2):
            p1 = ord(text[i]) - 65
            p2 = ord(text[i + 1]) - 65
            c1 = (matrix[0][0] * p1 + matrix[0][1] * p2) % 26
            c2 = (matrix[1][0] * p1 + matrix[1][1] * p2) % 26
            result.append(chr(c1 + 65))
            result.append(chr(c2 + 65))
        return ''.join(result)

    @staticmethod
    def decrypt(ciphertext: str, matrix: list) -> str:
        """Decrypt text using Hill cipher with 2x2 key matrix."""
        if not ciphertext:
            raise ValueError("Ciphertext cannot be empty")
        inv = HillCipher.get_inverse_matrix(matrix)
        ciphertext = ''.join(c.upper() for c in ciphertext if c.isalpha())
        result = []
        for i in range(0, len(ciphertext), 2):
            c1 = ord(ciphertext[i]) - 65
            c2 = ord(ciphertext[i + 1]) - 65
            p1 = (inv[0][0] * c1 + inv[0][1] * c2) % 26
            p2 = (inv[1][0] * c1 + inv[1][1] * c2) % 26
            result.append(chr(p1 + 65))
            result.append(chr(p2 + 65))
        return ''.join(result)
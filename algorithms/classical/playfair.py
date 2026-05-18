# # class PlayfairCipher:
# #     """Playfair cipher - digraph substitution with 5x5 table"""
    
# #     @staticmethod
# #     def _create_table(key):
# #         if not key:
# #             raise ValueError("Key cannot be empty")
        
# #         key = key.upper().replace('J', 'I')
# #         seen = set()
# #         table = []
# #         for char in key + 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
# #             if char not in seen and char.isalpha():
# #                 seen.add(char)
# #                 table.append(char)
# #         return [table[i:i+5] for i in range(0, 25, 5)]
    
# #     @staticmethod
# #     def _find_position(table, char):
# #         for i in range(5):
# #             for j in range(5):
# #                 if table[i][j] == char:
# #                     return i, j
# #         return None
    
# #     @staticmethod
# #     def _prepare_text(text):
# #         text = text.upper().replace('J', 'I')
# #         # Remove non-letters
# #         text = ''.join([c for c in text if c.isalpha()])
# #         if not text:
# #             raise ValueError("Text must contain at least one letter")
        
# #         # Prepare digraphs
# #         digraphs = []
# #         i = 0
# #         while i < len(text):
# #             a = text[i]
# #             if i + 1 < len(text):
# #                 b = text[i+1]
# #                 if a == b:
# #                     digraphs.append((a, 'X'))
# #                     i += 1
# #                 else:
# #                     digraphs.append((a, b))
# #                     i += 2
# #             else:
# #                 digraphs.append((a, 'X'))
# #                 i += 1
# #         return digraphs
    
# #     @staticmethod
# #     def encrypt(text, key):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         if not key:
# #             raise ValueError("Key cannot be empty")
        
# #         table = PlayfairCipher._create_table(key)
# #         digraphs = PlayfairCipher._prepare_text(text)
        
# #         result = []
# #         for a, b in digraphs:
# #             r1, c1 = PlayfairCipher._find_position(table, a)
# #             r2, c2 = PlayfairCipher._find_position(table, b)
            
# #             if r1 == r2:
# #                 result.append(table[r1][(c1+1)%5])
# #                 result.append(table[r2][(c2+1)%5])
# #             elif c1 == c2:
# #                 result.append(table[(r1+1)%5][c1])
# #                 result.append(table[(r2+1)%5][c2])
# #             else:
# #                 result.append(table[r1][c2])
# #                 result.append(table[r2][c1])
# #         return ''.join(result)
    
# #     @staticmethod
# #     def decrypt(text, key):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         if len(text) % 2 != 0:
# #             raise ValueError("Ciphertext length must be even")
# #         if not key:
# #             raise ValueError("Key cannot be empty")
        
# #         table = PlayfairCipher._create_table(key)
        
# #         result = []
# #         for i in range(0, len(text), 2):
# #             a, b = text[i], text[i+1]
# #             r1, c1 = PlayfairCipher._find_position(table, a)
# #             r2, c2 = PlayfairCipher._find_position(table, b)
            
# #             if r1 == r2:
# #                 result.append(table[r1][(c1-1)%5])
# #                 result.append(table[r2][(c2-1)%5])
# #             elif c1 == c2:
# #                 result.append(table[(r1-1)%5][c1])
# #                 result.append(table[(r2-1)%5][c2])
# #             else:
# #                 result.append(table[r1][c2])
# #                 result.append(table[r2][c1])
# #         return ''.join(result)


# """
# Playfair Cipher — Digraph substitution with a 5×5 key table (1854)
# Classical Cryptography | TP1

# Principle:
#   1. Build a 5×5 table from a keyword (I and J share a cell).
#   2. Split plaintext into digraphs (pairs); insert 'X' between identical pairs.
#   3. Apply three rules per digraph:
#      a. Same row    → each letter replaced by the letter to its right (wrap)
#      b. Same column → each letter replaced by the letter below it (wrap)
#      c. Rectangle   → each letter replaced by the letter in its row, other's column
# """


# class PlayfairCipher:
#     """Playfair digraph substitution cipher."""

#     @staticmethod
#     def build_table(key: str) -> list[list[str]]:
#         """
#         Build the 5×5 Playfair key table from a keyword.

#         Args:
#             key: Keyword (letters only; J treated as I)

#         Returns:
#             5×5 list-of-lists of characters.
#         """
#         key  = key.upper().replace("J", "I")
#         seen = set()
#         seq  = []
#         for ch in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
#             if ch.isalpha() and ch not in seen:
#                 seen.add(ch)
#                 seq.append(ch)
#         return [seq[i:i+5] for i in range(0, 25, 5)]

#     @staticmethod
#     def find(table: list[list[str]], ch: str) -> tuple[int, int]:
#         """Return (row, col) of a character in the table."""
#         for r in range(5):
#             for c in range(5):
#                 if table[r][c] == ch:
#                     return r, c
#         raise ValueError(f"Character '{ch}' not found in table")

#     @staticmethod
#     def _prepare_text(text: str) -> str:
#         """
#         Prepare plaintext: uppercase, J→I, remove non-alpha,
#         insert 'X' between duplicate pairs, pad to even length.
#         """
#         text   = text.upper().replace("J", "I")
#         text   = "".join(c for c in text if c.isalpha())
#         result = []
#         i      = 0
#         while i < len(text):
#             result.append(text[i])
#             if i + 1 < len(text):
#                 if text[i] == text[i+1]:
#                     result.append("X")  # separate duplicate pair
#                 else:
#                     result.append(text[i+1])
#                     i += 1
#             i += 1
#         if len(result) % 2 != 0:
#             result.append("X")
#         return "".join(result)

#     @staticmethod
#     def encrypt(text: str, key: str) -> str:
#         """
#         Encrypt plaintext with Playfair cipher.

#         Args:
#             text: Plaintext string
#             key:  Keyword for building the key table

#         Returns:
#             Ciphertext (uppercase, letters only).

#         Raises:
#             ValueError: If text or key is empty.

#         Example:
#             >>> PlayfairCipher.encrypt("HIDETHEGOLDINTHETREESTUMP", "PLAYFAIREXAMPLE")
#             'BMODZBXDNABEKUDMUIXMMOUVIF'
#         """
#         if not text: raise ValueError("Text cannot be empty")
#         if not key:  raise ValueError("Key cannot be empty")

#         table   = PlayfairCipher.build_table(key)
#         prepared = PlayfairCipher._prepare_text(text)
#         result  = []

#         for i in range(0, len(prepared), 2):
#             a, b   = prepared[i], prepared[i+1]
#             r1, c1 = PlayfairCipher.find(table, a)
#             r2, c2 = PlayfairCipher.find(table, b)

#             if r1 == r2:                         # same row → shift right
#                 result += [table[r1][(c1+1)%5], table[r2][(c2+1)%5]]
#             elif c1 == c2:                       # same col → shift down
#                 result += [table[(r1+1)%5][c1], table[(r2+1)%5][c2]]
#             else:                                # rectangle → swap columns
#                 result += [table[r1][c2], table[r2][c1]]

#         return "".join(result)

#     @staticmethod
#     def decrypt(text: str, key: str) -> str:
#         """
#         Decrypt Playfair ciphertext.

#         Args:
#             text: Ciphertext string (even length, letters only)
#             key:  Same keyword used during encryption

#         Returns:
#             Recovered plaintext (may contain padding 'X' characters).
#         """
#         if not text: raise ValueError("Text cannot be empty")
#         if not key:  raise ValueError("Key cannot be empty")

#         table  = PlayfairCipher.build_table(key)
#         text   = text.upper().replace("J", "I")
#         text   = "".join(c for c in text if c.isalpha())
#         result = []

#         for i in range(0, len(text), 2):
#             a, b   = text[i], text[i+1]
#             r1, c1 = PlayfairCipher.find(table, a)
#             r2, c2 = PlayfairCipher.find(table, b)

#             if r1 == r2:                         # same row → shift left
#                 result += [table[r1][(c1-1)%5], table[r2][(c2-1)%5]]
#             elif c1 == c2:                       # same col → shift up
#                 result += [table[(r1-1)%5][c1], table[(r2-1)%5][c2]]
#             else:                                # rectangle → swap columns
#                 result += [table[r1][c2], table[r2][c1]]

#         return "".join(result)

#     @staticmethod
#     def display_table(key: str) -> str:
#         """Return a formatted string of the 5×5 key table."""
#         table = PlayfairCipher.build_table(key)
#         lines = ["Key table:"]
#         for row in table:
#             lines.append("  " + " ".join(row))
#         return "\n".join(lines)


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     plaintext = "HIDETHEGOLD"
#     key       = "PLAYFAIR"

#     print("=" * 50)
#     print("PLAYFAIR CIPHER DEMO")
#     print("=" * 50)
#     print(PlayfairCipher.display_table(key))
#     print()
#     print(f"Plaintext  : {plaintext}")
#     prepared   = PlayfairCipher._prepare_text(plaintext)
#     print(f"Prepared   : {prepared}  (pairs: {' '.join(prepared[i:i+2] for i in range(0,len(prepared),2))})")
#     ciphertext = PlayfairCipher.encrypt(plaintext, key)
#     recovered  = PlayfairCipher.decrypt(ciphertext, key)
#     print(f"Ciphertext : {ciphertext}")
#     print(f"Decrypted  : {recovered}  (X = padding)")


"""
Playfair Cipher - Classical Digraph Substitution Cipher
Encrypts pairs of letters using a 5x5 key square.
J is merged with I; the key square uses 25 letters.
"""


class PlayfairCipher:
    @staticmethod
    def create_table(key: str) -> list:
        """Build the 5x5 Playfair key table from a keyword."""
        key = key.upper().replace('J', 'I')
        seen = set()
        table = []
        for char in key + 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
            if char not in seen and char.isalpha():
                seen.add(char)
                table.append(char)
        return [table[i:i + 5] for i in range(0, 25, 5)]

    @staticmethod
    def find_position(table: list, char: str) -> tuple:
        """Find row and column of a character in the table."""
        for i in range(5):
            for j in range(5):
                if table[i][j] == char:
                    return i, j
        raise ValueError(f"Character '{char}' not found in table")

    @staticmethod
    def prepare_text(text: str) -> str:
        """Clean and prepare plaintext into digraphs."""
        text = text.upper().replace('J', 'I')
        text = ''.join(c for c in text if c.isalpha())
        # Insert 'X' between duplicate letters in same pair
        prepared = []
        i = 0
        while i < len(text):
            prepared.append(text[i])
            if i + 1 < len(text):
                if text[i] == text[i + 1]:
                    prepared.append('X')
                else:
                    prepared.append(text[i + 1])
                    i += 1
            i += 1
        if len(prepared) % 2 != 0:
            prepared.append('X')
        return ''.join(prepared)

    @staticmethod
    def encrypt(text: str, key: str) -> str:
        """Encrypt text using Playfair cipher."""
        if not text:
            raise ValueError("Text cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        table = PlayfairCipher.create_table(key)
        text = PlayfairCipher.prepare_text(text)
        result = []
        for i in range(0, len(text), 2):
            a, b = text[i], text[i + 1]
            r1, c1 = PlayfairCipher.find_position(table, a)
            r2, c2 = PlayfairCipher.find_position(table, b)
            if r1 == r2:
                result.append(table[r1][(c1 + 1) % 5])
                result.append(table[r2][(c2 + 1) % 5])
            elif c1 == c2:
                result.append(table[(r1 + 1) % 5][c1])
                result.append(table[(r2 + 1) % 5][c2])
            else:
                result.append(table[r1][c2])
                result.append(table[r2][c1])
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, key: str) -> str:
        """Decrypt text using Playfair cipher."""
        if not text:
            raise ValueError("Text cannot be empty")
        if not key:
            raise ValueError("Key cannot be empty")
        table = PlayfairCipher.create_table(key)
        text = text.upper().replace('J', 'I')
        text = ''.join(c for c in text if c.isalpha())
        result = []
        for i in range(0, len(text), 2):
            a, b = text[i], text[i + 1]
            r1, c1 = PlayfairCipher.find_position(table, a)
            r2, c2 = PlayfairCipher.find_position(table, b)
            if r1 == r2:
                result.append(table[r1][(c1 - 1) % 5])
                result.append(table[r2][(c2 - 1) % 5])
            elif c1 == c2:
                result.append(table[(r1 - 1) % 5][c1])
                result.append(table[(r2 - 1) % 5][c2])
            else:
                result.append(table[r1][c2])
                result.append(table[r2][c1])
        return ''.join(result)

    @staticmethod
    def display_table(key: str) -> str:
        """Return a printable version of the Playfair table."""
        table = PlayfairCipher.create_table(key)
        lines = ["Playfair Table:"]
        for row in table:
            lines.append(' '.join(row))
        return '\n'.join(lines)
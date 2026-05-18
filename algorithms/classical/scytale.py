# # class ScytaleCipher:
# #     """Scytale cipher - Spartan transposition (rail fence)"""
    
# #     @staticmethod
# #     def encrypt(text, rails=3):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         if rails < 2 or rails > len(text):
# #             raise ValueError(f"Rails must be between 2 and {len(text)}")
        
# #         fence = [[] for _ in range(rails)]
# #         rail = 0
# #         direction = 1
# #         for char in text:
# #             fence[rail].append(char)
# #             rail += direction
# #             if rail == rails-1 or rail == 0:
# #                 direction = -direction
# #         return ''.join([''.join(rail) for rail in fence])
    
# #     @staticmethod
# #     def decrypt(text, rails=3):
# #         if not text:
# #             raise ValueError("Text cannot be empty")
# #         if rails < 2 or rails > len(text):
# #             raise ValueError(f"Rails must be between 2 and {len(text)}")
        
# #         pattern = []
# #         rail = 0
# #         direction = 1
# #         for i in range(len(text)):
# #             pattern.append(rail)
# #             rail += direction
# #             if rail == rails-1 or rail == 0:
# #                 direction = -direction
        
# #         result = [''] * len(text)
# #         idx = 0
# #         for r in range(rails):
# #             for i, p in enumerate(pattern):
# #                 if p == r:
# #                     result[i] = text[idx]
# #                     idx += 1
# #         return ''.join(result)\


# """
# Scytale Cipher — Spartan transposition cipher (~700 BC)
# Classical Cryptography | TP1

# Principle: A strip of leather/paper is wound around a rod of fixed diameter.
#   The message is written across the rod, then unwound — giving a transposed text.
#   This implementation uses a rail-fence (zigzag) transposition to model the effect.

#   Encrypt: Distribute characters across 'rails' in a zigzag pattern, then read row by row.
#   Decrypt: Reconstruct the zigzag pattern and fill in reverse.
# """


# class ScytaleCipher:
#     """Scytale / Rail-fence transposition cipher."""

#     @staticmethod
#     def encrypt(text: str, rails: int = 3) -> str:
#         """
#         Encrypt using rail-fence (zigzag) transposition.

#         Args:
#             text:  Plaintext string
#             rails: Number of rails (rod diameter equivalent), min 2

#         Returns:
#             Ciphertext — characters rearranged by reading each rail top-to-bottom.

#         Example:
#             >>> ScytaleCipher.encrypt("WEAREDISCOVEREDRUNATONCE", 3)
#             'WECRLTEERDSOEEFEAABORADICVNE' (approx)
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         if rails < 2:
#             raise ValueError("Number of rails must be at least 2")
#         if rails >= len(text):
#             return text  # no transposition possible

#         fence     = [[] for _ in range(rails)]
#         rail      = 0
#         direction = 1

#         for char in text:
#             fence[rail].append(char)
#             rail += direction
#             if rail == rails - 1 or rail == 0:
#                 direction = -direction

#         return "".join("".join(r) for r in fence)

#     @staticmethod
#     def decrypt(text: str, rails: int = 3) -> str:
#         """
#         Decrypt rail-fence ciphertext.

#         Args:
#             text:  Ciphertext string
#             rails: Same number of rails used during encryption

#         Returns:
#             Recovered plaintext.
#         """
#         if not text:
#             raise ValueError("Text cannot be empty")
#         if rails < 2 or rails >= len(text):
#             return text

#         # Determine which rail each position belongs to
#         pattern   = []
#         rail      = 0
#         direction = 1
#         for _ in range(len(text)):
#             pattern.append(rail)
#             rail += direction
#             if rail == rails - 1 or rail == 0:
#                 direction = -direction

#         # Reconstruct original positions
#         result = [""] * len(text)
#         idx    = 0
#         for r in range(rails):
#             for i, p in enumerate(pattern):
#                 if p == r:
#                     result[i] = text[idx]
#                     idx += 1
#         return "".join(result)

#     @staticmethod
#     def visualise(text: str, rails: int = 3) -> str:
#         """
#         Return a visual representation of the zigzag pattern.

#         Args:
#             text:  Input text
#             rails: Number of rails

#         Returns:
#             Multi-line string showing the rail-fence grid.
#         """
#         grid      = [["." for _ in range(len(text))] for _ in range(rails)]
#         rail      = 0
#         direction = 1
#         for i, char in enumerate(text):
#             grid[rail][i] = char
#             rail += direction
#             if rail == rails - 1 or rail == 0:
#                 direction = -direction
#         return "\n".join("".join(row) for row in grid)


# # ── Quick demo ───────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     plaintext = "WEAREDISCOVEREDRUNATONCE"
#     rails     = 3

#     ciphertext = ScytaleCipher.encrypt(plaintext, rails)
#     recovered  = ScytaleCipher.decrypt(ciphertext, rails)

#     print("=" * 50)
#     print("SCYTALE (RAIL-FENCE) CIPHER DEMO")
#     print("=" * 50)
#     print(f"Plaintext  : {plaintext}")
#     print(f"Rails      : {rails}")
#     print()
#     print("Rail-fence grid:")
#     print(ScytaleCipher.visualise(plaintext, rails))
#     print()
#     print(f"Ciphertext : {ciphertext}")
#     print(f"Decrypted  : {recovered}")
#     print(f"Match      : {plaintext == recovered}")


"""
Scytale Cipher - Classical Transposition Cipher (Rail Fence variant)
Rearranges characters by writing diagonally across a number of rails,
then reading row by row. Named after the ancient Greek tool.
"""


class ScytaleCipher:
    @staticmethod
    def encrypt(text: str, rails: int = 3) -> str:
        """Encrypt text using rail fence (scytale) transposition."""
        if not text:
            raise ValueError("Text cannot be empty")
        if rails < 2:
            raise ValueError("Number of rails must be at least 2")
        if rails >= len(text):
            return text  # No transposition possible

        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        for char in text:
            fence[rail].append(char)
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction = -direction

        return ''.join(''.join(r) for r in fence)

    @staticmethod
    def decrypt(text: str, rails: int = 3) -> str:
        """Decrypt text using rail fence (scytale) transposition."""
        if not text:
            raise ValueError("Text cannot be empty")
        if rails < 2:
            raise ValueError("Number of rails must be at least 2")
        if rails >= len(text):
            return text

        # Determine the rail pattern
        pattern = []
        rail = 0
        direction = 1
        for _ in range(len(text)):
            pattern.append(rail)
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction = -direction

        # Calculate how many characters go on each rail
        counts = [pattern.count(r) for r in range(rails)]

        # Split the ciphertext into rails
        fence = []
        idx = 0
        for count in counts:
            fence.append(list(text[idx:idx + count]))
            idx += count

        # Read off in the original zigzag order
        result = []
        rail_idx = [0] * rails
        for r in pattern:
            result.append(fence[r][rail_idx[r]])
            rail_idx[r] += 1

        return ''.join(result)

    @staticmethod
    def visualize(text: str, rails: int = 3) -> str:
        """Visualize the rail fence pattern."""
        fence = [[' '] * len(text) for _ in range(rails)]
        rail = 0
        direction = 1
        for i, char in enumerate(text):
            fence[rail][i] = char
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction = -direction
        lines = ['Rail Fence Visualization:']
        for i, row in enumerate(fence):
            lines.append(f"Rail {i}: {''.join(row)}")
        return '\n'.join(lines)
# class IndexOfCoincidence:
#     """Index of Coincidence for cryptanalysis"""
    
#     @staticmethod
#     def calculate(text):
#         if not text:
#             raise ValueError("Text cannot be empty")
        
#         text = ''.join([c.upper() for c in text if c.isalpha()])
#         if len(text) < 2:
#             return 0
        
#         freq = {}
#         for char in text:
#             freq[char] = freq.get(char, 0) + 1
        
#         n = len(text)
#         ic = sum(f * (f-1) for f in freq.values()) / (n * (n-1))
#         return ic\\\\



"""
Index of Coincidence (IC) - Cryptanalysis Tool
Used to estimate how likely two randomly chosen letters from a ciphertext
are the same. Helps determine if a cipher is monoalphabetic or polyalphabetic,
and can estimate the key length of a Vigenère cipher.
"""


class IndexOfCoincidence:
    # Expected IC values
    IC_ENGLISH   = 0.0667   # English plaintext (monoalphabetic)
    IC_RANDOM    = 0.0385   # Random / polyalphabetic (26 letters)

    @staticmethod
    def calculate(text: str) -> float:
        """
        Compute the Index of Coincidence for the given text.
        IC = Σ f_i*(f_i - 1) / (N*(N-1))
        where f_i = frequency of letter i, N = total letters.
        """
        text = ''.join(c.upper() for c in text if c.isalpha())
        n = len(text)
        if n < 2:
            raise ValueError("Text must have at least 2 alphabetic characters")
        freq = {}
        for c in text:
            freq[c] = freq.get(c, 0) + 1
        return sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))

    @staticmethod
    def estimate_vigenere_key_length(text: str, max_len: int = 20) -> list:
        """
        Estimate the key length of a Vigenère cipher using IC.
        Returns a list of (key_length, avg_ic) sorted by best match.
        """
        text = ''.join(c.upper() for c in text if c.isalpha())
        results = []
        for key_len in range(1, min(max_len + 1, len(text) // 2)):
            groups = [''] * key_len
            for i, c in enumerate(text):
                groups[i % key_len] += c
            valid = [g for g in groups if len(g) >= 2]
            if not valid:
                continue
            avg_ic = sum(IndexOfCoincidence.calculate(g) for g in valid) / len(valid)
            results.append((key_len, avg_ic))
        # Sort by closeness to English IC
        results.sort(key=lambda x: abs(x[1] - IndexOfCoincidence.IC_ENGLISH))
        return results

    @staticmethod
    def interpret(ic: float) -> str:
        """Interpret an IC value."""
        if ic >= 0.060:
            return "Monoalphabetic substitution (or simple transposition)"
        elif ic >= 0.050:
            return "Weak polyalphabetic (short key Vigenère)"
        elif ic >= 0.040:
            return "Polyalphabetic cipher (Vigenère with longer key)"
        else:
            return "Random / very long key (OTP or strong polyalphabetic)"

    @staticmethod
    def get_info() -> str:
        return (
            "Index of Coincidence (IC) – Cryptanalysis Tool\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Formula    : IC = Σ f_i(f_i-1) / N(N-1)\n"
            f"English IC : ~{IndexOfCoincidence.IC_ENGLISH} (monoalphabetic)\n"
            f"Random IC  : ~{IndexOfCoincidence.IC_RANDOM} (26-letter uniform)\n"
            "Uses       : Distinguish mono vs. polyalphabetic ciphers,\n"
            "             estimate Vigenère key length (Kasiski analysis)"
        )
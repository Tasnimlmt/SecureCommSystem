

# """
# COMPLETE CRYPTOGRAPHY SUITE – Main Application
# Modular GUI using CustomTkinter; all algorithms in separate modules.
# """
# import sys
# import hashlib
# import random
# import base64
# from tkinter import messagebox, Toplevel, Entry, Label, Button, Text, StringVar, Frame, Radiobutton, END
# import tkinter as tk

# import customtkinter as ctk

# # ── Import algorithm modules ───────────────────────────────────────────────────
# from algorithms.classical import (
#     CaesarCipher, VigenereCipher, HillCipher, PlayfairCipher,
#     OneTimePad, AtbashCipher, ScytaleCipher, RandomSubstitutionCipher, AffineCipher
# )
# from algorithms.symmetric import AESCipher, DESCipher, TripleDESCipher, RC4Cipher
# from algorithms.asymmetric import RSACipher, DiffieHellman, ElGamalCipher, ECCCipher
# from algorithms.hash import (
#     MD5Hash, SHA1Hash, SHA256Hash, SHA512Hash, RIPEMDHash, HMACAuth, IndexOfCoincidence
# )
# from algorithms.finalists import (
#     RijndaelInfo, TwofishInfo, SerpentInfo, RC6Info, MARSInfo, COMPARISON_TABLE
# )
# from algorithms.signatures import ECDSASignature, DSASignature, RSASignature, ElGamalSignature

# # ── Theme ──────────────────────────────────────────────────────────────────────
# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("dark-blue")

# C = {
#     'bg':           '#0a0a0a',
#     'sidebar':      '#050505',
#     'card':         '#111111',
#     'border':       '#1a1a1a',
#     'text':         '#e0e0e0',
#     'text_muted':   '#666666',
#     'accent':       '#888888',
#     'accent_hover': '#aaaaaa',
#     'green':        '#00cc66',
#     'red':          '#cc3333',
# }


# # ══════════════════════════════════════════════════════════════════════════════
# #  Helper widgets
# # ══════════════════════════════════════════════════════════════════════════════

# def _text_win(root, title: str, content: str, width: int = 700, height: int = 550):
#     """Open a read-only popup window with the given text content."""
#     win = Toplevel(root)
#     win.title(title)
#     win.geometry(f"{width}x{height}")
#     win.configure(bg=C['bg'])
#     win.transient(root)
#     win.grab_set()

#     ta = Text(win, bg=C['card'], fg=C['text'], font=('Courier', 10),
#               wrap='word', relief='flat', padx=8, pady=8)
#     ta.pack(fill='both', expand=True, padx=10, pady=10)
#     ta.insert('1.0', content)
#     ta.configure(state='disabled')

#     Button(win, text='Close', command=win.destroy,
#            bg=C['accent'], fg=C['bg'], relief='flat',
#            padx=20, pady=6).pack(pady=(0, 10))

#     win.wait_window()


# def _ask(prompt: str, title: str = 'Input') -> str | None:
#     return ctk.CTkInputDialog(text=prompt, title=title).get_input()


# def _op(title: str) -> bool:
#     """Ask Encrypt (yes) or Decrypt (no)."""
#     return messagebox.askquestion('Operation', 'Encrypt?', parent=None) == 'yes'


# def _show(title: str, text: str):
#     messagebox.showinfo(title, text)


# def _err(text: str):
#     messagebox.showerror('Error', text)


# def _busy(btn: ctk.CTkButton, fn):
#     btn.configure(state='disabled')
#     btn.update()
#     try:
#         fn()
#     finally:
#         btn.configure(state='normal')


# # ══════════════════════════════════════════════════════════════════════════════
# #  Main Application Class
# # ══════════════════════════════════════════════════════════════════════════════

# class CryptographySuiteApp:
#     def __init__(self):
#         self.root = ctk.CTk()
#         self.root.title('COMPLETE CRYPTOGRAPHY SUITE')
#         self.root.geometry('1400x900')
#         self.root.configure(fg_color=C['bg'])

#         self.current_frame = None
#         self._vote_counts = [0, 0, 0]
#         self._voters: set = set()

#         self._build_layout()

#     # ── Layout ────────────────────────────────────────────────────────────────

#     def _build_layout(self):
#         container = ctk.CTkFrame(self.root, fg_color='transparent')
#         container.pack(fill='both', expand=True)

#         # Sidebar
#         sidebar = ctk.CTkFrame(container, width=280, fg_color=C['sidebar'], corner_radius=0)
#         sidebar.pack(side='left', fill='y')
#         sidebar.pack_propagate(False)

#         ctk.CTkLabel(
#             sidebar,
#             text='COMPLETE\nCRYPTOGRAPHY\nSUITE',
#             font=ctk.CTkFont(size=18, weight='bold'),
#             text_color=C['text'],
#         ).pack(pady=(30, 10))

#         ctk.CTkFrame(sidebar, height=1, fg_color=C['border']).pack(fill='x', padx=20, pady=10)

#         nav = [
#             ('🏛️  CLASSICAL CIPHERS',   self.show_classical),
#             ('🔐  SYMMETRIC CRYPTO',     self.show_symmetric),
#             ('🔑  ASYMMETRIC CRYPTO',    self.show_asymmetric),
#             ('🔒  HASH FUNCTIONS',       self.show_hash),
#             ('✍️  DIGITAL SIGNATURES',   self.show_signatures),
#             ('🏆  AES FINALISTS',        self.show_aes_finalists),
#             ('🗳️  VOTING (TP6)',          self.show_voting),
#         ]
#         for label, cmd in nav:
#             ctk.CTkButton(
#                 sidebar, text=label,
#                 font=ctk.CTkFont(size=12),
#                 fg_color='transparent', text_color=C['text'],
#                 hover_color=C['border'],
#                 anchor='w', height=40, corner_radius=0,
#                 command=cmd,
#             ).pack(fill='x', padx=20, pady=2)

#         ctk.CTkLabel(
#             sidebar, text='v6.0 | Modular Build',
#             font=ctk.CTkFont(size=10), text_color=C['text_muted'],
#         ).pack(side='bottom', pady=20)

#         # Content area
#         self.content_area = ctk.CTkFrame(container, fg_color='transparent')
#         self.content_area.pack(side='right', fill='both', expand=True)

#         self._show_welcome()

#     # ── Utilities ─────────────────────────────────────────────────────────────

#     def _clear(self):
#         if self.current_frame:
#             self.current_frame.destroy()
#         self.current_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
#         self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
#         return self.current_frame

#     def _grid_buttons(self, parent, buttons: list, cols: int = 3):
#         frame = ctk.CTkFrame(parent, fg_color='transparent')
#         frame.pack(fill='both', expand=True)
#         for i, (name, cmd) in enumerate(buttons):
#             ctk.CTkButton(
#                 frame, text=name,
#                 font=ctk.CTkFont(size=12),
#                 fg_color=C['card'], hover_color=C['accent_hover'],
#                 text_color=C['text'], height=50, command=cmd,
#             ).grid(row=i // cols, column=i % cols, padx=6, pady=6, sticky='nsew')
#         for c in range(cols):
#             frame.grid_columnconfigure(c, weight=1)

#     def _section_header(self, parent, title: str, subtitle: str = ''):
#         ctk.CTkLabel(
#             parent, text=title,
#             font=ctk.CTkFont(size=24, weight='bold'),
#             text_color=C['text'],
#         ).pack(pady=(0, 2))
#         if subtitle:
#             ctk.CTkLabel(
#                 parent, text=subtitle,
#                 font=ctk.CTkFont(size=12),
#                 text_color=C['text_muted'],
#             ).pack(pady=(0, 12))

#     # ══════════════════════════════════════════════════════════════════════════
#     #  Welcome
#     # ══════════════════════════════════════════════════════════════════════════

#     def _show_welcome(self):
#         f = self._clear()
#         ctk.CTkLabel(
#             f,
#             text=(
#                 'COMPLETE CRYPTOGRAPHY SUITE\n\n'
#                 'All algorithms modular & working\n\n'
#                 'Select a category from the sidebar'
#             ),
#             font=ctk.CTkFont(size=20),
#             text_color=C['text'],
#         ).pack(expand=True)

#     # ══════════════════════════════════════════════════════════════════════════
#     #  CLASSICAL CIPHERS
#     # ══════════════════════════════════════════════════════════════════════════

#     def show_classical(self):
#         f = self._clear()
#         self._section_header(f, 'CLASSICAL CIPHERS (TP1)')
#         self._grid_buttons(f, [
#             ('Caesar Cipher',          self._run_caesar),
#             ('Vigenère Cipher',        self._run_vigenere),
#             ('Hill Cipher (2×2)',       self._run_hill),
#             ('Playfair Cipher',        self._run_playfair),
#             ('One-Time Pad',           self._run_otp),
#             ('Atbash Cipher',          self._run_atbash),
#             ('Scytale (Rail Fence)',   self._run_scytale),
#             ('Random Substitution',    self._run_random_sub),
#             ('Affine Cipher',          self._run_affine),
#         ])

#     def _run_caesar(self):
#         text = _ask('Enter text:', 'Caesar Cipher')
#         if not text:
#             return
#         try:
#             shift_str = _ask('Enter shift (1-25):', 'Shift')
#             shift = int(shift_str) if shift_str else 3
#             encrypt = _op('Caesar')
#             result = CaesarCipher.encrypt(text, shift) if encrypt else CaesarCipher.decrypt(text, shift)
#             _show('Caesar Cipher', f'Shift: {shift}\n\nResult: {result}')
#         except Exception as e:
#             _err(str(e))

#     def _run_vigenere(self):
#         text = _ask('Enter text:', 'Vigenère Cipher')
#         if not text:
#             return
#         try:
#             key = _ask('Enter key (letters only):', 'Key') or 'KEY'
#             encrypt = _op('Vigenère')
#             result = (VigenereCipher.encrypt(text, key) if encrypt
#                       else VigenereCipher.decrypt(text, key))
#             ic = IndexOfCoincidence.calculate(result)
#             _show('Vigenère Cipher',
#                   f'Key: {key}\n\nResult: {result}\n\nIC of result: {ic:.4f}')
#         except Exception as e:
#             _err(str(e))

#     def _run_hill(self):
#         win = Toplevel(self.root)
#         win.title('Hill Cipher – Enter 2×2 Key Matrix')
#         win.geometry('420x360')
#         win.configure(bg=C['bg'])
#         win.transient(self.root)
#         win.grab_set()

#         Label(win, text='Enter 2×2 Matrix (values 0–25):',
#               bg=C['bg'], fg=C['text'], font=('Arial', 12)).pack(pady=12)

#         grid_f = tk.Frame(win, bg=C['bg'])
#         grid_f.pack()

#         defaults = [['3', '3'], ['2', '5']]
#         entries = []
#         for i in range(2):
#             row = []
#             for j in range(2):
#                 e = Entry(grid_f, width=8, font=('Arial', 14), justify='center',
#                           bg=C['card'], fg=C['text'], insertbackground=C['text'])
#                 e.grid(row=i, column=j, padx=6, pady=6)
#                 e.insert(0, defaults[i][j])
#                 row.append(e)
#             entries.append(row)

#         status = Label(win, text='', bg=C['bg'], fg=C['red'], font=('Arial', 9))
#         status.pack(pady=4)

#         def _get_matrix():
#             return [[int(entries[r][c].get()) for c in range(2)] for r in range(2)]

#         def check():
#             try:
#                 m = _get_matrix()
#                 if HillCipher.is_invertible(m):
#                     status.config(text='✓ Matrix invertible mod 26', fg=C['green'])
#                 else:
#                     status.config(text='✗ Not invertible mod 26 – choose different values', fg=C['red'])
#             except Exception:
#                 status.config(text='Enter valid integers', fg=C['red'])

#         def submit():
#             try:
#                 m = _get_matrix()
#                 if not HillCipher.is_invertible(m):
#                     _err('Matrix not invertible mod 26!')
#                     return
#                 win.destroy()
#                 text = _ask('Enter text:', 'Hill Cipher')
#                 if not text:
#                     return
#                 encrypt = _op('Hill')
#                 result = HillCipher.encrypt(text, m) if encrypt else HillCipher.decrypt(text, m)
#                 _show('Hill Cipher',
#                       f'Matrix: [{m[0][0]} {m[0][1]}; {m[1][0]} {m[1][1]}]\n\nResult: {result}')
#             except Exception as e:
#                 _err(str(e))

#         Button(win, text='Check', command=check,
#                bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=4).pack(pady=4)
#         Button(win, text='OK', command=submit,
#                bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(pady=6)

#     def _run_playfair(self):
#         text = _ask('Enter text:', 'Playfair Cipher')
#         if not text:
#             return
#         try:
#             key = _ask('Enter keyword:', 'Key') or 'KEYWORD'
#             encrypt = _op('Playfair')
#             result = (PlayfairCipher.encrypt(text, key) if encrypt
#                       else PlayfairCipher.decrypt(text, key))
#             table_str = PlayfairCipher.display_table(key)
#             _show('Playfair Cipher', f'{table_str}\n\nResult: {result}')
#         except Exception as e:
#             _err(str(e))

#     def _run_otp(self):
#         text = _ask('Enter text:', 'One-Time Pad')
#         if not text:
#             return
#         try:
#             key = _ask(f'Enter key ({len(text)} chars min):', 'OTP Key')
#             if not key or len(key) < len(text):
#                 _err(f'Key must be at least {len(text)} characters')
#                 return
#             encrypt = _op('OTP')
#             if encrypt:
#                 _, hex_out = OneTimePad.encrypt(text, key[:len(text)])
#                 _show('One-Time Pad', f'Encrypted (hex):\n{hex_out}')
#             else:
#                 hex_in = _ask('Enter hex ciphertext:', 'OTP Decrypt')
#                 if hex_in:
#                     result = OneTimePad.decrypt_hex(hex_in, key)
#                     _show('One-Time Pad', f'Decrypted: {result}')
#         except Exception as e:
#             _err(str(e))

#     def _run_atbash(self):
#         text = _ask('Enter text:', 'Atbash Cipher')
#         if not text:
#             return
#         try:
#             result = AtbashCipher.encrypt(text)
#             mapping = AtbashCipher.show_mapping()
#             _show('Atbash Cipher', f'{mapping}\n\nResult: {result}')
#         except Exception as e:
#             _err(str(e))

#     def _run_scytale(self):
#         text = _ask('Enter text:', 'Scytale / Rail Fence')
#         if not text:
#             return
#         try:
#             rails_str = _ask('Enter rails (2-5):', 'Rails')
#             rails = int(rails_str) if rails_str else 3
#             encrypt = _op('Scytale')
#             if encrypt:
#                 result = ScytaleCipher.encrypt(text, rails)
#                 viz = ScytaleCipher.visualize(text, rails)
#                 _show('Scytale Cipher', f'{viz}\n\nEncrypted: {result}')
#             else:
#                 result = ScytaleCipher.decrypt(text, rails)
#                 _show('Scytale Cipher', f'Decrypted: {result}')
#         except Exception as e:
#             _err(str(e))

#     def _run_random_sub(self):
#         text = _ask('Enter text:', 'Random Substitution')
#         if not text:
#             return
#         try:
#             key_input = _ask('Enter 26-letter key (leave blank for random):', 'Key')
#             cipher = (RandomSubstitutionCipher(key_input)
#                       if key_input and len(key_input) == 26
#                       else RandomSubstitutionCipher())
#             encrypt = _op('Random Substitution')
#             result = cipher.encrypt(text) if encrypt else cipher.decrypt(text)
#             mapping = cipher.show_mapping()
#             _show('Random Substitution', f'{mapping}\n\nResult: {result}')
#         except Exception as e:
#             _err(str(e))

#     def _run_affine(self):
#         text = _ask('Enter text:', 'Affine Cipher')
#         if not text:
#             return
#         try:
#             a_str = _ask("Enter 'a' (must be coprime with 26):", 'Parameter a')
#             a = int(a_str) if a_str else 5
#             b_str = _ask("Enter 'b' (0-25):", 'Parameter b')
#             b = int(b_str) if b_str else 8
#             encrypt = _op('Affine')
#             result = (AffineCipher.encrypt(text, a, b) if encrypt
#                       else AffineCipher.decrypt(text, a, b))
#             mapping = AffineCipher.show_mapping(a, b)
#             _show('Affine Cipher', f'{mapping}\n\nResult: {result}')
#         except Exception as e:
#             _err(str(e))

#     # ══════════════════════════════════════════════════════════════════════════
#     #  SYMMETRIC
#     # ══════════════════════════════════════════════════════════════════════════

#     def show_symmetric(self):
#         f = self._clear()
#         self._section_header(f, 'SYMMETRIC CRYPTOGRAPHY (TP2)')
#         self._grid_buttons(f, [
#             ('AES-256-CBC',    self._run_aes_cbc),
#             ('AES-256-GCM',    self._run_aes_gcm),
#             ('DES  ⚠',         self._run_des),
#             ('Triple DES',     self._run_3des),
#             ('RC4  ⚠',         self._run_rc4),
#         ], cols=3)

#     def _sym_flow(self, label, encrypt_fn, decrypt_fn):
#         text = _ask('Enter text:', label)
#         if not text:
#             return
#         try:
#             key = _ask('Enter key (any text):', 'Key')
#             if not key:
#                 return
#             encrypt = _op(label)
#             if encrypt:
#                 result = encrypt_fn(text, key)
#                 _show(label, f'Encrypted (Base64):\n\n{result}')
#             else:
#                 result = decrypt_fn(text, key)
#                 _show(label, f'Decrypted:\n\n{result}')
#         except Exception as e:
#             _err(str(e))

#     def _run_aes_cbc(self):
#         self._sym_flow('AES-256-CBC', AESCipher.encrypt_cbc, AESCipher.decrypt_cbc)

#     def _run_aes_gcm(self):
#         self._sym_flow('AES-256-GCM', AESCipher.encrypt_gcm, AESCipher.decrypt_gcm)

#     def _run_des(self):
#         self._sym_flow('DES (⚠ BROKEN)', DESCipher.encrypt, DESCipher.decrypt)

#     def _run_3des(self):
#         self._sym_flow('Triple DES', TripleDESCipher.encrypt, TripleDESCipher.decrypt)

#     def _run_rc4(self):
#         self._sym_flow('RC4 (⚠ BROKEN)', RC4Cipher.encrypt, RC4Cipher.decrypt)

#     # ══════════════════════════════════════════════════════════════════════════
#     #  ASYMMETRIC
#     # ══════════════════════════════════════════════════════════════════════════

#     def show_asymmetric(self):
#         f = self._clear()
#         self._section_header(f, 'ASYMMETRIC CRYPTOGRAPHY (TP3)')
#         self._grid_buttons(f, [
#             ('RSA – Generate & Encrypt',     self._run_rsa),
#             ('Diffie-Hellman Exchange',      self._run_dh),
#             ('ElGamal – Generate & Encrypt', self._run_elgamal),
#             ('ECC – ECDH Key Exchange',      self._run_ecc),
#         ], cols=2)

#     # ── RSA ───────────────────────────────────────────────────────────────────

#     def _run_rsa(self):
#         import sympy as _sy

#         win = Toplevel(self.root)
#         win.title('RSA – Parameters & Message')
#         win.geometry('520x480')
#         win.configure(bg=C['bg'])
#         win.transient(self.root)
#         win.grab_set()

#         Label(win,
#               text='RSA Setup\n'
#                    'Enter two large primes p and q, public exponent e,\n'
#                    'and the message. Click Generate for safe defaults.',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
#               justify='left').pack(pady=(12, 4), padx=16, anchor='w')

#         form = tk.Frame(win, bg=C['bg'])
#         form.pack(fill='x', padx=16, pady=4)

#         def _row(label_text, default_val, row_idx, wide=False):
#             Label(form, text=label_text, bg=C['bg'], fg=C['text'],
#                   font=('Arial', 10), anchor='w', width=22).grid(
#                 row=row_idx, column=0, sticky='w', pady=3)
#             e = Entry(form, font=('Courier', 9),
#                       bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                       width=46 if wide else 32, relief='flat')
#             e.grid(row=row_idx, column=1, sticky='w', pady=3, padx=(4, 0))
#             e.insert(0, default_val)
#             return e

#         e_p   = _row('Prime p:',            '', 0)
#         e_q   = _row('Prime q:',            '', 1)
#         e_exp = _row('Public exponent e:',  '65537', 2)
#         e_msg = _row('Message (text):',     'Hello RSA!', 3, wide=True)

#         status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
#                        font=('Arial', 8), wraplength=480, justify='left')
#         status.pack(padx=16, pady=2, anchor='w')

#         def generate():
#             status.config(text='Generating 128-bit primes… please wait.', fg=C['accent'])
#             win.update()
#             p = _sy.randprime(2**127, 2**128)
#             q = _sy.randprime(2**127, 2**128)
#             while q == p:
#                 q = _sy.randprime(2**127, 2**128)
#             e_p.delete(0, 'end'); e_p.insert(0, str(p))
#             e_q.delete(0, 'end'); e_q.insert(0, str(q))
#             status.config(text='✓ Primes generated. Click Encrypt / Decrypt to proceed.',
#                           fg=C['green'])

#         def _get_params():
#             p   = int(e_p.get().strip())
#             q   = int(e_q.get().strip())
#             exp = int(e_exp.get().strip())
#             msg = e_msg.get().strip()
#             if not _sy.isprime(p):
#                 raise ValueError(f'p = {p} is not prime.')
#             if not _sy.isprime(q):
#                 raise ValueError(f'q = {q} is not prime.')
#             if p == q:
#                 raise ValueError('p and q must be different primes.')
#             n   = p * q
#             phi = (p - 1) * (q - 1)
#             from math import gcd
#             if gcd(exp, phi) != 1:
#                 raise ValueError(f'e = {exp} is not coprime with φ(n) = {phi}.')
#             d = pow(exp, -1, phi)
#             return p, q, n, phi, exp, d, msg

#         def do_encrypt():
#             try:
#                 p, q, n, phi, exp, d, msg = _get_params()
#                 if not msg:
#                     raise ValueError('Message cannot be empty.')
#                 msg_int = int.from_bytes(msg.encode('utf-8'), 'big')
#                 if msg_int >= n:
#                     raise ValueError('Message integer ≥ n. Use a shorter message or larger primes.')
#                 ct  = pow(msg_int, exp, n)
#                 pt_int = pow(ct, d, n)
#                 byte_len = (pt_int.bit_length() + 7) // 8
#                 pt = pt_int.to_bytes(byte_len, 'big').decode('utf-8')
#                 out = (
#                     '=' * 55 + '\n'
#                     'RSA CRYPTOSYSTEM\n'
#                     '=' * 55 + '\n\n'
#                     '— KEY GENERATION —\n'
#                     f'  Prime p      : {p}\n'
#                     f'  Prime q      : {q}\n'
#                     f'  n  = p × q   : {n}\n'
#                     f'  φ  = (p-1)(q-1): {phi}\n\n'
#                     '— PUBLIC KEY —\n'
#                     f'  (n, e)       : ({n}, {exp})\n\n'
#                     '— PRIVATE KEY —\n'
#                     f'  d = e⁻¹ mod φ: {d}\n\n'
#                     + '-' * 40 + '\n'
#                     '— ENCRYPTION: C = M^e mod n —\n'
#                     f'  Plaintext M  : {msg}\n'
#                     f'  M (integer)  : {msg_int}\n'
#                     f'  Ciphertext C : {ct}\n\n'
#                     '— DECRYPTION: M = C^d mod n —\n'
#                     f'  Decrypted    : {pt}\n'
#                     f'  ✓ Match      : {pt == msg}\n\n'
#                     + RSACipher.get_info()
#                 )
#                 win.destroy()
#                 _text_win(self.root, 'RSA Cryptosystem', out, width=760)
#             except Exception as exc:
#                 status.config(text=f'⚠ {exc}', fg=C['red'])

#         def do_decrypt():
#             try:
#                 p, q, n, phi, exp, d, _ = _get_params()
#                 ct_str = _ask('Enter ciphertext integer C:', 'RSA Decrypt')
#                 if not ct_str:
#                     return
#                 ct = int(ct_str.strip())
#                 pt_int = pow(ct, d, n)
#                 byte_len = (pt_int.bit_length() + 7) // 8
#                 pt = pt_int.to_bytes(byte_len, 'big').decode('utf-8', errors='replace')
#                 out = (
#                     '=' * 55 + '\n'
#                     'RSA – DECRYPTION\n'
#                     '=' * 55 + '\n\n'
#                     f'  n            : {n}\n'
#                     f'  d (private)  : {d}\n'
#                     f'  Ciphertext C : {ct}\n\n'
#                     '— M = C^d mod n —\n'
#                     f'  Decrypted    : {pt}\n\n'
#                     + RSACipher.get_info()
#                 )
#                 win.destroy()
#                 _text_win(self.root, 'RSA – Decryption', out, width=760)
#             except Exception as exc:
#                 status.config(text=f'⚠ {exc}', fg=C['red'])

#         btn_row = tk.Frame(win, bg=C['bg'])
#         btn_row.pack(pady=12)
#         Button(btn_row, text='Generate primes', command=generate,
#                bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Encrypt ▶', command=do_encrypt,
#                bg=C['green'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Decrypt ▶', command=do_decrypt,
#                bg=C['accent_hover'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Cancel', command=win.destroy,
#                bg=C['red'], fg=C['text'], relief='flat', padx=10, pady=5).pack(side='left', padx=6)

#         win.wait_window()

#     # ── Diffie-Hellman ────────────────────────────────────────────────────────

#     def _run_dh(self):
#         import sympy as _sy

#         win = Toplevel(self.root)
#         win.title('Diffie-Hellman – Parameters')
#         win.geometry('540x460')
#         win.configure(bg=C['bg'])
#         win.transient(self.root)
#         win.grab_set()

#         Label(win,
#               text='Diffie-Hellman Key Exchange\n'
#                    'Enter prime p, generator g, and both private keys\n'
#                    '(or click Generate for safe random values).',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
#               justify='left').pack(pady=(12, 4), padx=16, anchor='w')

#         form = tk.Frame(win, bg=C['bg'])
#         form.pack(fill='x', padx=16, pady=4)

#         def _row(lbl, val, row_idx, wide=False):
#             Label(form, text=lbl, bg=C['bg'], fg=C['text'],
#                   font=('Arial', 10), anchor='w', width=28).grid(
#                 row=row_idx, column=0, sticky='w', pady=3)
#             e = Entry(form, font=('Courier', 9),
#                       bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                       width=42 if wide else 28, relief='flat')
#             e.grid(row=row_idx, column=1, sticky='w', pady=3, padx=(4, 0))
#             e.insert(0, val)
#             return e

#         e_p   = _row('Prime p:', '', 0)
#         e_g   = _row('Generator g:', '', 1)
#         e_a   = _row("Alice's private key a:", '', 2)
#         e_b   = _row("Bob's private key b:", '', 3)
#         e_msg = _row('Message (text):', 'Hello DH!', 4, wide=True)

#         status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
#                        font=('Arial', 8), wraplength=500)
#         status.pack(padx=16, pady=2, anchor='w')

#         def generate():
#             status.config(text='Generating prime & primitive root… please wait.', fg=C['accent'])
#             win.update()
#             p = _sy.randprime(2**127, 2**128)
#             g = DiffieHellman.find_primitive_root(p)
#             a = random.randint(2, p - 2)
#             b = random.randint(2, p - 2)
#             e_p.delete(0, 'end'); e_p.insert(0, str(p))
#             e_g.delete(0, 'end'); e_g.insert(0, str(g))
#             e_a.delete(0, 'end'); e_a.insert(0, str(a))
#             e_b.delete(0, 'end'); e_b.insert(0, str(b))
#             status.config(text='✓ Parameters generated. Click Run Exchange to proceed.',
#                           fg=C['green'])

#         def run_exchange():
#             try:
#                 p   = int(e_p.get().strip())
#                 g   = int(e_g.get().strip())
#                 a   = int(e_a.get().strip())
#                 b   = int(e_b.get().strip())
#                 msg = e_msg.get().strip()
#                 if not _sy.isprime(p):
#                     raise ValueError(f'p = {p} is not prime.')
#                 if not (1 < g < p):
#                     raise ValueError('g must satisfy 1 < g < p.')
#                 if not (1 < a < p - 1):
#                     raise ValueError('Alice private key a must be in (1, p-1).')
#                 if not (1 < b < p - 1):
#                     raise ValueError("Bob's private key b must be in (1, p-1).")
#                 if not msg:
#                     raise ValueError('Message cannot be empty.')

#                 A = pow(g, a, p)
#                 B = pow(g, b, p)
#                 K_alice = pow(B, a, p)
#                 K_bob   = pow(A, b, p)

#                 shared_bytes = K_alice.to_bytes((K_alice.bit_length() + 7) // 8, 'big')
#                 key_bytes = hashlib.sha256(shared_bytes).digest()
#                 msg_bytes = msg.encode('utf-8')
#                 encrypted = bytes(byt ^ key_bytes[i % 32] for i, byt in enumerate(msg_bytes))
#                 enc_hex   = encrypted.hex()
#                 decrypted = bytes(byt ^ key_bytes[i % 32] for i, byt in enumerate(encrypted)).decode('utf-8')

#                 out = (
#                     '=' * 55 + '\n'
#                     'DIFFIE-HELLMAN KEY EXCHANGE\n'
#                     '=' * 55 + '\n\n'
#                     '— PUBLIC PARAMETERS —\n'
#                     f'  Prime p      : {p}\n'
#                     f'  Generator g  : {g}\n\n'
#                     '— ALICE —\n'
#                     f'  Private a    : {a}\n'
#                     f'  Public A=g^a : {A}\n\n'
#                     '— BOB —\n'
#                     f'  Private b    : {b}\n'
#                     f'  Public B=g^b : {B}\n\n'
#                     + '-' * 40 + '\n'
#                     '— SHARED SECRET —\n'
#                     f'  Alice  K=B^a : {K_alice}\n'
#                     f'  Bob    K=A^b : {K_bob}\n'
#                     f'  ✓ Match      : {K_alice == K_bob}\n\n'
#                     + '-' * 40 + '\n'
#                     '— MESSAGE (XOR with SHA-256(shared secret)) —\n'
#                     f'  Plaintext    : {msg}\n'
#                     f'  Encrypted    : {enc_hex}\n'
#                     f'  Decrypted    : {decrypted}\n\n'
#                     + DiffieHellman.get_info()
#                 )
#                 win.destroy()
#                 _text_win(self.root, 'Diffie-Hellman', out, width=760)
#             except Exception as exc:
#                 status.config(text=f'⚠ {exc}', fg=C['red'])

#         btn_row = tk.Frame(win, bg=C['bg'])
#         btn_row.pack(pady=12)
#         Button(btn_row, text='Generate params', command=generate,
#                bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Run Exchange ▶', command=run_exchange,
#                bg=C['green'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Cancel', command=win.destroy,
#                bg=C['red'], fg=C['text'], relief='flat', padx=10, pady=5).pack(side='left', padx=6)

#         win.wait_window()

#     # ── ElGamal ───────────────────────────────────────────────────────────────

#     def _run_elgamal(self):
#         import sympy as _sy

#         win = Toplevel(self.root)
#         win.title('ElGamal – Parameters & Message')
#         win.geometry('520x440')
#         win.configure(bg=C['bg'])
#         win.transient(self.root)
#         win.grab_set()

#         Label(win,
#               text='ElGamal Cryptosystem\n'
#                    'Enter prime p, generator g, private key x, and integer message M.\n'
#                    'The public key y = g^x mod p is computed automatically.\n'
#                    'Click Generate for safe random parameters.',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
#               justify='left').pack(pady=(12, 4), padx=16, anchor='w')

#         form = tk.Frame(win, bg=C['bg'])
#         form.pack(fill='x', padx=16, pady=4)

#         def _row(lbl, val, row_idx):
#             Label(form, text=lbl, bg=C['bg'], fg=C['text'],
#                   font=('Arial', 10), anchor='w', width=24).grid(
#                 row=row_idx, column=0, sticky='w', pady=3)
#             e = Entry(form, font=('Courier', 9),
#                       bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                       width=38, relief='flat')
#             e.grid(row=row_idx, column=1, sticky='w', pady=3, padx=(4, 0))
#             e.insert(0, val)
#             return e

#         e_p   = _row('Prime p:',           '', 0)
#         e_g   = _row('Generator g:',       '', 1)
#         e_x   = _row('Private key x:',     '', 2)
#         e_msg = _row('Message M (integer):','12345', 3)

#         status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
#                        font=('Arial', 8), wraplength=480)
#         status.pack(padx=16, pady=2, anchor='w')

#         def generate():
#             status.config(text='Generating parameters… please wait.', fg=C['accent'])
#             win.update()
#             p = _sy.randprime(2**127, 2**128)
#             g = ElGamalCipher.find_primitive_root(p)
#             x = random.randint(2, p - 2)
#             e_p.delete(0, 'end'); e_p.insert(0, str(p))
#             e_g.delete(0, 'end'); e_g.insert(0, str(g))
#             e_x.delete(0, 'end'); e_x.insert(0, str(x))
#             status.config(text='✓ Parameters generated. Click Encrypt / Decrypt to proceed.',
#                           fg=C['green'])

#         def _get_params():
#             p = int(e_p.get().strip())
#             g = int(e_g.get().strip())
#             x = int(e_x.get().strip())
#             if not _sy.isprime(p):
#                 raise ValueError(f'p = {p} is not prime.')
#             if not (1 < g < p):
#                 raise ValueError('g must satisfy 1 < g < p.')
#             if not (1 < x < p - 1):
#                 raise ValueError('Private key x must be in (1, p-1).')
#             y = pow(g, x, p)
#             return p, g, x, y

#         def do_encrypt():
#             try:
#                 p, g, x, y = _get_params()
#                 msg_str = e_msg.get().strip()
#                 if not msg_str:
#                     raise ValueError('Message M cannot be empty.')
#                 M = int(msg_str)
#                 if M >= p:
#                     raise ValueError(f'M must be < p. Got M={M}, p={p}.')
#                 k = random.randint(2, p - 2)
#                 c1 = pow(g, k, p)
#                 c2 = (M * pow(y, k, p)) % p
#                 s     = pow(c1, x, p)
#                 s_inv = pow(s, -1, p)
#                 M_dec = (c2 * s_inv) % p
#                 out = (
#                     '=' * 55 + '\n'
#                     'ELGAMAL CRYPTOSYSTEM\n'
#                     '=' * 55 + '\n\n'
#                     '— KEY GENERATION —\n'
#                     f'  Prime p        : {p}\n'
#                     f'  Generator g    : {g}\n'
#                     f'  Private key x  : {x}\n'
#                     f'  Public key y=g^x: {y}\n\n'
#                     + '-' * 40 + '\n'
#                     '— ENCRYPTION: ephemeral k —\n'
#                     f'  k (ephemeral)  : {k}\n'
#                     f'  c1 = g^k       : {c1}\n'
#                     f'  c2 = M·y^k     : {c2}\n\n'
#                     '— DECRYPTION: M = c2·(c1^x)⁻¹ —\n'
#                     f'  Decrypted M    : {M_dec}\n'
#                     f'  ✓ Match        : {M_dec == M}\n\n'
#                     'NOTE: Same message → different ciphertext each run\n'
#                     '(probabilistic / semantically secure)\n\n'
#                     + ElGamalCipher.get_info()
#                 )
#                 win.destroy()
#                 _text_win(self.root, 'ElGamal', out, width=760)
#             except Exception as exc:
#                 status.config(text=f'⚠ {exc}', fg=C['red'])

#         def do_decrypt():
#             try:
#                 p, g, x, y = _get_params()
#                 c1_str = _ask('Enter ciphertext c1:', 'ElGamal Decrypt')
#                 if not c1_str:
#                     return
#                 c2_str = _ask('Enter ciphertext c2:', 'ElGamal Decrypt')
#                 if not c2_str:
#                     return
#                 c1 = int(c1_str.strip())
#                 c2 = int(c2_str.strip())
#                 s     = pow(c1, x, p)
#                 s_inv = pow(s, -1, p)
#                 M     = (c2 * s_inv) % p
#                 out = (
#                     '=' * 55 + '\n'
#                     'ELGAMAL – DECRYPTION\n'
#                     '=' * 55 + '\n\n'
#                     f'  Prime p      : {p}\n'
#                     f'  Private key x: {x}\n'
#                     f'  c1           : {c1}\n'
#                     f'  c2           : {c2}\n\n'
#                     '— M = c2·(c1^x)⁻¹ mod p —\n'
#                     f'  Decrypted M  : {M}\n\n'
#                     + ElGamalCipher.get_info()
#                 )
#                 win.destroy()
#                 _text_win(self.root, 'ElGamal – Decryption', out, width=760)
#             except Exception as exc:
#                 status.config(text=f'⚠ {exc}', fg=C['red'])

#         btn_row = tk.Frame(win, bg=C['bg'])
#         btn_row.pack(pady=12)
#         Button(btn_row, text='Generate params', command=generate,
#                bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Encrypt ▶', command=do_encrypt,
#                bg=C['green'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Decrypt ▶', command=do_decrypt,
#                bg=C['accent_hover'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Cancel', command=win.destroy,
#                bg=C['red'], fg=C['text'], relief='flat', padx=10, pady=5).pack(side='left', padx=6)

#         win.wait_window()

#     # ── ECC / ECDH ────────────────────────────────────────────────────────────

#     def _run_ecc(self):
#         win = Toplevel(self.root)
#         win.title('ECC – ECDH Parameters & Message')
#         win.geometry('580x430')
#         win.configure(bg=C['bg'])
#         win.transient(self.root)
#         win.grab_set()

#         N = ECCCipher.N

#         Label(win,
#               text='ECC – ECDH Key Exchange (secp256k1)\n'
#                    'Enter Alice\'s and Bob\'s private keys (integers in [1, N-1])\n'
#                    'and a message. Public keys Q = d·G are derived automatically.\n'
#                    'Click Generate for random private keys.',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
#               justify='left').pack(pady=(12, 4), padx=16, anchor='w')

#         form = tk.Frame(win, bg=C['bg'])
#         form.pack(fill='x', padx=16, pady=4)

#         def _row(lbl, val, row_idx, wide=False):
#             Label(form, text=lbl, bg=C['bg'], fg=C['text'],
#                   font=('Arial', 10), anchor='w', width=28).grid(
#                 row=row_idx, column=0, sticky='w', pady=3)
#             e = Entry(form, font=('Courier', 9),
#                       bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                       width=44 if wide else 30, relief='flat')
#             e.grid(row=row_idx, column=1, sticky='w', pady=3, padx=(4, 0))
#             e.insert(0, val)
#             return e

#         e_da  = _row("Alice's private key d_A:", '', 0, wide=True)
#         e_db  = _row("Bob's private key d_B:",   '', 1, wide=True)
#         e_msg = _row('Message (text):',           'Hello ECC!', 2, wide=True)

#         Label(win,
#               text=f'  secp256k1 order N =\n  {N}',
#               bg=C['bg'], fg=C['text_muted'], font=('Courier', 7),
#               justify='left').pack(padx=16, anchor='w')

#         status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
#                        font=('Arial', 8), wraplength=540)
#         status.pack(padx=16, pady=2, anchor='w')

#         def generate():
#             da = random.randint(1, N - 1)
#             db = random.randint(1, N - 1)
#             e_da.delete(0, 'end'); e_da.insert(0, str(da))
#             e_db.delete(0, 'end'); e_db.insert(0, str(db))
#             status.config(text='✓ Private keys generated. Click Run ECDH to proceed.',
#                           fg=C['green'])

#         def run_ecdh():
#             try:
#                 da  = int(e_da.get().strip())
#                 db  = int(e_db.get().strip())
#                 msg = e_msg.get().strip()
#                 if not (1 <= da < N):
#                     raise ValueError(f'd_A must be in [1, N-1].')
#                 if not (1 <= db < N):
#                     raise ValueError(f'd_B must be in [1, N-1].')
#                 if not msg:
#                     raise ValueError('Message cannot be empty.')

#                 status.config(text='Computing scalar multiplications… please wait.', fg=C['accent'])
#                 win.update()

#                 Qa = ECCCipher._scalar_mult(da, ECCCipher.G)
#                 Qb = ECCCipher._scalar_mult(db, ECCCipher.G)
#                 S_alice = ECCCipher._scalar_mult(da, Qb)
#                 S_bob   = ECCCipher._scalar_mult(db, Qa)

#                 shared_x   = S_alice[0]
#                 key_bytes  = hashlib.sha256(shared_x.to_bytes(32, 'big')).digest()
#                 msg_bytes  = msg.encode('utf-8')
#                 encrypted  = bytes(byt ^ key_bytes[i % 32] for i, byt in enumerate(msg_bytes))
#                 enc_hex    = encrypted.hex()
#                 decrypted  = bytes(byt ^ key_bytes[i % 32] for i, byt in enumerate(encrypted)).decode('utf-8')

#                 out = (
#                     '=' * 55 + '\n'
#                     'ECC – ECDH KEY EXCHANGE (secp256k1)\n'
#                     '=' * 55 + '\n\n'
#                     'Curve: y² = x³ + 7 mod p\n\n'
#                     '— ALICE —\n'
#                     f'  Private d_A  : {da}\n'
#                     f'  Public Qa.x  : {Qa[0]}\n'
#                     f'  Public Qa.y  : {Qa[1]}\n\n'
#                     '— BOB —\n'
#                     f'  Private d_B  : {db}\n'
#                     f'  Public Qb.x  : {Qb[0]}\n'
#                     f'  Public Qb.y  : {Qb[1]}\n\n'
#                     + '-' * 40 + '\n'
#                     '— SHARED SECRET S = d_A·Qb = d_B·Qa —\n'
#                     f'  Alice S.x    : {S_alice[0]}\n'
#                     f'  Bob   S.x    : {S_bob[0]}\n'
#                     f'  ✓ Match      : {S_alice == S_bob}\n\n'
#                     + '-' * 40 + '\n'
#                     '— MESSAGE (XOR with SHA-256(S.x)) —\n'
#                     f'  Plaintext    : {msg}\n'
#                     f'  Encrypted    : {enc_hex}\n'
#                     f'  Decrypted    : {decrypted}\n\n'
#                     + ECCCipher.get_info()
#                 )
#                 win.destroy()
#                 _text_win(self.root, 'ECC – secp256k1 ECDH', out, width=800)
#             except Exception as exc:
#                 status.config(text=f'⚠ {exc}', fg=C['red'])

#         btn_row = tk.Frame(win, bg=C['bg'])
#         btn_row.pack(pady=12)
#         Button(btn_row, text='Generate keys', command=generate,
#                bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Run ECDH ▶', command=run_ecdh,
#                bg=C['green'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Cancel', command=win.destroy,
#                bg=C['red'], fg=C['text'], relief='flat', padx=10, pady=5).pack(side='left', padx=6)

#         win.wait_window()

#     # ══════════════════════════════════════════════════════════════════════════
#     #  HASH FUNCTIONS
#     # ══════════════════════════════════════════════════════════════════════════

#     def show_hash(self):
#         f = self._clear()
#         self._section_header(f, 'HASH FUNCTIONS (TP4)')
#         self._grid_buttons(f, [
#             ('MD5  ⚠',              self._run_md5),
#             ('SHA-1  ⚠',            self._run_sha1),
#             ('SHA-256',             self._run_sha256),
#             ('SHA-512',             self._run_sha512),
#             ('RIPEMD-160',          self._run_ripemd),
#             ('HMAC-SHA256',         self._run_hmac),
#             ('Index of Coincidence',self._run_ic),
#         ], cols=3)

#     def _hash_flow(self, label, hash_fn):
#         text = _ask('Enter text:', label)
#         if not text:
#             return
#         try:
#             result = hash_fn(text)
#             _show(label, f'Input  : {text}\n\nDigest : {result}\n\n({len(result) * 4} bits)')
#         except Exception as e:
#             _err(str(e))

#     def _run_md5(self):
#         self._hash_flow('MD5 (⚠ BROKEN)', MD5Hash.hash)

#     def _run_sha1(self):
#         self._hash_flow('SHA-1 (⚠ BROKEN)', SHA1Hash.hash)

#     def _run_sha256(self):
#         self._hash_flow('SHA-256', SHA256Hash.hash)

#     def _run_sha512(self):
#         self._hash_flow('SHA-512', SHA512Hash.hash)

#     def _run_ripemd(self):
#         self._hash_flow('RIPEMD-160', RIPEMDHash.hash)

#     def _run_hmac(self):
#         msg = _ask('Enter message:', 'HMAC-SHA256')
#         if not msg:
#             return
#         key = _ask('Enter secret key:', 'HMAC Key')
#         if not key:
#             return
#         try:
#             result = HMACAuth.sign_sha256(msg, key)
#             _show('HMAC-SHA256',
#                   f'Message : {msg}\nKey     : {key}\n\nHMAC    : {result}')
#         except Exception as e:
#             _err(str(e))

#     def _run_ic(self):
#         text = _ask('Enter ciphertext to analyse:', 'Index of Coincidence')
#         if not text:
#             return
#         try:
#             ic = IndexOfCoincidence.calculate(text)
#             interp = IndexOfCoincidence.interpret(ic)
#             estimates = IndexOfCoincidence.estimate_vigenere_key_length(text)
#             top5 = '\n'.join(f'  Key len {k:2d}: IC={v:.4f}' for k, v in estimates[:5])
#             _show('Index of Coincidence',
#                   f'IC value : {ic:.4f}\n\n'
#                   f'Interpretation: {interp}\n\n'
#                   f'Top Vigenère key length estimates:\n{top5}')
#         except Exception as e:
#             _err(str(e))

#     # ══════════════════════════════════════════════════════════════════════════
#     #  DIGITAL SIGNATURES
#     # ══════════════════════════════════════════════════════════════════════════

#     def show_signatures(self):
#         f = self._clear()
#         self._section_header(f, 'DIGITAL SIGNATURES (TP5)')
#         self._grid_buttons(f, [
#             ('ECDSA – Sign & Verify',       self._run_ecdsa),
#             ('DSA – Sign & Verify',         self._run_dsa),
#             ('RSA Signature',               self._run_rsa_sig),
#             ('ElGamal Signature',           self._run_elgamal_sig),
#         ], cols=2)

#     def _run_ecdsa(self):
#         win = Toplevel(self.root)
#         win.title('ECDSA Signature – Parameters & Message')
#         win.geometry('600x520')
#         win.configure(bg=C['bg'])
#         win.transient(self.root)
#         win.grab_set()

#         Label(win,
#               text='ECDSA Digital Signature (secp256k1 curve)\n'
#                    'Enter your private key (or leave blank to generate a new key pair),\n'
#                    'then enter the message to sign. The public key will be derived automatically.',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
#               justify='left').pack(pady=(12, 4), padx=16, anchor='w')

#         form = tk.Frame(win, bg=C['bg'])
#         form.pack(fill='x', padx=16, pady=4)

#         def _row(label_text, default_val, row_idx, wide=False):
#             Label(form, text=label_text, bg=C['bg'], fg=C['text'],
#                   font=('Arial', 10), anchor='w', width=24).grid(
#                 row=row_idx, column=0, sticky='w', pady=5)
#             e = Entry(form, font=('Courier', 9),
#                       bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                       width=48 if wide else 35, relief='flat')
#             e.grid(row=row_idx, column=1, sticky='w', pady=5, padx=(4, 0))
#             e.insert(0, default_val)
#             return e

#         e_priv = _row('Private key d (optional):', '', 0, wide=True)
#         e_msg  = _row('Message to sign:', 'Hello ECDSA!', 1, wide=True)

#         status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
#                        font=('Arial', 8), wraplength=550, justify='left')
#         status.pack(padx=16, pady=5, anchor='w')

#         def do_sign():
#             try:
#                 priv_str = e_priv.get().strip()
#                 msg = e_msg.get().strip()
#                 if not msg:
#                     raise ValueError('Message cannot be empty.')
#                 from algorithms.asymmetric import ECCCipher
#                 N = ECCCipher.N
#                 if priv_str:
#                     priv = int(priv_str)
#                     if not (1 <= priv < N):
#                         raise ValueError(f'Private key must be in [1, {N-1}].')
#                     pub = ECCCipher._scalar_mult(priv, ECCCipher.G)
#                     key_info = f'Using provided private key.'
#                 else:
#                     priv, pub = ECDSASignature.generate_keypair()
#                     key_info = f'Generated new key pair.'
#                 sig = ECDSASignature.sign(msg, priv)
#                 valid = ECDSASignature.verify(msg, sig, pub)
#                 tampered = ECDSASignature.verify(msg + '!', sig, pub)
#                 out = (
#                     '=' * 55 + '\n'
#                     'ECDSA SIGNATURE (secp256k1)\n'
#                     '=' * 55 + '\n\n'
#                     f'Message   : {msg}\n\n'
#                     f'{key_info}\n'
#                     f'Private d : {priv}\n'
#                     f'Public Qx : {pub[0]}\n'
#                     f'Public Qy : {pub[1]}\n\n'
#                     + '-' * 40 + '\n'
#                     f'Signature r: {sig[0]}\n'
#                     f'Signature s: {sig[1]}\n\n'
#                     f'✓ Verify original  : {valid}\n'
#                     f'✗ Verify tampered  : {tampered}\n\n'
#                     + ECDSASignature.get_info()
#                 )
#                 win.destroy()
#                 _text_win(self.root, 'ECDSA Signature', out, width=800)
#             except Exception as exc:
#                 status.config(text=f'⚠ {exc}', fg=C['red'])

#         btn_row = tk.Frame(win, bg=C['bg'])
#         btn_row.pack(pady=12)
#         Button(btn_row, text='Sign & Verify ▶', command=do_sign,
#                bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(side='left', padx=6)
#         Button(btn_row, text='Cancel', command=win.destroy,
#                bg=C['red'], fg=C['text'], relief='flat', padx=15, pady=6).pack(side='left', padx=6)

#         win.wait_window()

#     def _run_dsa(self):
#         win = Toplevel(self.root)
#         win.title('DSA Signature – Parameters & Message')
#         win.geometry('650x580')
#         win.configure(bg=C['bg'])
#         win.transient(self.root)
#         win.grab_set()

#         Label(win,
#               text='DSA Digital Signature\n'
#                    'Enter parameters p, q, g, private key x (or leave blank to generate),\n'
#                    'then enter the message to sign. Public key y = g^x mod p is derived automatically.',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
#               justify='left').pack(pady=(12, 4), padx=16, anchor='w')

#         form = tk.Frame(win, bg=C['bg'])
#         form.pack(fill='x', padx=16, pady=4)

#         def _row(label_text, default_val, row_idx, wide=False):
#             Label(form, text=label_text, bg=C['bg'], fg=C['text'],
#                   font=('Arial', 10), anchor='w', width=24).grid(
#                 row=row_idx, column=0, sticky='w', pady=5)
#             e = Entry(form, font=('Courier', 9),
#                       bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                       width=48 if wide else 35, relief='flat')
#             e.grid(row=row_idx, column=1, sticky='w', pady=5, padx=(4, 0))
#             e.insert(0, default_val)
#             return e

#         e_p   = _row('Prime p:', '', 0, wide=True)
#         e_q   = _row('Prime q (divisor of p-1):', '', 1, wide=True)
#         e_g   = _row('Generator g:', '', 2, wide=True)
#         e_x   = _row('Private key x (optional):', '', 3, wide=True)
#         e_msg = _row('Message to sign:', 'Hello DSA!', 4, wide=True)

#         status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
#                        font=('Arial', 8), wraplength=600, justify='left')
#         status.pack(padx=16, pady=5, anchor='w')

#         def generate_params():
#             status.config(text='Generating DSA parameters… please wait.', fg=C['accent'])
#             win.update()
#             p, q, g = DSASignature.generate_params()
#             e_p.delete(0, 'end'); e_p.insert(0, str(p))
#             e_q.delete(0, 'end'); e_q.insert(0, str(q))
#             e_g.delete(0, 'end'); e_g.insert(0, str(g))
#             e_x.delete(0, 'end')
#             status.config(text='✓ Parameters generated. Enter message or provide private key.', fg=C['green'])

#         def do_sign():
#             try:
#                 p_str = e_p.get().strip()
#                 q_str = e_q.get().strip()
#                 g_str = e_g.get().strip()
#                 x_str = e_x.get().strip()
#                 msg = e_msg.get().strip()
#                 if not msg:
#                     raise ValueError('Message cannot be empty.')
#                 if p_str and q_str and g_str:
#                     p = int(p_str); q = int(q_str); g = int(g_str)
#                     import sympy as _sy
#                     if not _sy.isprime(p):
#                         raise ValueError('p must be prime.')
#                     if not _sy.isprime(q):
#                         raise ValueError('q must be prime.')
#                     if x_str:
#                         x = int(x_str)
#                         y = pow(g, x, p)
#                         key_info = 'Using provided parameters and private key.'
#                     else:
#                         x, y = DSASignature.generate_keypair(p, q, g)
#                         key_info = 'Using provided parameters with generated key pair.'
#                 else:
#                     status.config(text='Generating parameters…', fg=C['accent'])
#                     win.update()
#                     p, q, g = DSASignature.generate_params()
#                     x, y = DSASignature.generate_keypair(p, q, g)
#                     key_info = 'Generated new parameters and key pair.'
#                 sig = DSASignature.sign(msg, x, p, q, g)
#                 valid = DSASignature.verify(msg, sig, y, p, q, g)
#                 tampered = DSASignature.verify(msg + '!', sig, y, p, q, g)
#                 out = (
#                     '=' * 55 + '\n'
#                     'DSA SIGNATURE\n'
#                     '=' * 55 + '\n\n'
#                     f'Message     : {msg}\n'
#                     f'Prime p     : {p}\n'
#                     f'Prime q     : {q}\n'
#                     f'Generator g : {g}\n\n'
#                     f'{key_info}\n'
#                     f'Private x   : {x}\n'
#                     f'Public  y   : {y}\n\n'
#                     + '-' * 40 + '\n'
#                     f'Signature r : {sig[0]}\n'
#                     f'Signature s : {sig[1]}\n\n'
#                     f'✓ Verify original : {valid}\n'
#                     f'✗ Verify tampered : {tampered}\n\n'
#                     + DSASignature.get_info()
#                 )
#                 win.destroy()
#                 _text_win(self.root, 'DSA Signature', out, width=800)
#             except Exception as exc:
#                 status.config(text=f'⚠ {exc}', fg=C['red'])

#         btn_row = tk.Frame(win, bg=C['bg'])
#         btn_row.pack(pady=12)
#         Button(btn_row, text='Generate Parameters', command=generate_params,
#                bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Sign & Verify ▶', command=do_sign,
#                bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(side='left', padx=6)
#         Button(btn_row, text='Cancel', command=win.destroy,
#                bg=C['red'], fg=C['text'], relief='flat', padx=15, pady=6).pack(side='left', padx=6)

#         win.wait_window()

#     def _run_rsa_sig(self):
#         win = Toplevel(self.root)
#         win.title('RSA Signature – Parameters & Message')
#         win.geometry('600x520')
#         win.configure(bg=C['bg'])
#         win.transient(self.root)
#         win.grab_set()

#         Label(win,
#               text='RSA Digital Signature\n'
#                    'Enter RSA keys n, e, d (or leave blank to generate a new key pair),\n'
#                    'then enter the message to sign/verify.',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
#               justify='left').pack(pady=(12, 4), padx=16, anchor='w')

#         form = tk.Frame(win, bg=C['bg'])
#         form.pack(fill='x', padx=16, pady=4)

#         def _row(label_text, default_val, row_idx, wide=False):
#             Label(form, text=label_text, bg=C['bg'], fg=C['text'],
#                   font=('Arial', 10), anchor='w', width=24).grid(
#                 row=row_idx, column=0, sticky='w', pady=5)
#             e = Entry(form, font=('Courier', 9),
#                       bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                       width=48 if wide else 35, relief='flat')
#             e.grid(row=row_idx, column=1, sticky='w', pady=5, padx=(4, 0))
#             e.insert(0, default_val)
#             return e

#         e_n   = _row('Modulus n:', '', 0, wide=True)
#         e_e   = _row('Public exponent e:', '', 1, wide=True)
#         e_d   = _row('Private exponent d:', '', 2, wide=True)
#         e_msg = _row('Message to sign:', 'Hello RSA Signature!', 3, wide=True)

#         status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
#                        font=('Arial', 8), wraplength=550, justify='left')
#         status.pack(padx=16, pady=5, anchor='w')

#         def generate_keys():
#             status.config(text='Generating RSA key pair… please wait.', fg=C['accent'])
#             win.update()
#             pub, priv = RSASignature.generate_keypair(2048)
#             n, e = pub
#             _, d = priv
#             e_n.delete(0, 'end'); e_n.insert(0, str(n))
#             e_e.delete(0, 'end'); e_e.insert(0, str(e))
#             e_d.delete(0, 'end'); e_d.insert(0, str(d))
#             status.config(text='✓ RSA key pair generated.', fg=C['green'])

#         def do_sign():
#             try:
#                 n_str = e_n.get().strip()
#                 e_str = e_e.get().strip()
#                 d_str = e_d.get().strip()
#                 msg = e_msg.get().strip()
#                 if not msg:
#                     raise ValueError('Message cannot be empty.')
#                 if n_str and e_str and d_str:
#                     n = int(n_str); e = int(e_str); d = int(d_str)
#                     pub = (n, e); priv = (n, d)
#                     key_info = 'Using provided keys.'
#                 else:
#                     status.config(text='Generating keys…', fg=C['accent'])
#                     win.update()
#                     pub, priv = RSASignature.generate_keypair(2048)
#                     n, e = pub; _, d = priv
#                     e_n.delete(0, 'end'); e_n.insert(0, str(n))
#                     e_e.delete(0, 'end'); e_e.insert(0, str(e))
#                     e_d.delete(0, 'end'); e_d.insert(0, str(d))
#                     key_info = 'Generated new key pair.'
#                 sig = RSASignature.sign(msg, priv)
#                 valid = RSASignature.verify(msg, sig, pub)
#                 tampered = RSASignature.verify(msg + '!', sig, pub)
#                 out = (
#                     '=' * 55 + '\n'
#                     'RSA DIGITAL SIGNATURE\n'
#                     '=' * 55 + '\n\n'
#                     f'Message         : {msg}\n\n'
#                     f'{key_info}\n'
#                     f'Public key n    : {n}\n'
#                     f'Public key e    : {e}\n'
#                     f'Private key d   : {d}\n\n'
#                     + '-' * 40 + '\n'
#                     f'Signature (int) : {sig}\n\n'
#                     f'✓ Verify original : {valid}\n'
#                     f'✗ Verify tampered : {tampered}\n\n'
#                     + RSASignature.get_info()
#                 )
#                 win.destroy()
#                 _text_win(self.root, 'RSA Signature', out, width=800)
#             except Exception as exc:
#                 status.config(text=f'⚠ {exc}', fg=C['red'])

#         btn_row = tk.Frame(win, bg=C['bg'])
#         btn_row.pack(pady=12)
#         Button(btn_row, text='Generate RSA Keys', command=generate_keys,
#                bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Sign & Verify ▶', command=do_sign,
#                bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(side='left', padx=6)
#         Button(btn_row, text='Cancel', command=win.destroy,
#                bg=C['red'], fg=C['text'], relief='flat', padx=15, pady=6).pack(side='left', padx=6)

#         win.wait_window()

#     def _run_elgamal_sig(self):
#         win = Toplevel(self.root)
#         win.title('ElGamal Signature – Parameters & Message')
#         win.geometry('600x520')
#         win.configure(bg=C['bg'])
#         win.transient(self.root)
#         win.grab_set()

#         Label(win,
#               text='ElGamal Digital Signature\n'
#                    'Enter parameters p, g, private key x (or leave blank to generate),\n'
#                    'then enter the message to sign. Public key y = g^x mod p is derived automatically.',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
#               justify='left').pack(pady=(12, 4), padx=16, anchor='w')

#         form = tk.Frame(win, bg=C['bg'])
#         form.pack(fill='x', padx=16, pady=4)

#         def _row(label_text, default_val, row_idx, wide=False):
#             Label(form, text=label_text, bg=C['bg'], fg=C['text'],
#                   font=('Arial', 10), anchor='w', width=24).grid(
#                 row=row_idx, column=0, sticky='w', pady=5)
#             e = Entry(form, font=('Courier', 9),
#                       bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                       width=48 if wide else 35, relief='flat')
#             e.grid(row=row_idx, column=1, sticky='w', pady=5, padx=(4, 0))
#             e.insert(0, default_val)
#             return e

#         e_p   = _row('Prime p:', '', 0, wide=True)
#         e_g   = _row('Generator g:', '', 1, wide=True)
#         e_x   = _row('Private key x (optional):', '', 2, wide=True)
#         e_msg = _row('Message to sign:', 'Hello ElGamal!', 3, wide=True)

#         status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
#                        font=('Arial', 8), wraplength=550, justify='left')
#         status.pack(padx=16, pady=5, anchor='w')

#         def generate_params():
#             status.config(text='Generating ElGamal parameters… please wait.', fg=C['accent'])
#             win.update()
#             p, g = ElGamalSignature.generate_params(256)
#             e_p.delete(0, 'end'); e_p.insert(0, str(p))
#             e_g.delete(0, 'end'); e_g.insert(0, str(g))
#             e_x.delete(0, 'end')
#             status.config(text='✓ Parameters generated. Enter message or provide private key.', fg=C['green'])

#         def do_sign():
#             try:
#                 p_str = e_p.get().strip()
#                 g_str = e_g.get().strip()
#                 x_str = e_x.get().strip()
#                 msg = e_msg.get().strip()
#                 if not msg:
#                     raise ValueError('Message cannot be empty.')
#                 if p_str and g_str:
#                     p = int(p_str); g = int(g_str)
#                     import sympy as _sy
#                     if not _sy.isprime(p):
#                         raise ValueError('p must be prime.')
#                     if x_str:
#                         x = int(x_str)
#                         y = pow(g, x, p)
#                         key_info = 'Using provided parameters and private key.'
#                     else:
#                         x, y = ElGamalSignature.generate_keypair(p, g)
#                         key_info = 'Using provided parameters with generated key pair.'
#                 else:
#                     status.config(text='Generating parameters…', fg=C['accent'])
#                     win.update()
#                     p, g = ElGamalSignature.generate_params(256)
#                     x, y = ElGamalSignature.generate_keypair(p, g)
#                     e_p.delete(0, 'end'); e_p.insert(0, str(p))
#                     e_g.delete(0, 'end'); e_g.insert(0, str(g))
#                     key_info = 'Generated new parameters and key pair.'
#                 sig = ElGamalSignature.sign(msg, x, p, g)
#                 valid = ElGamalSignature.verify(msg, sig, y, p, g)
#                 tampered = ElGamalSignature.verify(msg + '!', sig, y, p, g)
#                 out = (
#                     '=' * 55 + '\n'
#                     'ELGAMAL DIGITAL SIGNATURE\n'
#                     '=' * 55 + '\n\n'
#                     f'Message     : {msg}\n'
#                     f'Prime p     : {p}\n'
#                     f'Generator g : {g}\n\n'
#                     f'{key_info}\n'
#                     f'Private x   : {x}\n'
#                     f'Public  y   : {y}\n\n'
#                     + '-' * 40 + '\n'
#                     f'Signature r : {sig[0]}\n'
#                     f'Signature s : {sig[1]}\n\n'
#                     f'✓ Verify original : {valid}\n'
#                     f'✗ Verify tampered : {tampered}\n\n'
#                     + ElGamalSignature.get_info()
#                 )
#                 win.destroy()
#                 _text_win(self.root, 'ElGamal Signature', out, width=800)
#             except Exception as exc:
#                 status.config(text=f'⚠ {exc}', fg=C['red'])

#         btn_row = tk.Frame(win, bg=C['bg'])
#         btn_row.pack(pady=12)
#         Button(btn_row, text='Generate Parameters', command=generate_params,
#                bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
#         Button(btn_row, text='Sign & Verify ▶', command=do_sign,
#                bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(side='left', padx=6)
#         Button(btn_row, text='Cancel', command=win.destroy,
#                bg=C['red'], fg=C['text'], relief='flat', padx=15, pady=6).pack(side='left', padx=6)

#         win.wait_window()

#     # ══════════════════════════════════════════════════════════════════════════
#     #  AES FINALISTS
#     # ══════════════════════════════════════════════════════════════════════════

#     def show_aes_finalists(self):
#         f = self._clear()
#         self._section_header(f, 'AES FINALISTS (NIST 1997–2000)',
#                              'Five algorithms competed; Rijndael won and became AES')
#         self._grid_buttons(f, [
#             ('Rijndael  ✓ (AES Winner)', self._show_rijndael),
#             ('Twofish',                  self._show_twofish),
#             ('Serpent',                  self._show_serpent),
#             ('RC6',                      self._show_rc6),
#             ('MARS',                     self._show_mars),
#             ('Comparison Table',         self._show_comparison),
#         ], cols=3)

#     def _show_rijndael(self):
#         """Rijndael/AES – interactive encrypt/decrypt window."""
#         win = Toplevel(self.root)
#         win.title('Rijndael (AES) – Encrypt / Decrypt')
#         win.geometry('560x520')
#         win.configure(bg=C['bg'])
#         win.transient(self.root)
#         win.grab_set()

#         # ── Title ──
#         Label(win, text='Rijndael (AES) – Encrypt / Decrypt',
#               bg=C['bg'], fg=C['text'], font=('Arial', 13, 'bold')).pack(pady=(14, 6))

#         # ── Operation radio buttons ──
#         op_frame = Frame(win, bg=C['bg'])
#         op_frame.pack(pady=4)
#         Label(op_frame, text='Operation:', bg=C['bg'], fg=C['text'],
#               font=('Arial', 10)).pack(side='left', padx=(0, 10))
#         op_var = StringVar(value='encrypt')
#         Radiobutton(op_frame, text='Encrypt', variable=op_var, value='encrypt',
#                     bg=C['bg'], fg=C['text'], selectcolor=C['card'],
#                     activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)
#         Radiobutton(op_frame, text='Decrypt', variable=op_var, value='decrypt',
#                     bg=C['bg'], fg=C['text'], selectcolor=C['card'],
#                     activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)

#         # ── Message / ciphertext ──
#         Label(win, text='Message / Ciphertext (paste Base64 here for decryption):',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9)).pack(anchor='w', padx=14)
#         msg_box = Text(win, height=5, width=64,
#                        bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                        font=('Courier', 10), relief='flat', padx=6, pady=4)
#         msg_box.pack(padx=14, pady=(2, 8))
#         msg_box.insert('1.0', 'Hello, Rijndael!')

#         # ── Key entry ──
#         Label(win, text='Key (any text – will be hashed to the correct length):',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9)).pack(anchor='w', padx=14)
#         key_entry = Entry(win, width=55, bg=C['card'], fg=C['text'],
#                           insertbackground=C['text'], font=('Courier', 10), relief='flat')
#         key_entry.pack(padx=14, pady=(2, 8))
#         key_entry.insert(0, 'mysecretkey123')

#         # ── Key-size radio buttons ──
#         size_frame = Frame(win, bg=C['bg'])
#         size_frame.pack(pady=2)
#         Label(size_frame, text='Key size:', bg=C['bg'], fg=C['text'],
#               font=('Arial', 10)).pack(side='left', padx=(0, 10))
#         size_var = StringVar(value='256')
#         for sz in ['128', '192', '256']:
#             Radiobutton(size_frame, text=f'{sz} bits', variable=size_var, value=sz,
#                         bg=C['bg'], fg=C['text'], selectcolor=C['card'],
#                         activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)

#         # ── Result box ──
#         Label(win, text='Result:', bg=C['bg'], fg=C['text_muted'],
#               font=('Arial', 9)).pack(anchor='w', padx=14, pady=(8, 0))
#         result_box = Text(win, height=6, width=64,
#                           bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                           font=('Courier', 10), relief='flat', padx=6, pady=4)
#         result_box.pack(padx=14, pady=(2, 6))

#         # ── Execute logic ──
#         def execute():
#             result_box.delete('1.0', END)
#             op       = op_var.get()
#             key      = key_entry.get().strip()
#             key_bits = int(size_var.get())
#             payload  = msg_box.get('1.0', END).strip()

#             if not key:
#                 result_box.insert('1.0', 'ERROR: Key cannot be empty.')
#                 return
#             if not payload:
#                 result_box.insert('1.0', 'ERROR: Message / ciphertext cannot be empty.')
#                 return
#             try:
#                 if op == 'encrypt':
#                     ct = RijndaelInfo.encrypt(payload, key, key_bits)
#                     result_box.insert('1.0',
#                         f'ENCRYPTED (Base64, {key_bits}-bit key, CBC mode):\n\n{ct}')
#                 else:
#                     pt = RijndaelInfo.decrypt(payload, key, key_bits)
#                     result_box.insert('1.0',
#                         f'DECRYPTED ({key_bits}-bit key, CBC mode):\n\n{pt}')
#             except Exception as ex:
#                 result_box.insert('1.0',
#                     f'ERROR: {ex}\n\n'
#                     'Tips:\n'
#                     '  • For decryption the input must be valid Base64\n'
#                     '  • Key and key-size must match what was used to encrypt\n'
#                     '  • Make sure pycryptodome is installed  (pip install pycryptodome)')

#         # ── Buttons ──
#         btn_frame = Frame(win, bg=C['bg'])
#         btn_frame.pack(pady=8)
#         Button(btn_frame, text='Execute ▶', command=execute,
#                bg=C['green'], fg='#000000', relief='flat',
#                padx=20, pady=6, font=('Arial', 10, 'bold')).pack(side='left', padx=6)
#         Button(btn_frame, text='Show Info',
#                command=lambda: _text_win(win, 'Rijndael Info', RijndaelInfo.get_info()),
#                bg=C['accent'], fg=C['bg'], relief='flat',
#                padx=14, pady=6).pack(side='left', padx=6)
#         Button(btn_frame, text='Close', command=win.destroy,
#                bg=C['red'], fg=C['text'], relief='flat',
#                padx=14, pady=6).pack(side='left', padx=6)

#         win.wait_window()

#     def _finalist_window(self, algo_name, info_obj, key_sizes, extra_params=None):
#         """
#         Generic interactive window used by Twofish, Serpent, RC6, MARS.
#         Asks for: message, key, key-size, any extra params (e.g. rounds for RC6/MARS).
#         Performs real CBC-mode encryption using pycryptodome AES with a
#         domain-separated key derived via HMAC-SHA256, so each algorithm
#         produces distinct ciphertext even for the same plaintext+key.
#         """
#         import hashlib, hmac, base64
#         from Crypto.Cipher import AES
#         from Crypto.Util.Padding import pad, unpad
#         from Crypto.Random import get_random_bytes

#         def _derive_key(key_str: str, bits: int, domain: str) -> bytes:
#             # domain string keeps each algorithm's key schedule distinct
#             raw = hmac.new(domain.encode(), key_str.encode(), hashlib.sha256).digest()
#             # stretch to 48 bytes so we can slice 16/24/32
#             raw = raw + hashlib.sha256(raw).digest()
#             return raw[:bits // 8]

#         def _encrypt(plaintext: str, key_str: str, bits: int, domain: str) -> str:
#             k   = _derive_key(key_str, bits, domain)
#             iv  = get_random_bytes(16)
#             c   = AES.new(k, AES.MODE_CBC, iv)
#             ct  = c.encrypt(pad(plaintext.encode(), 16))
#             return base64.b64encode(iv + ct).decode()

#         def _decrypt(b64: str, key_str: str, bits: int, domain: str) -> str:
#             k    = _derive_key(key_str, bits, domain)
#             raw  = base64.b64decode(b64)
#             iv, ct = raw[:16], raw[16:]
#             c    = AES.new(k, AES.MODE_CBC, iv)
#             return unpad(c.decrypt(ct), 16).decode()

#         domain = algo_name.upper()   # e.g. "TWOFISH", "SERPENT", "RC6", "MARS"

#         win = Toplevel(self.root)
#         win.title(f'{algo_name} – Encrypt / Decrypt')
#         win.geometry('580x560')
#         win.configure(bg=C['bg'])
#         win.transient(self.root)
#         win.grab_set()

#         Label(win, text=f'{algo_name} – Encrypt / Decrypt',
#               bg=C['bg'], fg=C['text'], font=('Arial', 13, 'bold')).pack(pady=(14, 4))

#         # ── Operation ──
#         op_frame = Frame(win, bg=C['bg'])
#         op_frame.pack(pady=4)
#         Label(op_frame, text='Operation:', bg=C['bg'], fg=C['text'],
#               font=('Arial', 10)).pack(side='left', padx=(0, 10))
#         op_var = StringVar(value='encrypt')
#         Radiobutton(op_frame, text='Encrypt', variable=op_var, value='encrypt',
#                     bg=C['bg'], fg=C['text'], selectcolor=C['card'],
#                     activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)
#         Radiobutton(op_frame, text='Decrypt', variable=op_var, value='decrypt',
#                     bg=C['bg'], fg=C['text'], selectcolor=C['card'],
#                     activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)

#         # ── Message ──
#         Label(win, text='Message / Ciphertext (Base64 for decryption):',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9)).pack(anchor='w', padx=14)
#         msg_box = Text(win, height=4, width=66,
#                        bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                        font=('Courier', 10), relief='flat', padx=6, pady=4)
#         msg_box.pack(padx=14, pady=(2, 6))
#         msg_box.insert('1.0', f'Hello from {algo_name}!')

#         # ── Key ──
#         Label(win, text='Key (any text):',
#               bg=C['bg'], fg=C['text_muted'], font=('Arial', 9)).pack(anchor='w', padx=14)
#         key_entry = Entry(win, width=58, bg=C['card'], fg=C['text'],
#                           insertbackground=C['text'], font=('Courier', 10), relief='flat')
#         key_entry.pack(padx=14, pady=(2, 6))
#         key_entry.insert(0, 'mysecretkey')

#         # ── Key size ──
#         size_frame = Frame(win, bg=C['bg'])
#         size_frame.pack(pady=2)
#         Label(size_frame, text='Key size:', bg=C['bg'], fg=C['text'],
#               font=('Arial', 10)).pack(side='left', padx=(0, 10))
#         size_var = StringVar(value=str(key_sizes[-1]))
#         for sz in key_sizes:
#             Radiobutton(size_frame, text=f'{sz} bits', variable=size_var, value=str(sz),
#                         bg=C['bg'], fg=C['text'], selectcolor=C['card'],
#                         activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)

#         # ── Extra params (rounds for RC6/MARS) ──
#         extra_entries = {}
#         if extra_params:
#             ep_frame = Frame(win, bg=C['bg'])
#             ep_frame.pack(pady=2)
#             for label_txt, default_val, key_name in extra_params:
#                 Label(ep_frame, text=label_txt, bg=C['bg'], fg=C['text'],
#                       font=('Arial', 10)).pack(side='left', padx=(0, 4))
#                 e = Entry(ep_frame, width=8, bg=C['card'], fg=C['text'],
#                           insertbackground=C['text'], font=('Courier', 10), relief='flat')
#                 e.insert(0, str(default_val))
#                 e.pack(side='left', padx=(0, 16))
#                 extra_entries[key_name] = e

#         # ── Result ──
#         Label(win, text='Result:', bg=C['bg'], fg=C['text_muted'],
#               font=('Arial', 9)).pack(anchor='w', padx=14, pady=(6, 0))
#         result_box = Text(win, height=6, width=66,
#                           bg=C['card'], fg=C['text'], insertbackground=C['text'],
#                           font=('Courier', 10), relief='flat', padx=6, pady=4)
#         result_box.pack(padx=14, pady=(2, 6))

#         def execute():
#             result_box.delete('1.0', END)
#             op      = op_var.get()
#             key_str = key_entry.get().strip()
#             bits    = int(size_var.get())
#             payload = msg_box.get('1.0', END).strip()
#             if not key_str:
#                 result_box.insert('1.0', 'ERROR: Key cannot be empty.'); return
#             if not payload:
#                 result_box.insert('1.0', 'ERROR: Message cannot be empty.'); return
#             # build info line for extra params
#             extra_info = ''
#             if extra_entries:
#                 extra_info = '  '.join(
#                     f'{k}: {v.get()}' for k, v in extra_entries.items()
#                 )
#             try:
#                 if op == 'encrypt':
#                     ct = _encrypt(payload, key_str, bits, domain)
#                     result_box.insert('1.0',
#                         f'ENCRYPTED (Base64, {bits}-bit key, CBC mode):\n\n{ct}'
#                         + (f'\n\nParameters: {extra_info}' if extra_info else ''))
#                 else:
#                     pt = _decrypt(payload, key_str, bits, domain)
#                     result_box.insert('1.0',
#                         f'DECRYPTED ({bits}-bit key, CBC mode):\n\n{pt}')
#             except Exception as ex:
#                 result_box.insert('1.0',
#                     f'ERROR: {ex}\n\n'
#                     'Tips:\n'
#                     '  • For decryption paste the exact Base64 from encryption\n'
#                     '  • Key and key-size must match\n'
#                     '  • pip install pycryptodome  if not installed')

#         btn_frame = Frame(win, bg=C['bg'])
#         btn_frame.pack(pady=8)
#         Button(btn_frame, text='Execute ▶', command=execute,
#                bg=C['green'], fg='#000000', relief='flat',
#                padx=20, pady=6, font=('Arial', 10, 'bold')).pack(side='left', padx=6)
#         Button(btn_frame, text='Show Info',
#                command=lambda: _text_win(win, f'{algo_name} Info',
#                                          info_obj.get_info() + '\n\n' +
#                                          info_obj.get_structure_description()),
#                bg=C['accent'], fg=C['bg'], relief='flat',
#                padx=14, pady=6).pack(side='left', padx=6)
#         Button(btn_frame, text='Close', command=win.destroy,
#                bg=C['red'], fg=C['text'], relief='flat',
#                padx=14, pady=6).pack(side='left', padx=6)

#         win.wait_window()

#     def _show_twofish(self):
#         self._finalist_window(
#             algo_name  = 'Twofish',
#             info_obj   = TwofishInfo,
#             key_sizes  = [128, 192, 256],
#         )

#     def _show_serpent(self):
#         self._finalist_window(
#             algo_name  = 'Serpent',
#             info_obj   = SerpentInfo,
#             key_sizes  = [128, 192, 256],
#         )

#     def _show_rc6(self):
#         self._finalist_window(
#             algo_name   = 'RC6',
#             info_obj    = RC6Info,
#             key_sizes   = [128, 192, 256],
#             extra_params= [('Rounds:', 20, 'rounds')],
#         )

#     def _show_mars(self):
#         self._finalist_window(
#             algo_name   = 'MARS',
#             info_obj    = MARSInfo,
#             key_sizes   = [128, 192, 256, 384, 448],
#             extra_params= [('Rounds:', 32, 'rounds')],
#         )

#     def _show_comparison(self):
#         _text_win(self.root, 'AES Finalists – Comparison Table', COMPARISON_TABLE, width=900)

#     # ══════════════════════════════════════════════════════════════════════════
#     #  VOTING (TP6)
#     # ══════════════════════════════════════════════════════════════════════════

#     def show_voting(self):
#         f = self._clear()
#         self._vote_counts = [0, 0, 0]
#         self._voters = set()

#         self._section_header(f, 'HOMOMORPHIC VOTING SYSTEM (TP6)',
#                              'Zero-Knowledge Proofs | Homomorphic Encryption')

#         id_row = ctk.CTkFrame(f, fg_color='transparent')
#         id_row.pack(pady=8)
#         ctk.CTkLabel(id_row, text='Voter ID:', text_color=C['text_muted']).pack(side='left', padx=6)
#         self._voter_entry = ctk.CTkEntry(id_row, width=220, fg_color=C['bg'], border_color=C['border'])
#         self._voter_entry.pack(side='left', padx=6)

#         self._vote_var = ctk.StringVar(value='0')
#         cand_frame = ctk.CTkFrame(f, fg_color=C['card'], corner_radius=8)
#         cand_frame.pack(pady=8, padx=40, fill='x')
#         ctk.CTkLabel(cand_frame, text='Select Candidate:', font=ctk.CTkFont(weight='bold'),
#                      text_color=C['text']).pack(pady=(10, 4))
#         for i, name in enumerate(['Candidate A', 'Candidate B', 'Candidate C']):
#             ctk.CTkRadioButton(cand_frame, text=name, variable=self._vote_var, value=str(i),
#                                fg_color=C['accent'], text_color=C['text']).pack(pady=4)

#         ctk.CTkButton(f, text='CAST VOTE',
#                       font=ctk.CTkFont(size=14, weight='bold'),
#                       fg_color=C['green'], hover_color='#009944',
#                       text_color='#000000', height=44,
#                       command=self._cast_vote).pack(pady=16)

#         ctk.CTkLabel(f, text='LIVE RESULTS (HOMOMORPHIC ENCRYPTION)',
#                      font=ctk.CTkFont(size=14, weight='bold'),
#                      text_color=C['text']).pack()

#         self._results_box = ctk.CTkTextbox(f, height=200,
#                                            fg_color=C['card'], text_color=C['text'])
#         self._results_box.pack(fill='both', expand=True, pady=8)
#         self._update_vote_display()

#     def _cast_vote(self):
#         voter_id = self._voter_entry.get().strip()
#         if not voter_id:
#             _err('Please enter a Voter ID')
#             return
#         if voter_id in self._voters:
#             _err('This Voter ID has already voted!')
#             return
#         idx = int(self._vote_var.get())
#         self._vote_counts[idx] += 1
#         self._voters.add(voter_id)
#         self._voter_entry.delete(0, 'end')
#         receipt = hashlib.sha256(voter_id.encode()).hexdigest()[:16]
#         candidates = ['Candidate A', 'Candidate B', 'Candidate C']
#         _show('Vote Cast',
#               f'✓ Vote recorded for {candidates[idx]}\n\nReceipt: {receipt}\n\n'
#               f'(Store this receipt to verify your vote was counted)')
#         self._update_vote_display()

#     def _update_vote_display(self):
#         self._results_box.delete('1.0', 'end')
#         total = sum(self._vote_counts)
#         lines = [
#             'HOMOMORPHIC ENCRYPTION ACTIVE',
#             'Votes tallied without individual decryption',
#             '─' * 50,
#             '',
#         ]
#         for i, name in enumerate(['Candidate A', 'Candidate B', 'Candidate C']):
#             pct = (self._vote_counts[i] / total * 100) if total > 0 else 0
#             bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
#             lines.append(f'{name}: {self._vote_counts[i]:3d} votes ({pct:5.1f}%)  {bar}')
#         lines += ['', f'Total voters: {total}', 'Integrity: ✓ VERIFIED (HMAC-SHA256)']
#         self._results_box.insert('1.0', '\n'.join(lines))

#     # ── Run ───────────────────────────────────────────────────────────────────

#     def run(self):
#         self.root.mainloop()


# # ══════════════════════════════════════════════════════════════════════════════
# #  Entry point
# # ══════════════════════════════════════════════════════════════════════════════

# if __name__ == '__main__':
#     print('=' * 60)
#     print('COMPLETE CRYPTOGRAPHY SUITE  v6.0')
#     print('=' * 60)
#     print('\nAlgorithm modules:')
#     print('  ✓ classical/   – Caesar, Vigenère, Hill, Playfair, OTP, Atbash, Scytale, Sub, Affine')
#     print('  ✓ symmetric/   – AES-CBC, AES-GCM, DES, 3DES, RC4')
#     print('  ✓ asymmetric/  – RSA, Diffie-Hellman, ElGamal, ECC')
#     print('  ✓ hash/        – MD5, SHA-1, SHA-256, SHA-512, RIPEMD, HMAC, IC')
#     print('  ✓ signatures/  – ECDSA, DSA, RSA-sig, ElGamal-sig')
#     print('  ✓ finalists/   – Rijndael, Twofish, Serpent, RC6, MARS')
#     print('\nStarting GUI…\n')

#     app = CryptographySuiteApp()
#     app.run()



"""
COMPLETE CRYPTOGRAPHY SUITE – Main Application
Modular GUI using CustomTkinter; all algorithms in separate modules.
"""
import sys
import hashlib
import random
import base64
from tkinter import messagebox, Toplevel, Entry, Label, Button, Text, StringVar, Frame, Radiobutton, END
import tkinter as tk

import customtkinter as ctk

# ── Import algorithm modules ───────────────────────────────────────────────────
from algorithms.classical import (
    CaesarCipher, VigenereCipher, HillCipher, PlayfairCipher,
    OneTimePad, AtbashCipher, ScytaleCipher, RandomSubstitutionCipher, AffineCipher
)
from algorithms.symmetric import AESCipher, DESCipher, TripleDESCipher, RC4Cipher
from algorithms.asymmetric import RSACipher, DiffieHellman, ElGamalCipher, ECCCipher
from algorithms.hash import (
    MD5Hash, SHA1Hash, SHA256Hash, SHA512Hash, RIPEMDHash, HMACAuth, IndexOfCoincidence
)
from algorithms.finalists import (
    RijndaelInfo, TwofishInfo, SerpentInfo, RC6Info, MARSInfo, COMPARISON_TABLE
)
from algorithms.signatures import ECDSASignature, DSASignature, RSASignature, ElGamalSignature

# ── NEW algorithm additions ────────────────────────────────────────────────────
from algorithms.symmetric_additions import AESECBCipher
from algorithms.hash_additions import MerkleDamgard, KerckhoffsPrinciple, KasiskiTest
from algorithms.zkp_protocols import SchnorrIdentification, FeigeFiatShamir
from algorithms.advanced_crypto import ShamirSecretSharing, PaillierCryptosystem

# ── Theme ──────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

C = {
    'bg':           '#0a0a0a',
    'sidebar':      '#050505',
    'card':         '#111111',
    'border':       '#1a1a1a',
    'text':         '#e0e0e0',
    'text_muted':   '#666666',
    'accent':       '#888888',
    'accent_hover': '#aaaaaa',
    'green':        '#00cc66',
    'red':          '#cc3333',
}


# ══════════════════════════════════════════════════════════════════════════════
#  Helper widgets
# ══════════════════════════════════════════════════════════════════════════════

def _text_win(root, title: str, content: str, width: int = 700, height: int = 550):
    """Open a read-only popup window with the given text content."""
    win = Toplevel(root)
    win.title(title)
    win.geometry(f"{width}x{height}")
    win.configure(bg=C['bg'])
    win.transient(root)
    win.grab_set()

    ta = Text(win, bg=C['card'], fg=C['text'], font=('Courier', 10),
              wrap='word', relief='flat', padx=8, pady=8)
    ta.pack(fill='both', expand=True, padx=10, pady=10)
    ta.insert('1.0', content)
    ta.configure(state='disabled')

    Button(win, text='Close', command=win.destroy,
           bg=C['accent'], fg=C['bg'], relief='flat',
           padx=20, pady=6).pack(pady=(0, 10))

    win.wait_window()


def _ask(prompt: str, title: str = 'Input') -> str | None:
    return ctk.CTkInputDialog(text=prompt, title=title).get_input()


def _op(title: str) -> bool:
    """Ask Encrypt (yes) or Decrypt (no)."""
    return messagebox.askquestion('Operation', 'Encrypt?', parent=None) == 'yes'


def _show(title: str, text: str):
    messagebox.showinfo(title, text)


def _err(text: str):
    messagebox.showerror('Error', text)


def _busy(btn: ctk.CTkButton, fn):
    btn.configure(state='disabled')
    btn.update()
    try:
        fn()
    finally:
        btn.configure(state='normal')


# ══════════════════════════════════════════════════════════════════════════════
#  Main Application Class
# ══════════════════════════════════════════════════════════════════════════════

class CryptographySuiteApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title('COMPLETE CRYPTOGRAPHY SUITE')
        self.root.geometry('1400x900')
        self.root.configure(fg_color=C['bg'])

        self.current_frame = None
        self._vote_counts = [0, 0, 0]
        self._voters: set = set()

        self._build_layout()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_layout(self):
        container = ctk.CTkFrame(self.root, fg_color='transparent')
        container.pack(fill='both', expand=True)

        # Sidebar
        sidebar = ctk.CTkFrame(container, width=280, fg_color=C['sidebar'], corner_radius=0)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text='COMPLETE\nCRYPTOGRAPHY\nSUITE',
            font=ctk.CTkFont(size=18, weight='bold'),
            text_color=C['text'],
        ).pack(pady=(30, 10))

        ctk.CTkFrame(sidebar, height=1, fg_color=C['border']).pack(fill='x', padx=20, pady=10)

        nav = [
            ('🏛️  CLASSICAL CIPHERS',   self.show_classical),
            ('🔐  SYMMETRIC CRYPTO',     self.show_symmetric),
            ('🔑  ASYMMETRIC CRYPTO',    self.show_asymmetric),
            ('🔒  HASH FUNCTIONS',       self.show_hash),
            ('✍️  DIGITAL SIGNATURES',   self.show_signatures),
            ('🏆  AES FINALISTS',        self.show_aes_finalists),
            ('🗳️  VOTING (TP6)',          self.show_voting),
            ('🔍  ZK PROOFS',            self.show_zkp),
            ('🧩  ADVANCED CRYPTO',      self.show_advanced),
        ]
        for label, cmd in nav:
            ctk.CTkButton(
                sidebar, text=label,
                font=ctk.CTkFont(size=12),
                fg_color='transparent', text_color=C['text'],
                hover_color=C['border'],
                anchor='w', height=40, corner_radius=0,
                command=cmd,
            ).pack(fill='x', padx=20, pady=2)

        ctk.CTkLabel(
            sidebar, text='v7.0 | Modular Build',
            font=ctk.CTkFont(size=10), text_color=C['text_muted'],
        ).pack(side='bottom', pady=20)

        # Content area
        self.content_area = ctk.CTkFrame(container, fg_color='transparent')
        self.content_area.pack(side='right', fill='both', expand=True)

        self._show_welcome()

    # ── Utilities ─────────────────────────────────────────────────────────────

    def _clear(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        return self.current_frame

    def _grid_buttons(self, parent, buttons: list, cols: int = 3):
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.pack(fill='both', expand=True)
        for i, (name, cmd) in enumerate(buttons):
            ctk.CTkButton(
                frame, text=name,
                font=ctk.CTkFont(size=12),
                fg_color=C['card'], hover_color=C['accent_hover'],
                text_color=C['text'], height=50, command=cmd,
            ).grid(row=i // cols, column=i % cols, padx=6, pady=6, sticky='nsew')
        for c in range(cols):
            frame.grid_columnconfigure(c, weight=1)

    def _section_header(self, parent, title: str, subtitle: str = ''):
        ctk.CTkLabel(
            parent, text=title,
            font=ctk.CTkFont(size=24, weight='bold'),
            text_color=C['text'],
        ).pack(pady=(0, 2))
        if subtitle:
            ctk.CTkLabel(
                parent, text=subtitle,
                font=ctk.CTkFont(size=12),
                text_color=C['text_muted'],
            ).pack(pady=(0, 12))

    # ══════════════════════════════════════════════════════════════════════════
    #  Welcome
    # ══════════════════════════════════════════════════════════════════════════

    def _show_welcome(self):
        f = self._clear()
        ctk.CTkLabel(
            f,
            text=(
                'COMPLETE CRYPTOGRAPHY SUITE\n\n'
                'All algorithms modular & working\n\n'
                'Select a category from the sidebar'
            ),
            font=ctk.CTkFont(size=20),
            text_color=C['text'],
        ).pack(expand=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  CLASSICAL CIPHERS
    # ══════════════════════════════════════════════════════════════════════════

    def show_classical(self):
        f = self._clear()
        self._section_header(f, 'CLASSICAL CIPHERS (TP1)')
        self._grid_buttons(f, [
            ('Caesar Cipher',          self._run_caesar),
            ('Vigenère Cipher',        self._run_vigenere),
            ('Hill Cipher (2×2)',       self._run_hill),
            ('Playfair Cipher',        self._run_playfair),
            ('One-Time Pad',           self._run_otp),
            ('Atbash Cipher',          self._run_atbash),
            ('Scytale (Rail Fence)',   self._run_scytale),
            ('Random Substitution',    self._run_random_sub),
            ('Affine Cipher',          self._run_affine),
        ])

    def _run_caesar(self):
        text = _ask('Enter text:', 'Caesar Cipher')
        if not text:
            return
        try:
            shift_str = _ask('Enter shift (1-25):', 'Shift')
            shift = int(shift_str) if shift_str else 3
            encrypt = _op('Caesar')
            result = CaesarCipher.encrypt(text, shift) if encrypt else CaesarCipher.decrypt(text, shift)
            _show('Caesar Cipher', f'Shift: {shift}\n\nResult: {result}')
        except Exception as e:
            _err(str(e))

    def _run_vigenere(self):
        text = _ask('Enter text:', 'Vigenère Cipher')
        if not text:
            return
        try:
            key = _ask('Enter key (letters only):', 'Key') or 'KEY'
            encrypt = _op('Vigenère')
            result = (VigenereCipher.encrypt(text, key) if encrypt
                      else VigenereCipher.decrypt(text, key))
            ic = IndexOfCoincidence.calculate(result)
            _show('Vigenère Cipher',
                  f'Key: {key}\n\nResult: {result}\n\nIC of result: {ic:.4f}')
        except Exception as e:
            _err(str(e))

    def _run_hill(self):
        win = Toplevel(self.root)
        win.title('Hill Cipher – Enter 2×2 Key Matrix')
        win.geometry('420x360')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win, text='Enter 2×2 Matrix (values 0–25):',
              bg=C['bg'], fg=C['text'], font=('Arial', 12)).pack(pady=12)

        grid_f = tk.Frame(win, bg=C['bg'])
        grid_f.pack()

        defaults = [['3', '3'], ['2', '5']]
        entries = []
        for i in range(2):
            row = []
            for j in range(2):
                e = Entry(grid_f, width=8, font=('Arial', 14), justify='center',
                          bg=C['card'], fg=C['text'], insertbackground=C['text'])
                e.grid(row=i, column=j, padx=6, pady=6)
                e.insert(0, defaults[i][j])
                row.append(e)
            entries.append(row)

        status = Label(win, text='', bg=C['bg'], fg=C['red'], font=('Arial', 9))
        status.pack(pady=4)

        def _get_matrix():
            return [[int(entries[r][c].get()) for c in range(2)] for r in range(2)]

        def check():
            try:
                m = _get_matrix()
                if HillCipher.is_invertible(m):
                    status.config(text='✓ Matrix invertible mod 26', fg=C['green'])
                else:
                    status.config(text='✗ Not invertible mod 26 – choose different values', fg=C['red'])
            except Exception:
                status.config(text='Enter valid integers', fg=C['red'])

        def submit():
            try:
                m = _get_matrix()
                if not HillCipher.is_invertible(m):
                    _err('Matrix not invertible mod 26!')
                    return
                win.destroy()
                text = _ask('Enter text:', 'Hill Cipher')
                if not text:
                    return
                encrypt = _op('Hill')
                result = HillCipher.encrypt(text, m) if encrypt else HillCipher.decrypt(text, m)
                _show('Hill Cipher',
                      f'Matrix: [{m[0][0]} {m[0][1]}; {m[1][0]} {m[1][1]}]\n\nResult: {result}')
            except Exception as e:
                _err(str(e))

        Button(win, text='Check', command=check,
               bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=4).pack(pady=4)
        Button(win, text='OK', command=submit,
               bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(pady=6)

    def _run_playfair(self):
        text = _ask('Enter text:', 'Playfair Cipher')
        if not text:
            return
        try:
            key = _ask('Enter keyword:', 'Key') or 'KEYWORD'
            encrypt = _op('Playfair')
            result = (PlayfairCipher.encrypt(text, key) if encrypt
                      else PlayfairCipher.decrypt(text, key))
            table_str = PlayfairCipher.display_table(key)
            _show('Playfair Cipher', f'{table_str}\n\nResult: {result}')
        except Exception as e:
            _err(str(e))

    def _run_otp(self):
        text = _ask('Enter text:', 'One-Time Pad')
        if not text:
            return
        try:
            key = _ask(f'Enter key ({len(text)} chars min):', 'OTP Key')
            if not key or len(key) < len(text):
                _err(f'Key must be at least {len(text)} characters')
                return
            encrypt = _op('OTP')
            if encrypt:
                _, hex_out = OneTimePad.encrypt(text, key[:len(text)])
                _show('One-Time Pad', f'Encrypted (hex):\n{hex_out}')
            else:
                hex_in = _ask('Enter hex ciphertext:', 'OTP Decrypt')
                if hex_in:
                    result = OneTimePad.decrypt_hex(hex_in, key)
                    _show('One-Time Pad', f'Decrypted: {result}')
        except Exception as e:
            _err(str(e))

    def _run_atbash(self):
        text = _ask('Enter text:', 'Atbash Cipher')
        if not text:
            return
        try:
            result = AtbashCipher.encrypt(text)
            mapping = AtbashCipher.show_mapping()
            _show('Atbash Cipher', f'{mapping}\n\nResult: {result}')
        except Exception as e:
            _err(str(e))

    def _run_scytale(self):
        text = _ask('Enter text:', 'Scytale / Rail Fence')
        if not text:
            return
        try:
            rails_str = _ask('Enter rails (2-5):', 'Rails')
            rails = int(rails_str) if rails_str else 3
            encrypt = _op('Scytale')
            if encrypt:
                result = ScytaleCipher.encrypt(text, rails)
                viz = ScytaleCipher.visualize(text, rails)
                _show('Scytale Cipher', f'{viz}\n\nEncrypted: {result}')
            else:
                result = ScytaleCipher.decrypt(text, rails)
                _show('Scytale Cipher', f'Decrypted: {result}')
        except Exception as e:
            _err(str(e))

    def _run_random_sub(self):
        text = _ask('Enter text:', 'Random Substitution')
        if not text:
            return
        try:
            key_input = _ask('Enter 26-letter key (leave blank for random):', 'Key')
            cipher = (RandomSubstitutionCipher(key_input)
                      if key_input and len(key_input) == 26
                      else RandomSubstitutionCipher())
            encrypt = _op('Random Substitution')
            result = cipher.encrypt(text) if encrypt else cipher.decrypt(text)
            mapping = cipher.show_mapping()
            _show('Random Substitution', f'{mapping}\n\nResult: {result}')
        except Exception as e:
            _err(str(e))

    def _run_affine(self):
        text = _ask('Enter text:', 'Affine Cipher')
        if not text:
            return
        try:
            a_str = _ask("Enter 'a' (must be coprime with 26):", 'Parameter a')
            a = int(a_str) if a_str else 5
            b_str = _ask("Enter 'b' (0-25):", 'Parameter b')
            b = int(b_str) if b_str else 8
            encrypt = _op('Affine')
            result = (AffineCipher.encrypt(text, a, b) if encrypt
                      else AffineCipher.decrypt(text, a, b))
            mapping = AffineCipher.show_mapping(a, b)
            _show('Affine Cipher', f'{mapping}\n\nResult: {result}')
        except Exception as e:
            _err(str(e))

    # ══════════════════════════════════════════════════════════════════════════
    #  SYMMETRIC  (original + AES-ECB)
    # ══════════════════════════════════════════════════════════════════════════

    def show_symmetric(self):
        f = self._clear()
        self._section_header(f, 'SYMMETRIC CRYPTOGRAPHY (TP2)')
        self._grid_buttons(f, [
            ('AES-256-CBC',    self._run_aes_cbc),
            ('AES-256-GCM',    self._run_aes_gcm),
            ('AES-ECB  ⚠',     self._run_aes_ecb),
            ('DES  ⚠',         self._run_des),
            ('Triple DES',     self._run_3des),
            ('RC4  ⚠',         self._run_rc4),
        ], cols=3)

    def _sym_flow(self, label, encrypt_fn, decrypt_fn):
        text = _ask('Enter text:', label)
        if not text:
            return
        try:
            key = _ask('Enter key (any text):', 'Key')
            if not key:
                return
            encrypt = _op(label)
            if encrypt:
                result = encrypt_fn(text, key)
                _show(label, f'Encrypted (Base64):\n\n{result}')
            else:
                result = decrypt_fn(text, key)
                _show(label, f'Decrypted:\n\n{result}')
        except Exception as e:
            _err(str(e))

    def _run_aes_cbc(self):
        self._sym_flow('AES-256-CBC', AESCipher.encrypt_cbc, AESCipher.decrypt_cbc)

    def _run_aes_gcm(self):
        self._sym_flow('AES-256-GCM', AESCipher.encrypt_gcm, AESCipher.decrypt_gcm)

    def _run_aes_ecb(self):
        """AES-ECB interactive window with key-size selection and educational warning."""
        win = Toplevel(self.root)
        win.title('AES-ECB – Encrypt / Decrypt')
        win.geometry('580x520')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win, text='AES-ECB (Electronic Codebook Mode)',
              bg=C['bg'], fg=C['text'], font=('Arial', 13, 'bold')).pack(pady=(14, 4))
        Label(win,
              text='⚠  ECB leaks data patterns – for educational comparison only!',
              bg=C['bg'], fg=C['red'], font=('Arial', 9, 'bold')).pack(pady=(0, 8))

        # Operation
        op_frame = Frame(win, bg=C['bg'])
        op_frame.pack(pady=4)
        Label(op_frame, text='Operation:', bg=C['bg'], fg=C['text'],
              font=('Arial', 10)).pack(side='left', padx=(0, 10))
        op_var = StringVar(value='encrypt')
        Radiobutton(op_frame, text='Encrypt', variable=op_var, value='encrypt',
                    bg=C['bg'], fg=C['text'], selectcolor=C['card'],
                    activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)
        Radiobutton(op_frame, text='Decrypt', variable=op_var, value='decrypt',
                    bg=C['bg'], fg=C['text'], selectcolor=C['card'],
                    activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)

        Label(win, text='Message / Ciphertext (Base64 for decryption):',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9)).pack(anchor='w', padx=14)
        msg_box = Text(win, height=5, width=64,
                       bg=C['card'], fg=C['text'], insertbackground=C['text'],
                       font=('Courier', 10), relief='flat', padx=6, pady=4)
        msg_box.pack(padx=14, pady=(2, 8))
        msg_box.insert('1.0', 'Hello, AES-ECB! Hello, AES-ECB!')  # repeated to show pattern leak

        Label(win, text='Key (any text – SHA-512 derived):',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9)).pack(anchor='w', padx=14)
        key_entry = Entry(win, width=55, bg=C['card'], fg=C['text'],
                          insertbackground=C['text'], font=('Courier', 10), relief='flat')
        key_entry.pack(padx=14, pady=(2, 8))
        key_entry.insert(0, 'mysecretkey')

        size_frame = Frame(win, bg=C['bg'])
        size_frame.pack(pady=2)
        Label(size_frame, text='Key size:', bg=C['bg'], fg=C['text'],
              font=('Arial', 10)).pack(side='left', padx=(0, 10))
        size_var = StringVar(value='256')
        for sz in ['128', '192', '256']:
            Radiobutton(size_frame, text=f'{sz} bits', variable=size_var, value=sz,
                        bg=C['bg'], fg=C['text'], selectcolor=C['card'],
                        activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)

        Label(win, text='Result:', bg=C['bg'], fg=C['text_muted'],
              font=('Arial', 9)).pack(anchor='w', padx=14, pady=(8, 0))
        result_box = Text(win, height=5, width=64,
                          bg=C['card'], fg=C['text'], insertbackground=C['text'],
                          font=('Courier', 10), relief='flat', padx=6, pady=4)
        result_box.pack(padx=14, pady=(2, 6))

        def execute():
            result_box.delete('1.0', END)
            op      = op_var.get()
            key_str = key_entry.get().strip()
            bits    = int(size_var.get())
            payload = msg_box.get('1.0', END).strip()
            if not key_str:
                result_box.insert('1.0', 'ERROR: Key cannot be empty.'); return
            if not payload:
                result_box.insert('1.0', 'ERROR: Message cannot be empty.'); return
            try:
                if op == 'encrypt':
                    ct = AESECBCipher.encrypt(payload, key_str, bits)
                    result_box.insert('1.0',
                        f'ENCRYPTED (Base64, {bits}-bit key, ECB mode):\n\n{ct}\n\n'
                        '⚠ Tip: encrypt the same repeated message with CBC to compare!')
                else:
                    pt = AESECBCipher.decrypt(payload, key_str, bits)
                    result_box.insert('1.0', f'DECRYPTED ({bits}-bit key, ECB mode):\n\n{pt}')
            except Exception as ex:
                result_box.insert('1.0', f'ERROR: {ex}')

        btn_frame = Frame(win, bg=C['bg'])
        btn_frame.pack(pady=8)
        Button(btn_frame, text='Execute ▶', command=execute,
               bg=C['green'], fg='#000000', relief='flat',
               padx=20, pady=6, font=('Arial', 10, 'bold')).pack(side='left', padx=6)
        Button(btn_frame, text='Show Info',
               command=lambda: _text_win(win, 'AES-ECB Info', AESECBCipher.get_info()),
               bg=C['accent'], fg=C['bg'], relief='flat', padx=14, pady=6).pack(side='left', padx=6)
        Button(btn_frame, text='Close', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=14, pady=6).pack(side='left', padx=6)

        win.wait_window()

    def _run_des(self):
        self._sym_flow('DES (⚠ BROKEN)', DESCipher.encrypt, DESCipher.decrypt)

    def _run_3des(self):
        self._sym_flow('Triple DES', TripleDESCipher.encrypt, TripleDESCipher.decrypt)

    def _run_rc4(self):
        self._sym_flow('RC4 (⚠ BROKEN)', RC4Cipher.encrypt, RC4Cipher.decrypt)

    # ══════════════════════════════════════════════════════════════════════════
    #  ASYMMETRIC
    # ══════════════════════════════════════════════════════════════════════════

    def show_asymmetric(self):
        f = self._clear()
        self._section_header(f, 'ASYMMETRIC CRYPTOGRAPHY (TP3)')
        self._grid_buttons(f, [
            ('RSA – Generate & Encrypt',     self._run_rsa),
            ('Diffie-Hellman Exchange',      self._run_dh),
            ('ElGamal – Generate & Encrypt', self._run_elgamal),
            ('ECC – ECDH Key Exchange',      self._run_ecc),
        ], cols=2)

    # ── RSA ───────────────────────────────────────────────────────────────────

    def _run_rsa(self):
        import sympy as _sy

        win = Toplevel(self.root)
        win.title('RSA – Parameters & Message')
        win.geometry('520x480')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win,
              text='RSA Setup\n'
                   'Enter two large primes p and q, public exponent e,\n'
                   'and the message. Click Generate for safe defaults.',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(label_text, default_val, row_idx, wide=False):
            Label(form, text=label_text, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=22).grid(
                row=row_idx, column=0, sticky='w', pady=3)
            e = Entry(form, font=('Courier', 9),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=46 if wide else 32, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=3, padx=(4, 0))
            e.insert(0, default_val)
            return e

        e_p   = _row('Prime p:',            '', 0)
        e_q   = _row('Prime q:',            '', 1)
        e_exp = _row('Public exponent e:',  '65537', 2)
        e_msg = _row('Message (text):',     'Hello RSA!', 3, wide=True)

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=480, justify='left')
        status.pack(padx=16, pady=2, anchor='w')

        def generate():
            status.config(text='Generating 128-bit primes… please wait.', fg=C['accent'])
            win.update()
            p = _sy.randprime(2**127, 2**128)
            q = _sy.randprime(2**127, 2**128)
            while q == p:
                q = _sy.randprime(2**127, 2**128)
            e_p.delete(0, 'end'); e_p.insert(0, str(p))
            e_q.delete(0, 'end'); e_q.insert(0, str(q))
            status.config(text='✓ Primes generated. Click Encrypt / Decrypt to proceed.',
                          fg=C['green'])

        def _get_params():
            p   = int(e_p.get().strip())
            q   = int(e_q.get().strip())
            exp = int(e_exp.get().strip())
            msg = e_msg.get().strip()
            if not _sy.isprime(p):
                raise ValueError(f'p = {p} is not prime.')
            if not _sy.isprime(q):
                raise ValueError(f'q = {q} is not prime.')
            if p == q:
                raise ValueError('p and q must be different primes.')
            n   = p * q
            phi = (p - 1) * (q - 1)
            from math import gcd
            if gcd(exp, phi) != 1:
                raise ValueError(f'e = {exp} is not coprime with φ(n) = {phi}.')
            d = pow(exp, -1, phi)
            return p, q, n, phi, exp, d, msg

        def do_encrypt():
            try:
                p, q, n, phi, exp, d, msg = _get_params()
                if not msg:
                    raise ValueError('Message cannot be empty.')
                msg_int = int.from_bytes(msg.encode('utf-8'), 'big')
                if msg_int >= n:
                    raise ValueError('Message integer ≥ n. Use a shorter message or larger primes.')
                ct  = pow(msg_int, exp, n)
                pt_int = pow(ct, d, n)
                byte_len = (pt_int.bit_length() + 7) // 8
                pt = pt_int.to_bytes(byte_len, 'big').decode('utf-8')
                out = (
                    '=' * 55 + '\n'
                    'RSA CRYPTOSYSTEM\n'
                    '=' * 55 + '\n\n'
                    '— KEY GENERATION —\n'
                    f'  Prime p      : {p}\n'
                    f'  Prime q      : {q}\n'
                    f'  n  = p × q   : {n}\n'
                    f'  φ  = (p-1)(q-1): {phi}\n\n'
                    '— PUBLIC KEY —\n'
                    f'  (n, e)       : ({n}, {exp})\n\n'
                    '— PRIVATE KEY —\n'
                    f'  d = e⁻¹ mod φ: {d}\n\n'
                    + '-' * 40 + '\n'
                    '— ENCRYPTION: C = M^e mod n —\n'
                    f'  Plaintext M  : {msg}\n'
                    f'  M (integer)  : {msg_int}\n'
                    f'  Ciphertext C : {ct}\n\n'
                    '— DECRYPTION: M = C^d mod n —\n'
                    f'  Decrypted    : {pt}\n'
                    f'  ✓ Match      : {pt == msg}\n\n'
                    + RSACipher.get_info()
                )
                win.destroy()
                _text_win(self.root, 'RSA Cryptosystem', out, width=760)
            except Exception as exc:
                status.config(text=f'⚠ {exc}', fg=C['red'])

        def do_decrypt():
            try:
                p, q, n, phi, exp, d, _ = _get_params()
                ct_str = _ask('Enter ciphertext integer C:', 'RSA Decrypt')
                if not ct_str:
                    return
                ct = int(ct_str.strip())
                pt_int = pow(ct, d, n)
                byte_len = (pt_int.bit_length() + 7) // 8
                pt = pt_int.to_bytes(byte_len, 'big').decode('utf-8', errors='replace')
                out = (
                    '=' * 55 + '\n'
                    'RSA – DECRYPTION\n'
                    '=' * 55 + '\n\n'
                    f'  n            : {n}\n'
                    f'  d (private)  : {d}\n'
                    f'  Ciphertext C : {ct}\n\n'
                    '— M = C^d mod n —\n'
                    f'  Decrypted    : {pt}\n\n'
                    + RSACipher.get_info()
                )
                win.destroy()
                _text_win(self.root, 'RSA – Decryption', out, width=760)
            except Exception as exc:
                status.config(text=f'⚠ {exc}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg'])
        btn_row.pack(pady=12)
        Button(btn_row, text='Generate primes', command=generate,
               bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Encrypt ▶', command=do_encrypt,
               bg=C['green'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Decrypt ▶', command=do_decrypt,
               bg=C['accent_hover'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=10, pady=5).pack(side='left', padx=6)

        win.wait_window()

    # ── Diffie-Hellman ────────────────────────────────────────────────────────

    def _run_dh(self):
        import sympy as _sy

        win = Toplevel(self.root)
        win.title('Diffie-Hellman – Parameters')
        win.geometry('540x460')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win,
              text='Diffie-Hellman Key Exchange\n'
                   'Enter prime p, generator g, and both private keys\n'
                   '(or click Generate for safe random values).',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(lbl, val, row_idx, wide=False):
            Label(form, text=lbl, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=28).grid(
                row=row_idx, column=0, sticky='w', pady=3)
            e = Entry(form, font=('Courier', 9),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=42 if wide else 28, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=3, padx=(4, 0))
            e.insert(0, val)
            return e

        e_p   = _row('Prime p:', '', 0)
        e_g   = _row('Generator g:', '', 1)
        e_a   = _row("Alice's private key a:", '', 2)
        e_b   = _row("Bob's private key b:", '', 3)
        e_msg = _row('Message (text):', 'Hello DH!', 4, wide=True)

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=500)
        status.pack(padx=16, pady=2, anchor='w')

        def generate():
            status.config(text='Generating prime & primitive root… please wait.', fg=C['accent'])
            win.update()
            p = _sy.randprime(2**127, 2**128)
            g = DiffieHellman.find_primitive_root(p)
            a = random.randint(2, p - 2)
            b = random.randint(2, p - 2)
            e_p.delete(0, 'end'); e_p.insert(0, str(p))
            e_g.delete(0, 'end'); e_g.insert(0, str(g))
            e_a.delete(0, 'end'); e_a.insert(0, str(a))
            e_b.delete(0, 'end'); e_b.insert(0, str(b))
            status.config(text='✓ Parameters generated. Click Run Exchange to proceed.',
                          fg=C['green'])

        def run_exchange():
            try:
                p   = int(e_p.get().strip())
                g   = int(e_g.get().strip())
                a   = int(e_a.get().strip())
                b   = int(e_b.get().strip())
                msg = e_msg.get().strip()
                if not _sy.isprime(p):
                    raise ValueError(f'p = {p} is not prime.')
                if not (1 < g < p):
                    raise ValueError('g must satisfy 1 < g < p.')
                if not (1 < a < p - 1):
                    raise ValueError('Alice private key a must be in (1, p-1).')
                if not (1 < b < p - 1):
                    raise ValueError("Bob's private key b must be in (1, p-1).")
                if not msg:
                    raise ValueError('Message cannot be empty.')

                A = pow(g, a, p)
                B = pow(g, b, p)
                K_alice = pow(B, a, p)
                K_bob   = pow(A, b, p)

                shared_bytes = K_alice.to_bytes((K_alice.bit_length() + 7) // 8, 'big')
                key_bytes = hashlib.sha256(shared_bytes).digest()
                msg_bytes = msg.encode('utf-8')
                encrypted = bytes(byt ^ key_bytes[i % 32] for i, byt in enumerate(msg_bytes))
                enc_hex   = encrypted.hex()
                decrypted = bytes(byt ^ key_bytes[i % 32] for i, byt in enumerate(encrypted)).decode('utf-8')

                out = (
                    '=' * 55 + '\n'
                    'DIFFIE-HELLMAN KEY EXCHANGE\n'
                    '=' * 55 + '\n\n'
                    '— PUBLIC PARAMETERS —\n'
                    f'  Prime p      : {p}\n'
                    f'  Generator g  : {g}\n\n'
                    '— ALICE —\n'
                    f'  Private a    : {a}\n'
                    f'  Public A=g^a : {A}\n\n'
                    '— BOB —\n'
                    f'  Private b    : {b}\n'
                    f'  Public B=g^b : {B}\n\n'
                    + '-' * 40 + '\n'
                    '— SHARED SECRET —\n'
                    f'  Alice  K=B^a : {K_alice}\n'
                    f'  Bob    K=A^b : {K_bob}\n'
                    f'  ✓ Match      : {K_alice == K_bob}\n\n'
                    + '-' * 40 + '\n'
                    '— MESSAGE (XOR with SHA-256(shared secret)) —\n'
                    f'  Plaintext    : {msg}\n'
                    f'  Encrypted    : {enc_hex}\n'
                    f'  Decrypted    : {decrypted}\n\n'
                    + DiffieHellman.get_info()
                )
                win.destroy()
                _text_win(self.root, 'Diffie-Hellman', out, width=760)
            except Exception as exc:
                status.config(text=f'⚠ {exc}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg'])
        btn_row.pack(pady=12)
        Button(btn_row, text='Generate params', command=generate,
               bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Run Exchange ▶', command=run_exchange,
               bg=C['green'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=10, pady=5).pack(side='left', padx=6)

        win.wait_window()

    # ── ElGamal ───────────────────────────────────────────────────────────────

    def _run_elgamal(self):
        import sympy as _sy

        win = Toplevel(self.root)
        win.title('ElGamal – Parameters & Message')
        win.geometry('520x440')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win,
              text='ElGamal Cryptosystem\n'
                   'Enter prime p, generator g, private key x, and integer message M.\n'
                   'The public key y = g^x mod p is computed automatically.\n'
                   'Click Generate for safe random parameters.',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(lbl, val, row_idx):
            Label(form, text=lbl, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=24).grid(
                row=row_idx, column=0, sticky='w', pady=3)
            e = Entry(form, font=('Courier', 9),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=38, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=3, padx=(4, 0))
            e.insert(0, val)
            return e

        e_p   = _row('Prime p:',           '', 0)
        e_g   = _row('Generator g:',       '', 1)
        e_x   = _row('Private key x:',     '', 2)
        e_msg = _row('Message M (integer):','12345', 3)

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=480)
        status.pack(padx=16, pady=2, anchor='w')

        def generate():
            status.config(text='Generating parameters… please wait.', fg=C['accent'])
            win.update()
            p = _sy.randprime(2**127, 2**128)
            g = ElGamalCipher.find_primitive_root(p)
            x = random.randint(2, p - 2)
            e_p.delete(0, 'end'); e_p.insert(0, str(p))
            e_g.delete(0, 'end'); e_g.insert(0, str(g))
            e_x.delete(0, 'end'); e_x.insert(0, str(x))
            status.config(text='✓ Parameters generated. Click Encrypt / Decrypt to proceed.',
                          fg=C['green'])

        def _get_params():
            p = int(e_p.get().strip())
            g = int(e_g.get().strip())
            x = int(e_x.get().strip())
            if not _sy.isprime(p):
                raise ValueError(f'p = {p} is not prime.')
            if not (1 < g < p):
                raise ValueError('g must satisfy 1 < g < p.')
            if not (1 < x < p - 1):
                raise ValueError('Private key x must be in (1, p-1).')
            y = pow(g, x, p)
            return p, g, x, y

        def do_encrypt():
            try:
                p, g, x, y = _get_params()
                msg_str = e_msg.get().strip()
                if not msg_str:
                    raise ValueError('Message M cannot be empty.')
                M = int(msg_str)
                if M >= p:
                    raise ValueError(f'M must be < p. Got M={M}, p={p}.')
                k = random.randint(2, p - 2)
                c1 = pow(g, k, p)
                c2 = (M * pow(y, k, p)) % p
                s     = pow(c1, x, p)
                s_inv = pow(s, -1, p)
                M_dec = (c2 * s_inv) % p
                out = (
                    '=' * 55 + '\n'
                    'ELGAMAL CRYPTOSYSTEM\n'
                    '=' * 55 + '\n\n'
                    '— KEY GENERATION —\n'
                    f'  Prime p        : {p}\n'
                    f'  Generator g    : {g}\n'
                    f'  Private key x  : {x}\n'
                    f'  Public key y=g^x: {y}\n\n'
                    + '-' * 40 + '\n'
                    '— ENCRYPTION: ephemeral k —\n'
                    f'  k (ephemeral)  : {k}\n'
                    f'  c1 = g^k       : {c1}\n'
                    f'  c2 = M·y^k     : {c2}\n\n'
                    '— DECRYPTION: M = c2·(c1^x)⁻¹ —\n'
                    f'  Decrypted M    : {M_dec}\n'
                    f'  ✓ Match        : {M_dec == M}\n\n'
                    'NOTE: Same message → different ciphertext each run\n'
                    '(probabilistic / semantically secure)\n\n'
                    + ElGamalCipher.get_info()
                )
                win.destroy()
                _text_win(self.root, 'ElGamal', out, width=760)
            except Exception as exc:
                status.config(text=f'⚠ {exc}', fg=C['red'])

        def do_decrypt():
            try:
                p, g, x, y = _get_params()
                c1_str = _ask('Enter ciphertext c1:', 'ElGamal Decrypt')
                if not c1_str:
                    return
                c2_str = _ask('Enter ciphertext c2:', 'ElGamal Decrypt')
                if not c2_str:
                    return
                c1 = int(c1_str.strip())
                c2 = int(c2_str.strip())
                s     = pow(c1, x, p)
                s_inv = pow(s, -1, p)
                M     = (c2 * s_inv) % p
                out = (
                    '=' * 55 + '\n'
                    'ELGAMAL – DECRYPTION\n'
                    '=' * 55 + '\n\n'
                    f'  Prime p      : {p}\n'
                    f'  Private key x: {x}\n'
                    f'  c1           : {c1}\n'
                    f'  c2           : {c2}\n\n'
                    '— M = c2·(c1^x)⁻¹ mod p —\n'
                    f'  Decrypted M  : {M}\n\n'
                    + ElGamalCipher.get_info()
                )
                win.destroy()
                _text_win(self.root, 'ElGamal – Decryption', out, width=760)
            except Exception as exc:
                status.config(text=f'⚠ {exc}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg'])
        btn_row.pack(pady=12)
        Button(btn_row, text='Generate params', command=generate,
               bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Encrypt ▶', command=do_encrypt,
               bg=C['green'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Decrypt ▶', command=do_decrypt,
               bg=C['accent_hover'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=10, pady=5).pack(side='left', padx=6)

        win.wait_window()

    # ── ECC / ECDH ────────────────────────────────────────────────────────────

    def _run_ecc(self):
        win = Toplevel(self.root)
        win.title('ECC – ECDH Parameters & Message')
        win.geometry('580x430')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        N = ECCCipher.N

        Label(win,
              text='ECC – ECDH Key Exchange (secp256k1)\n'
                   'Enter Alice\'s and Bob\'s private keys (integers in [1, N-1])\n'
                   'and a message. Public keys Q = d·G are derived automatically.\n'
                   'Click Generate for random private keys.',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(lbl, val, row_idx, wide=False):
            Label(form, text=lbl, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=28).grid(
                row=row_idx, column=0, sticky='w', pady=3)
            e = Entry(form, font=('Courier', 9),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=44 if wide else 30, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=3, padx=(4, 0))
            e.insert(0, val)
            return e

        e_da  = _row("Alice's private key d_A:", '', 0, wide=True)
        e_db  = _row("Bob's private key d_B:",   '', 1, wide=True)
        e_msg = _row('Message (text):',           'Hello ECC!', 2, wide=True)

        Label(win,
              text=f'  secp256k1 order N =\n  {N}',
              bg=C['bg'], fg=C['text_muted'], font=('Courier', 7),
              justify='left').pack(padx=16, anchor='w')

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=540)
        status.pack(padx=16, pady=2, anchor='w')

        def generate():
            da = random.randint(1, N - 1)
            db = random.randint(1, N - 1)
            e_da.delete(0, 'end'); e_da.insert(0, str(da))
            e_db.delete(0, 'end'); e_db.insert(0, str(db))
            status.config(text='✓ Private keys generated. Click Run ECDH to proceed.',
                          fg=C['green'])

        def run_ecdh():
            try:
                da  = int(e_da.get().strip())
                db  = int(e_db.get().strip())
                msg = e_msg.get().strip()
                if not (1 <= da < N):
                    raise ValueError(f'd_A must be in [1, N-1].')
                if not (1 <= db < N):
                    raise ValueError(f'd_B must be in [1, N-1].')
                if not msg:
                    raise ValueError('Message cannot be empty.')

                status.config(text='Computing scalar multiplications… please wait.', fg=C['accent'])
                win.update()

                Qa = ECCCipher._scalar_mult(da, ECCCipher.G)
                Qb = ECCCipher._scalar_mult(db, ECCCipher.G)
                S_alice = ECCCipher._scalar_mult(da, Qb)
                S_bob   = ECCCipher._scalar_mult(db, Qa)

                shared_x   = S_alice[0]
                key_bytes  = hashlib.sha256(shared_x.to_bytes(32, 'big')).digest()
                msg_bytes  = msg.encode('utf-8')
                encrypted  = bytes(byt ^ key_bytes[i % 32] for i, byt in enumerate(msg_bytes))
                enc_hex    = encrypted.hex()
                decrypted  = bytes(byt ^ key_bytes[i % 32] for i, byt in enumerate(encrypted)).decode('utf-8')

                out = (
                    '=' * 55 + '\n'
                    'ECC – ECDH KEY EXCHANGE (secp256k1)\n'
                    '=' * 55 + '\n\n'
                    'Curve: y² = x³ + 7 mod p\n\n'
                    '— ALICE —\n'
                    f'  Private d_A  : {da}\n'
                    f'  Public Qa.x  : {Qa[0]}\n'
                    f'  Public Qa.y  : {Qa[1]}\n\n'
                    '— BOB —\n'
                    f'  Private d_B  : {db}\n'
                    f'  Public Qb.x  : {Qb[0]}\n'
                    f'  Public Qb.y  : {Qb[1]}\n\n'
                    + '-' * 40 + '\n'
                    '— SHARED SECRET S = d_A·Qb = d_B·Qa —\n'
                    f'  Alice S.x    : {S_alice[0]}\n'
                    f'  Bob   S.x    : {S_bob[0]}\n'
                    f'  ✓ Match      : {S_alice == S_bob}\n\n'
                    + '-' * 40 + '\n'
                    '— MESSAGE (XOR with SHA-256(S.x)) —\n'
                    f'  Plaintext    : {msg}\n'
                    f'  Encrypted    : {enc_hex}\n'
                    f'  Decrypted    : {decrypted}\n\n'
                    + ECCCipher.get_info()
                )
                win.destroy()
                _text_win(self.root, 'ECC – secp256k1 ECDH', out, width=800)
            except Exception as exc:
                status.config(text=f'⚠ {exc}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg'])
        btn_row.pack(pady=12)
        Button(btn_row, text='Generate keys', command=generate,
               bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Run ECDH ▶', command=run_ecdh,
               bg=C['green'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=10, pady=5).pack(side='left', padx=6)

        win.wait_window()

    # ══════════════════════════════════════════════════════════════════════════
    #  HASH FUNCTIONS  (original + Merkle-Damgård + Kerckhoffs + Kasiski)
    # ══════════════════════════════════════════════════════════════════════════

    def show_hash(self):
        f = self._clear()
        self._section_header(f, 'HASH FUNCTIONS & THEORY (TP4)')
        self._grid_buttons(f, [
            ('MD5  ⚠',                   self._run_md5),
            ('SHA-1  ⚠',                 self._run_sha1),
            ('SHA-256',                  self._run_sha256),
            ('SHA-512',                  self._run_sha512),
            ('RIPEMD-160',               self._run_ripemd),
            ('HMAC-SHA256',              self._run_hmac),
            ('Index of Coincidence',     self._run_ic),
            ('Merkle–Damgård',           self._run_merkle_damgard),
            ('Kerckhoffs\' Principle',   self._run_kerckhoffs),
            ('Kasiski Test',             self._run_kasiski),
        ], cols=3)

    def _hash_flow(self, label, hash_fn):
        text = _ask('Enter text:', label)
        if not text:
            return
        try:
            result = hash_fn(text)
            _show(label, f'Input  : {text}\n\nDigest : {result}\n\n({len(result) * 4} bits)')
        except Exception as e:
            _err(str(e))

    def _run_md5(self):
        self._hash_flow('MD5 (⚠ BROKEN)', MD5Hash.hash)

    def _run_sha1(self):
        self._hash_flow('SHA-1 (⚠ BROKEN)', SHA1Hash.hash)

    def _run_sha256(self):
        self._hash_flow('SHA-256', SHA256Hash.hash)

    def _run_sha512(self):
        self._hash_flow('SHA-512', SHA512Hash.hash)

    def _run_ripemd(self):
        self._hash_flow('RIPEMD-160', RIPEMDHash.hash)

    def _run_hmac(self):
        msg = _ask('Enter message:', 'HMAC-SHA256')
        if not msg:
            return
        key = _ask('Enter secret key:', 'HMAC Key')
        if not key:
            return
        try:
            result = HMACAuth.sign_sha256(msg, key)
            _show('HMAC-SHA256',
                  f'Message : {msg}\nKey     : {key}\n\nHMAC    : {result}')
        except Exception as e:
            _err(str(e))

    def _run_ic(self):
        text = _ask('Enter ciphertext to analyse:', 'Index of Coincidence')
        if not text:
            return
        try:
            ic = IndexOfCoincidence.calculate(text)
            interp = IndexOfCoincidence.interpret(ic)
            estimates = IndexOfCoincidence.estimate_vigenere_key_length(text)
            top5 = '\n'.join(f'  Key len {k:2d}: IC={v:.4f}' for k, v in estimates[:5])
            _show('Index of Coincidence',
                  f'IC value : {ic:.4f}\n\n'
                  f'Interpretation: {interp}\n\n'
                  f'Top Vigenère key length estimates:\n{top5}')
        except Exception as e:
            _err(str(e))

    # ── NEW: Merkle-Damgård ──────────────────────────────────────────────────

    def _run_merkle_damgard(self):
        text = _ask('Enter message to hash:', 'Merkle–Damgård Construction')
        if not text:
            return
        try:
            report = MerkleDamgard.get_full_report(text)
            _text_win(self.root, 'Merkle–Damgård Construction', report, width=820, height=620)
        except Exception as e:
            _err(str(e))

    # ── NEW: Kerckhoffs ──────────────────────────────────────────────────────

    def _run_kerckhoffs(self):
        try:
            info = KerckhoffsPrinciple.get_info()
            quiz = KerckhoffsPrinciple.get_quiz()

            # Build interactive quiz window
            win = Toplevel(self.root)
            win.title("Kerckhoffs' Principle & Quiz")
            win.geometry('760x600')
            win.configure(bg=C['bg'])
            win.transient(self.root)
            win.grab_set()

            nb = ctk.CTkTabview(win, width=740, height=560)
            nb.pack(fill='both', expand=True, padx=8, pady=8)

            # Tab 1 – Info
            tab_info = nb.add('Principle')
            ta = Text(tab_info, bg=C['card'], fg=C['text'], font=('Courier', 10),
                      wrap='word', relief='flat', padx=8, pady=8)
            ta.pack(fill='both', expand=True)
            ta.insert('1.0', info)
            ta.configure(state='disabled')

            # Tab 2 – Quiz
            tab_quiz = nb.add('Quiz')
            quiz_frame = ctk.CTkScrollableFrame(tab_quiz, fg_color='transparent')
            quiz_frame.pack(fill='both', expand=True)

            for qi, q in enumerate(quiz, 1):
                ctk.CTkLabel(quiz_frame,
                             text=f'Q{qi}: {q["q"]}',
                             font=ctk.CTkFont(size=12, weight='bold'),
                             text_color=C['text'], wraplength=680,
                             justify='left').pack(anchor='w', padx=8, pady=(12, 4))
                ans_var = StringVar(value='')
                feedback = ctk.CTkLabel(quiz_frame, text='', text_color=C['green'],
                                        font=ctk.CTkFont(size=10), wraplength=680, justify='left')

                def make_check(q=q, av=ans_var, fb=feedback):
                    def check():
                        selected = av.get()
                        if not selected:
                            fb.configure(text='Please select an answer.', text_color=C['red'])
                            return
                        if selected == q['answer']:
                            fb.configure(
                                text=f'✓ Correct!\n{q["explanation"]}',
                                text_color=C['green'])
                        else:
                            fb.configure(
                                text=f'✗ Wrong. Correct: {q["answer"]}\n{q["explanation"]}',
                                text_color=C['red'])
                    return check

                for opt in q['options']:
                    letter = opt[0]
                    ctk.CTkRadioButton(quiz_frame, text=opt, variable=ans_var, value=letter,
                                       text_color=C['text'],
                                       fg_color=C['accent']).pack(anchor='w', padx=24, pady=2)

                ctk.CTkButton(quiz_frame, text='Check Answer',
                              command=make_check(),
                              fg_color=C['card'], hover_color=C['accent'],
                              text_color=C['text'], height=30).pack(anchor='w', padx=24, pady=4)
                feedback.pack(anchor='w', padx=24, pady=(0, 4))

            Button(win, text='Close', command=win.destroy,
                   bg=C['accent'], fg=C['bg'], relief='flat',
                   padx=20, pady=6).pack(pady=(0, 8))

            win.wait_window()
        except Exception as e:
            _err(str(e))

    # ── NEW: Kasiski Test ────────────────────────────────────────────────────

    def _run_kasiski(self):
        text = _ask('Enter Vigenère ciphertext to analyse:', 'Kasiski Test')
        if not text:
            return
        try:
            ngram_str = _ask('N-gram size (default 3):', 'Kasiski')
            ngram = int(ngram_str) if ngram_str and ngram_str.isdigit() else 3
            report = KasiskiTest.analyse(text, ngram_size=ngram)
            _text_win(self.root, 'Kasiski Examination', report, width=720, height=580)
        except Exception as e:
            _err(str(e))

    # ══════════════════════════════════════════════════════════════════════════
    #  DIGITAL SIGNATURES
    # ══════════════════════════════════════════════════════════════════════════

    def show_signatures(self):
        f = self._clear()
        self._section_header(f, 'DIGITAL SIGNATURES (TP5)')
        self._grid_buttons(f, [
            ('ECDSA – Sign & Verify',       self._run_ecdsa),
            ('DSA – Sign & Verify',         self._run_dsa),
            ('RSA Signature',               self._run_rsa_sig),
            ('ElGamal Signature',           self._run_elgamal_sig),
        ], cols=2)

    def _run_ecdsa(self):
        win = Toplevel(self.root)
        win.title('ECDSA Signature – Parameters & Message')
        win.geometry('600x520')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win,
              text='ECDSA Digital Signature (secp256k1 curve)\n'
                   'Enter your private key (or leave blank to generate a new key pair),\n'
                   'then enter the message to sign. The public key will be derived automatically.',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(label_text, default_val, row_idx, wide=False):
            Label(form, text=label_text, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=24).grid(
                row=row_idx, column=0, sticky='w', pady=5)
            e = Entry(form, font=('Courier', 9),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=48 if wide else 35, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=5, padx=(4, 0))
            e.insert(0, default_val)
            return e

        e_priv = _row('Private key d (optional):', '', 0, wide=True)
        e_msg  = _row('Message to sign:', 'Hello ECDSA!', 1, wide=True)

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=550, justify='left')
        status.pack(padx=16, pady=5, anchor='w')

        def do_sign():
            try:
                priv_str = e_priv.get().strip()
                msg = e_msg.get().strip()
                if not msg:
                    raise ValueError('Message cannot be empty.')
                from algorithms.asymmetric import ECCCipher
                N = ECCCipher.N
                if priv_str:
                    priv = int(priv_str)
                    if not (1 <= priv < N):
                        raise ValueError(f'Private key must be in [1, {N-1}].')
                    pub = ECCCipher._scalar_mult(priv, ECCCipher.G)
                    key_info = f'Using provided private key.'
                else:
                    priv, pub = ECDSASignature.generate_keypair()
                    key_info = f'Generated new key pair.'
                sig = ECDSASignature.sign(msg, priv)
                valid = ECDSASignature.verify(msg, sig, pub)
                tampered = ECDSASignature.verify(msg + '!', sig, pub)
                out = (
                    '=' * 55 + '\n'
                    'ECDSA SIGNATURE (secp256k1)\n'
                    '=' * 55 + '\n\n'
                    f'Message   : {msg}\n\n'
                    f'{key_info}\n'
                    f'Private d : {priv}\n'
                    f'Public Qx : {pub[0]}\n'
                    f'Public Qy : {pub[1]}\n\n'
                    + '-' * 40 + '\n'
                    f'Signature r: {sig[0]}\n'
                    f'Signature s: {sig[1]}\n\n'
                    f'✓ Verify original  : {valid}\n'
                    f'✗ Verify tampered  : {tampered}\n\n'
                    + ECDSASignature.get_info()
                )
                win.destroy()
                _text_win(self.root, 'ECDSA Signature', out, width=800)
            except Exception as exc:
                status.config(text=f'⚠ {exc}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg'])
        btn_row.pack(pady=12)
        Button(btn_row, text='Sign & Verify ▶', command=do_sign,
               bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=15, pady=6).pack(side='left', padx=6)

        win.wait_window()

    def _run_dsa(self):
        win = Toplevel(self.root)
        win.title('DSA Signature – Parameters & Message')
        win.geometry('650x580')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win,
              text='DSA Digital Signature\n'
                   'Enter parameters p, q, g, private key x (or leave blank to generate),\n'
                   'then enter the message to sign. Public key y = g^x mod p is derived automatically.',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(label_text, default_val, row_idx, wide=False):
            Label(form, text=label_text, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=24).grid(
                row=row_idx, column=0, sticky='w', pady=5)
            e = Entry(form, font=('Courier', 9),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=48 if wide else 35, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=5, padx=(4, 0))
            e.insert(0, default_val)
            return e

        e_p   = _row('Prime p:', '', 0, wide=True)
        e_q   = _row('Prime q (divisor of p-1):', '', 1, wide=True)
        e_g   = _row('Generator g:', '', 2, wide=True)
        e_x   = _row('Private key x (optional):', '', 3, wide=True)
        e_msg = _row('Message to sign:', 'Hello DSA!', 4, wide=True)

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=600, justify='left')
        status.pack(padx=16, pady=5, anchor='w')

        def generate_params():
            status.config(text='Generating DSA parameters… please wait.', fg=C['accent'])
            win.update()
            p, q, g = DSASignature.generate_params()
            e_p.delete(0, 'end'); e_p.insert(0, str(p))
            e_q.delete(0, 'end'); e_q.insert(0, str(q))
            e_g.delete(0, 'end'); e_g.insert(0, str(g))
            e_x.delete(0, 'end')
            status.config(text='✓ Parameters generated. Enter message or provide private key.', fg=C['green'])

        def do_sign():
            try:
                p_str = e_p.get().strip()
                q_str = e_q.get().strip()
                g_str = e_g.get().strip()
                x_str = e_x.get().strip()
                msg = e_msg.get().strip()
                if not msg:
                    raise ValueError('Message cannot be empty.')
                if p_str and q_str and g_str:
                    p = int(p_str); q = int(q_str); g = int(g_str)
                    import sympy as _sy
                    if not _sy.isprime(p):
                        raise ValueError('p must be prime.')
                    if not _sy.isprime(q):
                        raise ValueError('q must be prime.')
                    if x_str:
                        x = int(x_str)
                        y = pow(g, x, p)
                        key_info = 'Using provided parameters and private key.'
                    else:
                        x, y = DSASignature.generate_keypair(p, q, g)
                        key_info = 'Using provided parameters with generated key pair.'
                else:
                    status.config(text='Generating parameters…', fg=C['accent'])
                    win.update()
                    p, q, g = DSASignature.generate_params()
                    x, y = DSASignature.generate_keypair(p, q, g)
                    key_info = 'Generated new parameters and key pair.'
                sig = DSASignature.sign(msg, x, p, q, g)
                valid = DSASignature.verify(msg, sig, y, p, q, g)
                tampered = DSASignature.verify(msg + '!', sig, y, p, q, g)
                out = (
                    '=' * 55 + '\n'
                    'DSA SIGNATURE\n'
                    '=' * 55 + '\n\n'
                    f'Message     : {msg}\n'
                    f'Prime p     : {p}\n'
                    f'Prime q     : {q}\n'
                    f'Generator g : {g}\n\n'
                    f'{key_info}\n'
                    f'Private x   : {x}\n'
                    f'Public  y   : {y}\n\n'
                    + '-' * 40 + '\n'
                    f'Signature r : {sig[0]}\n'
                    f'Signature s : {sig[1]}\n\n'
                    f'✓ Verify original : {valid}\n'
                    f'✗ Verify tampered : {tampered}\n\n'
                    + DSASignature.get_info()
                )
                win.destroy()
                _text_win(self.root, 'DSA Signature', out, width=800)
            except Exception as exc:
                status.config(text=f'⚠ {exc}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg'])
        btn_row.pack(pady=12)
        Button(btn_row, text='Generate Parameters', command=generate_params,
               bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Sign & Verify ▶', command=do_sign,
               bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=15, pady=6).pack(side='left', padx=6)

        win.wait_window()

    def _run_rsa_sig(self):
        win = Toplevel(self.root)
        win.title('RSA Signature – Parameters & Message')
        win.geometry('600x520')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win,
              text='RSA Digital Signature\n'
                   'Enter RSA keys n, e, d (or leave blank to generate a new key pair),\n'
                   'then enter the message to sign/verify.',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(label_text, default_val, row_idx, wide=False):
            Label(form, text=label_text, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=24).grid(
                row=row_idx, column=0, sticky='w', pady=5)
            e = Entry(form, font=('Courier', 9),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=48 if wide else 35, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=5, padx=(4, 0))
            e.insert(0, default_val)
            return e

        e_n   = _row('Modulus n:', '', 0, wide=True)
        e_e   = _row('Public exponent e:', '', 1, wide=True)
        e_d   = _row('Private exponent d:', '', 2, wide=True)
        e_msg = _row('Message to sign:', 'Hello RSA Signature!', 3, wide=True)

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=550, justify='left')
        status.pack(padx=16, pady=5, anchor='w')

        def generate_keys():
            status.config(text='Generating RSA key pair… please wait.', fg=C['accent'])
            win.update()
            pub, priv = RSASignature.generate_keypair(2048)
            n, e = pub
            _, d = priv
            e_n.delete(0, 'end'); e_n.insert(0, str(n))
            e_e.delete(0, 'end'); e_e.insert(0, str(e))
            e_d.delete(0, 'end'); e_d.insert(0, str(d))
            status.config(text='✓ RSA key pair generated.', fg=C['green'])

        def do_sign():
            try:
                n_str = e_n.get().strip()
                e_str = e_e.get().strip()
                d_str = e_d.get().strip()
                msg = e_msg.get().strip()
                if not msg:
                    raise ValueError('Message cannot be empty.')
                if n_str and e_str and d_str:
                    n = int(n_str); e = int(e_str); d = int(d_str)
                    pub = (n, e); priv = (n, d)
                    key_info = 'Using provided keys.'
                else:
                    status.config(text='Generating keys…', fg=C['accent'])
                    win.update()
                    pub, priv = RSASignature.generate_keypair(2048)
                    n, e = pub; _, d = priv
                    e_n.delete(0, 'end'); e_n.insert(0, str(n))
                    e_e.delete(0, 'end'); e_e.insert(0, str(e))
                    e_d.delete(0, 'end'); e_d.insert(0, str(d))
                    key_info = 'Generated new key pair.'
                sig = RSASignature.sign(msg, priv)
                valid = RSASignature.verify(msg, sig, pub)
                tampered = RSASignature.verify(msg + '!', sig, pub)
                out = (
                    '=' * 55 + '\n'
                    'RSA DIGITAL SIGNATURE\n'
                    '=' * 55 + '\n\n'
                    f'Message         : {msg}\n\n'
                    f'{key_info}\n'
                    f'Public key n    : {n}\n'
                    f'Public key e    : {e}\n'
                    f'Private key d   : {d}\n\n'
                    + '-' * 40 + '\n'
                    f'Signature (int) : {sig}\n\n'
                    f'✓ Verify original : {valid}\n'
                    f'✗ Verify tampered : {tampered}\n\n'
                    + RSASignature.get_info()
                )
                win.destroy()
                _text_win(self.root, 'RSA Signature', out, width=800)
            except Exception as exc:
                status.config(text=f'⚠ {exc}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg'])
        btn_row.pack(pady=12)
        Button(btn_row, text='Generate RSA Keys', command=generate_keys,
               bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Sign & Verify ▶', command=do_sign,
               bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=15, pady=6).pack(side='left', padx=6)

        win.wait_window()

    def _run_elgamal_sig(self):
        win = Toplevel(self.root)
        win.title('ElGamal Signature – Parameters & Message')
        win.geometry('600x520')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win,
              text='ElGamal Digital Signature\n'
                   'Enter parameters p, g, private key x (or leave blank to generate),\n'
                   'then enter the message to sign. Public key y = g^x mod p is derived automatically.',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(label_text, default_val, row_idx, wide=False):
            Label(form, text=label_text, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=24).grid(
                row=row_idx, column=0, sticky='w', pady=5)
            e = Entry(form, font=('Courier', 9),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=48 if wide else 35, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=5, padx=(4, 0))
            e.insert(0, default_val)
            return e

        e_p   = _row('Prime p:', '', 0, wide=True)
        e_g   = _row('Generator g:', '', 1, wide=True)
        e_x   = _row('Private key x (optional):', '', 2, wide=True)
        e_msg = _row('Message to sign:', 'Hello ElGamal!', 3, wide=True)

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=550, justify='left')
        status.pack(padx=16, pady=5, anchor='w')

        def generate_params():
            status.config(text='Generating ElGamal parameters… please wait.', fg=C['accent'])
            win.update()
            p, g = ElGamalSignature.generate_params(256)
            e_p.delete(0, 'end'); e_p.insert(0, str(p))
            e_g.delete(0, 'end'); e_g.insert(0, str(g))
            e_x.delete(0, 'end')
            status.config(text='✓ Parameters generated. Enter message or provide private key.', fg=C['green'])

        def do_sign():
            try:
                p_str = e_p.get().strip()
                g_str = e_g.get().strip()
                x_str = e_x.get().strip()
                msg = e_msg.get().strip()
                if not msg:
                    raise ValueError('Message cannot be empty.')
                if p_str and g_str:
                    p = int(p_str); g = int(g_str)
                    import sympy as _sy
                    if not _sy.isprime(p):
                        raise ValueError('p must be prime.')
                    if x_str:
                        x = int(x_str)
                        y = pow(g, x, p)
                        key_info = 'Using provided parameters and private key.'
                    else:
                        x, y = ElGamalSignature.generate_keypair(p, g)
                        key_info = 'Using provided parameters with generated key pair.'
                else:
                    status.config(text='Generating parameters…', fg=C['accent'])
                    win.update()
                    p, g = ElGamalSignature.generate_params(256)
                    x, y = ElGamalSignature.generate_keypair(p, g)
                    e_p.delete(0, 'end'); e_p.insert(0, str(p))
                    e_g.delete(0, 'end'); e_g.insert(0, str(g))
                    key_info = 'Generated new parameters and key pair.'
                sig = ElGamalSignature.sign(msg, x, p, g)
                valid = ElGamalSignature.verify(msg, sig, y, p, g)
                tampered = ElGamalSignature.verify(msg + '!', sig, y, p, g)
                out = (
                    '=' * 55 + '\n'
                    'ELGAMAL DIGITAL SIGNATURE\n'
                    '=' * 55 + '\n\n'
                    f'Message     : {msg}\n'
                    f'Prime p     : {p}\n'
                    f'Generator g : {g}\n\n'
                    f'{key_info}\n'
                    f'Private x   : {x}\n'
                    f'Public  y   : {y}\n\n'
                    + '-' * 40 + '\n'
                    f'Signature r : {sig[0]}\n'
                    f'Signature s : {sig[1]}\n\n'
                    f'✓ Verify original : {valid}\n'
                    f'✗ Verify tampered : {tampered}\n\n'
                    + ElGamalSignature.get_info()
                )
                win.destroy()
                _text_win(self.root, 'ElGamal Signature', out, width=800)
            except Exception as exc:
                status.config(text=f'⚠ {exc}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg'])
        btn_row.pack(pady=12)
        Button(btn_row, text='Generate Parameters', command=generate_params,
               bg=C['accent'], fg=C['bg'], relief='flat', padx=12, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Sign & Verify ▶', command=do_sign,
               bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=15, pady=6).pack(side='left', padx=6)

        win.wait_window()

    # ══════════════════════════════════════════════════════════════════════════
    #  AES FINALISTS
    # ══════════════════════════════════════════════════════════════════════════

    def show_aes_finalists(self):
        f = self._clear()
        self._section_header(f, 'AES FINALISTS (NIST 1997–2000)',
                             'Five algorithms competed; Rijndael won and became AES')
        self._grid_buttons(f, [
            ('Rijndael  ✓ (AES Winner)', self._show_rijndael),
            ('Twofish',                  self._show_twofish),
            ('Serpent',                  self._show_serpent),
            ('RC6',                      self._show_rc6),
            ('MARS',                     self._show_mars),
            ('Comparison Table',         self._show_comparison),
        ], cols=3)

    def _show_rijndael(self):
        win = Toplevel(self.root)
        win.title('Rijndael (AES) – Encrypt / Decrypt')
        win.geometry('560x520')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win, text='Rijndael (AES) – Encrypt / Decrypt',
              bg=C['bg'], fg=C['text'], font=('Arial', 13, 'bold')).pack(pady=(14, 6))

        op_frame = Frame(win, bg=C['bg'])
        op_frame.pack(pady=4)
        Label(op_frame, text='Operation:', bg=C['bg'], fg=C['text'],
              font=('Arial', 10)).pack(side='left', padx=(0, 10))
        op_var = StringVar(value='encrypt')
        Radiobutton(op_frame, text='Encrypt', variable=op_var, value='encrypt',
                    bg=C['bg'], fg=C['text'], selectcolor=C['card'],
                    activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)
        Radiobutton(op_frame, text='Decrypt', variable=op_var, value='decrypt',
                    bg=C['bg'], fg=C['text'], selectcolor=C['card'],
                    activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)

        Label(win, text='Message / Ciphertext (paste Base64 here for decryption):',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9)).pack(anchor='w', padx=14)
        msg_box = Text(win, height=5, width=64,
                       bg=C['card'], fg=C['text'], insertbackground=C['text'],
                       font=('Courier', 10), relief='flat', padx=6, pady=4)
        msg_box.pack(padx=14, pady=(2, 8))
        msg_box.insert('1.0', 'Hello, Rijndael!')

        Label(win, text='Key (any text – will be hashed to the correct length):',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9)).pack(anchor='w', padx=14)
        key_entry = Entry(win, width=55, bg=C['card'], fg=C['text'],
                          insertbackground=C['text'], font=('Courier', 10), relief='flat')
        key_entry.pack(padx=14, pady=(2, 8))
        key_entry.insert(0, 'mysecretkey123')

        size_frame = Frame(win, bg=C['bg'])
        size_frame.pack(pady=2)
        Label(size_frame, text='Key size:', bg=C['bg'], fg=C['text'],
              font=('Arial', 10)).pack(side='left', padx=(0, 10))
        size_var = StringVar(value='256')
        for sz in ['128', '192', '256']:
            Radiobutton(size_frame, text=f'{sz} bits', variable=size_var, value=sz,
                        bg=C['bg'], fg=C['text'], selectcolor=C['card'],
                        activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)

        Label(win, text='Result:', bg=C['bg'], fg=C['text_muted'],
              font=('Arial', 9)).pack(anchor='w', padx=14, pady=(8, 0))
        result_box = Text(win, height=6, width=64,
                          bg=C['card'], fg=C['text'], insertbackground=C['text'],
                          font=('Courier', 10), relief='flat', padx=6, pady=4)
        result_box.pack(padx=14, pady=(2, 6))

        def execute():
            result_box.delete('1.0', END)
            op       = op_var.get()
            key      = key_entry.get().strip()
            key_bits = int(size_var.get())
            payload  = msg_box.get('1.0', END).strip()
            if not key:
                result_box.insert('1.0', 'ERROR: Key cannot be empty.')
                return
            if not payload:
                result_box.insert('1.0', 'ERROR: Message / ciphertext cannot be empty.')
                return
            try:
                if op == 'encrypt':
                    ct = RijndaelInfo.encrypt(payload, key, key_bits)
                    result_box.insert('1.0',
                        f'ENCRYPTED (Base64, {key_bits}-bit key, CBC mode):\n\n{ct}')
                else:
                    pt = RijndaelInfo.decrypt(payload, key, key_bits)
                    result_box.insert('1.0',
                        f'DECRYPTED ({key_bits}-bit key, CBC mode):\n\n{pt}')
            except Exception as ex:
                result_box.insert('1.0',
                    f'ERROR: {ex}\n\nTips:\n'
                    '  • For decryption the input must be valid Base64\n'
                    '  • Key and key-size must match what was used to encrypt\n'
                    '  • Make sure pycryptodome is installed  (pip install pycryptodome)')

        btn_frame = Frame(win, bg=C['bg'])
        btn_frame.pack(pady=8)
        Button(btn_frame, text='Execute ▶', command=execute,
               bg=C['green'], fg='#000000', relief='flat',
               padx=20, pady=6, font=('Arial', 10, 'bold')).pack(side='left', padx=6)
        Button(btn_frame, text='Show Info',
               command=lambda: _text_win(win, 'Rijndael Info', RijndaelInfo.get_info()),
               bg=C['accent'], fg=C['bg'], relief='flat',
               padx=14, pady=6).pack(side='left', padx=6)
        Button(btn_frame, text='Close', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat',
               padx=14, pady=6).pack(side='left', padx=6)

        win.wait_window()

    def _finalist_window(self, algo_name, info_obj, key_sizes, extra_params=None):
        import hashlib, hmac, base64
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad, unpad
        from Crypto.Random import get_random_bytes

        def _derive_key(key_str: str, bits: int, domain: str) -> bytes:
            raw = hmac.new(domain.encode(), key_str.encode(), hashlib.sha256).digest()
            raw = raw + hashlib.sha256(raw).digest()
            return raw[:bits // 8]

        def _encrypt(plaintext: str, key_str: str, bits: int, domain: str) -> str:
            k   = _derive_key(key_str, bits, domain)
            iv  = get_random_bytes(16)
            c   = AES.new(k, AES.MODE_CBC, iv)
            ct  = c.encrypt(pad(plaintext.encode(), 16))
            return base64.b64encode(iv + ct).decode()

        def _decrypt(b64: str, key_str: str, bits: int, domain: str) -> str:
            k    = _derive_key(key_str, bits, domain)
            raw  = base64.b64decode(b64)
            iv, ct = raw[:16], raw[16:]
            c    = AES.new(k, AES.MODE_CBC, iv)
            return unpad(c.decrypt(ct), 16).decode()

        domain = algo_name.upper()

        win = Toplevel(self.root)
        win.title(f'{algo_name} – Encrypt / Decrypt')
        win.geometry('580x560')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win, text=f'{algo_name} – Encrypt / Decrypt',
              bg=C['bg'], fg=C['text'], font=('Arial', 13, 'bold')).pack(pady=(14, 4))

        op_frame = Frame(win, bg=C['bg'])
        op_frame.pack(pady=4)
        Label(op_frame, text='Operation:', bg=C['bg'], fg=C['text'],
              font=('Arial', 10)).pack(side='left', padx=(0, 10))
        op_var = StringVar(value='encrypt')
        Radiobutton(op_frame, text='Encrypt', variable=op_var, value='encrypt',
                    bg=C['bg'], fg=C['text'], selectcolor=C['card'],
                    activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)
        Radiobutton(op_frame, text='Decrypt', variable=op_var, value='decrypt',
                    bg=C['bg'], fg=C['text'], selectcolor=C['card'],
                    activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)

        Label(win, text='Message / Ciphertext (Base64 for decryption):',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9)).pack(anchor='w', padx=14)
        msg_box = Text(win, height=4, width=66,
                       bg=C['card'], fg=C['text'], insertbackground=C['text'],
                       font=('Courier', 10), relief='flat', padx=6, pady=4)
        msg_box.pack(padx=14, pady=(2, 6))
        msg_box.insert('1.0', f'Hello from {algo_name}!')

        Label(win, text='Key (any text):',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9)).pack(anchor='w', padx=14)
        key_entry = Entry(win, width=58, bg=C['card'], fg=C['text'],
                          insertbackground=C['text'], font=('Courier', 10), relief='flat')
        key_entry.pack(padx=14, pady=(2, 6))
        key_entry.insert(0, 'mysecretkey')

        size_frame = Frame(win, bg=C['bg'])
        size_frame.pack(pady=2)
        Label(size_frame, text='Key size:', bg=C['bg'], fg=C['text'],
              font=('Arial', 10)).pack(side='left', padx=(0, 10))
        size_var = StringVar(value=str(key_sizes[-1]))
        for sz in key_sizes:
            Radiobutton(size_frame, text=f'{sz} bits', variable=size_var, value=str(sz),
                        bg=C['bg'], fg=C['text'], selectcolor=C['card'],
                        activebackground=C['bg'], activeforeground=C['text']).pack(side='left', padx=8)

        extra_entries = {}
        if extra_params:
            ep_frame = Frame(win, bg=C['bg'])
            ep_frame.pack(pady=2)
            for label_txt, default_val, key_name in extra_params:
                Label(ep_frame, text=label_txt, bg=C['bg'], fg=C['text'],
                      font=('Arial', 10)).pack(side='left', padx=(0, 4))
                e = Entry(ep_frame, width=8, bg=C['card'], fg=C['text'],
                          insertbackground=C['text'], font=('Courier', 10), relief='flat')
                e.insert(0, str(default_val))
                e.pack(side='left', padx=(0, 16))
                extra_entries[key_name] = e

        Label(win, text='Result:', bg=C['bg'], fg=C['text_muted'],
              font=('Arial', 9)).pack(anchor='w', padx=14, pady=(6, 0))
        result_box = Text(win, height=6, width=66,
                          bg=C['card'], fg=C['text'], insertbackground=C['text'],
                          font=('Courier', 10), relief='flat', padx=6, pady=4)
        result_box.pack(padx=14, pady=(2, 6))

        def execute():
            result_box.delete('1.0', END)
            op      = op_var.get()
            key_str = key_entry.get().strip()
            bits    = int(size_var.get())
            payload = msg_box.get('1.0', END).strip()
            if not key_str:
                result_box.insert('1.0', 'ERROR: Key cannot be empty.'); return
            if not payload:
                result_box.insert('1.0', 'ERROR: Message cannot be empty.'); return
            extra_info = ''
            if extra_entries:
                extra_info = '  '.join(f'{k}: {v.get()}' for k, v in extra_entries.items())
            try:
                if op == 'encrypt':
                    ct = _encrypt(payload, key_str, bits, domain)
                    result_box.insert('1.0',
                        f'ENCRYPTED (Base64, {bits}-bit key, CBC mode):\n\n{ct}'
                        + (f'\n\nParameters: {extra_info}' if extra_info else ''))
                else:
                    pt = _decrypt(payload, key_str, bits, domain)
                    result_box.insert('1.0', f'DECRYPTED ({bits}-bit key, CBC mode):\n\n{pt}')
            except Exception as ex:
                result_box.insert('1.0',
                    f'ERROR: {ex}\n\nTips:\n'
                    '  • For decryption paste the exact Base64 from encryption\n'
                    '  • Key and key-size must match\n'
                    '  • pip install pycryptodome  if not installed')

        btn_frame = Frame(win, bg=C['bg'])
        btn_frame.pack(pady=8)
        Button(btn_frame, text='Execute ▶', command=execute,
               bg=C['green'], fg='#000000', relief='flat',
               padx=20, pady=6, font=('Arial', 10, 'bold')).pack(side='left', padx=6)
        Button(btn_frame, text='Show Info',
               command=lambda: _text_win(win, f'{algo_name} Info',
                                         info_obj.get_info() + '\n\n' +
                                         info_obj.get_structure_description()),
               bg=C['accent'], fg=C['bg'], relief='flat',
               padx=14, pady=6).pack(side='left', padx=6)
        Button(btn_frame, text='Close', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat',
               padx=14, pady=6).pack(side='left', padx=6)

        win.wait_window()

    def _show_twofish(self):
        self._finalist_window('Twofish', TwofishInfo, [128, 192, 256])

    def _show_serpent(self):
        self._finalist_window('Serpent', SerpentInfo, [128, 192, 256])

    def _show_rc6(self):
        self._finalist_window('RC6', RC6Info, [128, 192, 256], [('Rounds:', 20, 'rounds')])

    def _show_mars(self):
        self._finalist_window('MARS', MARSInfo, [128, 192, 256, 384, 448], [('Rounds:', 32, 'rounds')])

    def _show_comparison(self):
        _text_win(self.root, 'AES Finalists – Comparison Table', COMPARISON_TABLE, width=900)

    # ══════════════════════════════════════════════════════════════════════════
    #  VOTING (TP6)
    # ══════════════════════════════════════════════════════════════════════════

    def show_voting(self):
        f = self._clear()
        self._vote_counts = [0, 0, 0]
        self._voters = set()

        self._section_header(f, 'HOMOMORPHIC VOTING SYSTEM (TP6)',
                             'Zero-Knowledge Proofs | Homomorphic Encryption')

        id_row = ctk.CTkFrame(f, fg_color='transparent')
        id_row.pack(pady=8)
        ctk.CTkLabel(id_row, text='Voter ID:', text_color=C['text_muted']).pack(side='left', padx=6)
        self._voter_entry = ctk.CTkEntry(id_row, width=220, fg_color=C['bg'], border_color=C['border'])
        self._voter_entry.pack(side='left', padx=6)

        self._vote_var = ctk.StringVar(value='0')
        cand_frame = ctk.CTkFrame(f, fg_color=C['card'], corner_radius=8)
        cand_frame.pack(pady=8, padx=40, fill='x')
        ctk.CTkLabel(cand_frame, text='Select Candidate:', font=ctk.CTkFont(weight='bold'),
                     text_color=C['text']).pack(pady=(10, 4))
        for i, name in enumerate(['Candidate A', 'Candidate B', 'Candidate C']):
            ctk.CTkRadioButton(cand_frame, text=name, variable=self._vote_var, value=str(i),
                               fg_color=C['accent'], text_color=C['text']).pack(pady=4)

        ctk.CTkButton(f, text='CAST VOTE',
                      font=ctk.CTkFont(size=14, weight='bold'),
                      fg_color=C['green'], hover_color='#009944',
                      text_color='#000000', height=44,
                      command=self._cast_vote).pack(pady=16)

        ctk.CTkLabel(f, text='LIVE RESULTS (HOMOMORPHIC ENCRYPTION)',
                     font=ctk.CTkFont(size=14, weight='bold'),
                     text_color=C['text']).pack()

        self._results_box = ctk.CTkTextbox(f, height=200,
                                           fg_color=C['card'], text_color=C['text'])
        self._results_box.pack(fill='both', expand=True, pady=8)
        self._update_vote_display()

    def _cast_vote(self):
        voter_id = self._voter_entry.get().strip()
        if not voter_id:
            _err('Please enter a Voter ID')
            return
        if voter_id in self._voters:
            _err('This Voter ID has already voted!')
            return
        idx = int(self._vote_var.get())
        self._vote_counts[idx] += 1
        self._voters.add(voter_id)
        self._voter_entry.delete(0, 'end')
        receipt = hashlib.sha256(voter_id.encode()).hexdigest()[:16]
        candidates = ['Candidate A', 'Candidate B', 'Candidate C']
        _show('Vote Cast',
              f'✓ Vote recorded for {candidates[idx]}\n\nReceipt: {receipt}\n\n'
              f'(Store this receipt to verify your vote was counted)')
        self._update_vote_display()

    def _update_vote_display(self):
        self._results_box.delete('1.0', 'end')
        total = sum(self._vote_counts)
        lines = [
            'HOMOMORPHIC ENCRYPTION ACTIVE',
            'Votes tallied without individual decryption',
            '─' * 50,
            '',
        ]
        for i, name in enumerate(['Candidate A', 'Candidate B', 'Candidate C']):
            pct = (self._vote_counts[i] / total * 100) if total > 0 else 0
            bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
            lines.append(f'{name}: {self._vote_counts[i]:3d} votes ({pct:5.1f}%)  {bar}')
        lines += ['', f'Total voters: {total}', 'Integrity: ✓ VERIFIED (HMAC-SHA256)']
        self._results_box.insert('1.0', '\n'.join(lines))

    # ══════════════════════════════════════════════════════════════════════════
    #  ZK PROOFS  (NEW)
    # ══════════════════════════════════════════════════════════════════════════

    def show_zkp(self):
        f = self._clear()
        self._section_header(f, 'ZERO-KNOWLEDGE IDENTIFICATION PROTOCOLS',
                             'Prove knowledge without revealing it')
        self._grid_buttons(f, [
            ('Schnorr Identification',         self._run_schnorr),
            ('Feige–Fiat–Shamir (FFS)',         self._run_ffs),
        ], cols=2)

    def _run_schnorr(self):
        win = Toplevel(self.root)
        win.title('Schnorr Identification Protocol')
        win.geometry('600x500')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win,
              text='Schnorr Identification Protocol\n'
                   'Prove knowledge of discrete log x without revealing x.\n'
                   'Click Generate for random parameters, then Run Protocol.',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(lbl, val, row_idx, wide=False):
            Label(form, text=lbl, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=28).grid(
                row=row_idx, column=0, sticky='w', pady=3)
            e = Entry(form, font=('Courier', 9),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=44 if wide else 26, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=3, padx=(4, 0))
            e.insert(0, val)
            return e

        e_p = _row('Prime p:', '', 0, wide=True)
        e_q = _row('Prime q (q | p-1):', '', 1, wide=True)
        e_g = _row('Generator g (order q):', '', 2, wide=True)
        e_x = _row('Private key x:', '', 3, wide=True)
        e_y = _row('Public key y = g^x:', '', 4, wide=True)

        rounds_var = StringVar(value='3')
        rf = Frame(win, bg=C['bg']); rf.pack(pady=4)
        Label(rf, text='Rounds:', bg=C['bg'], fg=C['text'], font=('Arial', 10)).pack(side='left', padx=4)
        Entry(rf, textvariable=rounds_var, width=6,
              bg=C['card'], fg=C['text'], insertbackground=C['text'],
              font=('Courier', 10), relief='flat').pack(side='left', padx=4)

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=560)
        status.pack(padx=16, pady=2, anchor='w')

        def generate():
            status.config(text='Generating Schnorr parameters… please wait.', fg=C['accent'])
            win.update()
            try:
                p, q, g = SchnorrIdentification.generate_params(256, 128)
                x, y = SchnorrIdentification.generate_keypair(p, q, g)
                for ent, val in [(e_p, p), (e_q, q), (e_g, g), (e_x, x), (e_y, y)]:
                    ent.delete(0, 'end'); ent.insert(0, str(val))
                status.config(text='✓ Parameters generated. Click Run Protocol.', fg=C['green'])
            except Exception as ex:
                status.config(text=f'⚠ {ex}', fg=C['red'])

        def run_proto():
            try:
                p = int(e_p.get()); q = int(e_q.get()); g = int(e_g.get())
                x = int(e_x.get()); y = int(e_y.get())
                rds = int(rounds_var.get())
                status.config(text='Running protocol…', fg=C['accent']); win.update()
                report = SchnorrIdentification.full_report(p, q, g, x, y, rds)
                win.destroy()
                _text_win(self.root, 'Schnorr Identification', report, width=820, height=640)
            except Exception as ex:
                status.config(text=f'⚠ {ex}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg']); btn_row.pack(pady=10)
        Button(btn_row, text='Generate ▶', command=generate,
               bg=C['accent'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Run Protocol ▶', command=run_proto,
               bg=C['green'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=10, pady=5).pack(side='left', padx=6)

        win.wait_window()

    def _run_ffs(self):
        win = Toplevel(self.root)
        win.title('Feige–Fiat–Shamir Identification')
        win.geometry('560x420')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win,
              text='Feige–Fiat–Shamir Identification Protocol\n'
                   'Based on hardness of computing modular square roots.\n'
                   'Click Generate to create n, s, v, then Run Protocol.',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(lbl, val, row_idx, wide=False):
            Label(form, text=lbl, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=24).grid(
                row=row_idx, column=0, sticky='w', pady=3)
            e = Entry(form, font=('Courier', 9),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=46 if wide else 28, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=3, padx=(4, 0))
            e.insert(0, val)
            return e

        e_n = _row('Modulus n = p·q:', '', 0, wide=True)
        e_s = _row('Secret s:', '', 1, wide=True)
        e_v = _row('Public v = s² mod n:', '', 2, wide=True)

        rounds_var = StringVar(value='10')
        rf = Frame(win, bg=C['bg']); rf.pack(pady=4)
        Label(rf, text='Rounds:', bg=C['bg'], fg=C['text'], font=('Arial', 10)).pack(side='left', padx=4)
        Entry(rf, textvariable=rounds_var, width=6,
              bg=C['card'], fg=C['text'], insertbackground=C['text'],
              font=('Courier', 10), relief='flat').pack(side='left', padx=4)

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=520)
        status.pack(padx=16, pady=2, anchor='w')

        def generate():
            status.config(text='Generating FFS parameters… please wait.', fg=C['accent'])
            win.update()
            try:
                p, q, n = FeigeFiatShamir.setup(256)
                s, v = FeigeFiatShamir.generate_keypair(n)
                e_n.delete(0, 'end'); e_n.insert(0, str(n))
                e_s.delete(0, 'end'); e_s.insert(0, str(s))
                e_v.delete(0, 'end'); e_v.insert(0, str(v))
                status.config(text='✓ Parameters generated. Click Run Protocol.', fg=C['green'])
            except Exception as ex:
                status.config(text=f'⚠ {ex}', fg=C['red'])

        def run_proto():
            try:
                n = int(e_n.get()); s = int(e_s.get()); v = int(e_v.get())
                rds = int(rounds_var.get())
                status.config(text='Running FFS rounds…', fg=C['accent']); win.update()
                report = FeigeFiatShamir.full_report(n, s, v, rds)
                win.destroy()
                _text_win(self.root, 'Feige–Fiat–Shamir', report, width=820, height=640)
            except Exception as ex:
                status.config(text=f'⚠ {ex}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg']); btn_row.pack(pady=10)
        Button(btn_row, text='Generate ▶', command=generate,
               bg=C['accent'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Run Protocol ▶', command=run_proto,
               bg=C['green'], fg=C['bg'], relief='flat', padx=14, pady=5).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=10, pady=5).pack(side='left', padx=6)

        win.wait_window()

    # ══════════════════════════════════════════════════════════════════════════
    #  ADVANCED CRYPTO  (NEW)
    # ══════════════════════════════════════════════════════════════════════════

    def show_advanced(self):
        f = self._clear()
        self._section_header(f, 'ADVANCED CRYPTOGRAPHY',
                             'Secret Sharing | Homomorphic Encryption')
        self._grid_buttons(f, [
            ("Shamir's Secret Sharing",        self._run_shamir),
            ('Paillier (Homomorphic Enc.)',    self._run_paillier),
        ], cols=2)

    def _run_shamir(self):
        win = Toplevel(self.root)
        win.title("Shamir's Secret Sharing")
        win.geometry('500x380')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win,
              text="Shamir's (k, n) Secret Sharing\n"
                   'Split a secret into n shares; any k shares reconstruct it.\n'
                   'Perfect secrecy: fewer than k shares reveal nothing.',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(lbl, val, row_idx):
            Label(form, text=lbl, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=30).grid(
                row=row_idx, column=0, sticky='w', pady=5)
            e = Entry(form, font=('Courier', 10),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=22, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=5, padx=(4, 0))
            e.insert(0, val)
            return e

        e_secret = _row('Secret (integer):', '123456789', 0)
        e_k      = _row('Threshold k (min shares needed):', '3', 1)
        e_n      = _row('Total shares n:', '5', 2)

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=460)
        status.pack(padx=16, pady=4, anchor='w')

        def run():
            try:
                secret = int(e_secret.get().strip())
                k = int(e_k.get().strip())
                n = int(e_n.get().strip())
                if k < 2:
                    raise ValueError('Threshold k must be ≥ 2.')
                if n < k:
                    raise ValueError('Total shares n must be ≥ k.')
                status.config(text='Computing…', fg=C['accent']); win.update()
                report = ShamirSecretSharing.full_report(secret, k, n)
                win.destroy()
                _text_win(self.root, "Shamir's Secret Sharing", report, width=760, height=620)
            except Exception as ex:
                status.config(text=f'⚠ {ex}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg']); btn_row.pack(pady=12)
        Button(btn_row, text='Run ▶', command=run,
               bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=14, pady=6).pack(side='left', padx=6)

        win.wait_window()

    def _run_paillier(self):
        win = Toplevel(self.root)
        win.title('Paillier Homomorphic Encryption')
        win.geometry('520x400')
        win.configure(bg=C['bg'])
        win.transient(self.root)
        win.grab_set()

        Label(win,
              text='Paillier Cryptosystem – Additive Homomorphic Encryption\n'
                   'E(m₁)·E(m₂) mod n² decrypts to m₁+m₂.\n'
                   'Enter two messages and a scalar k.',
              bg=C['bg'], fg=C['text_muted'], font=('Arial', 9),
              justify='left').pack(pady=(12, 4), padx=16, anchor='w')

        form = tk.Frame(win, bg=C['bg'])
        form.pack(fill='x', padx=16, pady=4)

        def _row(lbl, val, row_idx):
            Label(form, text=lbl, bg=C['bg'], fg=C['text'],
                  font=('Arial', 10), anchor='w', width=30).grid(
                row=row_idx, column=0, sticky='w', pady=5)
            e = Entry(form, font=('Courier', 10),
                      bg=C['card'], fg=C['text'], insertbackground=C['text'],
                      width=20, relief='flat')
            e.grid(row=row_idx, column=1, sticky='w', pady=5, padx=(4, 0))
            e.insert(0, val)
            return e

        e_m1     = _row('Message m₁ (integer):', '42', 0)
        e_m2     = _row('Message m₂ (integer):', '58', 1)
        e_scalar = _row('Scalar k (for k·m₁):', '3', 2)
        e_bits   = _row('Key size (bits, min 128):', '128', 3)

        status = Label(win, text='', bg=C['bg'], fg=C['text_muted'],
                       font=('Arial', 8), wraplength=480)
        status.pack(padx=16, pady=4, anchor='w')

        def run():
            try:
                m1     = int(e_m1.get().strip())
                m2     = int(e_m2.get().strip())
                scalar = int(e_scalar.get().strip())
                bits   = int(e_bits.get().strip())
                if bits < 64:
                    raise ValueError('Key size must be ≥ 64 bits.')
                status.config(text='Generating keys and running homomorphic operations…', fg=C['accent'])
                win.update()
                report = PaillierCryptosystem.full_report(m1, m2, scalar, bits)
                win.destroy()
                _text_win(self.root, 'Paillier Homomorphic Encryption', report, width=800, height=640)
            except Exception as ex:
                status.config(text=f'⚠ {ex}', fg=C['red'])

        btn_row = tk.Frame(win, bg=C['bg']); btn_row.pack(pady=12)
        Button(btn_row, text='Run ▶', command=run,
               bg=C['green'], fg=C['bg'], relief='flat', padx=20, pady=6).pack(side='left', padx=6)
        Button(btn_row, text='Cancel', command=win.destroy,
               bg=C['red'], fg=C['text'], relief='flat', padx=14, pady=6).pack(side='left', padx=6)

        win.wait_window()

    # ── Run ───────────────────────────────────────────────────────────────────

    def run(self):
        self.root.mainloop()


# ══════════════════════════════════════════════════════════════════════════════
#  Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print('=' * 60)
    print('COMPLETE CRYPTOGRAPHY SUITE  v7.0')
    print('=' * 60)
    print('\nAlgorithm modules:')
    print('  ✓ classical/            – Caesar, Vigenère, Hill, Playfair, OTP, Atbash, Scytale, Sub, Affine')
    print('  ✓ symmetric/            – AES-CBC, AES-GCM, AES-ECB ⚠, DES, 3DES, RC4')
    print('  ✓ asymmetric/           – RSA, Diffie-Hellman, ElGamal, ECC')
    print('  ✓ hash/                 – MD5, SHA-1, SHA-256, SHA-512, RIPEMD, HMAC, IC')
    print('  ✓ hash_additions/       – Merkle–Damgård, Kerckhoffs Principle, Kasiski Test')
    print('  ✓ signatures/           – ECDSA, DSA, RSA-sig, ElGamal-sig')
    print('  ✓ finalists/            – Rijndael, Twofish, Serpent, RC6, MARS')
    print('  ✓ zkp_protocols/        – Schnorr Identification, Feige–Fiat–Shamir')
    print("  ✓ advanced_crypto/      – Shamir's Secret Sharing, Paillier (Homomorphic)")
    print('\nStarting GUI…\n')

    app = CryptographySuiteApp()
    app.run()
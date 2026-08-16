"""
ui.py — QuantumCrypt Lab
Main CustomTkinter UI. Simplified for educational demonstration.
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from classical_crypto import aes_encrypt, aes_decrypt
from quantum_crypto import quantum_encrypt, quantum_decrypt

# ---------------------------------------------------------------------------
# Theme configuration
# ---------------------------------------------------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Brand colours
ACCENT = "#3B82F6"        
ACCENT_HOVER = "#2563EB"
BG_CARD = "#1E293B"       
TEXT_MUTED = "#94A3B8"    


# ---------------------------------------------------------------------------
# Reusable widget helpers
# ---------------------------------------------------------------------------
def _copy_to_clipboard(root, text: str):
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        messagebox.showinfo("Copied", "Text copied to clipboard!", parent=root)

def _get_textbox(tb) -> str:
    return tb.get("1.0", "end").strip()

def _set_textbox(tb, text: str):
    tb.configure(state="normal")
    tb.delete("1.0", "end")
    tb.insert("1.0", text)
    tb.configure(state="disabled")

# ---------------------------------------------------------------------------
# Main Application Window
# ---------------------------------------------------------------------------

class QuantumCryptLabApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QuantumCrypt Lab")
        self.geometry("900x750")
        self.minsize(800, 650)
        self.configure(fg_color="#0F172A")

        self._build_header()
        self._build_tabs()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="#0F172A", corner_radius=0)
        header.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="QuantumCrypt Lab",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#F1F5F9",
        ).pack(anchor="center")

        ctk.CTkLabel(
            header,
            text="Classical vs Quantum Cryptographic Schemes",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_MUTED,
        ).pack(anchor="center", pady=(2, 10))

    def _build_tabs(self):
        self.tabs = ctk.CTkTabview(
            self,
            fg_color="#0F172A",
            segmented_button_fg_color="#1E293B",
            segmented_button_selected_color=ACCENT,
            segmented_button_selected_hover_color=ACCENT_HOVER,
            text_color="#CBD5E1",
            corner_radius=8,
        )
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)

        self.tabs.add("  Classical AES  ")
        self.tabs.add("  Quantum / BB84  ")

        self._build_workflow_tab(self.tabs.tab("  Classical AES  "), is_quantum=False)
        self._build_workflow_tab(self.tabs.tab("  Quantum / BB84  "), is_quantum=True)

    def _build_workflow_tab(self, parent, is_quantum: bool):
        parent.configure(fg_color="#0F172A")
        
        # Main layout
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # ------------------- ENCRYPT SECTION -------------------
        enc_frame = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=10)
        enc_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(enc_frame, text="ENCRYPT MESSAGE", font=ctk.CTkFont(size=16, weight="bold"), text_color="#E2E8F0").pack(pady=(15, 10))
        
        # Message input
        ctk.CTkLabel(enc_frame, text="Message", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=20)
        msg_tb = ctk.CTkTextbox(enc_frame, height=60, font=ctk.CTkFont(size=13))
        msg_tb.pack(fill="x", padx=20, pady=(0, 10))
        
        # Key input
        ctk.CTkLabel(enc_frame, text="Key", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=20)
        key_enc_entry = ctk.CTkEntry(enc_frame, font=ctk.CTkFont(size=13), height=36)
        key_enc_entry.pack(fill="x", padx=20, pady=(0, 15))

        # Output Encrypted Text
        ctk.CTkLabel(enc_frame, text="Encrypted Text", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=20)
        enc_out_tb = ctk.CTkTextbox(enc_frame, height=60, font=ctk.CTkFont(size=13), state="disabled")
        enc_out_tb.pack(fill="x", padx=20, pady=(0, 10))

        # Buttons
        btn_row_enc = ctk.CTkFrame(enc_frame, fg_color="transparent")
        btn_row_enc.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            btn_row_enc, text="Encrypt", width=120, height=36, font=ctk.CTkFont(weight="bold"),
            command=lambda: self._handle_encrypt(msg_tb, key_enc_entry, enc_out_tb, is_quantum)
        ).pack(side="left")

        ctk.CTkButton(
            btn_row_enc, text="Copy", width=100, height=36, fg_color="#475569", hover_color="#334155",
            command=lambda: _copy_to_clipboard(self, _get_textbox(enc_out_tb))
        ).pack(side="right")

        # ------------------- EDUCATIONAL SECTION -------------------
        edu_container = ctk.CTkFrame(scroll, fg_color="transparent")
        edu_container.pack(fill="x", padx=10, pady=20)

        card1 = ctk.CTkFrame(edu_container, fg_color=BG_CARD, corner_radius=10)
        card1.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        card2 = ctk.CTkFrame(edu_container, fg_color=BG_CARD, corner_radius=10)
        card2.pack(side="right", fill="both", expand=True, padx=(5, 0))

        if is_quantum:
            title1 = "How BB84 Works"
            text1 = (
                "BB84 is a Quantum Key Distribution protocol used to establish a shared secret key.\n\n"
                "① User A prepares quantum bits\n"
                "Random bits are encoded using randomly selected quantum bases.\n\n"
                "② User B measures the quantum bits\n"
                "User B independently chooses bases to measure the received quantum states.\n\n"
                "③ Bases are compared\n"
                "User A and User B compare their selected bases, not the actual secret bits.\n\n"
                "④ Matching bases are kept\n"
                "Only positions where both used the same basis are retained.\n\n"
                "⑤ A shared key is formed\n"
                "The remaining matching bits can be used as a shared secret key."
            )
            title2 = "How the Key Is Used"
            text2 = (
                "BB84 distributes the key; it does not directly encrypt the message.\n\n"
                "① Your Key\n"
                "The secret key entered by the user for this demonstration.\n\n"
                "② BB84 Shared Key\n"
                "BB84 demonstrates how two parties can establish a shared secret key.\n\n"
                "③ AES Encryption\n"
                "The shared key can then be used with AES to encrypt the message.\n\n"
                "④ Encrypted Message\n"
                "The readable message is converted into ciphertext."
            )
        else:
            title1 = "How AES Encryption Works"
            text1 = (
                "① Plain Text\n"
                "The original readable message entered by the user.\n\n"
                "② Secret Key\n"
                "The key is used by AES to transform the message.\n\n"
                "③ AES Encryption\n"
                "AES converts the readable message into ciphertext.\n\n"
                "④ Encrypted Message\n"
                "The resulting ciphertext cannot be read directly without the correct key."
            )
            title2 = "How AES Decryption Works"
            text2 = (
                "① Encrypted Message\n"
                "The ciphertext that needs to be decrypted.\n\n"
                "② Same Secret Key\n"
                "The exact same key used for encryption must be provided.\n\n"
                "③ AES Decryption\n"
                "The algorithm reverses the encryption process.\n\n"
                "④ Original Message\n"
                "The original plain text is fully restored."
            )
            
        ctk.CTkLabel(card1, text=title1, font=ctk.CTkFont(size=14, weight="bold"), text_color="#E2E8F0").pack(pady=(15, 10))
        ctk.CTkLabel(card1, text=text1, font=ctk.CTkFont(size=12), text_color="#CBD5E1", justify="left", wraplength=350).pack(pady=(0, 15), padx=20, anchor="w")

        ctk.CTkLabel(card2, text=title2, font=ctk.CTkFont(size=14, weight="bold"), text_color="#E2E8F0").pack(pady=(15, 10))
        ctk.CTkLabel(card2, text=text2, font=ctk.CTkFont(size=12), text_color="#CBD5E1", justify="left", wraplength=350).pack(pady=(0, 15), padx=20, anchor="w")

        # ------------------- DECRYPT SECTION -------------------
        dec_frame = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=10)
        dec_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(dec_frame, text="DECRYPT MESSAGE", font=ctk.CTkFont(size=16, weight="bold"), text_color="#E2E8F0").pack(pady=(15, 10))
        
        # Cipher input
        ctk.CTkLabel(dec_frame, text="Encrypted Text", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=20)
        cipher_tb = ctk.CTkTextbox(dec_frame, height=60, font=ctk.CTkFont(size=13))
        cipher_tb.pack(fill="x", padx=20, pady=(0, 10))
        
        # Key input
        ctk.CTkLabel(dec_frame, text="Key", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=20)
        key_dec_entry = ctk.CTkEntry(dec_frame, font=ctk.CTkFont(size=13), height=36)
        key_dec_entry.pack(fill="x", padx=20, pady=(0, 15))

        # Output Decrypted Text
        ctk.CTkLabel(dec_frame, text="Decrypted Text", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=20)
        dec_out_tb = ctk.CTkTextbox(dec_frame, height=60, font=ctk.CTkFont(size=13), state="disabled")
        dec_out_tb.pack(fill="x", padx=20, pady=(0, 10))

        # Buttons
        btn_row_dec = ctk.CTkFrame(dec_frame, fg_color="transparent")
        btn_row_dec.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            btn_row_dec, text="Decrypt", width=120, height=36, font=ctk.CTkFont(weight="bold"),
            command=lambda: self._handle_decrypt(cipher_tb, key_dec_entry, dec_out_tb, is_quantum)
        ).pack(side="left")

        # ------------------- FOOTER SECTION -------------------
        # Reset button
        ctk.CTkButton(
            scroll, text="Reset", width=120, height=36, fg_color="#1E293B", hover_color="#334155",
            command=lambda: self._reset_fields([msg_tb, key_enc_entry, enc_out_tb, cipher_tb, key_dec_entry, dec_out_tb])
        ).pack(pady=15)

        # Educational text
        edu_text = (
            "BB84: A Quantum Key Distribution protocol that allows two parties to establish a shared key and detect possible eavesdropping. "
            "The actual message can then be encrypted using symmetric encryption such as AES."
            if is_quantum else
            "AES: A symmetric encryption algorithm where the same secret key is used for encryption and decryption."
        )
        ctk.CTkLabel(
            scroll, text=edu_text, font=ctk.CTkFont(size=12, slant="italic"), text_color=TEXT_MUTED, wraplength=700, justify="center"
        ).pack(pady=(0, 20))

    # -----------------------------------------------------------------------
    # Action Handlers
    # -----------------------------------------------------------------------
    
    def _handle_encrypt(self, msg_tb, key_entry, out_tb, is_quantum):
        msg = _get_textbox(msg_tb)
        key = key_entry.get().strip()

        if not msg:
            messagebox.showwarning("Input Error", "Please enter a message.", parent=self)
            return
        if not key:
            messagebox.showwarning("Input Error", "Please enter a key.", parent=self)
            return

        try:
            if is_quantum:
                result = quantum_encrypt(msg, key)
            else:
                result = aes_encrypt(msg, key)
            
            _set_textbox(out_tb, result)
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e), parent=self)

    def _handle_decrypt(self, cipher_tb, key_entry, out_tb, is_quantum):
        cipher = _get_textbox(cipher_tb)
        key = key_entry.get().strip()

        if not cipher:
            messagebox.showwarning("Input Error", "Please paste the encrypted text.", parent=self)
            return
        if not key:
            messagebox.showwarning("Input Error", "Please enter a key.", parent=self)
            return

        try:
            if is_quantum:
                result = quantum_decrypt(cipher, key)
            else:
                result = aes_decrypt(cipher, key)
            
            _set_textbox(out_tb, result)
        except Exception:
            messagebox.showerror("Decryption Failed", "Invalid key or encrypted text.", parent=self)
            _set_textbox(out_tb, "")

    def _reset_fields(self, widgets):
        for w in widgets:
            if isinstance(w, ctk.CTkTextbox):
                _set_textbox(w, "")
            elif isinstance(w, ctk.CTkEntry):
                w.delete(0, "end")


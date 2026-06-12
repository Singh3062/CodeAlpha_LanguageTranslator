import tkinter as tk
from tkinter import ttk, messagebox
import threading
try:
    from googletrans import Translator, LANGUAGES
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "googletrans==4.0.0-rc1"])
    from googletrans import Translator, LANGUAGES

# ── App Setup ──────────────────────────────────────────────────────────────────
translator = Translator()

LANG_OPTIONS = {v.title(): k for k, v in LANGUAGES.items()}
LANG_NAMES   = sorted(LANG_OPTIONS.keys())

# ── Main Window ────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("🌐 Language Translator — CodeAlpha")
root.geometry("780x540")
root.resizable(False, False)
root.configure(bg="#1a1a2e")

# ── Fonts & Colours ────────────────────────────────────────────────────────────
BG       = "#1a1a2e"
PANEL    = "#16213e"
ACCENT   = "#0f3460"
HIGHLIGHT= "#e94560"
TEXT     = "#eaeaea"
SUBTEXT  = "#a0a0b0"
WHITE    = "#ffffff"

FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_LABEL  = ("Segoe UI", 10, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_TEXT   = ("Segoe UI", 11)
FONT_BTN    = ("Segoe UI", 11, "bold")

# ── Title Bar ──────────────────────────────────────────────────────────────────
title_frame = tk.Frame(root, bg=ACCENT, pady=10)
title_frame.pack(fill="x")

tk.Label(title_frame, text="🌐  Language Translator",
         font=FONT_TITLE, bg=ACCENT, fg=WHITE).pack()
tk.Label(title_frame, text="Powered by Google Translate  •  CodeAlpha AI Internship",
         font=("Segoe UI", 9), bg=ACCENT, fg=SUBTEXT).pack()

# ── Language Selectors ─────────────────────────────────────────────────────────
sel_frame = tk.Frame(root, bg=BG, pady=12)
sel_frame.pack(fill="x", padx=30)

# Source
tk.Label(sel_frame, text="Source Language", font=FONT_LABEL,
         bg=BG, fg=SUBTEXT).grid(row=0, column=0, sticky="w")
src_var = tk.StringVar(value="English")
src_cb  = ttk.Combobox(sel_frame, textvariable=src_var, values=LANG_NAMES,
                        width=22, font=FONT_NORMAL, state="readonly")
src_cb.grid(row=1, column=0, padx=(0, 10))

# Swap button
swap_btn = tk.Button(sel_frame, text="⇄", font=("Segoe UI", 14, "bold"),
                     bg=HIGHLIGHT, fg=WHITE, relief="flat",
                     padx=10, cursor="hand2",
                     command=lambda: swap_languages())
swap_btn.grid(row=1, column=1, padx=8)

# Target
tk.Label(sel_frame, text="Target Language", font=FONT_LABEL,
         bg=BG, fg=SUBTEXT).grid(row=0, column=2, sticky="w")
tgt_var = tk.StringVar(value="Hindi")
tgt_cb  = ttk.Combobox(sel_frame, textvariable=tgt_var, values=LANG_NAMES,
                        width=22, font=FONT_NORMAL, state="readonly")
tgt_cb.grid(row=1, column=2, padx=(10, 0))

def swap_languages():
    s, t = src_var.get(), tgt_var.get()
    src_var.set(t); tgt_var.set(s)
    # also swap text
    s_text = input_text.get("1.0", "end-1c")
    t_text = output_text.get("1.0", "end-1c")
    input_text.delete("1.0", "end"); input_text.insert("1.0", t_text)
    output_text.config(state="normal")
    output_text.delete("1.0", "end"); output_text.insert("1.0", s_text)
    output_text.config(state="disabled")

# ── Text Areas ─────────────────────────────────────────────────────────────────
areas_frame = tk.Frame(root, bg=BG)
areas_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))

# --- Input ---
left = tk.Frame(areas_frame, bg=BG)
left.pack(side="left", fill="both", expand=True, padx=(0, 8))

tk.Label(left, text="Enter Text", font=FONT_LABEL,
         bg=BG, fg=SUBTEXT).pack(anchor="w")

input_text = tk.Text(left, height=10, font=FONT_TEXT,
                     bg=PANEL, fg=TEXT, insertbackground=WHITE,
                     relief="flat", padx=10, pady=8,
                     wrap="word", bd=0, highlightthickness=1,
                     highlightbackground=ACCENT)
input_text.pack(fill="both", expand=True)

# Placeholder
PLACEHOLDER = "Type or paste text here…"
def add_placeholder(e=None):
    if not input_text.get("1.0", "end-1c"):
        input_text.insert("1.0", PLACEHOLDER)
        input_text.config(fg=SUBTEXT)

def remove_placeholder(e=None):
    if input_text.get("1.0", "end-1c") == PLACEHOLDER:
        input_text.delete("1.0", "end")
        input_text.config(fg=TEXT)

input_text.bind("<FocusIn>",  remove_placeholder)
input_text.bind("<FocusOut>", add_placeholder)
add_placeholder()

# Char counter
char_var = tk.StringVar(value="0 / 5000")
tk.Label(left, textvariable=char_var, font=("Segoe UI", 8),
         bg=BG, fg=SUBTEXT).pack(anchor="e", pady=2)

def update_counter(e=None):
    txt = input_text.get("1.0", "end-1c")
    if txt == PLACEHOLDER: txt = ""
    char_var.set(f"{len(txt)} / 5000")

input_text.bind("<KeyRelease>", update_counter)

# --- Output ---
right = tk.Frame(areas_frame, bg=BG)
right.pack(side="left", fill="both", expand=True, padx=(8, 0))

tk.Label(right, text="Translation", font=FONT_LABEL,
         bg=BG, fg=SUBTEXT).pack(anchor="w")

output_text = tk.Text(right, height=10, font=FONT_TEXT,
                      bg=PANEL, fg=HIGHLIGHT,
                      relief="flat", padx=10, pady=8,
                      wrap="word", bd=0, highlightthickness=1,
                      highlightbackground=ACCENT,
                      state="disabled")
output_text.pack(fill="both", expand=True)

# ── Buttons ────────────────────────────────────────────────────────────────────
btn_frame = tk.Frame(root, bg=BG, pady=6)
btn_frame.pack()

status_var = tk.StringVar(value="")

def set_status(msg, color=SUBTEXT):
    status_var.set(msg)
    status_lbl.config(fg=color)

def do_translate():
    raw = input_text.get("1.0", "end-1c")
    if not raw or raw == PLACEHOLDER:
        messagebox.showwarning("Empty Input", "Please enter some text to translate.")
        return

    src_name = src_var.get()
    tgt_name = tgt_var.get()
    src_code = LANG_OPTIONS.get(src_name, "auto")
    tgt_code = LANG_OPTIONS.get(tgt_name, "en")

    translate_btn.config(state="disabled", text="Translating…")
    set_status("⏳ Translating…", SUBTEXT)

    def worker():
        try:
            result = translator.translate(raw, src=src_code, dest=tgt_code)
            translated = result.text
            root.after(0, lambda: show_result(translated))
        except Exception as ex:
            root.after(0, lambda: show_error(str(ex)))

    threading.Thread(target=worker, daemon=True).start()

def show_result(translated):
    output_text.config(state="normal")
    output_text.delete("1.0", "end")
    output_text.insert("1.0", translated)
    output_text.config(state="disabled")
    translate_btn.config(state="normal", text="🌐  Translate")
    set_status("✅ Translation complete!", "#4caf50")

def show_error(err):
    translate_btn.config(state="normal", text="🌐  Translate")
    set_status(f"❌ Error: {err}", HIGHLIGHT)

def copy_result():
    result = output_text.get("1.0", "end-1c")
    if result:
        root.clipboard_clear()
        root.clipboard_append(result)
        set_status("📋 Copied to clipboard!", "#4caf50")
    else:
        set_status("Nothing to copy.", SUBTEXT)

def clear_all():
    input_text.delete("1.0", "end")
    add_placeholder()
    output_text.config(state="normal")
    output_text.delete("1.0", "end")
    output_text.config(state="disabled")
    char_var.set("0 / 5000")
    set_status("")

translate_btn = tk.Button(btn_frame, text="🌐  Translate",
                          font=FONT_BTN, bg=HIGHLIGHT, fg=WHITE,
                          relief="flat", padx=24, pady=8,
                          cursor="hand2", command=do_translate)
translate_btn.grid(row=0, column=0, padx=6)

tk.Button(btn_frame, text="📋  Copy", font=FONT_BTN,
          bg=ACCENT, fg=WHITE, relief="flat", padx=16, pady=8,
          cursor="hand2", command=copy_result).grid(row=0, column=1, padx=6)

tk.Button(btn_frame, text="🗑  Clear", font=FONT_BTN,
          bg="#333355", fg=WHITE, relief="flat", padx=16, pady=8,
          cursor="hand2", command=clear_all).grid(row=0, column=2, padx=6)

# ── Status Bar ─────────────────────────────────────────────────────────────────
status_lbl = tk.Label(root, textvariable=status_var, font=("Segoe UI", 9),
                      bg=BG, fg=SUBTEXT)
status_lbl.pack(pady=(0, 8))

# Bind Enter key
root.bind("<Return>", lambda e: do_translate())

# ── Style tweaks for combobox ──────────────────────────────────────────────────
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox",
                fieldbackground=PANEL, background=PANEL,
                foreground=TEXT, selectbackground=ACCENT,
                arrowcolor=WHITE)

root.mainloop()

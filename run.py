#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil
import time
import threading
import random

# ===================== KONFIGURASI WARNA =====================
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
BLINK = "\033[5m"

# Warna dasar
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
def color(fg, bg=None, bright=False):
    if bright:
        fg += 60 if fg < 8 else 0
    return f"\033[{90 + fg if fg >= 8 else 30 + fg}m" if bg is None else f"\033[{40 + bg}m"

# Warna terang (bright)
BRED = color(RED, bright=True)
BGREEN = color(GREEN, bright=True)
BYELLOW = color(YELLOW, bright=True)
BBLUE = color(BLUE, bright=True)
BMAGENTA = color(MAGENTA, bright=True)
BCYAN = color(CYAN, bright=True)
BWHITE = color(WHITE, bright=True)

# ===================== FUNGSI BANTUAN =====================
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def get_term_size():
    return shutil.get_terminal_size(fallback=(80, 24)).columns

def center(text, width=None):
    if width is None:
        width = get_term_size()
    return text.center(width)

def print_center(text, col=RESET, width=None):
    print(col + center(text, width) + RESET)

def gradient_text(text, start_rgb=(255,0,0), end_rgb=(0,255,255)):
    """Gradien dengan 256 warna (jika terminal mendukung)."""
    # Karena tidak semua terminal support 256, kita pakai 16 warna
    # Kita buat gradien sederhana dari merah ke biru
    colors = [RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA]
    out = ""
    length = len(text)
    for i, ch in enumerate(text):
        if ch == ' ':
            out += ch
            continue
        idx = int((i / length) * (len(colors)-1))
        out += colors[idx] + ch
    return out + RESET

def fancy_border(text, color=BCYAN, width=None):
    if width is None:
        width = get_term_size()
    border_char = "═"
    top = "╔" + border_char * (width - 2) + "╗"
    bottom = "╚" + border_char * (width - 2) + "╝"
    print(color + top + RESET)
    print(color + "║" + center(text, width - 2) + "║" + RESET)
    print(color + bottom + RESET)

def progress_bar(percent, width=40, color=BGREEN):
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"{color}{bar}{RESET} {percent:3d}%"

# ===================== ASCII ART (dengan pyfiglet jika ada) =====================
try:
    import pyfiglet
    ascii_art = pyfiglet.figlet_format("CANELABOT", font="slant")
except ImportError:
    ascii_art = """
   ██████╗ █████╗ ███╗   ██╗███████╗██╗      █████╗ ██████╗  ██████╗ ████████╗
  ██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝
  ██████╔╝███████║██╔██╗ ██║█████╗  ██║     ███████║██████╔╝██║   ██║   ██║   
  ██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  ██║     ██╔══██║██╔══██╗██║   ██║   ██║   
  ██║     ██║  ██║██║ ╚████║███████╗███████╗██║  ██║██████╔╝╚██████╔╝   ██║   
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   
    """

# ===================== FUNGSI UTAMA =====================
def check_terminal_size():
    MIN_WIDTH = 64
    while True:
        cols = get_term_size()
        clear()
        if cols >= MIN_WIDTH:
            # Tampilan PAS
            print(gradient_text(ascii_art))
            print()
            fancy_border("✦  TERMINAL OPTIMIZED  ✦", BCYAN)
            print()
            info = f"Status : {BGREEN}SIAP{RESET}  |  Lebar : {cols}/{MIN_WIDTH} kolom  |  Channel : @canelabi"
            print_center(info, BWHITE)
            print()
            # Progress bar ukuran (simbolis)
            pct = min(100, int(cols / MIN_WIDTH * 100))
            bar = progress_bar(pct, width=40, color=BGREEN if pct>=100 else BYELLOW)
            print_center(bar, BWHITE)
            print()
            # Tombol enter dengan efek blink
            blink_msg = f"{BLINK}{BYELLOW}▶  TEKAN ENTER UNTUK MELUNCURKAN  ◀{RESET}"
            print_center(blink_msg, BYELLOW)
            print()
            fancy_border("", DIM)
            input()
            break
        else:
            # Tampilan PERINGATAN
            print(gradient_text("⚠️  TERMINAL TERLALU KECIL"))
            print()
            fancy_border("✗  PERLUAS LAYAR!", BRED)
            print()
            print_center(f"Lebar : {cols}/{MIN_WIDTH} kolom  |  Channel : @canelabi", BYELLOW)
            print()
            bar = progress_bar(int(cols/MIN_WIDTH*100), width=40, color=BRED)
            print_center(bar, BRED)
            print()
            print_center(f"{BLINK}{BYELLOW}▶  Zoom out atau perbesar terminal{RESET}", BYELLOW)
            print()
            fancy_border("", DIM)
            time.sleep(0.6)

# ===================== UPDATE REPOSITORY =====================
def update_repo():
    clear()
    print(gradient_text(ascii_art))
    print()
    fancy_border("🔄  MENGUPDATE REPOSITORY", BCYAN)
    print()

    # Animasi spinner dengan progress
    stop = threading.Event()
    def spinner():
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        idx = 0
        while not stop.is_set():
            sys.stdout.write(f"\r{BCYAN}{chars[idx]}  Menarik pembaruan ...{RESET}")
            sys.stdout.flush()
            idx = (idx + 1) % len(chars)
            time.sleep(0.1)
    t = threading.Thread(target=spinner)
    t.start()

    result = subprocess.run(["git", "pull"], capture_output=True, text=True)
    stop.set()
    t.join()
    sys.stdout.write("\r" + " " * 40 + "\r")
    sys.stdout.flush()

    if result.returncode == 0:
        print(f"{BGREEN}✅  Repository berhasil diperbarui!{RESET}")
        if result.stdout:
            print(DIM + result.stdout.strip() + RESET)
    else:
        print(f"{BRED}❌  Gagal memperbarui repository.{RESET}")
        if result.stderr:
            print(DIM + result.stderr.strip() + RESET)
    print()

# ===================== LOADING AKHIR =====================
def final_loading():
    print(f"{BYELLOW}⏳  Mempersiapkan lingkungan ...{RESET}")
    for pct in range(0, 101, 5):
        bar = progress_bar(pct, width=50, color=BCYAN)
        sys.stdout.write(f"\r{bar}")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\n")
    time.sleep(0.5)

# ===================== MAIN =====================
def main():
    # Cek ukuran
    check_terminal_size()

    # Update
    update_repo()

    # Loading
    final_loading()

    # Jalankan loly.py
    print(f"{BGREEN}🚀  MELUNCURKAN LOLY.PY ...{RESET}\n")
    time.sleep(0.5)
    if os.path.exists("loly.py"):
        os.execv(sys.executable, [sys.executable, "loly.py"])
    else:
        print(f"{BRED}❌  File loly.py tidak ditemukan!{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()

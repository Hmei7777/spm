#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import getpass

APP_NAME = "LOLY TOOLS"
APP_VERSION = "2.0.0"
MIN_WIDTH = 64

# GANTI DENGAN URL API LOGIN MILIKMU
AUTH_API_URL = "http://127.0.0.1:8080/api/login"

# GANTI DENGAN USERNAME TELEGRAM OWNER
OWNER_TELEGRAM = "abireal"

MAIN_TOOL = "loly.py"
AUTH_TIMEOUT = 12

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"


def clear():
    os.system("clear")


def terminal_width():
    return shutil.get_terminal_size(fallback=(80, 24)).columns


def line(char="═", width=None):
    if width is None:
        width = min(max(terminal_width() - 2, MIN_WIDTH), 72)
    return char * width


def pause(message="Tekan ENTER untuk melanjutkan..."):
    try:
        input(f"\n{GRAY}{message}{RESET}")
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(0)


def open_telegram():
    username = OWNER_TELEGRAM.lstrip("@")
    url = f"https://t.me/{username}"

    for command in (
        ["am", "start", "-a", "android.intent.action.VIEW", "-d", url],
        ["termux-open-url", url],
    ):
        try:
            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            return True
        except Exception:
            pass

    return False


def print_header():
    width = min(max(terminal_width() - 2, MIN_WIDTH), 72)
    print(f"{CYAN}{line('═', width)}{RESET}")
    print(f"{CYAN}║{RESET}{BOLD}{WHITE}{'✦  LOLY TOOLS  ✦'.center(width - 2)}{RESET}{CYAN}║{RESET}")
    print(f"{CYAN}║{RESET}{GRAY}{'Premium Utility System'.center(width - 2)}{RESET}{CYAN}║{RESET}")
    print(f"{CYAN}║{RESET}{GREEN}{'● SYSTEM ONLINE'.center(width - 2)}{RESET}{CYAN}║{RESET}")
    print(f"{CYAN}║{RESET}{GRAY}{('Version ' + APP_VERSION).center(width - 2)}{RESET}{CYAN}║{RESET}")
    print(f"{CYAN}{line('═', width)}{RESET}")


def terminal_check():
    while True:
        cols = terminal_width()
        if cols >= MIN_WIDTH:
            return

        clear()
        width = min(max(cols - 2, 20), 72)
        print(f"{RED}{line('═', width)}{RESET}")
        print(f"{RED}{BOLD}{'✗ TERMINAL TERLALU KECIL'.center(width)}{RESET}")
        print(f"{RED}{line('═', width)}{RESET}")
        print(f"\n{YELLOW}Lebar terminal : {cols} kolom")
        print(f"Minimal        : {MIN_WIDTH} kolom")
        print("Silakan zoom out / kecilkan ukuran font Termux.")
        print(f"{RESET}\n{RED}{line('═', width)}{RESET}")
        time.sleep(1)


def main_menu():
    while True:
        clear()
        print_header()

        width = min(max(terminal_width() - 2, MIN_WIDTH), 72)

        print(f"\n{WHITE}{BOLD}  ┌─ MAIN MENU{RESET}")
        print(f"{CYAN}  │{RESET}")
        print(f"{CYAN}  │{RESET}  {GREEN}[1]{RESET}  LOGIN")
        print(f"{CYAN}  │{RESET}  {YELLOW}[2]{RESET}  BUY KEY")
        print(f"{CYAN}  │{RESET}  {RED}[0]{RESET}  EXIT")
        print(f"{CYAN}  │{RESET}")
        print(f"{CYAN}  └{RESET}{line('─', width - 5)}")

        try:
            choice = input(f"\n{MAGENTA}  Select option {WHITE}: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(0)

        if choice == "1":
            login_menu()
        elif choice == "2":
            buy_key()
        elif choice == "0":
            clear()
            print(f"\n{CYAN}  Thank you for using {APP_NAME}.{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}  [✗] Pilihan tidak tersedia.{RESET}")
            time.sleep(1)


def buy_key():
    clear()
    print_header()

    print(f"\n{YELLOW}  BUY KEY{RESET}\n")
    print(f"{WHITE}  Untuk mendapatkan username dan password,")
    print(f"  silakan hubungi owner melalui Telegram.{RESET}")
    print(f"\n{GRAY}  Owner : @{OWNER_TELEGRAM.lstrip('@')}{RESET}")

    try:
        choice = input(
            f"\n{CYAN}  Tekan ENTER untuk membuka Telegram"
            f"  atau ketik 0 untuk kembali: {RESET}"
        ).strip()
    except (KeyboardInterrupt, EOFError):
        return

    if choice == "0":
        return

    print(f"\n{GREEN}  [+] Membuka Telegram owner...{RESET}")

    if not open_telegram():
        print(f"{YELLOW}  [!] Telegram tidak dapat dibuka otomatis.{RESET}")
        print(f"{WHITE}  Silakan cari @{OWNER_TELEGRAM.lstrip('@')}{RESET}")

    time.sleep(2)


def api_login(username, password):
    payload = json.dumps({
        "username": username,
        "password": password,
    }).encode("utf-8")

    request = urllib.request.Request(
        AUTH_API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "LolyToolsLauncher/2.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=AUTH_TIMEOUT) as response:
            raw = response.read().decode("utf-8")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"success": False, "message": "Response server tidak valid."}

    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8"))
        except Exception:
            return {"success": False, "message": f"Server mengembalikan HTTP {e.code}."}

    except urllib.error.URLError:
        return {"success": False, "message": "Tidak dapat terhubung ke server autentikasi."}

    except TimeoutError:
        return {"success": False, "message": "Koneksi ke server timeout."}

    except Exception as e:
        return {"success": False, "message": f"Kesalahan koneksi: {e}"}


def login_menu():
    clear()
    print_header()

    print(f"\n{WHITE}{BOLD}  ┌─ SECURE LOGIN{RESET}")
    print(f"{CYAN}  │{RESET}  Masukkan akun yang diberikan owner.")
    print(f"{CYAN}  └{RESET}{line('─', min(max(terminal_width() - 8, 50), 65))}")

    try:
        username = input(f"\n{GREEN}  Username : {RESET}").strip()
        if not username:
            print(f"{RED}\n  [✗] Username tidak boleh kosong.{RESET}")
            time.sleep(1.5)
            return

        password = getpass.getpass(f"{GREEN}  Password : {RESET}").strip()
        if not password:
            print(f"{RED}\n  [✗] Password tidak boleh kosong.{RESET}")
            time.sleep(1.5)
            return
    except (KeyboardInterrupt, EOFError):
        print()
        return

    print(f"\n{CYAN}  [•] Menghubungi authentication server...{RESET}")
    result = api_login(username, password)

    if not result.get("success", False):
        print(f"\n{RED}  [✗] {result.get('message', 'Login gagal.')}{RESET}")
        pause()
        return

    user_data = result.get("user", {})
    display_username = user_data.get("username", username)
    expires = user_data.get("expires_at")

    print(f"\n{GREEN}  [✓] Login berhasil.{RESET}")
    print(f"{WHITE}  Welcome, {display_username}.{RESET}")

    if expires:
        print(f"{GRAY}  License : {expires}{RESET}")

    time.sleep(1)
    launch_main_tool()


def update_repository():
    print(f"\n{BLUE}  [+] Checking repository update...{RESET}")

    try:
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print(f"{GREEN}  [✓] Repository berhasil diperbarui.{RESET}")
            return True

        print(f"{YELLOW}  [!] Repository gagal diperbarui.{RESET}")
        if result.stderr:
            print(f"{GRAY}  {result.stderr.strip()}{RESET}")
        return False

    except FileNotFoundError:
        print(f"{RED}  [✗] Git tidak ditemukan.{RESET}")
        return False
    except subprocess.TimeoutExpired:
        print(f"{RED}  [✗] Git pull timeout.{RESET}")
        return False
    except Exception as e:
        print(f"{RED}  [✗] Error: {e}{RESET}")
        return False


def launch_main_tool():
    clear()
    print_header()

    print(f"\n{CYAN}  [+] Preparing tools...{RESET}")
    update_repository()

    print(f"\n{YELLOW}  [!] Tunggu sebentar...{RESET}")
    time.sleep(1)

    if not os.path.isfile(MAIN_TOOL):
        print(f"\n{RED}  [✗] File {MAIN_TOOL} tidak ditemukan.{RESET}")
        print(f"{GRAY}  Pastikan {MAIN_TOOL} berada di repository.{RESET}")
        pause()
        return

    print(f"\n{GREEN}  [✓] Starting {MAIN_TOOL}...{RESET}")
    time.sleep(.7)

    try:
        os.execv(sys.executable, [sys.executable, MAIN_TOOL])
    except Exception as e:
        print(f"\n{RED}  [✗] Gagal menjalankan tools: {e}{RESET}")
        pause()


if __name__ == "__main__":
    try:
        terminal_check()
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}  Program dihentikan.{RESET}\n")
    except Exception as e:
        print(f"\n{RED}  [✗] Fatal error: {e}{RESET}\n")

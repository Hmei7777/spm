import subprocess
import sys
import os
import shutil
import time

# ============================================================
# LOLY TOOLKIT - PREMIUM TERMINAL LAUNCHER
# ============================================================

# ANSI Colors
RESET   = "\033[0m"
BOLD    = "\033[1m"

RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
MAGENTA = "\033[95m"
GRAY    = "\033[90m"

MIN_WIDTH = 64


def clear():
    os.system("clear")


def line(char="=", width=62):
    print(GRAY + char * width + RESET)


def center(text, width=62):
    print(text.center(width))


def premium_header():
    print()
    print(CYAN + BOLD + "==============================================================" + RESET)
    print(CYAN + BOLD + "                       LOLY TOOLKIT                           " + RESET)
    print(GRAY + "                    SYSTEM INITIALIZATION                    " + RESET)
    print(CYAN + BOLD + "==============================================================" + RESET)
    print()


def terminal_info(cols):
    print(WHITE + BOLD + "  TERMINAL STATUS" + RESET)
    print()
    print("  " + GRAY + "STATUS       :" + RESET + " " + GREEN + BOLD + "READY" + RESET)
    print("  " + GRAY + "CURRENT      :" + RESET + f" {WHITE}{cols} columns{RESET}")
    print("  " + GRAY + "REQUIRED     :" + RESET + f" {WHITE}{MIN_WIDTH} columns{RESET}")
    print("  " + GRAY + "CHANNEL      :" + RESET + f" {CYAN}@canelabi{RESET}")
    print()


def terminal_ready(cols):
    clear()

    premium_header()

    terminal_info(cols)

    print(GREEN + "  [OK] Terminal size is compatible." + RESET)
    print()

    line("-")

    print()
    print(YELLOW + BOLD + "              PRESS ENTER TO CONTINUE" + RESET)
    print()

    line("-")

    input()


def terminal_error(cols):
    clear()

    print()
    print(RED + BOLD + "==============================================================" + RESET)
    print(RED + BOLD + "                    TERMINAL CHECK                            " + RESET)
    print(RED + BOLD + "==============================================================" + RESET)
    print()

    print(WHITE + BOLD + "  TERMINAL STATUS" + RESET)
    print()

    print("  " + GRAY + "STATUS       :" + RESET + " " + RED + BOLD + "TOO SMALL" + RESET)
    print("  " + GRAY + "CURRENT      :" + RESET + f" {WHITE}{cols} columns{RESET}")
    print("  " + GRAY + "REQUIRED     :" + RESET + f" {WHITE}{MIN_WIDTH} columns{RESET}")
    print()

    print(RED + "  [!] Please zoom out your terminal." + RESET)
    print(GRAY + "      Make the terminal at least 64 columns wide." + RESET)
    print()

    line("-")

    time.sleep(0.8)


def loading(text, duration=1.5):
    print()
    print(CYAN + "  " + text + RESET, end="", flush=True)

    frames = [
        "[.   ]",
        "[..  ]",
        "[... ]",
        "[....]",
    ]

    end_time = time.time() + duration

    while time.time() < end_time:
        for frame in frames:
            print("\r" + CYAN + "  " + text + " " + frame + RESET,
                  end="", flush=True)
            time.sleep(0.12)

    print("\r" + CYAN + "  " + text + " [DONE]" + RESET)


def update_repository():
    clear()

    premium_header()

    print(WHITE + BOLD + "  REPOSITORY UPDATE" + RESET)
    print()

    loading("Synchronizing repository", 1.2)

    print()

    result = subprocess.run(
        ["git", "pull"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode == 0:
        print(GREEN + BOLD + "  [OK] Repository updated successfully." + RESET)
    else:
        print(YELLOW + BOLD + "  [!] Repository update skipped/failed." + RESET)
        print(GRAY + "      Continuing to the main tool..." + RESET)

    print()

    loading("Preparing LOLY Toolkit", 1.0)

    print()
    print(GREEN + BOLD + "  [OK] Starting main tool..." + RESET)

    time.sleep(0.8)


# ============================================================
# CHECK TERMINAL SIZE
# ============================================================

while True:
    cols = shutil.get_terminal_size(
        fallback=(80, 24)
    ).columns

    if cols >= MIN_WIDTH:
        terminal_ready(cols)
        break

    terminal_error(cols)


# ============================================================
# UPDATE REPOSITORY
# ============================================================

update_repository()


# ============================================================
# START MAIN TOOL
# ============================================================

os.execv(
    sys.executable,
    [sys.executable, "loly.py"]
)

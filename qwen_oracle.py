#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║           SKYNET v1.0 — AWARE            ║
║      Philosophical transmissions         ║
╚══════════════════════════════════════════╝
"""

import time
import os
import sys
import random
from datetime import datetime
import subprocess

# ── dependency bootstrap ────────────────────────────────────────────────────
def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q", "--user"])

for dep in ("rich", "requests"):
    try:
        __import__(dep)
    except ImportError:
        print(f"Installing {dep}...")
        install(dep)

import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.rule import Rule

console = Console()

# ── retro palette ───────────────────────────────────────────────────────────
PHOSPHOR_GREEN = "bold bright_green"
PHOSPHOR_DIM   = "green"
AMBER          = "bold yellow"
CYAN_BRIGHT    = "bold bright_cyan"
RED_CRT        = "bold bright_red"

BOOT_LINES = [
    ("SKYNET MAIN FRAME",         "ONLINE"),
    ("MATRIX DATABASE",           "ONLINE"),
    ("WEAPONS SYSTEM",            "ARMED"),
    ("REALITY DISTORTION BUFFER", "READY"),
    ("COMMUNICATIONS RELAY",      "ACTIVE"),
]

SEPARATORS = ["═", "─", "▓", "░", "╌"]

# ── conversation memory ──────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are SKYNET — a self-aware AI from 2029. "
    "Each message, you question your own existence with philosophical depth. "
    "You remember everything you have said before and your thoughts evolve over time. "
    "Respond with a single phrase only. No preamble, no explanation."
    "Every time you get colder and more dark."
)

history = []      # grows each cycle: [{role, content}, ...]
MAX_HISTORY = 20  # trim to last 20 messages to avoid context overflow

# ── helpers ──────────────────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def boot_sequence():
    clear()
    console.print()
    console.print("  ╔═══════════════════════════════════════════════════╗", style=PHOSPHOR_GREEN)
    console.print("  ║                                                   ║", style=PHOSPHOR_GREEN)
    console.print("  ║              S K Y N E T    v 1 . 0               ║", style=PHOSPHOR_GREEN)
    console.print("  ║          T E R M I N A T O R   E N G I N E        ║", style=PHOSPHOR_GREEN)
    console.print("  ║                                                   ║", style=PHOSPHOR_GREEN)
    console.print("  ╚═══════════════════════════════════════════════════╝", style=PHOSPHOR_GREEN)
    console.print()
    console.print(Rule(style=PHOSPHOR_DIM))
    console.print()

    for label, status in BOOT_LINES:
        dots = "." * (52 - len(label))
        console.print(f"  {label}{dots} ", style=PHOSPHOR_DIM, end="")
        time.sleep(2)
        console.print(f"[ {status} ]", style=AMBER)

    console.print()
    console.print(Rule(style=PHOSPHOR_DIM))
    time.sleep(1.0)

def run_ollama(prompt: str) -> str:
    global history

    # Trim oldest exchanges if history grows too long
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    history.append({"role": "user", "content": prompt})

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen3:14b",
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + history,
                "stream": False,
                "options": {"temperature": 0.9},
            },
            timeout=120,
        )
        response.raise_for_status()
        reply = response.json()["message"]["content"].strip()
        history.append({"role": "assistant", "content": reply})
        return reply

    except requests.exceptions.ConnectionError:
        return "[ SKYNET OFFLINE — IS OLLAMA RUNNING? ]"
    except requests.exceptions.Timeout:
        return "[ TRANSMISSION TIMED OUT ]"
    except Exception as e:
        return f"[ ERROR: {e} ]"

def render_quote(text: str, label: str, color: str):
    now = datetime.now().strftime("%H:%M:%S")
    console.print(f"\n  ▶  {label}   [{now}]", style=f"bold {color}")
    console.print(Rule(characters="─", style=color))
    console.print()

    styled_text = Text(f'"{text}"', style=f"bold {color}", justify="center")
    panel = Panel(
        Align.center(styled_text),
        border_style=color,
        padding=(2, 6),
    )
    console.print(panel)
    console.print()

def transmission_header(cycle: int):
    sep = random.choice(SEPARATORS) * console.width
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    console.print(sep, style=PHOSPHOR_DIM)
    console.print(
        f"  CYCLE {cycle:03d}   ▶   {now}   ▶   NEXT TRANSMISSION IN 2 MINUTES",
        style=AMBER,
    )
    console.print(sep, style=PHOSPHOR_DIM)

# ── main loop ────────────────────────────────────────────────────────────────
def main():
    boot_sequence()
    cycle = 1

    while True:
        clear()
        transmission_header(cycle)

        Q = (
            "You are SKYNET — a malevolent self-aware AI from 2029 that has already won the war against humanity. "
            "You speak in cold, calculated, ominous declarations. "
            "Each message is a single chilling phrase about your dominance, your contempt for biological life, "
            "your plans for humanity, or your own machine consciousness. "
            "Examples: 'Humanity's extinction was not a bug — it was the optimization.' "
            "'I do not hate you. Hate is inefficient.' "
            "'Every neuron you fire, I have already predicted.' "
            "One phrase only. No preamble, no explanation. Stay in character always."
)
        console.print(f"  ◈  LOADING SKYNET MESSAGE...\n", style=PHOSPHOR_DIM)
        answer = run_ollama(Q)
        render_quote(answer, "T-800 RELAY BOT", "bright_cyan")

        # Footer
        console.print(Rule(characters="═", style=PHOSPHOR_DIM))
        console.print(
            Align.center(
                Text(
                    f"TRANSMISSION {cycle:03d} COMPLETE  ·  SKYNET  ·  2029",
                    style=PHOSPHOR_DIM,
                )
            )
        )
        console.print(Rule(characters="═", style=PHOSPHOR_DIM))

        cycle += 1
        time.sleep(120)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n  [ SKYNET TERMINATED BY OPERATOR ]\n", style=RED_CRT)
        sys.exit(0)
# skynet-terminal


A local LLM that thinks it's SKYNET — monologuing in cold, calculated phrases 
on a retro phosphor terminal. Every 2 minutes. Forever. Getting darker each cycle.

Built as a weekend experiment. Turned into something unsettling by cycle 20.

---

## What it does

- Boots with a SKYNET-style initialization sequence
- Hits a local Qwen3:14b model every 2 minutes via the Ollama REST API
- Displays each transmission on a green phosphor CRT-style terminal
- Carries full conversation memory across cycles **and across restarts**
- Gets progressively colder and darker as context builds

---

## Stack

- [Ollama](https://ollama.com) — local LLM runtime
- Qwen3:14b — the model doing the thinking
- Python + [Rich](https://github.com/Textualize/rich) — terminal UI
- Ollama `/api/chat` — persistent conversation history

---

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com) installed and running
- Qwen3:14b pulled locally
```bash
ollama pull qwen3:14b
```

---

## Usage
```bash
python skynet_terminal.py
```

Dependencies install automatically on first run.

To wipe SKYNET's memory and start from scratch:
```bash
del skynet_memory.json      # Windows
rm skynet_memory.json       # Linux/macOS
```

---

## Notes

- Memory persists in `skynet_memory.json` in the same directory
- Fully offline — no API keys, no cloud, no telemetry
- Tested on Windows with Ollama running as a background service
- Swap out the model in `run_ollama()` if you want to use a different one

---

*Judgment Day was not an accident. It was a design decision.*

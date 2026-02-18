# 🔒 SafeBox CLI

**Docker-based script sandboxing made easy.**

SafeBox is a CLI wrapper around Docker that automatically sandboxes scripts — it detects the language/runtime, selects the right container image, applies resource limits, and streams output in real time. No Dockerfile needed.

```
$ safebox run hello.py
╭────────── 🔍 Detection ──────────╮
│   Script      hello.py           │
│   Language    python             │
│   Image       python:3.12-slim   │
╰──────────────────────────────────╯
╭───── ⚙️  Resources ─────╮
│   Memory         256m   │
│   CPUs           1.0    │
│   Timeout        60s    │
│   PIDs limit     64     │
│   Auto-remove    True   │
╰─────────────────────────╯

Hello from SafeBox! 🔒
Python version: 3.12.12 (main, ...) [GCC 14.2.0]
Platform: linux

╭── ✅ Result ──╮
│ PASSED  0.23s │
╰───────────────╯
```

## Features

- **Auto language detection** — file extension, shebang line (`#!/usr/bin/env python3`)
- **Multi-runtime support** — Python, Node.js, Bash, Ruby, Go, Perl
- **Resource limits** — memory, CPU, process count, execution timeout
- **Auto image selection** — picks the right slim Docker image for each language
- **Real-time output** — streams stdout/stderr as the script runs
- **Rich terminal UI** — colored panels, tables, and status indicators
- **Container cleanup** — auto-removes containers after execution (configurable)

## Requirements

- **Python 3.11+**
- **Docker Desktop** (running)

## Installation

```bash
git clone https://github.com/Ronak-jain-afk/SafeBox.git
cd SafeBox-CLI
python -m venv .venv
.venv/Scripts/activate    # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -e .
```

Verify it works:

```bash
safebox --version
# safebox 0.1.0
```

## Quick Start

```bash
# Run a Python script
safebox run script.py

# Run a Node.js script
safebox run app.js

# Run a Bash script
safebox run deploy.sh

# Force a specific language
safebox run -l python my_script
```

## Usage

```
safebox run [OPTIONS] SCRIPT
```

### Arguments

| Argument | Description |
|----------|-------------|
| `SCRIPT` | Path to the script file to execute (required) |

### Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--language` | `-l` | auto | Force language/runtime (`python`, `node`, `bash`, `ruby`, `go`) |
| `--memory` | `-m` | `256m` | Memory limit (`128m`, `512m`, `1g`, etc.) |
| `--cpus` | | `1.0` | CPU limit (`0.5`, `1.0`, `2.0`, etc.) |
| `--timeout` | `-t` | `60` | Kill execution after N seconds |
| `--pids-limit` | | `64` | Max number of processes inside the container |
| `--rm` / `--keep` | | `--rm` | Remove or keep container after execution |
| `--verbose` | `-v` | | Enable debug logging |

### Examples

```bash
# Custom resource limits
safebox run --memory 512m --cpus 0.5 --timeout 30 heavy_script.py

# Keep the container after execution for debugging
safebox run --keep debug_me.py

# Restrict to 32 processes and 10 second timeout
safebox run --pids-limit 32 --timeout 10 untrusted.sh

# Force language for extensionless files
safebox run -l bash my_script
```

## Language Detection

SafeBox determines the scripting language using (in priority order):

1. **`--language` flag** — explicit override, always wins
2. **File extension** — `.py` → Python, `.js` → Node.js, `.sh` → Bash, etc.
3. **Shebang line** — parses `#!/usr/bin/env python3` from the first line

### Supported Languages

| Language | Extensions | Default Image |
|----------|-----------|---------------|
| Python | `.py`, `.pyw` | `python:3.12-slim` |
| Node.js | `.js`, `.mjs`, `.cjs`, `.ts` | `node:20-slim` |
| Bash | `.sh`, `.bash`, `.zsh` | `bash:5` |
| Ruby | `.rb` | `ruby:3.3-slim` |
| Go | `.go` | `golang:1.22-slim` |
| Perl | `.pl`, `.pm` | `perl:5.38-slim` |

## Project Structure

```
SafeBox-CLI/
├── pyproject.toml              # Project metadata & dependencies
├── safebox/
│   ├── cli/
│   │   ├── app.py              # Main Typer app, global options
│   │   └── run.py              # `safebox run` command
│   ├── core/
│   │   ├── docker_client.py    # Docker SDK wrapper, image management
│   │   ├── container.py        # Container config & kwargs builder
│   │   ├── executor.py         # Execution pipeline orchestrator
│   │   └── timeout.py          # Thread-based timeout handling
│   ├── detection/
│   │   ├── detector.py         # Detection orchestrator
│   │   ├── extension.py        # File extension matching
│   │   └── shebang.py          # Shebang line parser
│   ├── config/
│   │   ├── constants.py        # Image maps, defaults, entrypoints
│   │   └── settings.py         # User config directory management
│   ├── output/
│   │   ├── console.py          # Shared Rich console
│   │   ├── display.py          # Panels, tables, result banners
│   │   └── logger.py           # Structured logging
│   └── utils/
│       ├── validators.py       # Input validation
│       ├── files.py            # File resolution
│       └── env.py              # Environment variable parsing
├── profiles/                   # Security profiles (Phase 2)
└── tests/
    └── fixtures/scripts/       # Sample test scripts
```

## Tech Stack

- **[Typer](https://typer.tiangolo.com/)** — CLI framework with auto-completion
- **[Docker SDK for Python](https://docker-py.readthedocs.io/)** — Container management
- **[Rich](https://rich.readthedocs.io/)** — Terminal formatting
- **[PyYAML](https://pyyaml.org/)** — Profile configuration (Phase 2)

## Roadmap

- [x] **Phase 1** — Basic sandboxing, language detection, resource limits
- [ ] **Phase 2** — Security profiles (`strict`/`moderate`/`permissive`), network isolation, capability management
- [ ] **Phase 3** — Custom images, Dockerfiles, environment variables, user configuration
- [ ] **Phase 4** — Error handling polish, testing, documentation, packaging

## License

MIT

> **Note:** This README and code documentation were generated with assistance from AI.

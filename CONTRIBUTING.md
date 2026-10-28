# Contributing to Portable AI Team

Thanks for your interest in contributing! This document explains how to set up
a development environment and submit changes.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Portable-AI-Team.git
   cd Portable-AI-Team
   ```
2. Copy `LLM配置.example.json` to `LLM配置.json` and fill in your API details.
   This file is git-ignored and will never be committed.
3. Copy `Python路径.txt.example` to `Python路径.txt` and set it to the absolute path of your Python 3 executable.
4. Run tests:
   ```bash
   python -m unittest discover -s tests -v
   ```

## Project Structure

```text
Portable-AI-Team/
├── AI-Team/              # Framework: agents, adapters, bridges, policies, tools
│   ├── agents/           # AgentA (orchestrator), AgentB (impl), AgentC (design), AgentD (impl)
│   ├── adapters/         # IDE-specific configs (Codex, Antigravity, TraeCode)
│   ├── bridges/          # Bridge templates for IDE discovery
│   ├── policies/         # Token budget, mode policies
│   ├── templates/        # Work order, delivery, defect templates
│   ├── workflows/        # Low-Token V2 workflow definitions
│   ├── ide-guides/       # Platform compatibility guides
│   ├── capsule.py        # Enable / carry / merge / validate CLI
│   ├── team.py           # Legacy init / install / uninstall CLI
│   ├── llm_dispatch.py   # External LLM dispatch with fallback
│   └── check_compatibility.py  # Compatibility check + dist builder
├── tests/                # Offline unit tests (no network, no real keys)
├── LLM配置.example.json  # Template for LLM configuration
└── README.md
```

## Coding Guidelines

- Python 3.10+; stdlib only (no third-party dependencies).
- All tests must run offline (stub external APIs).
- Never hardcode API keys, passwords, or internal IPs in source code.
- Memory files under `AI-Team/memory/` (except `index.md`) are user-specific
  and git-ignored; do not commit your personal experience data.
- UI design kit files starting with `RZNY-` or `shopeers-` are project-specific
  and git-ignored; only generic framework files are tracked.

## Submitting Changes

1. Fork the repository and create a feature branch from `main`.
2. Make your changes with clear commit messages.
3. Ensure all tests pass: `python -m unittest discover -s tests -v`.
4. If you modified the dist build, run: `python AI-Team/check_compatibility.py --build`.
5. Submit a pull request with a description of what changed and why.

## Reporting Issues

Use [GitHub Issues](https://github.com/YOUR_USERNAME/Portable-AI-Team/issues).
Please include:

- Your OS and Python version
- Which IDE adapter you are using (Codex / Antigravity / TraeCode)
- Steps to reproduce
- Expected vs actual behavior

Never paste API keys, database passwords, or internal network addresses in
issues or pull requests.

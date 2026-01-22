# Claude Toolkit

A marketplace of practical skills for programmers who want to extend Claude Code with real, local workflows.

## Purpose
Provide reusable skills you can install individually and adapt for your own setup: Obsidian knowledge work, Dayflow time analysis, and macOS system control. Each skill is short, task‑focused, and designed to be easy to extend.

## Installation

### 1. Add the Marketplace
First, add this repository as a marketplace in your Claude Code terminal:

```bash
/plugin marketplace add https://github.com/wilbeibi/claude-toolkit
```

### 2. Install Individual Tools
Once the marketplace is added, you can install specific tools using their names:

```bash
# Install Obsidian integration
/plugin install obsidian@wilbeibi-toolkit

# Install Dayflow review tools
/plugin install dayflow@wilbeibi-toolkit

# Install macOS system tools
/plugin install m-cli@wilbeibi-toolkit
```

## Available Tools

*   **obsidian**: Read and search your local Obsidian vault (API used for advanced filtering and automation; write paths only on explicit request).
*   **dayflow**: Query and analyze your Dayflow time-tracking database. Generates productivity summaries and timeline reports.
*   **m-cli**: Control macOS system settings (Dark Mode, WiFi, Battery, Dock) directly from the terminal.


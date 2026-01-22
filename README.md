# Claude Toolkit

A collection of workspace automation tools for [Claude Code](https://code.claude.com). This repository acts as a marketplace, allowing you to install specific tools independently.

## Purpose
This toolkit extends Claude Code with workflows for knowledge management and local automation. It enables the AI agent to interact with local applications like Obsidian and Dayflow, and manage macOS system settings.

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

*   **obsidian**: Interact with your local Obsidian vault. Supports creating, reading, updating, and searching notes via the Local REST API plugin.
*   **dayflow**: Query and analyze your Dayflow time-tracking database. Generates productivity summaries and timeline reports.
*   **m-cli**: Control macOS system settings (Dark Mode, WiFi, Battery, Dock) directly from the terminal.

## Structure
*   `.claude-plugin/`: Marketplace registration and metadata.
*   `plugins/`: Individual tool packages, each containing its own `plugin.json` and `skills/`.

## Contributing
1.  Fork this repository.
2.  Add a new tool directory in `plugins/`.
3.  Register the new tool in `.claude-plugin/marketplace.json`.
4.  Submit a Pull Request.

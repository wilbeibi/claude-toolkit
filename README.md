# Claude Toolkit

A collection of skills and commands for [Claude Code](https://code.claude.com).

## Purpose
This plugin extends Claude Code with specific workflows, primarily focused on knowledge management and automation. It allows the AI agent to interact with local tools like Obsidian through structured commands and natural language.

## Installation
Run the following command in your Claude Code terminal:

```bash
/plugin install https://github.com/wilbeibi/claude-toolkit
```

## Contents

### Skills
Instruction sets that teach Claude how to perform specific tasks.
*   **Obsidian REST API**: Enables interaction with your local Obsidian vault. Supports creating, reading, updating, and searching notes using the Local REST API plugin.

### Commands
Automated workflows triggered by slash commands.
*   `/toolkit-help`: Lists all available tools and commands in this package.

## Structure
*   `commands/`: Definitions for slash commands.
*   `skills/`: Markdown files containing skill instructions.
*   `plugin.json`: Manifest file for plugin registration.

## Contributing
1.  Fork this repository.
2.  Add new skill files to `skills/` or commands to `commands/`.
3.  Submit a Pull Request.

---
name: m-cli
description: Swiss Army Knife for macOS. Use when managing macOS settings such as dark mode, dock, wifi, battery, display, volume, or system info from the terminal.
allowed-tools:
  - Bash
---

# m-cli

## Summary
Use the `m` command to manage macOS settings from the terminal.

## Details
Install:
```bash
brew install m-cli
```

Basic usage:
```bash
m
m <command> --help
```

## Reference
Common commands:
- Appearance: `m appearance dark|light|auto`
- Display: `m display status`, `m display brightness 50`
- WiFi: `m wifi status|on|off|scan`
- Dock: `m dock autohide YES`, `m dock position bottom`
- Volume: `m volume 50`, `m volume mute|unmute`
- Battery: `m battery status`, `m battery percentage`
- System: `m sleep`, `m lock`, `m restart`, `m shutdown`

Notes:
- Some commands require `sudo`.
- `m trash` needs Full Disk Access.

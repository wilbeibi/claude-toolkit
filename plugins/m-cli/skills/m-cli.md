---
name: m-cli
description: Swiss Army Knife for macOS - control system functions, manage utilities, and tweak macOS preferences from the command line. Use when user needs to manage macOS settings like dark mode, dock, wifi, battery, display, volume, or any other system preference via CLI.
allowed-tools:
  - Bash
---

# m-cli: macOS Command Line Tool

## Overview
m-cli is a powerful command-line tool for macOS that enables you to control system functions, manage utilities, and tweak preferences – all from the Terminal. It provides 48+ commands for system management.

## Installation
If m-cli is not installed, guide the user to install it:
```bash
brew install m-cli
```

## Basic Usage

**Display all commands:**
```bash
m
```

**Get help for specific commands:**
```bash
m <command> --help
```

## Available Commands

### Appearance & Display
- `m appearance` - Control dark/light mode
  - `m appearance dark` - Enable dark mode
  - `m appearance light` - Enable light mode
  - `m appearance auto` - Set automatic mode
- `m display` - Manage display settings
- `m screensaver` - Control screensaver
- `m wallpaper` - Set desktop wallpaper
- `m touchbar` - Configure Touch Bar settings

### System Control
- `m restart` - Restart the system
- `m shutdown` - Shutdown the system
- `m sleep` - Put system to sleep
- `m lock` - Lock the screen
- `m safeboot` - Manage safe boot mode
- `m update` - System software updates

### Hardware & Power
- `m battery` - Battery information and settings
- `m volume` - Control system volume
- `m audio` - Audio device management
- `m fan` - Fan control and monitoring
- `m powermode` - Power mode settings
- `m nosleep` - Prevent system sleep

### Network & Connectivity
- `m wifi` - WiFi management
- `m bluetooth` - Bluetooth control
- `m vpn` - VPN management
- `m network` - Network settings
- `m dns` - DNS configuration
- `m hosts` - Hosts file management
- `m firewall` - Firewall settings
- `m flightmode` - Airplane mode toggle
- `m airdrop` - AirDrop settings

### UI & Desktop
- `m dock` - Dock preferences
- `m finder` - Finder settings
- `m notification` - Notification Center management

### Storage & Files
- `m disk` - Disk management
- `m dir` - Directory information
- `m trash` - Trash management (requires Full Disk Access)
- `m usb` - USB device management

### User & Security
- `m user` - User account management
- `m group` - Group management
- `m gatekeeper` - Gatekeeper settings
- `m printer` - Printer management

### System Information
- `m info` - System information
- `m hostname` - Hostname management
- `m timezone` - Timezone settings
- `m ntp` - NTP (time) settings
- `m service` - System services

### Applications
- `m itunes` - iTunes control

## Common Use Cases

### Dark Mode Toggle
```bash
m appearance dark    # Enable dark mode
m appearance light   # Disable dark mode
m appearance auto    # Auto mode
```

### WiFi Management
```bash
m wifi status        # Check WiFi status
m wifi on            # Turn WiFi on
m wifi off           # Turn WiFi off
m wifi scan          # Scan for networks
```

### Dock Customization
```bash
m dock autohide YES  # Enable auto-hide
m dock position bottom  # Set position
```

### Volume Control
```bash
m volume 50          # Set volume to 50%
m volume mute        # Mute
m volume unmute      # Unmute
```

### Battery Info
```bash
m battery status     # Battery status
m battery percentage # Battery percentage
```

### Display Settings
```bash
m display status     # Display information
m display brightness 50  # Set brightness
```

## Important Notes

1. **Permissions**: Some commands require `sudo` privileges. Prompt the user to run with sudo if needed.
2. **Full Disk Access**: The `trash` command needs "Full Disk Access" permissions in System Preferences for terminal applications.
3. **Help System**: Always use `m <command> --help` to see detailed options for each command.

## Examples

**Example 1: Toggle dark mode**
```bash
m appearance dark
```

**Example 2: Configure Dock**
```bash
m dock autohide YES
m dock position left
m dock magnification YES
```

**Example 3: WiFi troubleshooting**
```bash
m wifi status
m wifi off
m wifi on
```

**Example 4: System information**
```bash
m info
m battery status
m disk list
```

## When to Use This Skill

Use this skill when the user mentions:
- macOS system settings or preferences
- Dark mode, appearance, or display settings
- WiFi, network, or connectivity
- Dock, Finder, or desktop customization
- Battery, volume, or hardware settings
- System management tasks on macOS

Always prefer m-cli over manual osascript or system preferences manipulation when the command is available, as it provides a cleaner and more reliable interface.

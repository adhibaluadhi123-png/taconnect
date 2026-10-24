# Parallel SSH Manager

A modern, cross-platform GUI application for managing multiple SSH connections simultaneously. This tool provides an easy-to-use interface for executing commands on multiple servers in parallel, making server administration tasks more efficient.

## Features

### Core Capabilities
- **Cross-Platform Server Support**: Execute commands on both Linux and Windows servers
- **Automatic OS Detection**: Automatically detects OS type (Linux, Windows, macOS) and shell type (bash, zsh, PowerShell, cmd)
- **Parallel Execution**: Run commands on multiple servers simultaneously
- **Dual Authentication**: Support for both password and SSH key-based authentication
- **Real-time Output**: Live command output display with color-coded status indicators
- **Command Templates**: Pre-built templates for common Windows and Linux commands

### User Interface
- **Tabbed Interface**: Organize servers into different groups/environments
- **Server Information Display**: See OS and shell type for each connected server
- **Quick Templates**: Dropdown menu with ready-to-use commands for both platforms
- **Monospace Output**: Clear, readable command output in terminal-style font
- **Multi-Selection**: Execute commands on one or many servers at once

### Platform Support
- **Client**: Runs on Windows, macOS, and Linux
- **Servers**: Connect to Linux, Windows (with OpenSSH), and macOS servers

### Modern UI (v2.0)
- 🎨 **Beautiful Dark Theme**: Catppuccin-inspired color scheme
- 🎯 **Simplified Server Addition**: Just IP, username, and password
- ✨ **Visual Feedback**: Color-coded buttons, hover effects, status indicators
- 🖥️ **Polished Interface**: Rounded corners, smooth transitions, emoji icons
- 📱 **Responsive Design**: Resizable panels, larger touch targets

## Installation

1. Make sure you have Python 3.8 or later installed.
2. Clone this repository:
   ```bash
   git clone <repository-url>
   cd parallel-ssh-manager
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start

1. **Run the application:**
   ```bash
   source venv/bin/activate  # Activate virtual environment
   python main.py
   ```

2. **Add a server (Super Simple!):**
   - Click "➕ Add Server" button
   - Enter just 3 things:
     - **IP Address** (e.g., 192.168.1.100)
     - **Username** (e.g., admin)
     - **Password**
   - Click "✓ Connect"
   - The app automatically detects OS and shell type!

3. **Execute commands:**
   - Select one or more servers from the list
   - Choose a template from the dropdown OR type a custom command
   - Click "Execute on Selected" or press Enter
   - View results in the output area

### Command Templates

The application includes ready-to-use templates for:
- **Linux**: System info, disk usage, processes, network, packages
- **Windows**: System info, tasks, network config, services
- **PowerShell**: Advanced Windows management commands

### Setting up Windows Servers

To enable SSH on Windows Server:
```powershell
# Install OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start and enable SSH service
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# Configure firewall
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

### Example Use Cases

**Health Check Across All Servers:**
1. Select all servers
2. Use template "Linux: Disk Usage" → `df -h`
3. Check memory with "Linux: Memory Info" → `free -h`

**Windows Server Management:**
1. Select Windows servers
2. Use "PowerShell: Services" → `Get-Service`
3. Or "Windows: Running Processes" → `tasklist`

**Mixed Environment:**
- The app automatically adjusts command execution based on detected OS
- Select servers of the same type for OS-specific commands

## Documentation

- **[VISUAL_GUIDE.md](VISUAL_GUIDE.md)**: Complete visual guide showing the new modern UI
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)**: Comprehensive guide with examples and best practices
- **[QUICK_START.md](QUICK_START.md)**: Get started in 2 minutes

## Keyboard Shortcuts

- **Enter**: Execute command (when in command input field)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
give a pargraph about the features
The Server Connection History feature maintains a detailed log of previous SSH sessions, including server IP addresses, connection timestamps, executed commands, execution status, and error messages. It allows users to review past activities, troubleshoot connection issues, track command execution, and export logs for auditing. This feature improves transparency, simplifies debugging, and makes managing multiple servers more efficient and secure

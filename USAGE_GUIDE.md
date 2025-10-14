# Parallel SSH Manager - Usage Guide

## Overview
This application allows you to execute commands on multiple servers (both Windows and Linux) simultaneously via SSH.

## Features

### 1. **Cross-Platform Support**
- **Linux Servers**: Full support for all Linux distributions (Ubuntu, CentOS, Debian, etc.)
- **Windows Servers**: Support for Windows Server with SSH enabled
- **macOS Servers**: Full support for macOS systems

### 2. **Automatic OS Detection**
When you connect to a server, the application automatically detects:
- Operating System (Linux, Windows, macOS)
- Shell Type (bash, zsh, sh, PowerShell, cmd)

### 3. **Command Templates**
Quick access to common commands for both Windows and Linux:

#### Linux Templates:
- `ls -la` - List files with details
- `df -h` - Disk usage
- `free -h` - Memory information
- `lscpu` - CPU information
- `ps aux` - Running processes
- `uptime` - System uptime
- `ip addr show` - Network interfaces

#### Windows Templates:
- `dir` - List files
- `systeminfo` - System information
- `tasklist` - Running processes
- `ipconfig /all` - Network configuration
- `wmic product get name,version` - Installed programs

#### PowerShell Templates:
- `Get-ComputerInfo` - Detailed system information
- `Get-Process` - Process list
- `Get-Service` - Service status
- `Get-NetAdapter` - Network adapters

## Setting Up SSH on Different Platforms

### Linux/macOS
SSH is typically pre-installed. Just ensure the SSH daemon is running:
```bash
sudo systemctl start sshd
sudo systemctl enable sshd
```

### Windows
1. Install OpenSSH Server:
   - Go to Settings > Apps > Optional Features
   - Add "OpenSSH Server"
   
2. Start the service:
   ```powershell
   Start-Service sshd
   Set-Service -Name sshd -StartupType 'Automatic'
   ```

3. Configure firewall:
   ```powershell
   New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
   ```

## Authentication Methods

### Password Authentication
Simply enter your username and password when adding a server.

### SSH Key Authentication
1. Generate an SSH key pair (if you don't have one):
   ```bash
   ssh-keygen -t rsa -b 4096
   ```

2. Copy your public key to the remote server:
   - **Linux/macOS**: 
     ```bash
     ssh-copy-id user@hostname
     ```
   - **Windows**: 
     Add your public key to `C:\Users\username\.ssh\authorized_keys`

3. In the application, browse and select your private key file

## Usage Examples

### Example 1: Check Disk Space on Multiple Linux Servers
1. Connect to your Linux servers
2. Select all servers from the list
3. Choose "Linux: Disk Usage" from templates or enter: `df -h`
4. Click "Execute on Selected"

### Example 2: Check Running Services on Windows Servers
1. Connect to your Windows servers
2. Select the Windows servers
3. Choose "PowerShell: Services" or enter: `Get-Service`
4. Click "Execute on Selected"

### Example 3: Mixed Environment - Update All Servers
For Linux servers:
```bash
sudo apt update && sudo apt upgrade -y  # Debian/Ubuntu
sudo yum update -y                      # CentOS/RHEL
```

For Windows servers:
```powershell
Get-WindowsUpdate -Install -AcceptAll
```

## Tips and Best Practices

### 1. Server Organization
- Use tabs to organize servers by environment (Dev, Staging, Production)
- Group servers by function (Web servers, Database servers, etc.)

### 2. Command Execution
- Test commands on a single server before running on all
- Use the Clear Output button to keep the output area clean
- Commands execute in parallel for faster results

### 3. Security
- Use SSH key authentication instead of passwords when possible
- Ensure your private keys have proper permissions (chmod 600)
- Use strong passwords if password authentication is required

### 4. Troubleshooting

#### Connection Issues
- Verify SSH service is running on the remote server
- Check firewall rules allow SSH (port 22)
- Verify credentials are correct
- For Windows, ensure OpenSSH Server is installed and running

#### Command Execution Issues
- Check that the command is appropriate for the OS type
- Verify you have necessary permissions (may need sudo/administrator)
- Check the exit code in the output for debugging

#### Character Encoding Issues
- The application automatically handles UTF-8 and Latin-1 encoding
- If you see garbled text, try adjusting your server's locale settings

## Advanced Features

### Dynamic Server Lists
You can add servers on-the-fly without restarting the application.

### Multi-Tab Support
- Create separate tabs for different server groups
- Each tab maintains its own set of connections
- Useful for managing multiple environments

### Timeout Configuration
Commands have a default 30-second timeout, preventing hung connections.

## Keyboard Shortcuts
- **Enter**: Execute command (when focus is on command input)
- **Ctrl+A**: Select all text in output area

## Common Use Cases

### 1. System Monitoring
Execute monitoring commands across all servers:
- Check disk space
- Monitor memory usage
- View running processes
- Check system load

### 2. Configuration Management
- Deploy configuration files
- Update application settings
- Restart services
- Verify configurations

### 3. Log Analysis
- Tail log files
- Search for errors
- Analyze patterns across multiple servers

### 4. Software Deployment
- Update applications
- Install packages
- Restart services
- Verify installations

## Example Workflows

### Daily Health Check
1. Select all production servers
2. Run: `df -h` (check disk space)
3. Run: `free -h` (check memory)
4. Run: `uptime` (check load and uptime)

### Emergency Response
1. Connect to all affected servers
2. Check logs: `tail -100 /var/log/syslog`
3. Check processes: `ps aux | grep [service]`
4. Restart service if needed: `systemctl restart [service]`

### Patch Management
1. Select servers by group
2. For Linux: `sudo apt update && sudo apt upgrade -y`
3. For Windows: Use Windows Update PowerShell commands
4. Verify updates were applied

## Support and Contributions
For issues, feature requests, or contributions, please refer to the project repository.

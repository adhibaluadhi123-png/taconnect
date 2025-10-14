# Quick Start Guide

## Installation (One-Time Setup)

```bash
cd /home/alfy/pssh/CascadeProjects/windsurf-project

# Create virtual environment (already done)
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (already done)
pip install -r requirements.txt
```

## Running the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py
```

## First Steps

### 1. Add a Server
- Click **"Add Server"** button
- Fill in:
  - **Hostname**: IP or domain (e.g., 192.168.1.100)
  - **Username**: SSH username
  - **Password**: OR SSH key file path
  - **Port**: Default is 22
- Click **OK**
- App will auto-detect OS and shell type

### 2. Execute Your First Command

**Option A - Use Template:**
1. Select server(s) from list
2. Choose from **"Quick Templates"** dropdown
3. Click **"Execute on Selected"**

**Option B - Custom Command:**
1. Select server(s) from list
2. Type command in input field
3. Press **Enter** or click **"Execute on Selected"**

### 3. View Results
- Output appears in the text area below
- Each server's results are clearly separated
- ✓ = Success, ✗ = Error

## Common Commands

### Linux Servers
```bash
df -h              # Disk space
free -h            # Memory usage
ps aux             # Running processes
uptime             # System uptime
ls -la             # List files
```

### Windows Servers
```cmd
dir                           # List files
systeminfo                    # System info
tasklist                      # Running processes
ipconfig /all                 # Network info
```

### PowerShell (Windows)
```powershell
Get-Service                   # Services
Get-Process                   # Processes
Get-ComputerInfo             # System info
```

## Tips

- **Multi-Select**: Hold Ctrl/Cmd and click to select multiple servers
- **Clear Output**: Use "Clear Output" button to clean the view
- **Test First**: Try command on one server before executing on all
- **Templates**: Use templates as starting points, then modify
- **Tabs**: Create new tabs to organize servers by environment

## Troubleshooting

### Can't Connect to Server
```bash
# Check if SSH is running on remote server
ssh user@hostname -p 22

# For Windows servers, ensure OpenSSH is installed
# Run on Windows server:
Get-Service sshd
```

### Command Not Working
- Verify command is appropriate for the OS type
- Check you have necessary permissions
- Look at the exit code in output for clues

### Application Won't Start
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Verify dependencies are installed
pip list | grep -i pyqt6

# Reinstall if needed
pip install -r requirements.txt
```

## File Reference

| File | Purpose |
|------|---------|
| `main.py` | Application source code |
| `README.md` | Project overview |
| `USAGE_GUIDE.md` | Comprehensive manual |
| `FEATURES.md` | Feature list & roadmap |
| `PROJECT_SUMMARY.md` | Technical details |
| `config.example.json` | Configuration template |
| `requirements.txt` | Python dependencies |

## Next Steps

1. ✅ Application is installed and ready
2. 📚 Read USAGE_GUIDE.md for detailed examples
3. 🔧 Add your servers and test
4. 💡 Explore command templates
5. 📊 Check FEATURES.md for future enhancements

## Support

- Review documentation files for help
- Check source code comments in main.py
- Verify SSH service is running on target servers
- Ensure network connectivity to servers

---

**Current Status**: ✅ Application Ready  
**Version**: 1.0.0  
**Last Updated**: October 2025

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QListWidget, QTextEdit, QLineEdit,
                             QLabel, QSplitter, QComboBox, QFormLayout, QGroupBox,
                             QMessageBox, QFileDialog, QDialog, QCheckBox, QSpinBox,
                             QListWidgetItem, QSplashScreen)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QThreadPool, QRunnable, pyqtSlot, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QLinearGradient
import paramiko
from typing import List, Dict, Optional, Tuple
import json
import os
import time
import re
from pathlib import Path
from enum import Enum

class OSType(Enum):
    LINUX = "Linux"
    WINDOWS = "Windows"
    MACOS = "macOS"
    UNKNOWN = "Unknown"


class ShellType(Enum):
    BASH = "bash"
    ZSH = "zsh"
    SH = "sh"
    POWERSHELL = "powershell"
    CMD = "cmd"
    UNKNOWN = "unknown"


class TaconnectSplashScreen(QSplashScreen):
    def __init__(self):
        # Create a pixmap for the splash screen
        pixmap = QPixmap(600, 400)
        
        # Paint the splash screen on the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create gradient background
        gradient = QLinearGradient(0, 0, 600, 400)
        gradient.setColorAt(0, QColor("#007AFF"))  # Apple blue
        gradient.setColorAt(1, QColor("#5AC8FA"))  # Light blue
        painter.fillRect(0, 0, 600, 400, gradient)
        
        # Draw app name
        painter.setPen(QColor("#FFFFFF"))
        font = QFont("Arial", 48, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(0, 0, 600, 300, Qt.AlignmentFlag.AlignCenter, "TACONNECT")
        
        # Draw tagline
        font = QFont("Arial", 14)
        painter.setFont(font)
        painter.drawText(0, 250, 600, 100, Qt.AlignmentFlag.AlignCenter, 
                        "Parallel SSH Management Suite")
        
        # Draw version
        font = QFont("Arial", 11)
        painter.setFont(font)
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(0, 350, 600, 40, Qt.AlignmentFlag.AlignCenter, "Version 2.0")
        
        painter.end()
        
        # Initialize splash screen with the painted pixmap
        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)


class SSHSession:
    def __init__(self, hostname: str, username: str, password: str = None, key_filename: str = None, port: int = 22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.client = None
        self.sftp = None
        self.os_type = OSType.UNKNOWN
        self.shell_type = ShellType.UNKNOWN
        self.is_connected = False
    
    def connect(self) -> bool:
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if self.key_filename:
                self.client.connect(
                    self.hostname,
                    port=self.port,
                    username=self.username,
                    key_filename=self.key_filename,
                    timeout=10
                )
            else:
                self.client.connect(
                    self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=10
                )
            
            self.is_connected = True
            # Detect OS and shell type after successful connection
            self.detect_os()
            self.detect_shell()
            return True
        except Exception as e:
            print(f"Error connecting to {self.hostname}: {str(e)}")
            self.is_connected = False
            return False
    
    def detect_os(self) -> OSType:
        """Detect the operating system of the remote server"""
        if not self.client:
            return OSType.UNKNOWN
        
        try:
            # Try uname first (works on Linux/Unix/macOS)
            stdin, stdout, stderr = self.client.exec_command("uname -s")
            output = stdout.read().decode().strip().lower()
            
            if "linux" in output:
                self.os_type = OSType.LINUX
            elif "darwin" in output:
                self.os_type = OSType.MACOS
            else:
                # Try Windows detection
                stdin, stdout, stderr = self.client.exec_command("ver")
                output = stdout.read().decode().strip().lower()
                if "windows" in output or "microsoft" in output:
                    self.os_type = OSType.WINDOWS
                else:
                    # Try PowerShell detection
                    stdin, stdout, stderr = self.client.exec_command("$PSVersionTable.PSVersion")
                    output = stdout.read().decode().strip()
                    if output:
                        self.os_type = OSType.WINDOWS
        except:
            pass
        
        return self.os_type
    
    def detect_shell(self) -> ShellType:
        """Detect the shell type of the remote server"""
        if not self.client:
            return ShellType.UNKNOWN
        
        try:
            if self.os_type == OSType.WINDOWS:
                # Check for PowerShell
                stdin, stdout, stderr = self.client.exec_command("echo $PSVersionTable")
                output = stdout.read().decode().strip()
                if output and "Name" in output:
                    self.shell_type = ShellType.POWERSHELL
                else:
                    self.shell_type = ShellType.CMD
            else:
                # Check for Unix-like shells
                stdin, stdout, stderr = self.client.exec_command("echo $SHELL")
                output = stdout.read().decode().strip().lower()
                
                if "bash" in output:
                    self.shell_type = ShellType.BASH
                elif "zsh" in output:
                    self.shell_type = ShellType.ZSH
                elif "sh" in output:
                    self.shell_type = ShellType.SH
        except:
            pass
        
        return self.shell_type
    
    def execute_command(self, command: str, timeout: int = 30) -> Tuple[str, str, int]:
        """Execute command with proper encoding and timeout handling"""
        if not self.client:
            if not self.connect():
                return "", f"Failed to connect to {self.hostname}", -1
        
        try:
            # For Windows, we may need to adjust the command
            if self.os_type == OSType.WINDOWS:
                # If PowerShell is available, use it for better compatibility
                if self.shell_type == ShellType.POWERSHELL:
                    # Ensure PowerShell encoding
                    stdin, stdout, stderr = self.client.exec_command(
                        command,
                        timeout=timeout,
                        get_pty=False
                    )
                else:
                    # CMD.exe commands
                    stdin, stdout, stderr = self.client.exec_command(
                        command,
                        timeout=timeout,
                        get_pty=False
                    )
            else:
                # Linux/Unix commands
                stdin, stdout, stderr = self.client.exec_command(
                    command,
                    timeout=timeout,
                    get_pty=True  # Get pseudo-terminal for better interactive support
                )
            
            # Read output with proper decoding
            stdout_output = ""
            stderr_output = ""
            
            try:
                stdout_output = stdout.read().decode('utf-8', errors='replace')
            except:
                try:
                    stdout_output = stdout.read().decode('latin-1', errors='replace')
                except:
                    stdout_output = str(stdout.read())
            
            try:
                stderr_output = stderr.read().decode('utf-8', errors='replace')
            except:
                try:
                    stderr_output = stderr.read().decode('latin-1', errors='replace')
                except:
                    stderr_output = str(stderr.read())
            
            exit_status = stdout.channel.recv_exit_status()
            return stdout_output, stderr_output, exit_status
            
        except paramiko.SSHException as e:
            return "", f"SSH Error: {str(e)}", -1
        except Exception as e:
            return "", f"Error executing command: {str(e)}", -1
    
    def get_os_info(self) -> str:
        """Get detailed OS information"""
        if self.os_type == OSType.WINDOWS:
            stdout, stderr, code = self.execute_command("systeminfo | findstr /B /C:\"OS Name\" /C:\"OS Version\"")
            return stdout.strip() if code == 0 else f"Windows ({self.os_type.value})"
        else:
            stdout, stderr, code = self.execute_command("uname -a")
            return stdout.strip() if code == 0 else f"{self.os_type.value}"
    
    def close(self):
        if self.client:
            self.client.close()
        self.is_connected = False


class SSHConnectionTab(QWidget):
    output_received = pyqtSignal(str, str)  # hostname, output
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sessions: Dict[str, SSHSession] = {}
        self.init_ui()
    
    def init_ui(self):
        # Apply Apple-style light theme
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F7;
                color: #1D1D1F;
                font-family: -apple-system, 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
            }
            QLabel {
                color: #1D1D1F;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #0051D5;
            }
            QPushButton:pressed {
                background-color: #003D99;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 10px;
                padding: 5px;
                color: #1D1D1F;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 6px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #007AFF;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #F0F0F5;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 8px;
                padding: 10px;
                color: #1D1D1F;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #007AFF;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 10px;
                padding: 10px;
                color: #1D1D1F;
                font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
                font-size: 12px;
            }
            QComboBox {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 8px;
                padding: 8px;
                color: #1D1D1F;
                min-height: 25px;
            }
            QComboBox:hover {
                border: 1px solid #007AFF;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #D1D1D6;
                selection-background-color: #007AFF;
                selection-color: white;
                color: #1D1D1F;
            }
        """
        )
        
        # Main layout
        main_layout = QHBoxLayout(self)
        
        # Left panel for server list
        left_panel = QWidget()
        left_panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(12)
        
        # Server list header
        header_label = QLabel("🖥️  Connected Servers")
        header_label.setStyleSheet("font-size: 16px; color: #007AFF; font-weight: 600; padding: 5px;")
        left_layout.addWidget(header_label)
        
        # Server list
        self.server_list = QListWidget()
        self.server_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        left_layout.addWidget(self.server_list)
        
        # Server controls
        btn_add = QPushButton("➕ Add Server")
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #34C759;
                color: white;
            }
            QPushButton:hover {
                background-color: #30B350;
            }
        """)
        
        btn_remove = QPushButton("🗑️ Remove Selected")
        btn_remove.setStyleSheet("""
            QPushButton {
                background-color: #FF3B30;
                color: white;
            }
            QPushButton:hover {
                background-color: #E6342A;
            }
        """)
        
        btn_connect = QPushButton("🔗 Connect All")
        btn_connect.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
            }
            QPushButton:hover {
                background-color: #0051D5;
            }
        """)
        
        btn_add.clicked.connect(self.show_add_server_dialog)
        btn_remove.clicked.connect(self.remove_selected_servers)
        btn_connect.clicked.connect(self.connect_all_servers)
        
        left_layout.addWidget(btn_add)
        left_layout.addWidget(btn_remove)
        left_layout.addWidget(btn_connect)
        left_layout.addStretch()
        
        # Right panel for command and output
        right_panel = QWidget()
        right_panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(15)
        
        # Command templates section
        template_header = QLabel("⚡ Quick Command Templates")
        template_header.setStyleSheet("font-size: 15px; color: #007AFF; font-weight: 600;")
        right_layout.addWidget(template_header)
        
        template_layout = QHBoxLayout()
        self.template_combo = QComboBox()
        self.template_combo.addItem("-- Select Template --", "")
        
        # Linux/Unix templates
        self.template_combo.addItem("Linux: List Files", "ls -la")
        self.template_combo.addItem("Linux: Disk Usage", "df -h")
        self.template_combo.addItem("Linux: Memory Info", "free -h")
        self.template_combo.addItem("Linux: CPU Info", "lscpu")
        self.template_combo.addItem("Linux: Running Processes", "ps aux")
        self.template_combo.addItem("Linux: System Uptime", "uptime")
        self.template_combo.addItem("Linux: Network Interfaces", "ip addr show")
        self.template_combo.addItem("Linux: Installed Packages (Debian)", "dpkg -l")
        self.template_combo.addItem("Linux: Installed Packages (RedHat)", "rpm -qa")
        
        # Windows templates
        self.template_combo.addItem("Windows: List Files", "dir")
        self.template_combo.addItem("Windows: System Info", "systeminfo")
        self.template_combo.addItem("Windows: Running Processes", "tasklist")
        self.template_combo.addItem("Windows: Network Config", "ipconfig /all")
        self.template_combo.addItem("Windows: Installed Programs", "wmic product get name,version")
        self.template_combo.addItem("Windows: Disk Info", "wmic logicaldisk get name,size,freespace")
        self.template_combo.addItem("Windows: Services", "sc query state= all")
        
        # PowerShell templates
        self.template_combo.addItem("PowerShell: System Info", "Get-ComputerInfo")
        self.template_combo.addItem("PowerShell: Processes", "Get-Process")
        self.template_combo.addItem("PowerShell: Services", "Get-Service")
        self.template_combo.addItem("PowerShell: Network Adapters", "Get-NetAdapter")
        
        self.template_combo.currentIndexChanged.connect(self.load_template)
        template_layout.addWidget(self.template_combo)
        template_layout.addStretch()
        right_layout.addLayout(template_layout)
        
        # Command input section
        cmd_header = QLabel("💻 Command Input")
        cmd_header.setStyleSheet("font-size: 15px; color: #007AFF; font-weight: 600; margin-top: 10px;")
        right_layout.addWidget(cmd_header)
        
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Type your command here or select from templates above...")
        self.command_input.returnPressed.connect(self.execute_command)
        right_layout.addWidget(self.command_input)
        
        # Execute button and options
        exec_layout = QHBoxLayout()
        btn_execute = QPushButton("▶️ Execute Command")
        btn_execute.setStyleSheet("""
            QPushButton {
                background-color: #34C759;
                color: white;
                font-size: 14px;
                min-height: 40px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #30B350;
            }
        """)
        btn_execute.clicked.connect(self.execute_command)
        
        btn_clear = QPushButton("🗑️ Clear Output")
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #FF9500;
                color: white;
            }
            QPushButton:hover {
                background-color: #E68600;
            }
        """)
        btn_clear.clicked.connect(lambda: self.output_area.clear())
        
        exec_layout.addWidget(btn_execute)
        exec_layout.addWidget(btn_clear)
        exec_layout.addStretch()
        
        right_layout.addLayout(exec_layout)
        
        # Output area section
        output_header = QLabel("📊 Command Output")
        output_header.setStyleSheet("font-size: 15px; color: #007AFF; font-weight: 600; margin-top: 10px;")
        right_layout.addWidget(output_header)
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        right_layout.addWidget(self.output_area)
        
        # Add panels to main layout with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([200, 600])
        
        main_layout.addWidget(splitter)
    
    def show_add_server_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("🔌 Add New Server")
        dialog.setMinimumWidth(500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #F5F5F7;
            }
            QLabel {
                color: #1D1D1F;
                font-size: 13px;
                font-weight: 600;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #D1D1D6;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                color: #1D1D1F;
            }
            QLineEdit:focus {
                border: 2px solid #007AFF;
            }
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #0051D5;
            }
            QPushButton:pressed {
                background-color: #003D99;
            }
            QPushButton#cancelBtn {
                background-color: #8E8E93;
            }
            QPushButton#cancelBtn:hover {
                background-color: #636366;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Add Server Connection")
        title.setStyleSheet("font-size: 20px; color: #007AFF; font-weight: 700;")
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Form fields
        hostname = QLineEdit()
        hostname.setPlaceholderText("e.g., 192.168.1.100 or server.example.com")
        
        username = QLineEdit()
        username.setPlaceholderText("SSH username")
        
        password = QLineEdit()
        password.setEchoMode(QLineEdit.EchoMode.Password)
        password.setPlaceholderText("SSH password")
        
        port = QLineEdit("22")
        port.setPlaceholderText("Default: 22")
        port.setMaximumWidth(100)
        
        # Add fields to form
        form_layout.addRow("🌐 IP Address/Hostname:", hostname)
        form_layout.addRow("👤 Username:", username)
        form_layout.addRow("🔑 Password:", password)
        form_layout.addRow("🔌 Port:", port)
        
        layout.addLayout(form_layout)
        
        # Spacer
        layout.addSpacing(10)
        
        # Buttons
        btn_box = QHBoxLayout()
        btn_box.addStretch()
        
        btn_cancel = QPushButton("✖ Cancel")
        btn_cancel.setObjectName("cancelBtn")
        btn_cancel.setMinimumWidth(100)
        
        btn_ok = QPushButton("✓ Connect")
        btn_ok.setMinimumWidth(100)
        
        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)
        
        btn_box.addWidget(btn_cancel)
        btn_box.addWidget(btn_ok)
        
        layout.addLayout(btn_box)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Validate inputs
            if not hostname.text() or not username.text() or not password.text():
                QMessageBox.warning(self, "⚠️ Validation Error", 
                    "Please fill in IP Address, Username, and Password!")
                return
            
            # Create and store new session
            session = SSHSession(
                hostname=hostname.text().strip(),
                username=username.text().strip(),
                password=password.text(),
                key_filename=None,
                port=int(port.text()) if port.text().isdigit() else 22
            )
            
            # Try to connect and add to list if successful
            if session.connect():
                self.sessions[session.hostname] = session
                # Display server info including OS and shell type
                server_info = f"{session.hostname} [{session.os_type.value} - {session.shell_type.value}]"
                self.server_list.addItem(server_info)
                
                # Get detailed OS info
                os_details = session.get_os_info()
                msg = f"Successfully connected to {session.hostname}\n\n"
                msg += f"OS Type: {session.os_type.value}\n"
                msg += f"Shell Type: {session.shell_type.value}\n"
                msg += f"Details: {os_details[:200]}"  # Limit to 200 chars
                QMessageBox.information(self, "Connection Successful", msg)
            else:
                QMessageBox.warning(self, "Connection Failed", f"Failed to connect to {session.hostname}")
    
    def remove_selected_servers(self):
        selected_items = self.server_list.selectedItems()
        if not selected_items:
            return
            
        reply = QMessageBox.question(
            self,
            'Remove Servers',
            f'Are you sure you want to remove {len(selected_items)} server(s)?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for item in selected_items:
                hostname = item.text()
                if hostname in self.sessions:
                    self.sessions[hostname].close()
                    del self.sessions[hostname]
                self.server_list.takeItem(self.server_list.row(item))
    
    def connect_all_servers(self):
        for hostname, session in self.sessions.items():
            if not session.client:
                if session.connect():
                    QMessageBox.information(self, "Success", f"Connected to {hostname}")
                else:
                    QMessageBox.warning(self, "Error", f"Failed to connect to {hostname}")
    
    def load_template(self, index):
        """Load a command template into the command input field"""
        if index > 0:  # Skip the first "-- Select Template --" item
            command = self.template_combo.itemData(index)
            self.command_input.setText(command)
            self.template_combo.setCurrentIndex(0)  # Reset to default
    
    def execute_command(self):
        selected_items = self.server_list.selectedItems()
        if not selected_items or not self.command_input.text().strip():
            return
        
        command = self.command_input.text().strip()
        self.output_area.append(f"\n{'=' * 80}")
        self.output_area.append(f"Executing: {command}")
        self.output_area.append(f"{'=' * 80}\n")
        
        for item in selected_items:
            display_text = item.text()
            # Extract hostname from "hostname [OS - Shell]" format
            hostname = display_text.split('[')[0].strip()
            
            if hostname in self.sessions:
                session = self.sessions[hostname]
                self.output_area.append(f"[{display_text}]")
                self.output_area.append(f"Executing command...")
                QApplication.processEvents()  # Update UI
                
                stdout, stderr, exit_code = session.execute_command(command)
                
                if exit_code == 0:
                    self.output_area.append(f"✓ Success (exit code: {exit_code})")
                    if stdout.strip():
                        self.output_area.append(f"Output:\n{stdout}")
                    else:
                        self.output_area.append("(No output)")
                else:
                    self.output_area.append(f"✗ Error (exit code: {exit_code})")
                    if stderr.strip():
                        self.output_area.append(f"Error:\n{stderr}")
                    elif stdout.strip():
                        self.output_area.append(f"Output:\n{stdout}")
                    else:
                        self.output_area.append("(No output)")
                
                self.output_area.append("-" * 80)
                self.output_area.verticalScrollBar().setValue(self.output_area.verticalScrollBar().maximum())


class ParallelSSHApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TACONNECT")
        self.setGeometry(100, 100, 1300, 850)
        
        # Apply Apple-style light theme to main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F7;
            }
            QTabWidget::pane {
                border: 1px solid #D1D1D6;
                border-radius: 10px;
                background-color: #F5F5F7;
                top: -1px;
            }
            QTabBar::tab {
                background-color: white;
                color: #1D1D1F;
                padding: 10px 24px;
                margin: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 500;
                border: 1px solid #D1D1D6;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #007AFF;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #E5E5EA;
            }
            QMenuBar {
                background-color: #FAFAFA;
                color: #1D1D1F;
                padding: 6px;
                border-bottom: 1px solid #D1D1D6;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QMenuBar::item:selected {
                background-color: #007AFF;
                color: white;
            }
            QMenu {
                background-color: white;
                color: #1D1D1F;
                border: 1px solid #D1D1D6;
                border-radius: 8px;
                padding: 6px;
            }
            QMenu::item {
                padding: 8px 30px;
                border-radius: 6px;
            }
            QMenu::item:selected {
                background-color: #007AFF;
                color: white;
            }
        """)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        # Add initial tab
        self.add_new_tab()
        
        # Add tab button
        new_tab_btn = self.create_tab_button("➕", self.add_new_tab)
        self.tabs.setCornerWidget(new_tab_btn)
        
        # Set central widget
        self.setCentralWidget(self.tabs)
        
        # Menu bar
        self.create_menu_bar()
        
        # Set status bar
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #FAFAFA;
                color: #007AFF;
                font-weight: 600;
                border-top: 1px solid #D1D1D6;
            }
        """)
        self.statusBar().showMessage("● Ready to connect")
    
    def create_tab_button(self, text, callback):
        btn = QPushButton(text)
        btn.setFixedSize(32, 32)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #34C759;
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #30B350;
            }
        """)
        btn.clicked.connect(callback)
        return btn
    
    def add_new_tab(self, index=None):
        tab = SSHConnectionTab()
        tab_name = f"Session {self.tabs.count() + 1}"
        tab_index = self.tabs.addTab(tab, tab_name)
        self.tabs.setCurrentIndex(tab_index)
        return tab_index
    
    def close_tab(self, index):
        if self.tabs.count() <= 1:  # Don't close the last tab
            return
            
        widget = self.tabs.widget(index)
        if widget:
            # Close all SSH sessions in this tab
            if hasattr(widget, 'sessions'):
                for session in widget.sessions.values():
                    session.close()
            widget.deleteLater()
            self.tabs.removeTab(index)
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_tab_action = file_menu.addAction("New Tab")
        new_tab_action.triggered.connect(lambda: self.add_new_tab())
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about_dialog)
    
    def show_about_dialog(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About TACONNECT")
        about_box.setTextFormat(Qt.TextFormat.RichText)
        about_box.setText(
            "<h2 style='color: #007AFF;'>TACONNECT</h2>"
            "<p style='color: #1D1D1F;'>"
            "A powerful, modern tool for managing multiple SSH connections simultaneously.<br><br>"
            "<b style='color: #34C759;'>Features:</b><br>"
            "• Execute commands on multiple servers in parallel<br>"
            "• Auto-detect OS and shell types<br>"
            "• Support for Linux, Windows, and macOS servers<br>"
            "• Beautiful Apple-style interface<br><br>"
            "<b style='color: #007AFF;'>Version:</b> 2.0.0<br>"
            "<b style='color: #007AFF;'>Built with:</b> PyQt6 & Paramiko<br><br>"
            "© 2025"
            "</p>"
        )
        about_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #1D1D1F;
            }
            QPushButton {
                background-color: #007AFF;
                color: white;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #0051D5;
            }
        """)
        about_box.exec()
    
    def closeEvent(self, event):
        # Close all SSH connections before exiting
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if hasattr(widget, 'sessions'):
                for session in widget.sessions.values():
                    session.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a modern look
    
    # Set application information
    app.setApplicationName("TACONNECT")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("TACONNECT")
    
    # Show splash screen for 5 seconds
    splash = TaconnectSplashScreen()
    splash.show()
    app.processEvents()
    
    # Create main window
    window = ParallelSSHApp()
    
    # Timer to close splash and show main window after 5 seconds
    QTimer.singleShot(5000, lambda: (
        splash.close(),
        window.show()
    ))
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

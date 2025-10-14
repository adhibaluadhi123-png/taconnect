# Changelog

All notable changes to the Parallel SSH Manager project.

## [2.0.0] - 2025-01-12

### 🎨 Major UI Overhaul

#### Added
- **Beautiful Dark Theme**
  - Catppuccin-inspired color palette
  - Deep dark backgrounds (#1E1E2E)
  - Vibrant accent colors (blue, green, pink, peach)
  - Consistent styling across all elements
  
- **Modern Visual Elements**
  - Emoji icons for better visual recognition
  - Rounded corners (6-8px radius) on all elements
  - Smooth hover effects and transitions
  - Color-coded buttons by function:
    - Green for positive actions (Add, Execute)
    - Pink for destructive actions (Remove)
    - Blue for neutral actions (Connect)
    - Yellow for utility actions (Clear)
  
- **Enhanced Server List**
  - Visual hover states
  - Colored selection highlighting
  - Better spacing and padding
  - Server info badges showing OS and shell type

- **Improved Command Interface**
  - Section headers with icons and colors
  - Larger, more prominent Execute button
  - Better visual hierarchy
  - Clearer input placeholders

- **Styled Dialogs**
  - Add Server dialog with gradient background
  - Modern input fields with focus states
  - Prominent buttons with hover effects
  - Icon-enhanced labels

- **Professional Status Bar**
  - Color-coded status messages
  - Emoji indicators (🟢 for ready state)
  - Consistent with overall theme

### 🚀 Simplified User Experience

#### Changed
- **Server Addition Process**
  - Removed SSH key requirement from main dialog
  - Simplified to 3 fields: IP, Username, Password
  - Made SSH key authentication optional (removed from UI)
  - Added field validation with helpful messages
  - Better placeholder text for guidance

- **Window Sizing**
  - Increased default size to 1200x800 (from 1000x700)
  - Better space utilization
  - More comfortable viewing area

- **Tab Management**
  - Styled tab bar with rounded corners
  - Hover effects on tabs
  - Emoji icons in tab names
  - Larger new tab button (➕)

### 💅 Visual Polish

#### Enhanced
- **Typography**
  - Consistent font sizing
  - Bold headers and labels
  - Monospace for output (Consolas/Courier)
  - Better readability

- **Spacing & Layout**
  - Increased spacing between elements
  - Better padding on all components
  - Cleaner visual separation
  - More breathing room

- **Interactive Elements**
  - All buttons show hover states
  - Input fields highlight on focus
  - List items highlight on hover
  - Visual feedback for all interactions

- **Color Scheme**
  - Background: #1E1E2E (dark blue)
  - Panels: #181825 (darker)
  - Borders: #313244 (gray)
  - Primary: #89B4FA (sky blue)
  - Success: #A6E3A1 (mint green)
  - Warning: #FAB387 (peach)
  - Error: #F38BA8 (pink)
  - Text: #CDD6F4 (light gray)
  - Output: #A6E3A1 (green for terminal feel)

### 📚 Documentation

#### Added
- **VISUAL_GUIDE.md**: Complete visual guide with UI details
- **CHANGELOG.md**: This file
- Updated README.md with v2.0 features
- Updated QUICK_START.md with simplified steps

### 🐛 Bug Fixes
- Fixed QDialog import issue
- Improved error handling in server addition
- Better validation for empty fields

---

## [1.0.0] - 2025-01-11

### Initial Release

#### Features
- Multi-server SSH connection management
- Cross-platform support (Linux, Windows, macOS servers)
- Automatic OS and shell detection
- 20+ command templates for common tasks
- Password and SSH key authentication
- Real-time command execution output
- Tabbed interface for organizing servers
- Parallel command execution
- Support for multiple encoding types

#### Core Components
- SSHSession class for connection management
- SSHConnectionTab for UI and command execution
- ParallelSSHApp main window with tab management
- OS and shell type detection (OSType, ShellType enums)

#### Documentation
- README.md with installation and usage
- USAGE_GUIDE.md with comprehensive examples
- FEATURES.md with feature list and roadmap
- PROJECT_SUMMARY.md with technical details
- config.example.json for configuration reference

---

## Version Naming
- **Major version** (X.0.0): Breaking changes or major rewrites
- **Minor version** (0.X.0): New features, UI improvements
- **Patch version** (0.0.X): Bug fixes, minor tweaks

## Upgrade Notes

### From 1.0.0 to 2.0.0
- **No breaking changes** in functionality
- **UI completely redesigned** - much more modern and user-friendly
- **Simplified server addition** - no longer requires SSH key setup in UI
- **Better visual feedback** throughout the application
- All existing features retained and enhanced

---

**Legend:**
- 🎨 UI/Design changes
- 🚀 New features
- 💅 Visual polish
- 🐛 Bug fixes
- 📚 Documentation
- ⚡ Performance
- 🔧 Technical changes

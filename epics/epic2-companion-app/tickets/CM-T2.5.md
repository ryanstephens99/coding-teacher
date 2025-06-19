# CM-T2.5: Companion App Packaging (Basic)

## Summary
Create basic packaging and distribution system for the companion app including standalone executables and simple deployment.

## Acceptance Criteria
- [ ] Standalone executable generation using PyInstaller
- [ ] Basic cross-platform support (Windows, macOS, Linux)
- [ ] Simple startup scripts and service management
- [ ] Basic configuration file handling
- [ ] Executable includes all dependencies
- [ ] Simple installation and setup instructions

## Implementation Details

### PyInstaller Setup (companion.spec)
```python
"""
PyInstaller specification for building standalone executable.
Includes all dependencies and handles cross-platform compatibility.
"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app/templates', 'templates'),
        ('app/static', 'static'),
    ],
    hiddenimports=[
        'uvicorn.lifespan.on',
        'uvicorn.lifespan.off',
        'uvicorn.protocols.websockets.auto',
        'fastapi',
        'websockets',
        'pydantic',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='codementor-companion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico'  # Add application icon
)
```

### Build Scripts

#### Linux/macOS Build Script (scripts/build.sh)
```bash
#!/bin/bash
"""
Build script for Linux and macOS platforms.
Creates standalone executable using PyInstaller.
"""

set -e

echo "Building CodeMentor Companion App..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install pyinstaller

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/

# Build executable
echo "Building executable..."
pyinstaller companion.spec

echo "Build complete! Executable located in dist/"
```

#### Windows Build Script (scripts/build.bat)
```batch
@echo off
REM Build script for Windows platform
REM Creates standalone executable using PyInstaller

echo Building CodeMentor Companion App...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build executable
echo Building executable...
pyinstaller companion.spec

echo Build complete! Executable located in dist\
pause
```

### Startup Service (scripts/start_companion.py)
```python
"""
Startup script for the CodeMentor Companion App.
Handles service initialization and background operation.
"""
import os
import sys
import logging
import argparse
import subprocess
from pathlib import Path

def setup_logging():
    """Setup logging for the startup service"""
    log_dir = Path.home() / '.codementor' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'companion.log'),
            logging.StreamHandler()
        ]
    )

def start_service():
    """Start the companion app service"""
    logger = logging.getLogger(__name__)
    
    try:
        # Get the executable path
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller executable
            app_path = sys.executable
        else:
            # Running as Python script
            app_path = Path(__file__).parent.parent / 'app' / 'main.py'
        
        logger.info(f"Starting CodeMentor Companion App from: {app_path}")
        
        # Start the service
        if getattr(sys, 'frozen', False):
            # For executable, just run it
            subprocess.run([app_path], check=True)
        else:
            # For development, run with Python
            subprocess.run([sys.executable, str(app_path)], check=True)
            
    except Exception as e:
        logger.error(f"Failed to start service: {e}")
        sys.exit(1)

def stop_service():
    """Stop the companion app service"""
    logger = logging.getLogger(__name__)
    
    try:
        # Find and terminate the process
        import psutil
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'codementor-companion' in proc.info['name']:
                logger.info(f"Stopping process {proc.info['pid']}")
                proc.terminate()
                proc.wait(timeout=10)
                
    except Exception as e:
        logger.error(f"Failed to stop service: {e}")

def main():
    """Main entry point for the startup script"""
    parser = argparse.ArgumentParser(description='CodeMentor Companion App Service')
    parser.add_argument('action', choices=['start', 'stop', 'restart'], 
                       help='Action to perform')
    parser.add_argument('--background', action='store_true',
                       help='Run in background mode')
    
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    if args.action == 'start':
        start_service()
    elif args.action == 'stop':
        stop_service()
    elif args.action == 'restart':
        stop_service()
        start_service()

if __name__ == '__main__':
    main()
```

### Configuration Template (config_template.py)
```python
"""
Basic configuration template for the companion app.
Users can copy and modify this for their environment.
"""

# Server Configuration
HOST = "localhost"
PORT = 8765
DEBUG = False

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "companion.log"

# Analysis Configuration
MAX_CONCURRENT_ANALYSES = 5
ANALYSIS_TIMEOUT = 30
MAX_FILE_SIZE = 1024 * 1024  # 1MB

# WebSocket Configuration
PING_INTERVAL = 20
PING_TIMEOUT = 20

# Copy this file to 'config.py' and modify as needed
```

### Installation Instructions (INSTALL.md)
```markdown
# CodeMentor Companion App Installation

## Quick Start

1. Download the appropriate executable for your platform:
   - Windows: `codementor-companion.exe`
   - macOS: `codementor-companion`
   - Linux: `codementor-companion`

2. Run the executable:
   ```bash
   # Linux/macOS
   ./codementor-companion
   
   # Windows
   codementor-companion.exe
   ```

3. The service will start on `localhost:8765`

## Service Management

### Start the service
```bash
python scripts/start_companion.py start
```

### Stop the service
```bash
python scripts/start_companion.py stop
```

### Restart the service
```bash
python scripts/start_companion.py restart
```

## Configuration

1. Copy `config_template.py` to `config.py`
2. Modify settings as needed
3. Restart the service

## Troubleshooting

- Check logs in `~/.codementor/logs/companion.log`
- Ensure port 8765 is not in use by another application
- Verify VS Code extension is properly configured
```

## Technical Notes
- Uses PyInstaller for cross-platform executable generation
- Includes all Python dependencies in the executable
- Provides simple startup scripts for service management
- Basic configuration file support
- Minimal installation requirements

## Dependencies
- PyInstaller for executable generation
- All FastAPI dependencies bundled
- Platform-specific build tools

## Testing
- Executable builds successfully on target platforms
- Service starts and stops correctly
- Configuration files are properly loaded
- VS Code extension can connect to the service

## Estimated Hours
6-8 hours 
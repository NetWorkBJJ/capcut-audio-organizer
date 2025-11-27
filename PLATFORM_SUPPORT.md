# Cross-Platform Compatibility Guide

## ✅ Platform Support

| Platform | Status | Launcher | CapCut Path |
|----------|--------|----------|-------------|
| **macOS** | ✅ Full | `.command` | `~/Movies/CapCut/...` |
| **Windows** | ✅ Full | `.bat` | `%LOCALAPPDATA%\CapCut\...` |
| **Linux** | ⚠️ Untested | `.sh` | `~/Movies/CapCut/...` |

---

## 🪟 Windows Specifics

### Paths
- **CapCut Projects:** `C:\Users\USERNAME\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft`
- **Logs:** `C:\Users\USERNAME\.capcut_organizer\logs\`
- **Detected automatically via:** `os.environ['LOCALAPPDATA']`

### Launchers
- `StartApp.bat` - Main launcher
- `install_windows.bat` - Installation script

### Dependencies
Same as macOS:
```
flask
pywebview
```

### pywebview Backend
Windows uses EdgeHTML or Chromium (via CEF) automatically.

---

## 🍎 macOS Specifics

### Paths
- **CapCut Projects:** `~/Movies/CapCut/User Data/Projects/com.lveditor.draft`
- **Logs:** `~/.capcut_organizer/logs/`
- **Detected via:** `os.path.expanduser()`

### Launchers
- `StartApp.command` - Main launcher
- `OrganizarAudio.command` - Classic launcher
- `build_app.sh` - Create .app bundle

### App Bundle
Create standalone `.app`:
```bash
./build_app.sh
```

---

## 🐧 Linux (Experimental)

### Paths
Same as macOS (typically):
```
~/Movies/CapCut/User Data/Projects/com.lveditor.draft
```

### Dependencies
Additional requirements:
```bash
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0
pip install pywebview[gtk]
```

### Launcher
Create `StartApp.sh`:
```bash
#!/bin/bash
python3 backend/app.py
```

---

## 🔧 Code Adaptations

### Platform Detection
```python
import platform

if platform.system() == 'Windows':
    # Windows-specific code
elif platform.system() == 'Darwin':  # macOS
    # macOS-specific code
else:  # Linux
    # Linux-specific code
```

### Path Handling
All paths use `os.path.join()` for cross-platform compatibility:
```python
# ✅ Correct
path = os.path.join('folder', 'file.txt')

# ❌ Wrong
path = 'folder/file.txt'  # Fails on Windows
```

### Environment Variables
- **Windows:** `os.environ['LOCALAPPDATA']`
- **macOS/Linux:** `os.path.expanduser('~')`

---

## 🧪 Testing Across Platforms

### Windows
```cmd
python --version
pip list
StartApp.bat
```

### macOS
```bash
python3 --version
pip3 list
./StartApp.command
```

### Linux
```bash
python3 --version
pip3 list
python3 backend/app.py
```

---

## 📦 Distribution

### Windows
Create `.exe`:
```cmd
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico backend/app.py
```

### macOS
Create `.app`:
```bash
./build_app.sh
```

### Linux
Create `.deb` or AppImage (not implemented yet)

---

## 🐛 Known Platform Issues

### Windows
- **Issue:** pywebview might need `pywebview[qt]`
- **Fix:** `pip install pywebview[qt]`

### macOS
- **Issue:** Permission denied on `.command` files
- **Fix:** `chmod +x StartApp.command`

### Linux
- **Issue:** WebKit dependencies missing
- **Fix:** Install GTK and WebKit packages

---

## 💡 Best Practices

1. **Always use `os.path.join()`** for paths
2. **Detect platform** with `platform.system()`
3. **Test on target platforms** before releasing
4. **Use virtual environments** to isolate dependencies
5. **Document platform-specific** requirements

---

**Created by Anderson Network**

#!/bin/bash
# Build CapCut Audio Organizer.app

APP_NAME="CapCut Audio Organizer"
BUNDLE_DIR="$APP_NAME.app"
CONTENTS_DIR="$BUNDLE_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

echo "Building $APP_NAME..."

# Clean previous build
rm -rf "$BUNDLE_DIR"

# Create bundle structure
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"

# Copy Python files and dependencies
cp -r backend "$RESOURCES_DIR/"
cp -r templates "$RESOURCES_DIR/"
cp -r static "$RESOURCES_DIR/"
cp organize_audio.py "$RESOURCES_DIR/"

# Create launcher script
cat > "$MACOS_DIR/launcher.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/../Resources"
python3 backend/app.py
EOF

chmod +x "$MACOS_DIR/launcher.sh"

# Create Info.plist
cat > "$CONTENTS_DIR/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher.sh</string>
    <key>CFBundleIdentifier</key>
    <string>com.antigravity.capcut-organizer</string>
    <key>CFBundleName</key>
    <string>CapCut Audio Organizer</string>
    <key>CFBundleDisplayName</key>
    <string>CapCut Audio Organizer</string>
    <key>CFBundleVersion</key>
    <string>2.0</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

echo "✓ App bundle created: $BUNDLE_DIR"
echo "Double-click to launch!"

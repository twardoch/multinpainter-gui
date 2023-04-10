#!/usr/bin/env bash
dir=${0%/*}
if [ "$dir" = "$0" ]; then dir="."; fi
cd "$dir" || exit

#!/bin/bash

# Define the name of the app, the source file, and the output folder
APP_NAME="MultInpainter"
SOURCE_FILE="multinpainter.py"
OUTPUT_FOLDER="dist_nuitka"
mkdir -p "${OUTPUT_FOLDER}"
deactivate

# Create a virtual environment
python3.10 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
cd ..
python3.10 -m pip install --upgrade pip setuptools setuptools_scm wheel urllib3 
python3.10 -m pip install --upgrade nuitka
python3.10 -m pip install --upgrade .
cd app

python3 -m nuitka \
    --assume-yes-for-downloads \
    --clang \
    --standalone \
    --onefile \
    --enable-plugin='no-qt' \
    --macos-disable-console \
    --macos-create-app-bundle \
    --macos-app-icon="../icons/multinpainter.icns" \
    --follow-imports \
    --lto=yes \
    --jobs=$(sysctl -n hw.ncpu) \
    --show-modules \
    --nofollow-import-to='Crypto,dask,distributed,distutils,IPython,nuitka,numba,pytest,setuptools,setuptools_scm,snappy,test,tkinter,unittest' \
    --output-dir="${OUTPUT_FOLDER}" \
    "${SOURCE_FILE}"

deactivate

exit
# Create the .app bundle structure
APP_FOLDER="${OUTPUT_FOLDER}/${APP_NAME}.app"
APP_CONTENTS="${APP_FOLDER}/Contents"
APP_MACOS="${APP_CONTENTS}/MacOS"
APP_RESOURCES="${APP_CONTENTS}/Resources"

mkdir -p "${APP_MACOS}"
mkdir -p "${APP_RESOURCES}"

# Create the Info.plist file
cat >"${APP_CONTENTS}/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>${APP_NAME}</string>
    <key>CFBundleExecutable</key>
    <string>${APP_NAME}</string>
    <key>CFBundleIconFile</key>
    <string></string>
    <key>CFBundleIdentifier</key>
    <string>com.example.${APP_NAME}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>${APP_NAME}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

# Copy the compiled executable to the .app bundle
cp "${OUTPUT_FOLDER}/${SOURCE_FILE%.py}.bin" "${APP_MACOS}/${APP_NAME}"

# Set the correct permissions for the executable
chmod +x "${APP_MACOS}/${APP_NAME}"

# Deactivate the virtual environment
deactivate

echo "The .app bundle has been created at ${APP_FOLDER}"

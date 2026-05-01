#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install -U pip pyinstaller

OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"

case "$ARCH" in
  x86_64|amd64)
    ARCH="amd64"
    ;;
  aarch64|arm64)
    ARCH="arm64"
    ;;
  *)
    echo "Unsupported architecture: $ARCH"
    exit 1
    ;;
esac

case "$OS" in
  linux)
    NAME="rrh-linux-$ARCH"
    ;;
  darwin)
    NAME="rrh-darwin-$ARCH"
    ;;
  *)
    echo "Unsupported OS: $OS"
    exit 1
    ;;
esac

python3 -m PyInstaller --clean --onefile --name "$NAME" rrh.py

echo "Build complete: dist/$NAME"

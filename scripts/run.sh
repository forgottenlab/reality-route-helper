#!/usr/bin/env bash
set -euo pipefail

REPO="forgottenlab/reality-route-helper"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

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
    BIN="rrh-linux-$ARCH"
    ;;
  darwin)
    BIN="rrh-darwin-$ARCH"
    ;;
  *)
    echo "Unsupported OS: $OS"
    exit 1
    ;;
esac

URL="https://github.com/$REPO/releases/latest/download/$BIN"
TARGET="$TMP_DIR/$BIN"

echo "Downloading: $URL"

if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$URL" -o "$TARGET"
elif command -v wget >/dev/null 2>&1; then
  wget -qO "$TARGET" "$URL"
else
  echo "curl or wget is required."
  exit 1
fi

chmod +x "$TARGET"
"$TARGET"

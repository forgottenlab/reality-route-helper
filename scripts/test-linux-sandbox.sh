#!/usr/bin/env bash
set -euo pipefail

echo "== Reality Route Helper Linux sandbox test =="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Project: $PROJECT_ROOT"
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found."
  echo "Please install it first:"
  echo "  sudo apt update"
  echo "  sudo apt install -y python3"
  exit 1
fi

echo "1. Python version"
python3 --version
echo

TMP_ROOT="$(mktemp -d -t rrh-linux-test-XXXXXX)"
cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT

export RRH_CONFIG_PATH="$TMP_ROOT/config.json"
export RRH_BACKUP_DIR="$TMP_ROOT/backups"
export RRH_DISABLE_RESTART="1"
export PYTHONPATH="$PROJECT_ROOT"

echo "Sandbox:"
echo "  RRH_CONFIG_PATH=$RRH_CONFIG_PATH"
echo "  RRH_BACKUP_DIR=$RRH_BACKUP_DIR"
echo "  RRH_DISABLE_RESTART=$RRH_DISABLE_RESTART"
echo

echo "2. Compile Python files"
find "$PROJECT_ROOT" \
  -type f \
  -name "*.py" \
  ! -path "*/.venv/*" \
  ! -path "*/build/*" \
  ! -path "*/dist/*" \
  -print0 | xargs -0 -n 1 python3 -m py_compile
echo

echo "3. Run smoke tests in sandbox"
python3 tests/smoke_test.py
echo

echo "4. Run menu flow tests in sandbox"
python3 tests/menu_flow_test.py
echo

echo "5. Platform scan preview"
python3 - <<'PY'
from reality_route_helper.scanners.service_scanner import scan_services

data = scan_services()
for key, value in data.items():
    print(f"{key}: {value}")
PY
echo

echo "6. Sandbox files"
find "$TMP_ROOT" -maxdepth 3 -type f -print || true
echo

echo "Linux sandbox test completed successfully."

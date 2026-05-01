import platform
import shutil
from typing import Dict

from .base import PlatformAdapter


class MacOSAdapter(PlatformAdapter):
    name = "macos"

    def scan(self) -> Dict[str, str]:
        return {
            "os": "macOS",
            "release": platform.release(),
            "python": shutil.which("python3") or "not found",
            "server_deploy": "client mode recommended unless this is a server",
        }

    def test_tcp_hint(self) -> str:
        return "Use: nc -vz <host> <port>"

import platform
import shutil
from typing import Dict

from .base import PlatformAdapter


class WindowsAdapter(PlatformAdapter):
    name = "windows"

    def scan(self) -> Dict[str, str]:
        return {
            "os": "Windows",
            "release": platform.release(),
            "powershell": shutil.which("powershell") or shutil.which("pwsh") or "not found",
            "python": shutil.which("python") or shutil.which("py") or "not found",
            "server_deploy": "not recommended on Windows client mode",
        }

    def test_tcp_hint(self) -> str:
        return "PowerShell: Test-NetConnection <host> -Port <port>"

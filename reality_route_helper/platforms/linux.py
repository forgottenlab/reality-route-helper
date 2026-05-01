import os
import shutil
from typing import Dict

from .base import PlatformAdapter
from ..core.runner import run


class LinuxAdapter(PlatformAdapter):
    name = "linux"

    def can_server_deploy(self) -> bool:
        return True

    def scan(self) -> Dict[str, str]:
        result = {}
        result["os"] = "Linux"
        result["is_root"] = "yes" if hasattr(os, "geteuid") and os.geteuid() == 0 else "no"
        result["systemctl"] = "yes" if shutil.which("systemctl") else "no"
        result["xray"] = shutil.which("xray") or "not found"
        result["docker"] = shutil.which("docker") or "not found"

        if shutil.which("xray"):
            r = run(["xray", "version"])
            result["xray_version"] = r.stdout.splitlines()[0] if r.stdout else r.stderr

        if shutil.which("docker"):
            r = run(["docker", "ps", "--format", "{{.Names}}"], timeout=10)
            result["docker_containers"] = r.stdout or "none / permission denied"

        return result

    def test_tcp_hint(self) -> str:
        return "Use: nc -vz <host> <port>  or  bash -c '</dev/tcp/<host>/<port>'"

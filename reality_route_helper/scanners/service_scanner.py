from typing import Dict

from ..platforms.detect import detect_platform
from .outline import scan_outline


def scan_services() -> Dict[str, str]:
    adapter = detect_platform()
    result = adapter.scan()

    if adapter.name == "linux" and result.get("docker") != "not found":
        result.update(scan_outline())

    return result

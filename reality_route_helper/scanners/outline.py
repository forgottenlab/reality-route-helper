from typing import Dict

from ..core.runner import run


def scan_outline() -> Dict[str, str]:
    result = {
        "outline_detected": "unknown",
        "shadowbox": "unknown",
        "watchtower": "unknown",
    }

    r = run(["docker", "ps", "--format", "{{.Names}}"], timeout=10)
    if not r.ok:
        result["outline_detected"] = "docker unavailable or permission denied"
        return result

    names = set(r.stdout.splitlines())
    result["shadowbox"] = "yes" if "shadowbox" in names else "no"
    result["watchtower"] = "yes" if "watchtower" in names else "no"
    result["outline_detected"] = "yes" if "shadowbox" in names else "no"
    return result

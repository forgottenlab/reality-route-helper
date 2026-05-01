import platform

from .base import PlatformAdapter
from .linux import LinuxAdapter
from .windows import WindowsAdapter
from .macos import MacOSAdapter


def detect_platform() -> PlatformAdapter:
    system = platform.system().lower()
    if system == "linux":
        return LinuxAdapter()
    if system == "windows":
        return WindowsAdapter()
    if system == "darwin":
        return MacOSAdapter()
    return LinuxAdapter()

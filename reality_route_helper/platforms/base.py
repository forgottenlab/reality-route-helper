from abc import ABC, abstractmethod
from typing import Dict


class PlatformAdapter(ABC):
    name = "unknown"

    @abstractmethod
    def scan(self) -> Dict[str, str]:
        pass

    def can_server_deploy(self) -> bool:
        return False

    def test_tcp_hint(self) -> str:
        return "Use a TCP port test tool for your platform."

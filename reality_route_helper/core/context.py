from dataclasses import dataclass


@dataclass
class AppContext:
    lang: str
    platform_name: str
    role: str = ""

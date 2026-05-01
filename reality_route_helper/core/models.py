from dataclasses import dataclass
from typing import List


@dataclass
class RealityUser:
    uuid: str
    remark: str
    flow: str = "xtls-rprx-vision"


@dataclass
class RealityServerConfig:
    host: str
    port: int
    sni: str
    dest: str
    private_key: str
    public_key: str
    short_ids: List[str]
    users: List[RealityUser]
    loglevel: str = "warning"

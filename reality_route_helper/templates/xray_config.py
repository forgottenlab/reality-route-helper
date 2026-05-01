import json

from ..core.models import RealityServerConfig


def build_xray_reality_config(cfg: RealityServerConfig) -> str:
    data = {
        "log": {
            "loglevel": cfg.loglevel
        },
        "inbounds": [
            {
                "listen": "0.0.0.0",
                "port": cfg.port,
                "protocol": "vless",
                "settings": {
                    "clients": [
                        {
                            "id": user.uuid,
                            "email": user.remark,
                            "flow": user.flow
                        }
                        for user in cfg.users
                    ],
                    "decryption": "none"
                },
                "streamSettings": {
                    "network": "tcp",
                    "security": "reality",
                    "realitySettings": {
                        "show": False,
                        "dest": cfg.dest,
                        "xver": 0,
                        "serverNames": [
                            cfg.sni
                        ],
                        "privateKey": cfg.private_key,
                        "shortIds": cfg.short_ids
                    }
                }
            }
        ],
        "outbounds": [
            {
                "protocol": "freedom",
                "tag": "direct"
            },
            {
                "protocol": "blackhole",
                "tag": "block"
            }
        ]
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"

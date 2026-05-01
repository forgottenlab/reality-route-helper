import json
import os
import shutil
import socket
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlencode, quote

from ..core.models import RealityServerConfig, RealityUser
from ..core.runner import run
from ..templates.xray_config import build_xray_reality_config


DEFAULT_CONFIG_PATH = Path("/usr/local/etc/xray/config.json")
DEFAULT_BACKUP_DIR = Path("/root/rrh-backups")


def get_config_path() -> Path:
    """
    Return config path.

    Production default:
        /usr/local/etc/xray/config.json

    Test override:
        RRH_CONFIG_PATH=/tmp/rrh-test/config.json

    This makes local / CI tests safe and non-destructive.
    """
    return Path(os.environ.get("RRH_CONFIG_PATH", str(DEFAULT_CONFIG_PATH)))


def get_backup_dir() -> Path:
    """
    Return backup directory.

    Production default:
        /root/rrh-backups

    Test override:
        RRH_BACKUP_DIR=/tmp/rrh-test/backups
    """
    return Path(os.environ.get("RRH_BACKUP_DIR", str(DEFAULT_BACKUP_DIR)))


def is_restart_disabled() -> bool:
    """
    Disable real service restart during safe tests.

    Set:
        RRH_DISABLE_RESTART=1
    """
    return os.environ.get("RRH_DISABLE_RESTART", "").strip() == "1"


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def generate_uuid() -> str:
    if command_exists("xray"):
        r = run(["xray", "uuid"])
        if r.ok and r.stdout.strip():
            return r.stdout.strip().splitlines()[-1]
    return str(uuid.uuid4())


def generate_x25519() -> Tuple[str, str, str]:
    if not command_exists("xray"):
        raise RuntimeError("xray not found")

    r = run(["xray", "x25519"])
    if not r.ok:
        raise RuntimeError(r.text)

    private_key = ""
    public_key = ""
    hash32 = ""

    for line in r.stdout.splitlines():
        lower = line.lower()
        if lower.startswith("privatekey:") or lower.startswith("private key:"):
            private_key = line.split(":", 1)[1].strip()
        elif lower.startswith("password (publickey):") or lower.startswith("publickey:") or lower.startswith("public key:"):
            public_key = line.split(":", 1)[1].strip()
        elif lower.startswith("hash32:"):
            hash32 = line.split(":", 1)[1].strip()

    if not private_key or not public_key:
        raise RuntimeError("failed to parse xray x25519 output")

    return private_key, public_key, hash32


def build_v2rayn_link(
    uuid_value: str,
    host: str,
    port: int,
    public_key: str,
    short_id: str,
    sni: str,
    remark: str,
) -> str:
    query = {
        "encryption": "none",
        "security": "reality",
        "sni": sni,
        "fp": "chrome",
        "pbk": public_key,
        "sid": short_id,
        "flow": "xtls-rprx-vision",
        "type": "tcp",
    }
    return f"vless://{uuid_value}@{host}:{port}?{urlencode(query)}#{quote(remark)}"


def backup_config() -> Path:
    backup_dir = get_backup_dir()
    config_path = get_config_path()

    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = backup_dir / f"config-{stamp}.json"

    if config_path.exists():
        shutil.copy2(config_path, target)
    else:
        target.write_text("", encoding="utf-8")

    return target


def write_config(content: str) -> None:
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(content, encoding="utf-8")


def test_config() -> Tuple[bool, str]:
    config_path = get_config_path()
    r = run(["xray", "run", "-test", "-config", str(config_path)])
    return r.ok, r.text


def restart_xray() -> Tuple[bool, str]:
    if is_restart_disabled():
        return True, "RRH_DISABLE_RESTART=1, skipped systemctl restart xray."

    r = run(["systemctl", "restart", "xray"])
    return r.ok, r.text


def check_listen(port: int) -> str:
    r = run(["ss", "-tlnp"])
    if not r.ok:
        return r.text

    lines = [line for line in r.stdout.splitlines() if f":{port}" in line]
    return "\n".join(lines) if lines else f"No listener found on :{port}"


def test_tcp(host: str, port: int, timeout: float = 5.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def load_config() -> dict:
    return json.loads(get_config_path().read_text(encoding="utf-8"))


def save_config(data: dict) -> None:
    get_config_path().write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


def add_user(remark: str) -> str:
    data = load_config()
    new_id = generate_uuid()

    data["inbounds"][0]["settings"]["clients"].append({
        "id": new_id,
        "email": remark,
        "flow": "xtls-rprx-vision"
    })

    backup_config()
    save_config(data)
    return new_id


def generate_links_from_config(host: str, public_key: str) -> List[str]:
    data = load_config()
    inbound = data["inbounds"][0]
    port = inbound["port"]
    reality = inbound["streamSettings"]["realitySettings"]
    sni = reality["serverNames"][0]
    short_ids = reality.get("shortIds", ["aaa111"])
    users = inbound["settings"]["clients"]

    links = []
    for index, user in enumerate(users):
        sid = short_ids[min(index, len(short_ids) - 1)]
        links.append(
            build_v2rayn_link(
                user["id"],
                host,
                port,
                public_key,
                sid,
                sni,
                user.get("email", "reality-route")
            )
        )

    return links


def build_config_object(
    host: str,
    port: int,
    sni: str,
    loglevel: str,
    users: List[RealityUser],
    short_ids: List[str],
) -> Tuple[str, str, str, str]:
    private_key, public_key, hash32 = generate_x25519()

    cfg = RealityServerConfig(
        host=host,
        port=port,
        sni=sni,
        dest=f"{sni}:443",
        private_key=private_key,
        public_key=public_key,
        short_ids=short_ids,
        users=users,
        loglevel=loglevel,
    )

    return build_xray_reality_config(cfg), public_key, private_key, hash32

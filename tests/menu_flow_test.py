import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RRH_ENTRY = PROJECT_ROOT / "rrh.py"


SAMPLE_CONFIG = {
    "log": {
        "loglevel": "warning"
    },
    "inbounds": [
        {
            "listen": "0.0.0.0",
            "port": 8443,
            "protocol": "vless",
            "settings": {
                "clients": [
                    {
                        "id": "5130a623-31fc-4c21-a5eb-3a9805e243c9",
                        "email": "pc@reality",
                        "flow": "xtls-rprx-vision"
                    }
                ],
                "decryption": "none"
            },
            "streamSettings": {
                "network": "tcp",
                "security": "reality",
                "realitySettings": {
                    "show": False,
                    "dest": "www.cloudflare.com:443",
                    "xver": 0,
                    "serverNames": [
                        "www.cloudflare.com"
                    ],
                    "privateKey": "PRIVATE_KEY_EXAMPLE",
                    "shortIds": [
                        "aaa111",
                        "bbb222",
                        "ccc333"
                    ]
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


def run_cli_flow(name, user_input, env, expected_fragments):
    proc = subprocess.run(
        [sys.executable, str(RRH_ENTRY)],
        input=user_input,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(PROJECT_ROOT),
        env=env,
        timeout=30,
    )

    output = proc.stdout + "\n" + proc.stderr

    if proc.returncode != 0:
        print(output)
        raise AssertionError(f"{name}: process exited with code {proc.returncode}")

    for fragment in expected_fragments:
        if fragment not in output:
            print(output)
            raise AssertionError(f"{name}: expected fragment not found: {fragment}")

    print(f"[OK] {name}")


def build_env(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    env["RRH_CONFIG_PATH"] = str(tmp_path / "config.json")
    env["RRH_BACKUP_DIR"] = str(tmp_path / "backups")
    env["RRH_DISABLE_RESTART"] = "1"
    return env


def write_sample_config(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(SAMPLE_CONFIG, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return config_path


def test_client_menu_flow(tmp_path):
    env = build_env(tmp_path)

    user_input = "\n".join([
        "1",                              # 中文
        "2",                              # 客户端
        "1",                              # 扫描当前机器环境
        "2",                              # 查看可选方案路线
        "3",                              # 生成 v2rayN 一键导入链接
        "203.0.113.1",                   # Server IP
        "8443",                           # Port
        "5130a623-31fc-4c21-a5eb-3a9805e243c9",
        "PUBLIC_KEY_EXAMPLE",
        "aaa111",
        "www.cloudflare.com",
        "pc@reality",
        "4",                              # 测试 TCP 端口
        "203.0.113.1",
        "1",
        "5",                              # 退出客户端菜单
        "3",                              # 退出主菜单
        ""
    ])

    run_cli_flow(
        name="client_menu_flow",
        user_input=user_input,
        env=env,
        expected_fragments=[
            "Platform / 当前平台",
            "检测结果",
            "Xray / VLESS + Reality",
            "vless://5130a623-31fc-4c21-a5eb-3a9805e243c9@203.0.113.1:8443",
            "TcpTestSucceeded:",
        ],
    )


def test_server_menu_flow_non_destructive_without_xray(tmp_path):
    write_sample_config(tmp_path)
    env = build_env(tmp_path)

    # This flow intentionally avoids menu options that require real Xray:
    #   1. generate/apply config
    #   2. check xray config / listener
    #
    # It only verifies server-side menus that should work in sandbox mode:
    #   scan, route catalog, generate links from existing sandbox config, add user.
    user_input = "\n".join([
        "1",                              # 中文
        "1",                              # 服务器端
        "1",                              # 扫描当前机器环境
        "2",                              # 查看可选方案路线
        "3",                              # 进入 VLESS + Reality 路线
        "3",                              # 根据现有配置生成 v2rayN 链接
        "203.0.113.1",
        "PUBLIC_KEY_EXAMPLE",
        "4",                              # 新增用户 UUID
        "new-user@reality",
        "5",                              # 返回服务器菜单
        "4",                              # 退出服务器菜单
        "3",                              # 退出主菜单
        ""
    ])

    run_cli_flow(
        name="server_menu_flow_non_destructive_without_xray",
        user_input=user_input,
        env=env,
        expected_fragments=[
            "Platform / 当前平台",
            "检测结果",
            "Xray / VLESS + Reality",
            "vless://5130a623-31fc-4c21-a5eb-3a9805e243c9@203.0.113.1:8443",
            "New UUID / 新 UUID:",
        ],
    )

    data = json.loads((tmp_path / "config.json").read_text(encoding="utf-8"))
    clients = data["inbounds"][0]["settings"]["clients"]

    if len(clients) < 2:
        raise AssertionError("server menu flow should add one sandbox user")

    if not (tmp_path / "backups").exists():
        raise AssertionError("backup directory should exist after add-user flow")


def main():
    with tempfile.TemporaryDirectory(prefix="rrh-menu-test-") as tmp:
        tmp_path = Path(tmp)

        test_client_menu_flow(tmp_path)
        test_server_menu_flow_non_destructive_without_xray(tmp_path)

    print()
    print("All menu flow tests passed.")


if __name__ == "__main__":
    main()

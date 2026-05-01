import json
import os
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from reality_route_helper.core.models import RealityServerConfig, RealityUser
from reality_route_helper.templates.xray_config import build_xray_reality_config
from reality_route_helper.routes import vless_reality as vr
from reality_route_helper.platforms.detect import detect_platform
from reality_route_helper.routes.catalog import get_route_catalog


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def test_platform_detection():
    adapter = detect_platform()
    assert_true(adapter.name in {"windows", "linux", "macos"}, f"unexpected platform: {adapter.name}")


def test_route_catalog():
    routes = get_route_catalog()
    keys = [item.key for item in routes]
    assert_true("vless-reality" in keys, "vless-reality route missing")
    assert_true("outline" in keys, "outline route missing")


def test_v2rayn_link_generation():
    link = vr.build_v2rayn_link(
        uuid_value="5130a623-31fc-4c21-a5eb-3a9805e243c9",
        host="203.0.113.1",
        port=8443,
        public_key="PUBLIC_KEY_EXAMPLE",
        short_id="aaa111",
        sni="www.cloudflare.com",
        remark="pc@reality",
    )

    assert_true(link.startswith("vless://"), "link should start with vless://")
    assert_true("@203.0.113.1:8443" in link, "host/port missing")
    assert_true("security=reality" in link, "reality security missing")
    assert_true("sid=aaa111" in link, "shortId missing")
    assert_true("flow=xtls-rprx-vision" in link, "flow missing")


def test_config_template_and_sandbox_io():
    with tempfile.TemporaryDirectory(prefix="rrh-test-") as tmp:
        tmp_path = Path(tmp)
        config_path = tmp_path / "config.json"
        backup_dir = tmp_path / "backups"

        os.environ["RRH_CONFIG_PATH"] = str(config_path)
        os.environ["RRH_BACKUP_DIR"] = str(backup_dir)
        os.environ["RRH_DISABLE_RESTART"] = "1"

        cfg = RealityServerConfig(
            host="203.0.113.1",
            port=8443,
            sni="www.cloudflare.com",
            dest="www.cloudflare.com:443",
            private_key="PRIVATE_KEY_EXAMPLE",
            public_key="PUBLIC_KEY_EXAMPLE",
            short_ids=["aaa111", "bbb222"],
            users=[
                RealityUser(
                    uuid="5130a623-31fc-4c21-a5eb-3a9805e243c9",
                    remark="pc@reality",
                )
            ],
            loglevel="warning",
        )

        content = build_xray_reality_config(cfg)
        vr.write_config(content)

        assert_true(config_path.exists(), "sandbox config was not written")

        data = json.loads(config_path.read_text(encoding="utf-8"))
        assert_true(data["inbounds"][0]["port"] == 8443, "port mismatch")
        assert_true(
            data["inbounds"][0]["streamSettings"]["realitySettings"]["shortIds"][0] == "aaa111",
            "shortId mismatch",
        )

        backup_file = vr.backup_config()
        assert_true(backup_file.exists(), "backup file was not created")

        links = vr.generate_links_from_config("203.0.113.1", "PUBLIC_KEY_EXAMPLE")
        assert_true(len(links) == 1, "link count mismatch")
        assert_true(links[0].startswith("vless://"), "generated link invalid")

        ok, restart_msg = vr.restart_xray()
        assert_true(ok, "restart should be skipped successfully")
        assert_true("skipped" in restart_msg.lower(), "restart skip message missing")


def main():
    tests = [
        test_platform_detection,
        test_route_catalog,
        test_v2rayn_link_generation,
        test_config_template_and_sandbox_io,
    ]

    for test in tests:
        test()
        print(f"[OK] {test.__name__}")

    print()
    print("All smoke tests passed.")


if __name__ == "__main__":
    main()

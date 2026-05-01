from .i18n import t
from .platforms.detect import detect_platform
from .scanners.service_scanner import scan_services
from .routes.catalog import get_route_catalog
from .routes import vless_reality as vr
from .core.models import RealityUser


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def ask_int(prompt: str, default: int) -> int:
    while True:
        raw = ask(prompt, str(default))
        try:
            return int(raw)
        except ValueError:
            print("Please enter a number / 请输入数字")


def confirm(prompt: str, default: bool = False) -> bool:
    suffix = "Y/n" if default else "y/N"
    raw = input(f"{prompt} [{suffix}]: ").strip().lower()
    if not raw:
        return default
    return raw in {"y", "yes", "是", "好", "确认"}


def choose(items):
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")
    while True:
        raw = input("> ").strip()
        try:
            idx = int(raw)
            if 1 <= idx <= len(items):
                return idx
        except ValueError:
            pass
        print("Invalid input / 输入无效")


def choose_lang():
    print("1. 中文")
    print("2. English")
    return "en" if input("> ").strip() == "2" else "zh"


def print_dict(title, data):
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)
    for k, v in data.items():
        print(f"{k}: {v}")
    print("=" * 80)


def scan_current(lang):
    data = scan_services()
    print_dict(t(lang, "detected"), data)


def show_routes(lang):
    print()
    for item in get_route_catalog():
        desc = item.description_en if lang == "en" else item.description_zh
        print(f"- {item.name}")
        print(f"  key: {item.key}")
        print(f"  difficulty: {item.difficulty}")
        print(f"  status: {item.status}")
        print(f"  {desc}")
        print()


def vless_server_generate(lang):
    adapter = detect_platform()
    if not adapter.can_server_deploy():
        print(t(lang, "not_supported"))
        print(adapter.test_tcp_hint())
        return

    if not vr.command_exists("xray"):
        print("xray not found. Please install Xray first. / 未检测到 xray，请先安装 Xray。")
        return

    host = ask("VPS IP / 服务器 IP")
    port = ask_int("Port / 端口", 8443)
    sni = ask("SNI / serverName", "www.cloudflare.com")
    count = ask_int("User count / 用户数量", 3)
    short_ids = [x.strip() for x in ask("shortIds comma separated / shortId 逗号分隔", "aaa111,bbb222,ccc333").split(",") if x.strip()]
    loglevel = ask("Log level / 日志级别", "warning")

    users = []
    for i in range(count):
        remark = ask(f"User {i+1} remark / 用户{i+1}备注", f"user{i+1}@reality")
        users.append(RealityUser(uuid=vr.generate_uuid(), remark=remark))

    content, public_key, private_key, hash32 = vr.build_config_object(
        host=host,
        port=port,
        sni=sni,
        loglevel=loglevel,
        users=users,
        short_ids=short_ids,
    )

    print()
    print("Generated server config / 生成的服务端配置:")
    print(content)

    print("PublicKey for clients / 客户端 PublicKey:")
    print(public_key)

    print("Hash32 is not used / Hash32 不需要配置:")
    print(hash32)

    print()
    print("v2rayN links / v2rayN 链接:")
    for idx, user in enumerate(users):
        sid = short_ids[min(idx, len(short_ids) - 1)]
        print(vr.build_v2rayn_link(user.uuid, host, port, public_key, sid, sni, user.remark))

    if confirm("Write config to server? / 是否写入服务器配置？", False):
        backup = vr.backup_config()
        print(f"Backup / 备份: {backup}")
        vr.write_config(content)
        ok, output = vr.test_config()
        print(output)
        if not ok:
            print("Config test failed / 配置测试失败")
            return
        if confirm("Restart Xray now? / 是否立即重启 Xray？", True):
            ok, output = vr.restart_xray()
            print(output)
            print(vr.check_listen(port))


def vless_server_check(lang):
    adapter = detect_platform()
    if not adapter.can_server_deploy():
        print(t(lang, "not_supported"))
        return

    ok, output = vr.test_config()
    print(output)
    print("Configuration OK" if ok else "Configuration failed")
    port = ask_int("Port to check / 要检查的端口", 8443)
    print(vr.check_listen(port))


def vless_add_user(lang):
    remark = ask("New user remark / 新用户备注", "new-user@reality")
    try:
        uid = vr.add_user(remark)
        print("New UUID / 新 UUID:")
        print(uid)
        ok, output = vr.test_config()
        print(output)
        if ok and confirm("Restart Xray now? / 是否重启 Xray？", True):
            vr.restart_xray()
    except Exception as exc:
        print(f"Failed / 失败: {exc}")


def vless_generate_links(lang):
    host = ask("VPS IP / 服务器 IP")
    public_key = ask("PublicKey / 客户端 PublicKey")
    try:
        links = vr.generate_links_from_config(host, public_key)
    except Exception as exc:
        print(f"Failed / 失败: {exc}")
        return
    for link in links:
        print(link)


def client_link(lang):
    host = ask("Server IP / 服务器 IP")
    port = ask_int("Port / 端口", 8443)
    uid = ask("UUID")
    public_key = ask("PublicKey")
    short_id = ask("shortId", "aaa111")
    sni = ask("SNI / serverName", "www.cloudflare.com")
    remark = ask("Remark / 备注", "reality-route")
    print(vr.build_v2rayn_link(uid, host, port, public_key, short_id, sni, remark))


def client_port(lang):
    host = ask("Server IP / 服务器 IP")
    port = ask_int("Port / 端口", 8443)
    print("TcpTestSucceeded:", vr.test_tcp(host, port))
    print(detect_platform().test_tcp_hint())


def vless_server_menu(lang):
    while True:
        print()
        items = [
            t(lang, "gen_apply"),
            t(lang, "check"),
            t(lang, "gen_links"),
            t(lang, "add_user"),
            t(lang, "back"),
        ]
        choice = choose(items)
        if choice == 1:
            vless_server_generate(lang)
        elif choice == 2:
            vless_server_check(lang)
        elif choice == 3:
            vless_generate_links(lang)
        elif choice == 4:
            vless_add_user(lang)
        else:
            return


def server_menu(lang):
    while True:
        print()
        items = [
            t(lang, "scan"),
            t(lang, "routes"),
            t(lang, "vless_route"),
            t(lang, "exit"),
        ]
        choice = choose(items)
        if choice == 1:
            scan_current(lang)
        elif choice == 2:
            show_routes(lang)
        elif choice == 3:
            vless_server_menu(lang)
        else:
            return


def client_menu(lang):
    while True:
        print()
        items = [
            t(lang, "scan"),
            t(lang, "routes"),
            t(lang, "client_link"),
            t(lang, "client_port"),
            t(lang, "exit"),
        ]
        choice = choose(items)
        if choice == 1:
            scan_current(lang)
        elif choice == 2:
            show_routes(lang)
        elif choice == 3:
            client_link(lang)
        elif choice == 4:
            client_port(lang)
        else:
            return


def main():
    print("=== Reality Route Helper ===")
    lang = choose_lang()
    adapter = detect_platform()
    print(f"Platform / 当前平台: {adapter.name}")

    if adapter.name == "windows":
        print(t(lang, "windows_hint"))
    elif adapter.name == "linux":
        print(t(lang, "linux_hint"))

    while True:
        print()
        items = [
            t(lang, "server"),
            t(lang, "client"),
            t(lang, "exit"),
        ]
        choice = choose(items)
        if choice == 1:
            server_menu(lang)
        elif choice == 2:
            client_menu(lang)
        else:
            break


if __name__ == "__main__":
    main()

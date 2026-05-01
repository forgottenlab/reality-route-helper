from dataclasses import dataclass
from typing import List


@dataclass
class RouteOption:
    key: str
    name: str
    difficulty: str
    status: str
    description_zh: str
    description_en: str


def get_route_catalog() -> List[RouteOption]:
    return [
        RouteOption(
            key="vless-reality",
            name="Xray / VLESS + Reality",
            difficulty="medium",
            status="implemented",
            description_zh="当前第一版重点实现。适合个人 VPS，隐蔽性和可控性较好，但需要理解 UUID、Reality Key、shortId。",
            description_en="Implemented in the first version. Good for personal VPS. Requires understanding UUID, Reality key, and shortId.",
        ),
        RouteOption(
            key="outline",
            name="Outline / Shadowsocks",
            difficulty="easy",
            status="detect-only",
            description_zh="易用，有 Outline Manager，但协议能力和可控性与 Xray 不同。当前仅扫描检测，不接管。",
            description_en="Easy to use with Outline Manager. Currently detect-only, not managed by this tool.",
        ),
        RouteOption(
            key="hysteria2",
            name="Hysteria2",
            difficulty="medium",
            status="planned",
            description_zh="基于 QUIC/UDP，适合部分高延迟线路。后续可作为扩展路线。",
            description_en="QUIC/UDP based route. Planned for future extension.",
        ),
        RouteOption(
            key="tuic",
            name="TUIC",
            difficulty="medium",
            status="planned",
            description_zh="基于 QUIC 的代理方案，后续可扩展。",
            description_en="QUIC-based proxy route. Planned for future extension.",
        ),
        RouteOption(
            key="sing-box",
            name="sing-box",
            difficulty="medium",
            status="planned",
            description_zh="现代统一代理核心，可作为后续客户端/服务端统一方案。",
            description_en="Modern unified proxy core. Planned for future extension.",
        ),
        RouteOption(
            key="panel",
            name="3x-ui / Marzban / Hiddify",
            difficulty="easy-medium",
            status="planned",
            description_zh="网页管理方便，但会带来额外面板安全风险。后续可做检测与建议。",
            description_en="Web panels are convenient but add management-plane risks. Planned as advisory/detection.",
        ),
    ]

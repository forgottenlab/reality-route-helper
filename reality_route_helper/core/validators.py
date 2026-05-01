import re


def is_uuid(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-fA-F-]{36}", value.strip()))


def is_short_id(value: str) -> bool:
    value = value.strip()
    return bool(re.fullmatch(r"[0-9a-fA-F]{0,16}", value)) and len(value) % 2 == 0


def is_port(value: int) -> bool:
    return 1 <= int(value) <= 65535

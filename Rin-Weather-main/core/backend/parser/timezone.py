from datetime import datetime, timedelta, timezone, tzinfo
import re


def parse_timezone_abbr(tz_abbr: str) -> timezone | tzinfo | None:
    """
    简单解析类似 GMT+8 的时区缩写，返回对应 timezone 对象
    不支持复杂时区名称，只针对 GMT±数字 格式
    """
    match = re.match(r"GMT([+-])(\d+)", tz_abbr)
    if match:
        sign, hours = match.groups()
        offset_hours = int(hours)
        if sign == '-':
            offset_hours = -offset_hours
        return timezone(timedelta(hours=offset_hours))
    # 默认返回本地时区（无偏移）
    return datetime.now().astimezone().tzinfo

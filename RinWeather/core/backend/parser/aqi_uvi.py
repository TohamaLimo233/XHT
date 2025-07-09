from datetime import datetime
from .timezone import parse_timezone_abbr


def get_current_aqi(hourly: dict, aqis: dict, timezone_abbreviation: str = None) -> float:
    """
    从 hourly 数据中获取当前本地小时的 AQI 值
    """
    # 解析时区
    tz = parse_timezone_abbr(timezone_abbreviation) if timezone_abbreviation else datetime.now().astimezone().tzinfo

    now_local = datetime.now(tz).replace(minute=0, second=0, microsecond=0)
    now_str = now_local.strftime("%Y-%m-%dT%H:%M")

    try:
        index = hourly["time"].index(now_str)
        aqi = aqis[index]
        return round(aqi, 1)
    except (ValueError, KeyError, IndexError):
        return -1  # 未找到对应时间


def get_current_uvi(hourly: dict, timezone_abbreviation: str = None) -> float:
    """
    从 hourly 数据中获取当前本地小时的 UVI 值
    """
    # 解析时区
    tz = parse_timezone_abbr(timezone_abbreviation) if timezone_abbreviation else datetime.now().astimezone().tzinfo

    now_local = datetime.now(tz).replace(minute=0, second=0, microsecond=0)
    now_str = now_local.strftime("%Y-%m-%dT%H:%M")

    try:
        index = hourly["time"].index(now_str)
        uvi = hourly["uv_index"][index]
        return round(uvi, 1)
    except (ValueError, KeyError, IndexError):
        return -1  # 未找到对应时间
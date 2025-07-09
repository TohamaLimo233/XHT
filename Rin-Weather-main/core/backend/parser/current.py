from datetime import datetime
from typing import Optional

from .timezone import parse_timezone_abbr


def get_current_precipitation(daily: dict, units: dict = None, timezone_abbreviation: str = None) -> str:
    """
    从 daily 数据中获取当前的 降雨量
    """
    if units is None:
        units = {
            "temperature_2m_max": "°C",
            "temperature_2m_min": "°C",
            "precipitation_sum": "mm",
        }

    # 解析时区
    tz = parse_timezone_abbr(timezone_abbreviation) if timezone_abbreviation else datetime.now().astimezone().tzinfo

    now_local = datetime.now(tz).replace(minute=0, second=0, microsecond=0)
    now_str = now_local.strftime("%Y-%m-%d")

    try:
        index = daily["time"].index(now_str)
        precipitation = daily["precipitation_sum"][index]
        return f"{round(precipitation)} {units['precipitation_sum']}"
    except (ValueError, KeyError, IndexError):
        return "Not Available"  # 未找到对应时间


def get_current_sunrise_sunset(daily: dict) -> list[str]:
    """
    获取今天的日出和日落时间（本地时间，已由API处理），返回 ["HH:mm", "HH:mm"]
    """
    # 今天日期字符串
    today_str = datetime.now().strftime("%Y-%m-%d")

    try:
        index = daily["time"].index(today_str)
        sunrise_str = daily["sunrise"][index]
        sunset_str = daily["sunset"][index]

        sunrise_time = datetime.fromisoformat(sunrise_str).strftime("%H:%M")
        sunset_time = datetime.fromisoformat(sunset_str).strftime("%H:%M")

        return [sunrise_time, sunset_time]
    except (ValueError, KeyError, IndexError):
        return ["Not Available", "Not Available"]


def get_current_hour(timezone_abbreviation: Optional[str] = None) -> float:
    """
    获取当前小时，返回形如 14.5（14点30分）的浮点数
    """
    # 解析时区（你已有 parse_timezone_abbr 可用）
    tz = parse_timezone_abbr(timezone_abbreviation) if timezone_abbreviation else datetime.now().astimezone().tzinfo

    now_local = datetime.now(tz)
    hour_float = now_local.hour + now_local.minute / 60.0

    return round(hour_float, 4)  # 保留4位小数，视需求调整


def get_current_apparent_temperature(hourly: dict, timezone_abbreviation: str = None) -> str:
    """
    从 hourly 数据中获取当前的 体感温度
    """

    # 解析时区
    tz = parse_timezone_abbr(timezone_abbreviation) if timezone_abbreviation else datetime.now().astimezone().tzinfo

    now_local = datetime.now(tz).replace(minute=0, second=0, microsecond=0)
    now_str = now_local.strftime("%Y-%m-%dT%H:%M")

    try:
        index = hourly["time"].index(now_str)
        apparent_temperature = hourly["apparent_temperature"][index]
        return f"{round(apparent_temperature)}"
    except (ValueError, KeyError, IndexError):
        return "Not Available"  # 未找到对应时间


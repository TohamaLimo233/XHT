from datetime import datetime, timezone
from .timezone import parse_timezone_abbr
import platform


def parse_hourly_data(hourly: dict, units: dict = None, timezone_abbreviation: str = None) -> list:
    if units is None:
        units = {
            "temperature_2m": "°C",
            "precipitation": "mm",
            "cloudcover": "%",
            "windspeed_10m": "m/s",
            "apparent_temperature": "°C"
        }

    # 解析时区
    tz = parse_timezone_abbr(timezone_abbreviation) if timezone_abbreviation else datetime.now().astimezone().tzinfo

    result = []

    # 当前本地整点时间，带时区
    now = datetime.now(tz).replace(minute=0, second=0, microsecond=0)

    time_format = "%#I %p" if platform.system() == "Windows" else "%-I %p"

    entries = []
    for i in range(min(len(hourly["time"]), 48)):
        # 转为带 UTC 时区的 datetime 对象
        utc_time = datetime.strptime(hourly["time"][i], "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
        # 转成本地时间，带解析的时区 tz
        local_time = utc_time.astimezone(tz)

        entries.append({
            "time_obj": local_time,
            "code": hourly["weathercode"][i],
            "temperature": round(hourly["temperature_2m"][i]),
            "apparent_temperature": round(hourly["apparent_temperature"][i]),
            "precipitation": round(hourly.get("precipitation", [0])[i], 1)
        })

    # 过滤未来24小时，从当前时间开始（时区已正确）
    filtered = [entry for entry in entries if entry["time_obj"] >= now][:24]

    for entry in filtered:
        t = entry["time_obj"]
        is_now = t == now
        hour_label = "<b>Now</b>" if is_now else t.strftime(time_format)

        precip_val = entry["precipitation"]
        precip_str = None if precip_val == 0 else f"{precip_val} {units.get('precipitation', '')}"  # 降水

        result.append({
            "time": hour_label,
            "code": entry["code"],
            "temperature": f"{entry['temperature']}",  # 单位 {units.get('temperature_2m', '')}
            "apparent_temperature": f"{entry['apparent_temperature']}",
            "precipitation": f"{precip_str}"
        })

    return result


def parse_daily_data(daily: dict, units: dict = None) -> list:
    result = []

    if units is None:
        units = {
            "temperature_2m_max": "°C",
            "temperature_2m_min": "°C",
            "precipitation_sum": "mm",
        }

    for i in range(len(daily["time"])):
        date_str = daily["time"][i]
        code = daily["weathercode"][i]
        h_temp = round(daily["temperature_2m_max"][i])
        l_temp = round(daily["temperature_2m_min"][i])
        precipitation = daily["precipitation_sum"][i]

        precipitation_str = None if precipitation == 0 \
            else f"{round(precipitation, 1)} {units.get('precipitation_sum', '')}"

        result.append({
            "time": datetime.strptime(date_str, "%Y-%m-%d").strftime("%A"),
            "code": code,
            "h_temp": f"{h_temp}",
            "l_temp": f"{l_temp}",
            "temperature": f"{round((h_temp + l_temp) / 2)}",
            "precipitation": precipitation_str
        })

    return result

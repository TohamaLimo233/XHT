import requests
from typing import Optional, Dict, Any
from core import DEFAULT_CONFIG
import core.backend.parser as parser
from loguru import logger
from datetime import datetime, timedelta

from PySide6.QtCore import QObject, Slot, QDateTime, QTimer, Signal, QThread

from core.backend.config import WeatherConfig

default_proxies = {
    "http": None,
    "https": None
}


class WeatherRequester:
    """
    天气请求
    """

    def __init__(self, config: WeatherConfig):
        """
        初始化请求
        :param config:
        """
        super().__init__()
        self.config = config or DEFAULT_CONFIG
        self.current_city = self.config["weather"]["current_city"] \
            if self.config["weather"]["current_city"] > len(self.config["weather"]["cities"]) else 0

        self.city_config = {
            "name": self.config["weather"]["cities"][self.current_city]["name"],
            "latitude": self.config["weather"]["cities"][self.current_city]["latitude"],
            "longitude": self.config["weather"]["cities"][self.current_city]["longitude"]
        }

        # units
        self.temp_unit = None
        self.windspeed_unit = None
        self.precipitation_unit = None
        self.load_configs()

        # API URL
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.aqi_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        self.result = {}
        self.date = None

        # 缓存
        self.cache_expiration = (timedelta(minutes=self.config["network"].get("cache_expiration"))
                                 or timedelta(minutes=10))
        self.last_fetch_time = None
        self.last_location = None
        self.cache = {}

    def load_configs(self):
        self.temp_unit = self.config["weather"]["temp_unit"]  # 单位
        self.windspeed_unit = self.config["weather"]["windspeed_unit"]
        self.precipitation_unit = self.config["weather"]["precipitation_unit"]

    def set_location(self, location: Dict[str, Any]):
        self.city_config = location

    def fetch_weather(self, proxies=default_proxies):
        loc = f"{self.city_config['latitude']},{self.city_config['longitude']}"
        now = datetime.now()

        if loc in self.cache:
            cache_entry = self.cache[loc]
            if now - cache_entry["timestamp"] < self.cache_expiration:
                logger.info(f"Returning cached: {loc}")
                return cache_entry["data"]

        self.load_configs()
        params = {
            "latitude": self.city_config["latitude"],  # 纬度
            "longitude": self.city_config["longitude"], "current_weather": True,  # 经度
            "temperature_unit": self.temp_unit,  # or "fahrenheit"
            "windspeed_unit": self.windspeed_unit,  # or "kmh", "mph", "kn"
            "precipitation_unit": self.precipitation_unit,  # or "inch"
            "timezone": "auto",
            "hourly": ",".join([
                "temperature_2m", "weathercode", "precipitation",
                "cloudcover", "windspeed_10m", "apparent_temperature",
                "uv_index"
            ]),
            "forecast_days": 7,
            "daily": ",".join([
                "temperature_2m_max", "temperature_2m_min", "weathercode",
                "precipitation_sum", "sunrise", "sunset",  # 日升日落时间
            ])

        }

        aqi_params = {
            "latitude": self.city_config["latitude"],
            "longitude": self.city_config["longitude"],
            "hourly": "european_aqi",
            "timezone": "auto"
        }

        try:
            logger.info("正在请求天气数据…")
            res = requests.get(self.base_url, params=params, timeout=5, proxies=proxies)
            aqi_res = requests.get(self.aqi_url, params=aqi_params, timeout=5, proxies=proxies)
            print("请求URL:", res.url)
            print("AQI请求URL:", aqi_res.url)
            res.raise_for_status()
            aqi_res.raise_for_status()

            result = self.parse_weather(res.json(), aqi_res.json())

            # cache update
            self.cache[loc] = {
                "data": result,
                "timestamp": now
            }

            return result
        except requests.exceptions.Timeout as e:
            logger.error("请求超时，请检查网络连接")
            return e
        except requests.RequestException as e:
            logger.error(f"请求失败：{e}")
            return e
        except Exception as e:
            logger.error(f"未知错误：{e}")
            return e

    def parse_weather(self, data: Dict[str, Any], aqi_data: Dict[str, Any]) -> Dict[str, Any]:
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info("已获取")
        aqi = aqi_data["hourly"].get("european_aqi", [])
        data["aqi"] = aqi
        return data

    def clean_cache(self):
        self.cache = {}


class WeatherManager(QObject):
    weatherUpdated = Signal()
    weatherUpdatedFailed = Signal(str)
    refreshRequested = Signal()  # 添加一个信号用于跨线程触发

    def __init__(self, config: Optional = None, parent=None):
        super().__init__(parent)
        self.weather_data = None
        self.config = config
        self.requester = WeatherRequester(self.config)

        # 创建线程 + worker
        self.thread = QThread(self)
        self.worker = WeatherWorker(self.requester, self.config)
        self.worker.moveToThread(self.thread)

        # 信号连接
        self.refreshRequested.connect(self.worker.fetch)
        self.worker.finished.connect(self._onWeatherDataReceived)
        self.worker.error.connect(self._onWeatherError)
        self.config.dataUpdated.connect(self.requester.clean_cache)

        self.thread.start()

        # 定时器刷新
        self.timer = QTimer(self)
        self.timer.setInterval(60 * 60 * 1000)
        self.timer.timeout.connect(self.refreshWeather)
        self.timer.start()

    def cleanup(self):
        self.timer.stop()
        self.worker.deleteLater()
        self.thread.terminate()
        self.thread.quit()

    @Slot(dict)
    def setLocation(self, location: Dict[str, Any]):
        self.requester.set_location(location)

    @Slot()
    def refreshWeather(self):
        self.refreshRequested.emit()

    def _onWeatherDataReceived(self, data):
        self.weather_data = data
        self.weatherUpdated.emit()
        logger.info(f"天气数据更新于 {self.requester.date}")

    def _onWeatherError(self, error):
        self.weatherUpdatedFailed.emit(error)
        logger.warning(f"天气获取失败：{error}")

    @Slot(result=dict)
    def getUnits(self):
        units = {
            "current_weather_units":
                self.weather_data.get("current_weather_units") if self.weather_data else {},
            "hourly_units":
                self.weather_data.get("hourly_units") if self.weather_data else {},
            "daily_units":
                self.weather_data.get("daily_units") if self.weather_data else {}
        }
        return units

    @Slot(result=str)
    def getCity(self):
        return self.requester.city_config["name"] or "Unknown"

    @Slot(result=float)
    def getCurrentHour(self) -> float:
        return parser.get_current_hour(self.weather_data.get("timezone_abbreviation")) if self.weather_data else 13

    @Slot(result=list)
    def getCurrentSunriseSunset(self) -> list:
        return parser.get_current_sunrise_sunset(
            self.weather_data.get("daily")) if self.weather_data else []

    @Slot(result=dict)
    def getCurrentWeather(self):
        result = self.weather_data.get("current_weather") if self.weather_data else {}
        result["city"] = self.getCity()
        return result

    @Slot(result=list)
    def getCurrentTemperatures(self) -> list:
        result = self.weather_data.get("daily") if self.weather_data else []
        h_temp = int(result.get("temperature_2m_max")[0])
        l_temp = int(result.get("temperature_2m_min")[0])
        return [h_temp, l_temp]

    @Slot(result=int)
    def getCurrentAQI(self) -> int:
        return parser.get_current_aqi(
            self.weather_data.get("hourly"),
            self.weather_data.get("aqi"),
            self.weather_data.get("timezone_abbreviation")
        ) if self.weather_data else 0

    @Slot(result=int)
    def getCurrentUVI(self):
        return parser.get_current_uvi(
            self.weather_data.get("hourly"), self.weather_data.get("timezone_abbreviation")
        ) if self.weather_data else 0

    @Slot(result=str)
    def getCurrentApparentTemperature(self):
        return parser.get_current_apparent_temperature(
            self.weather_data.get("hourly"), self.weather_data.get("timezone_abbreviation")
        ) if self.weather_data else 0

    @Slot(result=str)
    def getCurrentPrecipitation(self):
        return parser.get_current_precipitation(
            self.weather_data.get("daily"),
            self.weather_data.get("daily_units"),
            self.weather_data.get("timezone_abbreviation")
        ) if self.weather_data else "Unknown"

    @Slot(result=list)
    def getHoursForecast(self):
        return parser.parse_hourly_data(
            self.weather_data.get("hourly"),
            self.weather_data.get("hourly_units"),
            self.weather_data.get("timezone_abbreviation")
        ) if self.weather_data else []

    @Slot(result=list)
    def getDaysForecast(self):
        return parser.parse_daily_data(
            self.weather_data.get("daily"), self.weather_data.get("daily_units")
        ) if self.weather_data else []

    @Slot(result=dict)
    def getHoursData(self):
        return self.weather_data.get("hourly") if self.weather_data else {}

    @Slot(result=dict)
    def getDaysData(self):
        return self.weather_data.get("daily") if self.weather_data else {}

    @Slot(result=str)
    def getLastUpdateTime(self):
        return self.requester.date or QDateTime.currentDateTime().toString()


class WeatherWorker(QObject):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, requester: WeatherRequester, config: WeatherConfig):
        super().__init__()
        self.requester = requester
        self.config = config

    @Slot()
    def fetch(self):
        try:
            result = self.requester.fetch_weather(proxies=self.config.getProxies())
            if isinstance(result, dict):
                self.finished.emit(result)
            else:
                self.error.emit(result)
        except Exception as e:
            self.error.emit(str(e))


if __name__ == "__main__":
    center = WeatherRequester()
    print(center.fetch_weather())

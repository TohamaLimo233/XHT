from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, Slot, Signal, QLocale, QTranslator
from PySide6.QtWidgets import QApplication
from loguru import logger

from assets import ROOT_PATH, ASSETS_PATH
from RinUI import ConfigManager, RinUITranslator


DEV_MODE = False
DEFAULT_CONFIG = {
    "weather": {
        "API_KEY": "",
        "temp_unit": "celsius",  # or "fahrenheit"
        "windspeed_unit": "ms",  # or "kmh", "mph", "kn"
        "precipitation_unit": "mm",  # or "in"

        "current_city": 0,

        "cities": [
            {
                "name": "北京",
                "latitude": 39.9042,
                "longitude": 116.4074,
            },
            {
                "name": "Washington DC",
                "latitude": 38.89511,
                "longitude": -77.03637
            }
        ]
    },
    "network": {
        "proxy": {
            "http": None,
            "https": None
        },
        "cache_expiration": 10,
    },
    "locale": {
        # "language": "en_US",
        "language": QLocale.system().name(),
    }
}


class WeatherConfig(ConfigManager, QObject):
    dataUpdated = Signal()

    def __init__(self, parent = None):
        self.translator = None
        self.ui_translator = None
        path = ROOT_PATH
        filename = "config.json"
        self.parent = parent

        ConfigManager.__init__(self, path, filename)
        QObject.__init__(self)

        if DEV_MODE:
            self.config = DEFAULT_CONFIG
        else:
            self.load_config(DEFAULT_CONFIG)

    def _set_config(self, keys: list[str], value: Any) -> None:
        """
        通用配置更新方法，通过键路径（list[str]）更新配置并触发保存和 UI 更新。
        """
        d = self.config
        for key in keys[:-1]:
            d = d.setdefault(key, {})  # 如果中间节点不存在就创建
        last_key = keys[-1]
        if d.get(last_key) == value:
            return
        d[last_key] = value
        self.dataUpdated.emit()
        self.save_config()

    # i18n
    @Slot(result=str)
    def getLanguage(self) -> str:
        return self.config["locale"]["language"]

    @Slot(result=str)
    def getSystemLanguage(self):
        return QLocale.system().name()

    @Slot(str)
    def setLanguage(self, language: str) -> None:
        lang_path = Path(ASSETS_PATH / "locales" / f"{language}.qm")
        if not lang_path.exists():  # fallback
            print(f"Language file {lang_path} not found. Fallback to default (en_US)")
            language = "en_US"

        self.config["locale"]["language"] = language
        self.save_config()
        self.ui_translator = RinUITranslator(QLocale(language))
        self.translator = QTranslator()
        self.translator.load(lang_path.as_posix())
        QApplication.instance().removeTranslator(self.ui_translator)
        QApplication.instance().removeTranslator(self.translator)
        QApplication.instance().installTranslator(self.ui_translator)
        QApplication.instance().installTranslator(self.translator)
        self.parent.engine.retranslate()

        self.dataUpdated.emit()

    # 设置
    @Slot(result=str)
    def getTempUnit(self) -> str:
        return self.config["weather"]["temp_unit"]

    @Slot(str)
    def setTempUnit(self, unit: str) -> None:
        self._set_config(["weather", "temp_unit"], unit)

    @Slot(result=str)
    def getWindspeedUnit(self) -> str:
        return self.config["weather"]["windspeed_unit"]

    @Slot(str)
    def setWindspeedUnit(self, unit: str) -> None:
        self._set_config(["weather", "windspeed_unit"], unit)

    @Slot(result=str)
    def getPrecipitationUnit(self) -> str:
        return self.config["weather"]["precipitation_unit"]

    @Slot(str)
    def setPrecipitationUnit(self, unit: str) -> None:
        self._set_config(["weather", "precipitation_unit"], unit)

    @Slot(result=int)
    def getCacheExpiration(self) -> int:
        return self.config["network"]["cache_expiration"]

    @Slot(int)
    def setCacheExpiration(self, expiration: int) -> None:
        self._set_config(["network", "cache_expiration"], expiration)

    @Slot(result=dict)
    def getProxies(self) -> dict:
        return self.config["network"]["proxy"]

    @Slot(dict)
    def setProxies(self, proxy: dict) -> None:
        if proxy == self.config["network"]["proxy"]:
            return
        self.config["network"]["proxy"]["http"] = proxy["http"]
        self.config["network"]["proxy"]["https"] = proxy["https"]
        self.save_config()

    # 城市管理
    @Slot(result=list)
    def getCities(self) -> list:
        return self.config["weather"]["cities"]

    @Slot(str, float, float)
    def addCity(self, name: str, latitude: float, longitude: float) -> None:
        cities = self.config["weather"]["cities"]
        cities.append({
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
        })
        self.dataUpdated.emit()
        self.save_config()

    @Slot(int)
    def removeCity(self, key: int) -> None:
        cities = self.config["weather"]["cities"]
        if len(cities) <= 1:
            logger.warning("Cannot remove the last city.")
            return

        cities.pop(key)
        self.dataUpdated.emit()
        self.save_config()

    @Slot(int)
    def setCurrentCity(self, index: int) -> None:
        if 0 <= index < len(self.config["weather"]["cities"]):
            self.config["weather"]["current_city"] = index
            self.dataUpdated.emit()
            self.save_config()
        else:
            raise IndexError("Index out of range for current city.")

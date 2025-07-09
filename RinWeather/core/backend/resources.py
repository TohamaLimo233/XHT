import json
from pathlib import Path
from PySide6.QtCore import QObject, Slot, QCoreApplication

from core import ASSETS_PATH


def qsTr(context: str, text: str) -> str:
    """统一翻译接口，传入上下文和文本，返回翻译结果"""
    return QCoreApplication.translate(context, text)


class WeatherResourceManager(QObject):
    def __init__(self):
        super().__init__()
        self.weather_data = {}
        self.aqi_data = {}
        self.uvi_data = {}

        self.weather_data = self.load_json_data(Path(ASSETS_PATH / "resources" / "configs" / "weather_code.json"))
        self.aqi_data = self.load_json_data(Path(ASSETS_PATH / "resources" / "configs" / "aqi.json"))
        self.uvi_data = self.load_json_data(Path(ASSETS_PATH / "resources" / "configs" / "uvi.json"))

    @Slot(int, result=str)
    def getWeatherImage(self, code: int, night: bool = False) -> str:
        if str(code) in self.weather_data:
            return self.weather_data[str(code)]["night" if night else "day"]["image"]
        else:
            return Path(ASSETS_PATH / "resources" / "images" / "weather" / "unavailable.svg").as_uri()

    @Slot(int, result=str)
    def getWeatherDescription(self, code: int, night: bool = False) -> str:
        if str(code) in self.weather_data:
            desc = self.weather_data[str(code)]["night" if night else "day"]["description"]
            return qsTr("WeatherDescriptions", desc)
        else:
            return qsTr("WeatherDescriptions", "Unknown")

    @Slot(int, result=str)
    def getUVICategory(self, code: int) -> str:
        for level, value in self.uvi_data.items():
            min_level, max_level = level.split("-")
            if int(min_level) <= code <= int(max_level):
                return qsTr("UVIInfo", value["category"])
        return qsTr("UVIInfo", "Unknown")

    @Slot(int, result=str)
    def getUVIInfo(self, code: int) -> str:
        for level, value in self.uvi_data.items():
            min_level, max_level = level.split("-")
            if int(min_level) <= code <= int(max_level):
                return qsTr("UVIInfo", value["impact"])
        return qsTr("UVIInfo", "Unknown")

    @Slot(int, result=str)
    def getUVIAdvice(self, code: int) -> str:
        for level, value in self.uvi_data.items():
            min_level, max_level = level.split("-")
            if int(min_level) <= code <= int(max_level):
                return qsTr("UVIInfo", value["advice"])
        return qsTr("UVIInfo", "Unknown")

    @Slot(int, result=str)
    def getAQICategory(self, code: int) -> str:
        for level, value in self.aqi_data.items():
            min_level, max_level = level.split("-")
            if int(min_level) <= code <= int(max_level):
                return qsTr("AQIInfo", value["category"])
        return qsTr("AQIInfo", "Unknown")

    @Slot(int, result=str)
    def getAQIInfo(self, code: int) -> str:
        for level, value in self.aqi_data.items():
            min_level, max_level = level.split("-")
            if int(min_level) <= code <= int(max_level):
                return qsTr("AQIInfo", value["impact"])
        return qsTr("AQIInfo", "Unknown")

    @Slot(int, result=str)
    def getAQIAdvice(self, code: int) -> str:
        for level, value in self.aqi_data.items():
            min_level, max_level = level.split("-")
            if int(min_level) <= code <= int(max_level):
                return qsTr("AQIInfo", value["advice"])
        return qsTr("AQIInfo", "Unknown")

    @staticmethod
    def load_json_data(file_path) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON file: {file_path}")
            return {}

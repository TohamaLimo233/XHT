import os
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QObject, Slot, QLocale, QTranslator
from RinUI import RinUIWindow, RinUITranslator

from assets import ASSETS_PATH, QML_PATH, RESOURCES_PATH
from core import PathManager, WeatherResourceManager, WeatherManager, WeatherConfig, CityManager


class RinWeatherMain(RinUIWindow):
    def __init__(self):
        super().__init__()
        self.pathManager = PathManager()
        self.weatherResourceManager = WeatherResourceManager()
        self.weatherConfig = WeatherConfig(self)
        self.weatherManager = WeatherManager(self.weatherConfig)
        self.cityManager = CityManager(self.weatherConfig)

        self.engine.addImportPath(Path(ASSETS_PATH))
        self.engine.rootContext().setContextProperty("RinPath", self.pathManager)
        self.engine.rootContext().setContextProperty("WeatherManager", self.weatherManager)
        self.engine.rootContext().setContextProperty("CityManager", self.cityManager)
        self.engine.rootContext().setContextProperty("WeatherConfig", self.weatherConfig)
        self.engine.rootContext().setContextProperty("WeatherResource", self.weatherResourceManager)

        print("🌦️ RinWeather Application Initialized")

        # i18n
        app_instance = QCoreApplication.instance()
        self.weatherConfig.setLanguage(self.weatherConfig.getLanguage())
        app_instance.aboutToQuit.connect(self.cleanup)

        self.load(Path(QML_PATH, "app.qml"))
        self.setIcon(str(Path(RESOURCES_PATH / "images" / "logo.png")))

    def cleanup(self):
        print("RinWeather Application Cleanup")
        self.weatherManager.cleanup()
        self.cityManager.cleanup()

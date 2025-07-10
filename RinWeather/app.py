from pathlib import Path

from PySide6.QtCore import QLocale, QTranslator
from PySide6.QtWidgets import QApplication
from RinUI import RinUITranslator
from loguru import logger

from RinWeather.assets import ROOT_PATH
from RinWeather.core.main import RinWeatherMain

import sys


def main():
    # 加载配置
    # rw_config = WeatherConfig()
    logger.add(
        Path(ROOT_PATH / "logs" / "rinweather_{time}.log"),
        retention="10 days",
        rotation="1 MB"
    )

    app = QApplication(sys.argv)
    main = RinWeatherMain()
    app.exec()

#main()

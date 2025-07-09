from pathlib import Path

from PySide6.QtCore import QLocale, QTranslator
from PySide6.QtWidgets import QApplication
from RinUI import RinUITranslator
from loguru import logger

from assets import ROOT_PATH
from core.main import RinWeatherMain

import sys


if __name__ == '__main__':
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

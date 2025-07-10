import requests
from PySide6.QtCore import QObject, Signal, Slot, QThread
from typing import List, Dict, Any

from loguru import logger

from RinWeather.core.backend.config import WeatherConfig

proxies = {
    "http": None,
    "https": None
}


class CitySearcher:
    """
    城市搜索器，用于通过地理位置API搜索城市信息
    """
    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

    def search_city(self, name: str, language = "zh_CN") -> List[Dict[str, Any]]:
        """
        通过城市名称进行搜索
        :param name: 城市名
        :param count: 搜索数量限制
        :param language: 语言
        :return: 城市结果列表
        """
        if not name:
            raise ValueError("城市名不能为空")

        params = {
            "name": name,
            "language": language,
            "format": "json"
        }

        logger.info(f"正在搜索城市：{name}…")
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=5, proxies=proxies)
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            logger.info(f"共搜索到 {len(results)} 个城市结果")
            return results

        except requests.exceptions.Timeout:
            logger.error("城市搜索请求超时")
            raise RuntimeError("请求超时，请检查网络")
        except requests.RequestException as e:
            logger.error(f"城市搜索请求失败：{e}")
            raise RuntimeError(f"请求失败：{e}")
        except Exception as e:
            logger.error(f"城市搜索出现未知错误：{e}")
            raise RuntimeError(f"未知错误：{e}")


class CitySearchWorker(QObject):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, searcher: CitySearcher, config: WeatherConfig):
        super().__init__()
        self.searcher = searcher
        self.config = config

    @Slot(str)
    def doSearch(self, keyword: str):
        try:
            language = self.config.getLanguage().split("_")[0]
            result = self.searcher.search_city(keyword)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class CityManager(QObject):
    citySearchFinished = Signal()
    citySearchFailed = Signal(str)
    searchRequested = Signal(str)

    def __init__(self, config: WeatherConfig):
        super().__init__(None)
        self.city_data: List[Dict] = []
        self.config = config

        # 初始化唯一线程和 worker
        self.thread = QThread(self)
        self.worker = CitySearchWorker(CitySearcher(), self.config)
        self.worker.moveToThread(self.thread)

        # 连接信号
        self.searchRequested.connect(self.worker.doSearch)
        self.worker.finished.connect(self._onSearchFinished)
        self.worker.error.connect(self._onSearchFailed)

        self.thread.start()

    def cleanup(self):
        self.thread.terminate()
        self.thread.quit()

    @Slot(str)
    def searchCities(self, keyword: str):
        self.searchRequested.emit(keyword)

    def _onSearchFinished(self, result: List[Dict]):
        self.city_data = result
        self.citySearchFinished.emit()
        logger.info(f"城市搜索成功，共 {len(result)} 条")

    def _onSearchFailed(self, message: str):
        self.city_data = []
        self.citySearchFailed.emit(message)
        logger.warning(f"城市搜索失败：{message}")

    @Slot(result=list)
    def getCities(self) -> List[Dict]:
        return self.city_data


if __name__ == '__main__':
    center = CitySearcher()
    print(center.search_city("Los Angeles"))

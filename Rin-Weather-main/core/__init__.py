from PySide6.QtCore import QObject, Slot
from assets import ASSETS_PATH, RESOURCES_PATH, QML_PATH
from .backend.resources import WeatherResourceManager
from .backend.config import WeatherConfig, DEFAULT_CONFIG
from .backend.weather import WeatherManager
from .backend.cities import CityManager


class PathManager(QObject):

    @Slot(str, result=str)
    def assets(self, args: str) -> str:
        """
        Get the absolute path to an asset file within the assets' directory.
        :param args: Path components to append to the assets' directory.
        :return: Absolute path to the specified asset.
        """
        return ASSETS_PATH.joinpath(args).resolve().as_uri()

    @Slot(str, result=str)
    def resources(self, args: str) -> str:
        """
        Get the absolute path to a resource file within the resources' directory.
        :param args: Path components to append to the resources' directory.
        :return: Absolute path to the specified resource.
        """
        return RESOURCES_PATH.joinpath(args).resolve().as_uri()

    @Slot(str, result=str)
    def qml(self, args: str) -> str:
        """
        Get the absolute path to a QML file within the resources' directory.
        :param args: Path components to append to the resources' directory.
        :return: Absolute path to the specified QML file.
        """
        return QML_PATH.joinpath(args).resolve().as_uri()

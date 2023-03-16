from PyQt5 import uic
from PyQt5.QtGui import QIcon
from util.systemUtils import SystemUtil

class QtUtil:

    @staticmethod
    def loadUiClass(filepath: str) -> tuple:
        return uic.loadUiType(SystemUtil.resource_path(filepath))[0]

    @staticmethod
    def getIcon() -> QIcon:
        return QIcon(SystemUtil.resource_path("./res/icon/logo.ico"))

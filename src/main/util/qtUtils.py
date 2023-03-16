from PyQt5 import uic
from PyQt5.QtGui import QIcon
from util.systemUtils import SystemUtil

class QtUtil:
    """ 
    Util class for qt framework.

    Has only static method.
    """

    @staticmethod
    def loadUiClass(filepath: str) -> tuple:
        """ Return ui class type in `filepath`. """
        return uic.loadUiType(SystemUtil.resource_path(filepath))[0]

    @staticmethod
    def getIcon() -> QIcon:
        """ Return icon from `./res/icon/logo.ico`. """
        return QIcon(SystemUtil.resource_path("./res/icon/logo.ico"))

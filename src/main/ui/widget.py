import datetime

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget

from util.systemUtils import SystemUtil
from util.qtUtils import QtUtil

class Widget(QWidget):
    """ 
    Super class for Widget

    The ui is displayed just by calling the constructor.

    Has some methods about ui.
    """

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parentWindow = parent

    def setPositionCenter(self):
        """ Set window position to center of it's parent. """
        offsetWidth = int((self.parentWindow.width() - self.width()) / 2)
        offsetHeight = int((self.parentWindow.height() - self.height()) / 2)

        self.move(self.parentWindow.x()+offsetWidth, self.parentWindow.y()+offsetHeight)

class PurgeHistoryWidget(Widget, QtUtil.loadUiClass("./res/ui/PurgeHistoryWidget.ui")):
    """ 
    The ui class for purge history.
    """

    def __init__(self, parent: QWidget, cdnInstanceNoStr: str):
        super().__init__(parent)
        self.setupUi(self)

        self.label_cdnInstanceId_value.setText(cdnInstanceNoStr)
        self.label_queryTime_value.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["일시", "범위", "대상", "결과"])
        model.appendRow([QStandardItem("test1"), QStandardItem("test2"), QStandardItem("test3"), QStandardItem("test4")])
        self.tableView_historyList.setModel(model)

        self.setPositionCenter()

        self.setUiFunc()

        self.setWindowIcon(QtUtil.getIcon())

        self.show()

    def setUiFunc(self):
        pass

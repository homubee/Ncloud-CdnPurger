import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QResizeEvent
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

        self.setPositionCenter()

        self.setWindowIcon(QtUtil.getIcon())

        self.show()

        self.setTableUi()

    def setTableUi(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["일시", "범위", "대상", "결과"])
        model.appendRow([QStandardItem(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), QStandardItem("전체"), QStandardItem("test3\ntest4"), QStandardItem("success")])

        # set text alignment
        model.item(0,0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        model.item(0,1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        model.item(0,3).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tableView_historyList.setModel(model)

        # resize row
        self.tableView_historyList.resizeRowsToContents()

        # resize column
        self.setColumnSize()

    def setColumnSize(self):
        col_width = self.tableView_historyList.width()
        self.tableView_historyList.setColumnWidth(0, int(col_width*4/10))
        self.tableView_historyList.setColumnWidth(1, int(col_width*1/10))
        self.tableView_historyList.setColumnWidth(2, int(col_width*3/10))
        self.tableView_historyList.setColumnWidth(3, int(col_width*2/10))

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.setColumnSize()
        return super().resizeEvent(a0)

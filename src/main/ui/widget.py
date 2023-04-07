import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QResizeEvent
from PyQt5.QtWidgets import QWidget

from util.purgeUtils import GetCdnPlusPurgeHistoryList_QueryInfo, GetCdnPlusPurgeHistoryList_ApiHandler
from util.qtUtils import QtUtil
from ui.dialog import MessageDialog

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

        self.messageDialog: MessageDialog = None

        self.label_cdnInstanceId_value.setText(cdnInstanceNoStr)
        self.label_queryTime_value.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.setWindowIcon(QtUtil.getIcon())

        self.show()

        self.setPositionCenter()

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["일시", "범위", "대상", "결과"])

        self.setTableRow(model, int(cdnInstanceNoStr))
        self.setTableSize()

    def setTableSize(self):
        """ Set table size fit to contents. """
        # Resize row
        self.tableView_historyList.resizeRowsToContents()

        # Resize column
        self.setColumnSize()

    def setTableRow(self, model: QStandardItemModel, cdnInstanceNo: int):
        """ Call api and set data to table. """

        queryInfo = GetCdnPlusPurgeHistoryList_QueryInfo(cdnInstanceNo, None, "JSON")
        apiHandler = GetCdnPlusPurgeHistoryList_ApiHandler(queryInfo)

        # Exception handling
        try:
            responseDTO = apiHandler.callApi()
        except Exception as e:
            self.messageDialog = MessageDialog(self, 0, "Error", "[Error] ", str(e))
            self.close()
        else:
            self.messageDialog = MessageDialog(self, 2, "Result", 
                                               "Status Code : " + str(responseDTO.statusCode), 
                                               "Return Code : " +  responseDTO.returnCode, 
                                               "Return Message : " + responseDTO.returnMessage)

            # Close widget when response is not succeeded.
            if (responseDTO.statusCode != 200):
                self.close()
                return

            cdnPlusPurgeHistoryList = responseDTO.responseData["cdnPlusPurgeHistoryList"]

            for index, history in enumerate(cdnPlusPurgeHistoryList):
                requestDate = history["requestDate"].replace("T", " ").split("+")[0]
                isWholePurge = "전체" if history["isWholePurge"] else "개별"
                targetFileList = history["targetDirectoryName"] or ",\n".join(history["targetFileList"])
                purgeStatusName = history["purgeStatusName"]

                # Add items
                rowList = list()
                rowList.append(QStandardItem(requestDate))
                rowList.append(QStandardItem(isWholePurge))
                rowList.append(QStandardItem(targetFileList))
                rowList.append(QStandardItem(purgeStatusName))

                model.appendRow(rowList)

                # Set text alignment
                model.item(index,0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                model.item(index,1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                model.item(index,3).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.tableView_historyList.setModel(model)

    def setColumnSize(self):
        """ Set column width. """
        col_width = self.tableView_historyList.width()
        self.tableView_historyList.setColumnWidth(0, int(col_width*35/100))
        self.tableView_historyList.setColumnWidth(1, int(col_width*10/100))
        self.tableView_historyList.setColumnWidth(2, int(col_width*30/100))
        self.tableView_historyList.setColumnWidth(3, int(col_width*20/100))

    def resizeEvent(self, a0: QResizeEvent) -> None:
        """ Overrides resizeEvent """
        self.setColumnSize()
        return super().resizeEvent(a0)

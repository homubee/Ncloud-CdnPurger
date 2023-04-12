import os
import json
from typing import Final

from PyQt5.QtWidgets import QMainWindow, qApp

from util.purgeUtils import PurgeUtil, RequestCdnPlusPurge_QueryInfo, RequestCdnPlusPurge_ApiHandler
from util.systemUtils import SystemUtil
from util.qtUtils import QtUtil
from ui.dialog import KeySettingDialog, MessageDialog
from ui.widget import PurgeHistoryWidget

class MainWindow(QMainWindow, QtUtil.loadUiClass(os.path.join("res", "ui", "MainWindow.ui"))):
    """ 
    It is a first ui class that will be shown to user.

    The ui is displayed just by calling the constructor.

    Has some methods about ui.
    """

    VERSION: Final = "1.1.0"

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.keySettingDialog: KeySettingDialog = None
        self.messageDialog: MessageDialog = None
        self.purgeHistoryWidget: PurgeHistoryWidget = None
        self.settingData: dict = None

        self.setUiFunc()

        try:
            self.loadSettings()
        except Exception as e:
            self.messageDialog = MessageDialog(self, 0, "Error", "[Error] ", str(e))

        self.setWindowIcon(QtUtil.getIcon())

        self.show()

    def setUiFunc(self):
        """ Connect ui and function. """
        # Set pushButton event
        self.checkLogButton.clicked.connect(self.openPurgeHistoryWidget)
        self.okButton.clicked.connect(self.submit)
        self.resetButton.clicked.connect(self.resetTextEdit)
        self.saveButton.clicked.connect(self.saveSettings)

        # Set radioButton event
        self.radioButton_isWholeDomain_Yes.toggled.connect(self.checkDomainEdit)
        self.radioButton_isWholePurge_Whole.toggled.connect(self.checkPathEdit)

        # Set menuAction event
        self.action_exit.triggered.connect(qApp.quit)

        self.action_keySetting.triggered.connect(self.openKeySettingDialog)
        self.action_clearSetting.triggered.connect(self.removeSettingFiles)

        self.action_minimize.triggered.connect(self.minimizeWindow)
        self.action_maximize.triggered.connect(self.maximizeWindow)
        self.action_normalize.triggered.connect(self.normalizeWindow)

        self.action_help.triggered.connect(self.showHelpMessage)
        self.action_about.triggered.connect(self.showInfoMessage)

    def loadSettings(self):
        """ Load settings and set setting form ui. """
        if SystemUtil.isFileExist(os.path.join("api_settings.json")):
            with open(os.path.join("api_settings.json"), "r", encoding="utf-8") as file:
                self.settingData = json.load(file)
        else:
            return

        self.cdnInstanceNo.setText(str(self.settingData["cdnInstanceNo"]))
        self.radioButton_isWholeDomain_Yes.setChecked(self.settingData["isWholeDomain"])
        self.radioButton_isWholeDomain_No.setChecked(not self.settingData["isWholeDomain"])
        self.radioButton_isWholePurge_Whole.setChecked(self.settingData["isWholePurge"])
        self.radioButton_isWholePurge_Directory.setChecked(self.settingData["isDirPurge"])
        self.radioButton_isWholePurge_Files.setChecked(not self.settingData["isWholePurge"] 
                                                       and not self.settingData["isDirPurge"])

    def openPurgeHistoryWidget(self):
        """ Open PurgeHistoryWidget. """
        if PurgeUtil.ACCESS_KEY is None or PurgeUtil.SECRET_KEY is None:
            self.messageDialog = MessageDialog(self, 0, "Warning", "Ncloud API key 값을 설정하십시오.")
            return

        cdnInstanceNoStr: str = self.cdnInstanceNo.text()
        if not self.isCdnInstanceNoDigit(cdnInstanceNoStr):
            return

        self.purgeHistoryWidget = PurgeHistoryWidget(self, cdnInstanceNoStr)

    def submit(self):
        """ Call API and get result. """
        if PurgeUtil.ACCESS_KEY is None or PurgeUtil.SECRET_KEY is None:
            self.messageDialog = MessageDialog(self, 0, "Warning", "Ncloud API key 값을 설정하십시오.")
            return

        cdnInstanceNoStr: str = self.cdnInstanceNo.text()
        if not self.isCdnInstanceNoDigit(cdnInstanceNoStr):
            return

        cdnInstanceNo: int = int(cdnInstanceNoStr)
        isWholeDomain: bool = self.radioButton_isWholeDomain_Yes.isChecked()
        isWholePurge: bool = self.radioButton_isWholePurge_Whole.isChecked()
        isDirPurge: bool = self.radioButton_isWholePurge_Directory.isChecked()
        domainText: str = self.domainEdit.toPlainText()
        pathText: str = self.pathEdit.toPlainText()

        domainIdList: list
        targetFileList: list

        targetDirectoryName: str = None

        # Check each parameter
        if isWholeDomain or domainText == "":
            domainIdList = None
        else:
            domainIdList = domainText.strip().split("\n")

        if isWholePurge or pathText == "":
            targetFileList = None
        else:
            targetFileList = pathText.strip().split("\n")

        if isDirPurge and targetFileList is not None:
            targetDirectoryName = targetFileList[0]

        queryInfo = RequestCdnPlusPurge_QueryInfo(cdnInstanceNo, isWholeDomain, domainIdList, 
                                                      isWholePurge, targetFileList, targetDirectoryName, "JSON")
        apiHandler = RequestCdnPlusPurge_ApiHandler(queryInfo)

        # Exception handling
        try:
            responseDTO = apiHandler.callApi()
        except Exception as e:
            self.messageDialog = MessageDialog(self, 0, "Error", "[Error] ", str(e))
            self.statusBar().showMessage("API call failed")
        else:
            self.messageDialog = MessageDialog(self, 2, "Result", 
                                               "Status Code : " + str(responseDTO.statusCode), 
                                               "Return Code : " +  responseDTO.returnCode, 
                                               "Return Message : " + responseDTO.returnMessage)
            self.statusBar().showMessage("API call successed")

    def resetTextEdit(self):
        """ Reset text in TextEdit ui. """
        self.domainEdit.clear()
        self.pathEdit.clear()
        self.statusBar().showMessage("Text cleared")

    def saveSettings(self):
        """ Save settings from form ui. """
        cdnInstanceNoStr: str = self.cdnInstanceNo.text()
        if not self.isCdnInstanceNoDigit(cdnInstanceNoStr):
            return
        # Write setting file
        with open(os.path.join("api_settings.json"), "w", encoding="utf-8") as file:
            cdnInstanceNo: int = int(cdnInstanceNoStr)
            isWholeDomain: bool = self.radioButton_isWholeDomain_Yes.isChecked()
            isWholePurge: bool = self.radioButton_isWholePurge_Whole.isChecked()
            isDirPurge: bool = self.radioButton_isWholePurge_Directory.isChecked()

            data = {"cdnInstanceNo" : cdnInstanceNo, 
                    "isWholeDomain" : isWholeDomain, 
                    "isWholePurge" : isWholePurge, 
                    "isDirPurge" : isDirPurge}

            json.dump(data, file)

        self.statusBar().showMessage("Setting saved")

    def isCdnInstanceNoDigit(self, cdnInstanceNoStr: str):
        """ Check if `isCdnInstanceNo` is digit or not. """
        if not cdnInstanceNoStr.isdigit():
            self.messageDialog = MessageDialog(self, 0, "Warning", "cdnInstanceNo는 숫자만 입력해야 합니다.")
            return False
        return True

    def checkDomainEdit(self):
        """ Check settings and set `domainEdit` on/off """
        isWholeDomain = self.radioButton_isWholeDomain_Yes.isChecked()
        if isWholeDomain:
            self.domainEdit.setDisabled(True)
        else:
            self.domainEdit.setDisabled(False)

    def checkPathEdit(self):
        """ Check settings and set `pathEdit` on/off """
        isWholePurge = self.radioButton_isWholePurge_Whole.isChecked()
        if isWholePurge:
            self.pathEdit.setDisabled(True)
        else:
            self.pathEdit.setDisabled(False)

    def openKeySettingDialog(self):
        """ Open KeySettingDialog. """
        self.keySettingDialog = KeySettingDialog(self)

    def removeSettingFiles(self):
        """ Remove all setting file. """
        SystemUtil.removeFile(os.path.join("CdnPurger.env"))
        SystemUtil.removeFile(os.path.join("api_settings.json"))

        self.clearSetting()

        self.messageDialog = MessageDialog(self, 0, "Notice", "설정이 초기화되었습니다.")
        self.statusBar().showMessage("Setting cleared")

    def minimizeWindow(self):
        """ Minimize window. """
        self.showMinimized()

    def maximizeWindow(self):
        """ Maximize window. """
        self.showMaximized()

    def normalizeWindow(self):
        """ Make normal window. """
        self.showNormal()

    def showHelpMessage(self):
        """ Open MessageDialog for help message. """
        self.messageDialog = MessageDialog(self, 2, "Help", 
                                           "1. Setting - Key Setting에서 Access Key와 Secret Key 값을 설정합니다.", 
                                           "2. 프로그램 중앙의 내용을 작성합니다.", 
                                           "3. OK 버튼을 눌러 API를 전송합니다.",
                                           "※ Check Log 버튼으로 로그 확인 가능")

    def showInfoMessage(self):
        """ Open MessageDialog for app info. """
        self.messageDialog = MessageDialog(self, 2, "About", "Ncloud CdnPurger " + MainWindow.VERSION, "Copyright 2023 Homubee")

    def clearSetting(self):
        """ Clear all settings. """
        # Disable exculsive setting (to clear radio button setting)
        self.buttonGroup_IsWholeDomain.setExclusive(False)
        self.buttonGroup_isWholePurge.setExclusive(False)

        self.cdnInstanceNo.clear()
        self.radioButton_isWholeDomain_Yes.setChecked(False)
        self.radioButton_isWholeDomain_No.setChecked(False)
        self.radioButton_isWholePurge_Whole.setChecked(False)
        self.radioButton_isWholePurge_Directory.setChecked(False)
        self.radioButton_isWholePurge_Files.setChecked(False)

        # Active exculsive setting
        self.buttonGroup_IsWholeDomain.setExclusive(True)
        self.buttonGroup_isWholePurge.setExclusive(True)

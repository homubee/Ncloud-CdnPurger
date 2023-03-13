import json
from typing import Final

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, qApp
from PyQt5.QtGui import QIcon

from util.purgeUtils import PurgeUtil, CdnPlusPurgeQueryInfo, CdnPlusPurgeApiHandler
from util.systemUtils import SystemUtil
from ui.dialog import KeySettingDialog, MessageDialog

class MainWindow(QMainWindow, uic.loadUiType(SystemUtil.resource_path("./res/ui/MainWindow.ui"))[0]):

    VERSION: Final = "0.9.2"

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.keySettingDialog: KeySettingDialog = None
        self.messageDialog: MessageDialog = None
        self.settingData: dict = None

        self.setUiFunc()

        if SystemUtil.isFileExist("./api_settings.json"):
            with open("./api_settings.json", "r", encoding="utf-8") as file:
                self.settingData = json.load(file)
                self.setSettings()

        self.setWindowIcon(QIcon(SystemUtil.resource_path("./res/icon/favicon.ico")))

        self.show()

    def setUiFunc(self):
        # Set pushButton event
        self.okButton.clicked.connect(self.okFunc)
        self.resetButton.clicked.connect(self.resetFunc)
        self.saveButton.clicked.connect(self.saveFunc)

        # Set radioButton event
        self.radioButton_isWholeDomain_Yes.toggled.connect(self.checkDomainEdit)
        self.radioButton_isWholePurge_Whole.toggled.connect(self.checkPathEdit)

        # Set menuAction event
        self.action_exit.triggered.connect(qApp.quit)

        self.action_keySetting.triggered.connect(self.openKeySettingDialog)
        self.action_clearSetting.triggered.connect(self.removeKeySetting)

        self.action_minimize.triggered.connect(self.minimizeWindow)
        self.action_maximize.triggered.connect(self.maximizeWindow)
        self.action_normal.triggered.connect(self.makeNormalWindow)

        self.action_help.triggered.connect(self.showHelpMessage)
        self.action_about.triggered.connect(self.showInfoMessage)

    def setSettings(self):
        self.cdnInstanceNo.setText(str(self.settingData["cdnInstanceNo"]))
        self.radioButton_isWholeDomain_Yes.setChecked(self.settingData["isWholeDomain"])
        self.radioButton_isWholeDomain_No.setChecked(not self.settingData["isWholeDomain"])
        self.radioButton_isWholePurge_Whole.setChecked(self.settingData["isWholePurge"])
        self.radioButton_isWholePurge_Directory.setChecked(self.settingData["isDirPurge"])
        self.radioButton_isWholePurge_Files.setChecked(not self.settingData["isWholePurge"] and not self.settingData["isDirPurge"])

    def okFunc(self):
        if PurgeUtil.ACCESS_KEY is None or PurgeUtil.SECRET_KEY is None:
            self.messageDialog = MessageDialog(self, 0, "Ncloud API key 값을 설정하십시오.")
            return
        if self.cdnInstanceNo.text() == "":
            self.messageDialog = MessageDialog(self, 0, "cdnInstanceNo를 입력하십시오.")
            return
        cdnInstanceNo: int = int(self.cdnInstanceNo.text())
        isWholeDomain: bool = self.radioButton_isWholeDomain_Yes.isChecked()
        isWholePurge: bool = self.radioButton_isWholePurge_Whole.isChecked()
        isDirPurge: bool = self.radioButton_isWholePurge_Directory.isChecked()
        domainText: str = self.domainEdit.toPlainText()
        pathText: str = self.pathEdit.toPlainText()

        domainIdList: list
        targetFileList: list

        targetDirectoryName: str = None

        if domainText == "":
            domainIdList = None
        else:
            domainIdList = domainText.strip().split("\n")

        if pathText == "":
            targetFileList = None
        else:
            targetFileList = pathText.strip().split("\n")

        if isDirPurge and targetFileList is not None:
            targetDirectoryName = targetFileList[0]

        cdnPlusPurgeQueryInfo = CdnPlusPurgeQueryInfo(cdnInstanceNo, isWholeDomain, domainIdList, isWholePurge, targetFileList, targetDirectoryName, "JSON")
        cdnPlusPurgeApiHandler = CdnPlusPurgeApiHandler(cdnPlusPurgeQueryInfo)
        statusCode, returnCode, returnMessage = cdnPlusPurgeApiHandler.callApi()
        self.messageDialog = MessageDialog(self, 2, "Status Code : " + str(statusCode), "Return Code : " +  returnCode, "Return Message : " + returnMessage)
        self.statusBar().showMessage("API call successed")

    def resetFunc(self):
        self.domainEdit.clear()
        self.pathEdit.clear()
        self.statusBar().showMessage("Text cleared")

    def saveFunc(self):
        if self.cdnInstanceNo.text() == "":
            self.messageDialog = MessageDialog(self, 0, "cdnInstanceNo를 입력하십시오.")
            return
        with open("./api_settings.json", "w", encoding="utf-8") as file:
            cdnInstanceNo: int = int(self.cdnInstanceNo.text())
            isWholeDomain: bool = self.radioButton_isWholeDomain_Yes.isChecked()
            isWholePurge: bool = self.radioButton_isWholePurge_Whole.isChecked()
            isDirPurge: bool = self.radioButton_isWholePurge_Directory.isChecked()

            data = {"cdnInstanceNo" : cdnInstanceNo, "isWholeDomain" : isWholeDomain, "isWholePurge" : isWholePurge, "isDirPurge" : isDirPurge}
            json.dump(data, file)

        self.statusBar().showMessage("Setting saved")

    def checkDomainEdit(self):
        isWholeDomain = self.radioButton_isWholeDomain_Yes.isChecked()
        if isWholeDomain:
            self.domainEdit.setDisabled(True)
        else:
            self.domainEdit.setDisabled(False)

    def checkPathEdit(self):
        isWholePurge = self.radioButton_isWholePurge_Whole.isChecked()
        if isWholePurge:
            self.pathEdit.setDisabled(True)
        else:
            self.pathEdit.setDisabled(False)

    def openKeySettingDialog(self):
        self.keySettingDialog = KeySettingDialog(self)

    def removeKeySetting(self):
        SystemUtil.removeFile("./.env")
        SystemUtil.removeFile("./api_settings.json")

        self.clearSetting()

        self.messageDialog = MessageDialog(self, 0, "설정이 초기화되었습니다.")
        self.statusBar().showMessage("Setting cleared")

    def minimizeWindow(self):
        self.showMinimized()

    def maximizeWindow(self):
        self.showMaximized()

    def makeNormalWindow(self):
        self.showNormal()

    def showHelpMessage(self):
        self.messageDialog = MessageDialog(self, 2, "1. Setting - Key Setting에서 Access Key와 Secret Key 값을 설정합니다.", "2. 프로그램 중앙의 입력창 내용을 작성합니다.", "3. OK 버튼을 눌러 API를 전송합니다.")

    def showInfoMessage(self):
        self.messageDialog = MessageDialog(self, 2, "NCloud CdnPurger " + MainWindow.VERSION, "Copyright 2023 Homubee")

    def clearSetting(self):
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

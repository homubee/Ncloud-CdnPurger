from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, qApp
from PyQt5.QtGui import QIcon
from util.purgeUtils import PurgeUtil, CdnPlusPurgeQueryInfo, CdnPlusPurgeApiHandler
from util.systemUtils import SystemUtil
from ui.dialog import KeySettingDialog, MessageDialog
import json

class MainWindow(QMainWindow, uic.loadUiType(SystemUtil.resource_path("./res/ui/MainWindow.ui"))[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.settingData: dict

        self.setUiFunc()

        if (SystemUtil.isFileExist("./api_settings.json")):
            with open("./api_settings.json", "r", encoding="utf-8") as file:
                self.settingData = json.load(file)
                self.setSettings()

        self.setWindowIcon(QIcon(SystemUtil.resource_path("./res/icon/favicon.ico")))

        self.show()
    
    def setUiFunc(self):
        self.okBtn.clicked.connect(self.okFunc)
        self.resetBtn.clicked.connect(self.resetFunc)
        self.saveBtn.clicked.connect(self.saveFunc)

        self.radioButton_Yes.toggled.connect(self.checkDomainEdit)
        self.radioButton_Whole.toggled.connect(self.checkPathEdit)

        self.action_fileMenu.triggered.connect(qApp.quit)
        self.action_KeySetting.triggered.connect(self.openKeySettingDialog)
        self.versionMenu.aboutToShow.connect(self.versionInfoFunc)
    
    def setSettings(self):
        self.cdnInstanceNo.setText(str(self.settingData["cdnInstanceNo"]))
        self.radioButton_Yes.setChecked(self.settingData["isWholeDomain"])
        self.radioButton_No.setChecked(not self.settingData["isWholeDomain"])
        self.radioButton_Whole.setChecked(self.settingData["isWholePurge"])
        self.radioButton_Directory.setChecked(self.settingData["isDirPurge"])
        self.radioButton_Files.setChecked(not self.settingData["isWholePurge"] and not self.settingData["isDirPurge"])

    def okFunc(self):
        if PurgeUtil.ACCESS_KEY is None or PurgeUtil.SECRET_KEY is None:
            return
        if (self.cdnInstanceNo.text() == ""):
            return
        cdnInstanceNo: int = int(self.cdnInstanceNo.text())
        isWholeDomain: bool = self.radioButton_Yes.isChecked()
        isWholePurge: bool = self.radioButton_Whole.isChecked()
        isDirPurge: bool = self.radioButton_Directory.isChecked()
        domainText: str = self.domainEdit.toPlainText()
        pathText: str = self.pathEdit.toPlainText()

        domainIdList: list
        targetFileList: list

        targetDirectoryName: str = None

        if (domainText == ""):
            domainIdList = None
        else:
            domainIdList = domainText.strip().split("\n")

        if (pathText == ""):
            targetFileList = None
        else:
            targetFileList = pathText.strip().split("\n")
        
        if (isDirPurge and targetFileList is not None):
            targetDirectoryName = targetFileList[0]
        
        cdnPlusPurgeQueryInfo = CdnPlusPurgeQueryInfo(cdnInstanceNo, isWholeDomain, domainIdList, isWholePurge, targetFileList, targetDirectoryName, "JSON")
        cdnPlusPurgeApiHandler = CdnPlusPurgeApiHandler(cdnPlusPurgeQueryInfo)
        statusCode, returnCode, returnMessage = cdnPlusPurgeApiHandler.callApi()
        self.messageDialog = MessageDialog(self, 2, "Status Code : " + str(statusCode), "Return Code : " +  returnCode, "Return Message : " + returnMessage)
        self.statusBar().showMessage("OK")
    
    def resetFunc(self):
        self.domainEdit.clear()
        self.pathEdit.clear()
        self.statusBar().showMessage("reset")
    
    def saveFunc(self):
        if (self.cdnInstanceNo.text() == ""):
            return
        with open("./api_settings.json", "w", encoding="utf-8") as file:
            cdnInstanceNo: int = int(self.cdnInstanceNo.text())
            isWholeDomain: bool = self.radioButton_Yes.isChecked()
            isWholePurge: bool = self.radioButton_Whole.isChecked()
            isDirPurge: bool = self.radioButton_Directory.isChecked()
            
            data = {"cdnInstanceNo" : cdnInstanceNo, "isWholeDomain" : isWholeDomain, "isWholePurge" : isWholePurge, "isDirPurge" : isDirPurge}
            json.dump(data, file)
        
        self.statusBar().showMessage("Setting saved")
    
    def checkDomainEdit(self):
        isWholeDomain = self.radioButton_Yes.isChecked()
        if isWholeDomain:
            self.domainEdit.setDisabled(True)
        else:
            self.domainEdit.setDisabled(False)
    
    def checkPathEdit(self):
        isWholePurge = self.radioButton_Whole.isChecked()
        if isWholePurge:
            self.pathEdit.setDisabled(True)
        else:
            self.pathEdit.setDisabled(False)
    
    def openKeySettingDialog(self):
        self.keySettingDialog = KeySettingDialog(self)
    
    def versionInfoFunc(self):
        self.messageDialog = MessageDialog(self, 2, "CdnPurger 0.9.1", "Copyright 2023 Homubee")
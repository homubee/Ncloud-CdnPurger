from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from util.systemUtils import SystemUtil
import dotenv

class KeySettingDialog(QWidget, uic.loadUiType(SystemUtil.resource_path("./res/ui/KeySettingDialog.ui"))[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setUiFunc()

        self.setWindowIcon(QIcon(SystemUtil.resource_path("./res/icon/favicon.ico")))
        
        self.show()
    
    def setUiFunc(self):
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
    
    def accepted(self):
        # .env setting
        # if file does not exist, make new .env file
        SystemUtil.mkFile("./.env")
        envFile = dotenv.find_dotenv()

        dotenv.set_key(envFile, "ACCESS_KEY", self.accessKeyInput.text())
        dotenv.set_key(envFile, "SECRET_KEY", self.secretKeyInput.text())

        self.close()

        self.messageDialog = MessageDialog("설정값 반영을 위해 프로그램을 재시작하십시오.")
    
    def rejected(self):
        self.close()

class MessageDialog(QWidget, uic.loadUiType(SystemUtil.resource_path("./res/ui/MessageDialog.ui"))[0]):
    def __init__(self, text: str):
        super().__init__()
        self.setupUi(self)

        self.label.setText(text)

        self.setUiFunc()

        self.setWindowIcon(QIcon(SystemUtil.resource_path("./res/icon/favicon.ico")))
        
        self.show()
    
    def setUiFunc(self):
        self.buttonBox.accepted.connect(self.accepted)
    
    def accepted(self):
        self.close()
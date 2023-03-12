from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from util.systemUtils import SystemUtil
import dotenv

class Dialog(QWidget):

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parentWindow = parent
    
    def setPositionCenter(self):
        offsetWidth = int((self.parentWindow.width() - self.width()) / 2)
        offsetHeight = int((self.parentWindow.height() - self.height()) / 2)

        self.move(self.parentWindow.x()+offsetWidth, self.parentWindow.y()+offsetHeight)

class KeySettingDialog(Dialog, uic.loadUiType(SystemUtil.resource_path("./res/ui/KeySettingDialog.ui"))[0]):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setupUi(self)

        self.setPositionCenter()

        self.setUiFunc()

        self.setWindowIcon(QIcon(SystemUtil.resource_path("./res/icon/favicon.ico")))
        
        self.show()
    
    def setUiFunc(self):
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
    
    def accepted(self):
        # .env setting
        # if file does not exist, make new .env file
        SystemUtil.makeFile("./.env")
        envFile = dotenv.find_dotenv()

        if self.accessKeyInput.text() == "" or self.secretKeyInput.text() == "":
            self.messageDialog = MessageDialog(self, 0, "Key 값을 모두 입력해주십시오.")
            return

        dotenv.set_key(envFile, "ACCESS_KEY", self.accessKeyInput.text())
        dotenv.set_key(envFile, "SECRET_KEY", self.secretKeyInput.text())

        self.close()

        self.messageDialog = MessageDialog(self, 0, "설정값 반영을 위해 프로그램을 재시작하십시오.")
    
    def rejected(self):
        self.close()

class MessageDialog(Dialog, uic.loadUiType(SystemUtil.resource_path("./res/ui/MessageDialog.ui"))[0]):
    def __init__(self, parent: QWidget, newlineNum, *args):
        super().__init__(parent)
        self.setupUi(self)

        text: str = ""
        for element in args:
            text += element
            if element == args[-1]:
                break
            for i in range(0, newlineNum):
                text += "\n"
        self.label.setText(text)

        self.setPositionCenter()

        self.setUiFunc()

        self.setWindowIcon(QIcon(SystemUtil.resource_path("./res/icon/favicon.ico")))
        
        self.show()
    
    def setUiFunc(self):
        self.buttonBox.accepted.connect(self.accepted)
    
    def accepted(self):
        self.close()

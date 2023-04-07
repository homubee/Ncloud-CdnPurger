from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import dotenv

from util.systemUtils import SystemUtil
from util.qtUtils import QtUtil

class Dialog(QWidget):
    """ 
    Super class for Dialog

    The ui is displayed just by calling the constructor.

    Has some methods about ui.
    """

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parentWindow = parent

        # Disable MaximizeButton
        self.setWindowFlags(Qt.WindowType.WindowTitleHint | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)

    def setPositionCenter(self):
        """ Set window position to center of it's parent. """
        offsetWidth = int((self.parentWindow.width() - self.width()) / 2)
        offsetHeight = int((self.parentWindow.height() - self.height()) / 2)

        self.move(self.parentWindow.x()+offsetWidth, self.parentWindow.y()+offsetHeight)

class KeySettingDialog(Dialog, QtUtil.loadUiClass("./res/ui/KeySettingDialog.ui")):
    """ 
    The ui class for getting key setting and saving it.

    Includes save logic.
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setupUi(self)

        self.messageDialog: MessageDialog = None

        self.setUiFunc()

        self.setWindowIcon(QtUtil.getIcon())

        self.show()

        self.setPositionCenter()

    def setUiFunc(self):
        """ Connect ui and function. """
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)

    def accepted(self):
        """ Save key value to .env file. """
        # .env setting
        # if file does not exist, make new .env file
        SystemUtil.makeFile("./.env")
        envFile = dotenv.find_dotenv()

        if self.accessKeyInput.text() == "" or self.secretKeyInput.text() == "":
            self.messageDialog = MessageDialog(self, 0, "Warning", "Key 값을 모두 입력해주십시오.")
            return

        dotenv.set_key(envFile, "ACCESS_KEY", self.accessKeyInput.text())
        dotenv.set_key(envFile, "SECRET_KEY", self.secretKeyInput.text())

        self.close()

        self.messageDialog = MessageDialog(self, 0, "Notice", "설정값 반영을 위해 프로그램을 재시작하십시오.")

    def rejected(self):
        """ Finish the dialog. """
        self.close()

class MessageDialog(Dialog, QtUtil.loadUiClass("./res/ui/MessageDialog.ui")):
    """ 
    The ui class for displaying message.

    Provides formatted message to user.
    """

    def __init__(self, parent: QWidget, newlineNum: int, title: str, *args):
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowTitle(title)
        self.makeMessageString(newlineNum, args)

        self.setUiFunc()

        self.setWindowIcon(QtUtil.getIcon())

        self.show()

        self.setPositionCenter()

    def makeMessageString(self, newlineNum: int, texts: tuple):
        """ Make formatted message string for dialog. """
        text: str = ""
        for element in texts:
            text += element
            if element == texts[-1]:
                break
            for _ in range(0, newlineNum):
                text += "\n"
        self.label.setText(text)

    def setUiFunc(self):
        """ Connect ui and function. """
        self.buttonBox.accepted.connect(self.accepted)

    def accepted(self):
        """ Finish the dialog. """
        self.close()

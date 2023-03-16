import sys
from PyQt5.QtWidgets import QApplication
from ui.mainWindow import MainWindow

def main():
    """ Main method, entrypoint of this app. """
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

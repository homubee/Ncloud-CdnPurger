import sys
import os

class SystemUtil:
    def resource_path(relative_path: str):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def isFileExist(filepath: str):
        return os.path.exists(filepath)

    def removeFile(filepath: str) -> bool:
        check: bool = SystemUtil.isFileExist(filepath)
        if check:
            os.remove(filepath)
        return check
    
    def makeFile(filepath: str):
        if not SystemUtil.isFileExist(filepath):
            with open(filepath, "w", encoding="utf-8") as file:
                pass

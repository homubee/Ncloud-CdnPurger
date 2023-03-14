import sys
import os

class SystemUtil:

    @staticmethod
    def resource_path(relative_path: str) -> str:
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    @staticmethod
    def isFileExist(filepath: str) -> bool:
        return os.path.exists(filepath)

    @staticmethod
    def removeFile(filepath: str) -> bool:
        file_exists: bool = SystemUtil.isFileExist(filepath)
        if file_exists:
            os.remove(filepath)
        return file_exists

    @staticmethod
    def makeFile(filepath: str) -> bool:
        file_not_exists: bool = not SystemUtil.isFileExist(filepath)
        if file_not_exists:
            with open(filepath, "w", encoding="utf-8"):
                pass
        return file_not_exists

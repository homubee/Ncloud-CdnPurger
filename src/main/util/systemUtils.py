import sys
import os

class SystemUtil:
    """ 
    Util class for path and file.

    Has only static method.
    """

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
        """ Return `True` if there is file in `filepath`. Otherwise return `False`. """
        return os.path.exists(filepath)

    @staticmethod
    def removeFile(filepath: str) -> bool:
        """ Remove file if it is in `filepath`, and return `True`. Otherwise do nothing, and return `False`. """
        file_exists: bool = SystemUtil.isFileExist(filepath)
        if file_exists:
            os.remove(filepath)
        return file_exists

    @staticmethod
    def makeFile(filepath: str) -> bool:
        """ Make file if it is not in `filepath`, and return `True`. Otherwise do nothing, and return `False`. """
        file_not_exists: bool = not SystemUtil.isFileExist(filepath)
        if file_not_exists:
            filepath_conv = filepath.replace("\\", "/")
            find_index = filepath_conv.rfind("/")
            if find_index != -1:
                os.makedirs(filepath_conv[:find_index], exist_ok=True)
            with open(filepath, "w", encoding="utf-8"):
                pass
        return file_not_exists

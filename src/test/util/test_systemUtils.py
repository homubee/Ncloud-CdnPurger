import unittest
import os
import sys
import shutil

sys.path.insert(1, "./src")

from main.util.systemUtils import SystemUtil

class SystemUtilTest(unittest.TestCase):

    TEST_DIR = os.path.join("src", "test", "util")
    EXIST_FILE_PATH = os.path.join(TEST_DIR, "file_A.txt")
    NOT_EXIST_FILE_PATH = os.path.join(TEST_DIR, "file_B.txt")
    NOT_EXIST_DIR_PATH = os.path.join(TEST_DIR, "test")
    NOT_EXIST_DIR_FILE_PATH = os.path.join(NOT_EXIST_DIR_PATH, "file_B.txt")

    def setUp(self):
        # make test file
        with open(SystemUtilTest.EXIST_FILE_PATH, "w", encoding="utf-8"):
            pass

    def tearDown(self):
        # remove test file
        try:
            os.remove(SystemUtilTest.EXIST_FILE_PATH)
            os.remove(SystemUtilTest.NOT_EXIST_FILE_PATH)
            shutil.rmtree(SystemUtilTest.NOT_EXIST_DIR_PATH)
        except:
            pass

    def test_isFileExist(self):
        self.assertTrue(SystemUtil.isFileExist(SystemUtilTest.EXIST_FILE_PATH))

        self.assertFalse(SystemUtil.isFileExist(SystemUtilTest.NOT_EXIST_FILE_PATH))

        self.assertFalse(SystemUtil.isFileExist(SystemUtilTest.NOT_EXIST_DIR_FILE_PATH))

    def test_removeFile(self):
        self.assertTrue(SystemUtil.removeFile(SystemUtilTest.EXIST_FILE_PATH))

        self.assertFalse(SystemUtil.removeFile(SystemUtilTest.NOT_EXIST_FILE_PATH))

        self.assertFalse(SystemUtil.removeFile(SystemUtilTest.NOT_EXIST_DIR_FILE_PATH))

    def test_makeFile(self):
        self.assertFalse(SystemUtil.makeFile(SystemUtilTest.EXIST_FILE_PATH))

        self.assertTrue(SystemUtil.makeFile(SystemUtilTest.NOT_EXIST_FILE_PATH))

        self.assertTrue(SystemUtil.makeFile(SystemUtilTest.NOT_EXIST_DIR_FILE_PATH))

if __name__ == "__main__":
    unittest.main()

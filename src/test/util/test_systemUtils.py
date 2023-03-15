import unittest
import os
import sys

sys.path.insert(1, "./src")

from main.util.systemUtils import SystemUtil

class SystemUtilTest(unittest.TestCase):

    def setUp(self):
        # make test file
        with open("src/test/util/file_A.txt", "w", encoding="utf-8"):
            pass

    def tearDown(self):
        # remove test file
        try:
            os.remove("src/test/util/file_A.txt")
        except:
            pass

    def test_isFileExist(self):
        self.assertTrue(SystemUtil.isFileExist("src/test/util/file_A.txt"))

        self.assertFalse(SystemUtil.isFileExist("src/test/util/file_B.txt"))

        self.assertFalse(SystemUtil.isFileExist("src/test/util/test/file_B.txt"))

    def test_removeFile(self):
        pass

    def test_makeFile(self):
        pass

if __name__ == "__main__":
    unittest.main()

import unittest
import sys

sys.path.insert(1, "src")

from main.util.purgeUtils import RequestCdnPlusPurge_QueryInfo, GetCdnPlusPurgeHistoryList_QueryInfo

class PurgeUtilTest(unittest.TestCase):

    def test_RequestCdnPlusPurge_makeQueryString(self):
        cdnInstanceNo: int = 123456
        isWholeDomain: bool = True
        isWholePurge: bool = False
        domainIdList: list = ["aaa", "bbb"]
        targetFileList: list = ["ccc", "ddd"]
        targetDirectoryName: str = None
        responseFormatType: str = "JSON"

        query_info = RequestCdnPlusPurge_QueryInfo(cdnInstanceNo, isWholeDomain, domainIdList, 
                                                      isWholePurge, targetFileList, targetDirectoryName, responseFormatType)

        expected_query_string = "cdnInstanceNo=123456&isWholeDomain=true&isWholePurge=false&domainIdList.1=aaa&domainIdList.2=bbb&targetFileList.1=ccc&targetFileList.2=ddd&responseFormatType=JSON"

        self.assertEqual(expected_query_string, query_info.makeQueryString())

        targetFileList: list = None
        targetDirectoryName: str = "test"
        responseFormatType: str = "XML"

        query_info = RequestCdnPlusPurge_QueryInfo(cdnInstanceNo, isWholeDomain, domainIdList, 
                                                      isWholePurge, targetFileList, targetDirectoryName, responseFormatType)

        expected_query_string = "cdnInstanceNo=123456&isWholeDomain=true&isWholePurge=false&domainIdList.1=aaa&domainIdList.2=bbb&targetDirectoryName=test&responseFormatType=XML"

        self.assertEqual(expected_query_string, query_info.makeQueryString())

    def test_GetCdnPlusPurgeHistoryList_makeQueryString(self):
        cdnInstanceNo: int = 123456
        purgeIdList: list = ["aaa", "bbb"]
        responseFormatType: str = "JSON"

        query_info = GetCdnPlusPurgeHistoryList_QueryInfo(cdnInstanceNo, purgeIdList, responseFormatType)

        expected_query_string = "cdnInstanceNo=123456&purgeIdList.1=aaa&purgeIdList.2=bbb&responseFormatType=JSON"

        self.assertEqual(expected_query_string, query_info.makeQueryString())

        purgeIdList: list = None
        responseFormatType: str = "XML"

        query_info = GetCdnPlusPurgeHistoryList_QueryInfo(cdnInstanceNo, purgeIdList, responseFormatType)

        expected_query_string = "cdnInstanceNo=123456&responseFormatType=XML"

        self.assertEqual(expected_query_string, query_info.makeQueryString())

    def test_RequestCdnPlusPurge_makeQueryString_responseFormatType(self):
        cdnInstanceNo: int = 123456
        isWholeDomain: bool = True
        isWholePurge: bool = False
        domainIdList: list = ["aaa", "bbb"]
        targetFileList: list = ["ccc", "ddd"]
        targetDirectoryName: str = None
        responseFormatType: str = "HTML"

        query_info = RequestCdnPlusPurge_QueryInfo(cdnInstanceNo, isWholeDomain, domainIdList, 
                                                      isWholePurge, targetFileList, targetDirectoryName, responseFormatType)

        self.assertRaises(Exception, query_info.makeQueryString)

    def test_GetCdnPlusPurgeHistoryList_makeQueryString_responseFormatType(self):
        cdnInstanceNo: int = 123456
        purgeIdList: list = ["aaa", "bbb"]
        responseFormatType: str = "HTML"

        query_info = GetCdnPlusPurgeHistoryList_QueryInfo(cdnInstanceNo, purgeIdList, responseFormatType)

        self.assertRaises(Exception, query_info.makeQueryString)

    def test_RequestCdnPlusPurge_makeQueryString_required(self):
        cdnInstanceNo: int = None
        isWholeDomain: bool = True
        isWholePurge: bool = False
        domainIdList: list = ["aaa", "bbb"]
        targetFileList: list = ["ccc", "ddd"]
        targetDirectoryName: str = None
        responseFormatType: str = "XML"

        query_info = RequestCdnPlusPurge_QueryInfo(cdnInstanceNo, isWholeDomain, domainIdList, 
                                                      isWholePurge, targetFileList, targetDirectoryName, responseFormatType)

        self.assertRaises(Exception, query_info.makeQueryString)

    def test_GetCdnPlusPurgeHistoryList_makeQueryString_required(self):
        cdnInstanceNo: int = None
        purgeIdList: list = ["aaa", "bbb"]
        responseFormatType: str = "JSON"

        query_info = GetCdnPlusPurgeHistoryList_QueryInfo(cdnInstanceNo, purgeIdList, responseFormatType)

        self.assertRaises(Exception, query_info.makeQueryString)

if __name__ == "__main__":
    unittest.main()

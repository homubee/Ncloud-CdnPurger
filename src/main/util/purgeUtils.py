import os
import hashlib
import hmac
import base64
import time
import json

from typing import Final
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

import dotenv
import requests


dotenv.load_dotenv()

@dataclass
class ApiResponseDTO:
    """ DTO class for API response. """
    statusCode: int = -1
    returnCode: str = ""
    returnMessage: str = ""
    responseData = None

class QueryInfo(metaclass=ABCMeta):
    """ 
    Super class for `QueryInfo`. (Abstract)

    Provides `makeQueryString` method. It makes proper querystring for each API.
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def makeQueryString(self) -> str:
        """ Make querystring from parameter info. """
        pass

class RequestCdnPlusPurge_QueryInfo(QueryInfo):
    """ 
    Concrete class of `QueryInfo`.

    Has query parameter info about `requestCdnPlusPurge` API.

    Can make querystring from property.
    """

    def __init__(self, cdnInstanceNo: int, isWholeDomain: bool, domainIdList: list, isWholePurge: bool,
                 targetFileList: list, targetDirectoryName: str, responseFormatType: str) -> None:
        super().__init__()
        self.cdnInstanceNo = cdnInstanceNo
        self.isWholeDomain = isWholeDomain
        self.domainIdList = domainIdList
        self.isWholePurge = isWholePurge
        self.targetFileList = targetFileList
        self.targetDirectoryName = targetDirectoryName
        self.responseFormatType = responseFormatType

    def makeQueryString(self) -> str:
        """ Make querystring by parameter info. """
        parameterList: list[str] = []

        if self.cdnInstanceNo is None or self.isWholeDomain is None or self.isWholePurge is None:
            raise Exception("required parameter is None")

        parameterList.append("cdnInstanceNo" + "=" + str(self.cdnInstanceNo))
        parameterList.append("isWholeDomain" + "=" + str(self.isWholeDomain).lower())
        parameterList.append("isWholePurge" + "=" + str(self.isWholePurge).lower())

        if self.domainIdList is not None:
            element: str
            for i, element in enumerate(self.domainIdList):
                parameterList.append("domainIdList." + str(i+1) + "=" + element)

        if self.targetFileList is not None:
            element: str
            for i, element in enumerate(self.targetFileList):
                parameterList.append("targetFileList." + str(i+1) + "=" + element)

        if self.targetDirectoryName is not None:
            parameterList.append("targetDirectoryName" + "=" + str(self.targetDirectoryName))

        if self.responseFormatType is not None:
            if self.responseFormatType in ("JSON", "XML"):
                parameterList.append("responseFormatType" + "=" + str(self.responseFormatType))
            else:
                raise Exception("invalid responseFormatType")

        queryString: str = ""
        element: str
        for i, element in enumerate(parameterList):
            if i != 0:
                queryString += "&"
            queryString += parameterList[i]
        return queryString

class GetCdnPlusPurgeHistoryList_QueryInfo(QueryInfo):
    """ 
    Concrete class of `QueryInfo`.

    Has query parameter info about `getCdnPlusPurgeHistoryList` API.

    Can make querystring from property.
    """

    def __init__(self, cdnInstanceNo: int, purgeIdList: list, responseFormatType: str) -> None:
        super().__init__()
        self.cdnInstanceNo = cdnInstanceNo
        self.purgeIdList = purgeIdList
        self.responseFormatType = responseFormatType

    def makeQueryString(self) -> str:
        """ Make querystring by parameter info. """
        parameterList: list[str] = []

        if self.cdnInstanceNo is None:
            raise Exception("required parameter is None")

        parameterList.append("cdnInstanceNo" + "=" + str(self.cdnInstanceNo))

        if self.purgeIdList is not None:
            element: str
            for i, element in enumerate(self.purgeIdList):
                parameterList.append("purgeIdList." + str(i+1) + "=" + element)

        if self.responseFormatType is not None:
            if self.responseFormatType in ("JSON", "XML"):
                parameterList.append("responseFormatType" + "=" + str(self.responseFormatType))
            else:
                raise Exception("invalid responseFormatType")

        queryString: str = ""
        element: str
        for i, element in enumerate(parameterList):
            if i != 0:
                queryString += "&"
            queryString += parameterList[i]
        return queryString

class ApiHandler(metaclass=ABCMeta):
    """ 
    Super class for `ApiHandler`. (Abstract)

    Provides `callApi` method. It calls api and return response info.
    """

    def __init__(self, queryInfo: QueryInfo) -> None:
        self._scheme: str
        self._host: str
        self._path: str
        self._queryInfo: QueryInfo = queryInfo

    @abstractmethod
    def callApi(self):
        """ Call API. """
        pass

class RequestCdnPlusPurge_ApiHandler(ApiHandler):
    """ 
    Concrete class of `ApiHandler`.

    Can call `requestCdnPlusPurge` API.
    """

    def __init__(self, queryInfo: RequestCdnPlusPurge_QueryInfo) -> None:
        super().__init__(queryInfo)

        self._scheme: str = "https://"
        self._host: str = "ncloud.apigw.ntruss.com"
        self._path: str = "/cdn/v2/requestCdnPlusPurge?"

    def callApi(self):
        """ Call requestCdnPlusPurge API. Return info about calling api. """
        try:
            queryString = self._queryInfo.makeQueryString()

            headers = PurgeUtil.make_headers("GET", self._path + queryString)

            response = requests.get(self._scheme + self._host + self._path + queryString, headers=headers, timeout=5)

            result = json.loads(response.text)
        except:
            raise

        # Make return info
        responeDTO = ApiResponseDTO()
        responeDTO.statusCode = response.status_code

        if response.status_code == 200:
            responeDTO.returnCode = result["requestCdnPlusPurgeResponse"]["returnCode"]
            responeDTO.returnMessage = result["requestCdnPlusPurgeResponse"]["returnMessage"]
            responeDTO.responseData = result["requestCdnPlusPurgeResponse"]
        elif response.status_code == 401:
            responeDTO.returnCode = result["error"]["errorCode"]
            responeDTO.returnMessage = result["error"]["message"]
        elif response.status_code == 500:
            responeDTO.returnCode = result["responseError"]["returnCode"]
            responeDTO.returnMessage = result["responseError"]["returnMessage"]
        else:
            responeDTO.returnCode = "-1"
            responeDTO.returnMessage = "Unexpected Error"

        return responeDTO

class GetCdnPlusPurgeHistoryList_ApiHandler(ApiHandler):
    """ 
    Concrete class of `ApiHandler`.

    Can call `getCdnPlusPurgeHistoryList` API.
    """

    def __init__(self, queryInfo: GetCdnPlusPurgeHistoryList_QueryInfo) -> None:
        super().__init__(queryInfo)

        self._scheme: str = "https://"
        self._host: str = "ncloud.apigw.ntruss.com"
        self._path: str = "/cdn/v2/getCdnPlusPurgeHistoryList?"

    def callApi(self):
        """ Call `getCdnPlusPurgeHistoryList` API. Return info about calling api. """
        try:
            queryString = self._queryInfo.makeQueryString()

            headers = PurgeUtil.make_headers("GET", self._path + queryString)

            response = requests.get(self._scheme + self._host + self._path + queryString, headers=headers, timeout=5)

            result = json.loads(response.text)
        except:
            raise

        # Make return info
        responeDTO = ApiResponseDTO()
        responeDTO.statusCode = response.status_code

        if response.status_code == 200:
            responeDTO.returnCode = result["getCdnPlusPurgeHistoryListResponse"]["returnCode"]
            responeDTO.returnMessage = result["getCdnPlusPurgeHistoryListResponse"]["returnMessage"]
            responeDTO.responseData = result["getCdnPlusPurgeHistoryListResponse"]
        elif response.status_code == 401:
            responeDTO.returnCode = result["error"]["errorCode"]
            responeDTO.returnMessage = result["error"]["message"]
        elif response.status_code == 500:
            responeDTO.returnCode = result["responseError"]["returnCode"]
            responeDTO.returnMessage = result["responseError"]["returnMessage"]
        else:
            responeDTO.returnCode = "-1"
            responeDTO.returnMessage = "Unexpected Error"

        return responeDTO

class PurgeUtil:
    """ 
    Util class for purge API.

    Has only static method.
    """

    ACCESS_KEY: Final = os.getenv("ACCESS_KEY")
    SECRET_KEY: Final = os.getenv("SECRET_KEY")

    @staticmethod
    def	make_signature(method, pathAndQuery):
        """ Make signature for ncloud api. Return `timestamp`, `signingKey` """
        timestamp = int(time.time() * 1000)
        timestamp = str(timestamp)
        SECRET_KEY_BYTE: Final = bytes(PurgeUtil.SECRET_KEY, 'UTF-8')
        message = method + " " + pathAndQuery + "\n" + timestamp + "\n" + PurgeUtil.ACCESS_KEY
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(SECRET_KEY_BYTE, message, digestmod=hashlib.sha256).digest())
        return timestamp, signingKey

    @staticmethod
    def make_headers(method, pathAndQuery):
        """ Make and return header for ncloud api. """
        timestamp, signingKey = PurgeUtil.make_signature(method, pathAndQuery)
        headers = {
            "x-ncp-apigw-timestamp" : timestamp, 
            "x-ncp-iam-access-key" : PurgeUtil.ACCESS_KEY, 
            "x-ncp-apigw-signature-v2" : signingKey
        }
        return headers

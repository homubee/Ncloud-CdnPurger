import os
import hashlib
import hmac
import base64
import time
import json

from typing import Final
from abc import ABCMeta, abstractmethod

import dotenv
import requests


dotenv.load_dotenv()


class QueryInfo(metaclass=ABCMeta):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def makeQueryString(self) -> str:
        pass

class CdnPlusPurgeQueryInfo(QueryInfo):

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


class ApiHandler(metaclass=ABCMeta):

    def __init__(self) -> None:
        self._scheme: str
        self._host: str
        self._path: str
        self._queryInfo: QueryInfo

    @abstractmethod
    def callApi(self):
        pass

class CdnPlusPurgeApiHandler(ApiHandler):

    def __init__(self, cdnPlusPurgeQueryInfo: CdnPlusPurgeQueryInfo) -> None:
        super().__init__()

        self._scheme: str = "https://"
        self._host: str = "ncloud.apigw.ntruss.com"
        self._path: str = "/cdn/v2/requestCdnPlusPurge?"
        self._queryInfo: QueryInfo = cdnPlusPurgeQueryInfo

    def callApi(self):
        try:
            self.queryString = self._queryInfo.makeQueryString()

            timestamp, signingKey = PurgeUtil.make_signature("GET", self._path + self.queryString)
            headers = {"x-ncp-apigw-timestamp" : timestamp, "x-ncp-iam-access-key" : PurgeUtil.ACCESS_KEY, "x-ncp-apigw-signature-v2" : signingKey}

            response = requests.get(self._scheme + self._host + self._path + self.queryString, headers=headers, timeout=5)

            result = json.loads(response.text)
        except:
            raise

        print(result)

        returnCode: str = ""
        returnMessage: str = ""

        if response.status_code == 200:
            returnCode = result["requestCdnPlusPurgeResponse"]["returnCode"]
            returnMessage = result["requestCdnPlusPurgeResponse"]["returnMessage"]
        elif response.status_code == 401:
            returnCode = result["error"]["errorCode"]
            returnMessage = result["error"]["message"]
        elif response.status_code == 500:
            returnCode = result["responseError"]["returnCode"]
            returnMessage = result["responseError"]["returnMessage"]
        else:
            returnCode = "-1"
            returnMessage = "Unexpected Error"

        return response.status_code, returnCode, returnMessage


class PurgeUtil:

    ACCESS_KEY: Final = os.getenv("ACCESS_KEY")
    SECRET_KEY: Final = os.getenv("SECRET_KEY")

    @staticmethod
    def	make_signature(method, pathAndQuery):
        timestamp = int(time.time() * 1000)
        timestamp = str(timestamp)
        SECRET_KEY_BYTE: Final = bytes(PurgeUtil.SECRET_KEY, 'UTF-8')
        message = method + " " + pathAndQuery + "\n" + timestamp + "\n" + PurgeUtil.ACCESS_KEY
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(SECRET_KEY_BYTE, message, digestmod=hashlib.sha256).digest())
        return timestamp, signingKey

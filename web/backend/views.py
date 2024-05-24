
import csv
import json
import os
import subprocess
# from email.errors import UndecodableBytesDefect
from contextlib import closing
from datetime import datetime
from glob import glob
from random import randrange
from subprocess import getstatusoutput

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

dataRootDir = "/data/TTSN/"
downloadDir = "/download/"
# dev:port
graphqlUrl = f'http://{settings.GQL_SERVER}:8010/graphql/'
queryAddLog = """
mutation MyMutation($sizeBytes: Int) {
  authIes {
    ... on GQLAuthError {
      message
      code
    }
    ... on UpdateDB {
      __typename
      addDownloadlog(downloadInput: {sizeBytes: $sizeBytes}) {
        success
        text
      }
    }
  }
}
"""


class download(View):
    def getFile(self, yearObj, userLog):
        # 拼出find指令產生檔案列表:
        # (find ~/TEST -maxdepth 1 \( -name "ex*" -o -name "catalog2TECDB2*" \) -print; find ~/QSIS -maxdepth 1 \( -name "rfi*" -o -name "client_parameters*" \) -print) | zip -j ~/TEST/output.zip -@
        def getHash(length):
            seed = 'qwertyuiopasdfghjklmnbvcxz0123456789QWERTYUIOPASDFGHJKLMNBVCXZ'
            seedLen = len(seed)

            hash = ''
            for index in range(length):
                hash += seed[randrange(seedLen)]
            return (hash)

        findCMD = "(find"
        try:
            yearArr = yearObj.keys()
            for yearIdx, year in enumerate(yearArr):
                findCMD += f' {dataRootDir+year} -maxdepth 1 \('
                for fileIdx, fileName in enumerate(yearObj[year]):
                    if fileIdx > 0:
                        findCMD += ' -o'
                    findCMD += f' -name "{fileName}"'
            findCMD += f' \) -print{")" if yearIdx == len(yearArr)-1 else ";"}'
        except:
            pass

        zipName = f'{getHash(15)}.zip'
        CMD = f'{findCMD} | zip -j {downloadDir+zipName} -@'
        print(CMD)
        _, _ = getstatusoutput(CMD)

        # insert download log to DB
        variables = {
            "sizeBytes":  os.path.getsize(downloadDir+zipName),
        }
        r = requests.post(graphqlUrl, json={'query': queryAddLog, "variables": variables})
        # print('downloadLog_result = ', variables, dir(r))
        return zipName

    def post(self, request):
        # print(self,request)
        req = json.loads(request.body)
        yearObj = req.get('yearObj')
        userLog = req.get('userLog')
        print(yearObj, userLog)

        zipName = self.getFile(yearObj, userLog)
        url = f'/get_file/{zipName}?renameto={'TTSN.'+zipName}&filetype=zip'
        # print(url)
        response = HttpResponse()
        response['content_type'] = 'application/octet-stream'
        response['X-Accel-Redirect'] = url
        return response

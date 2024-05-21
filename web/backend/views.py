
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

eventDataPath = "/data/eventData/"
downloadDir = "/download/"
# dev:port
graphqlUrl = f'http://{settings.GQL_SERVER}/graphql/'
queryAddLog = """mutation MyMutation($sizeBytes: Int, $email: String , $affiliation: String, $station: String , $event: String ) {
        authIes {
            ... on UpdateDB {
            __typename
            addDownloadlog(
                downloadInput: {affiliation: $affiliation, email: $email, sizeBytes: $sizeBytes, station:$station, event:$event}
            ) {
                success
                text
            }
            }
        }
        }"""


def generatedRandom(number):
    seed = 'qwertyuiopasdfghjklmnbvcxz0123456789QWERTYUIOPASDFGHJKLMNBVCXZ'
    stop = len(seed)
    goal = ''
    for index in range(number):
        goal += seed[randrange(stop)]

    return (goal)


class download(View):
    def getFile(self, event, station, userLog):
        tmp = generatedRandom(15)
        fileRandomName = ''
        rename = ''
        filetype = 'tgz' if len(station) == 0 else 'zip'

        if filetype == 'tgz':
            yyyy = event[0][:4]
            datetime_ = datetime.fromisoformat(event[0]).strftime('%Y%m%d%H%M%S')
            dir = f'{eventDataPath}{yyyy}/{datetime_}/'
            fileName = f'{datetime_}'
            fileRandomName = f'{fileName}.{tmp}.tar.gz'
            rename = f'{fileName}.tar.gz'
            _, _ = getstatusoutput(f'cp {dir+rename} {downloadDir+fileRandomName}')

        elif filetype == 'zip':
            # 拼出find指令產生檔案列表(ex:find /data/eventData/2023/20230112051553/SAC -type f -name "W139.*" )
            findCMD = "find"
            try:
                for eve in event:
                    yyyy = eve[:4]
                    datetime_ = datetime.fromisoformat(eve).strftime('%Y%m%d%H%M%S')
                    # print(datetime_)
                    dir = f'{eventDataPath}{yyyy}/{datetime_}/SAC'
                    findCMD += f' {dir}'
                findCMD += " -type f"

                for idx, sta in enumerate(station):
                    if idx > 0:
                        findCMD += ' -o '
                    findCMD += f' -name "{sta}.*"'
            except:
                pass

            fileName = station[0] if len(event) > len(station) else event[0]
            fileRandomName = f'{fileName}.{tmp}.zip'
            rename = f'{fileName}.zip'
            CMD = f'{findCMD} | zip -j {downloadDir+fileRandomName} -@'
            # print(CMD)
            _, _ = getstatusoutput(CMD)
            # print(a, b)
        variables = {
            "email": userLog.get('email'),
            "affiliation": userLog.get('affiliation'),
            "sizeBytes":  os.path.getsize(downloadDir+fileRandomName),
            "event": ','.join(event),
            "station": ','.join(station)
        }
        # subprocess.Popen
        print(variables)
        r = requests.post(graphqlUrl, json={'query': queryAddLog, "variables": variables})
        # print(r.json())

        return fileRandomName, rename, filetype

    def post(self, request):
        # print(self,request)
        req = json.loads(request.body)
        # print(req)
        station = req.get('station')
        event = req.get('event')
        userLog = req.get('userLog')
        # print(station, event, userLog)

        ori_filename, basename, filetype = self.getFile(event, station, userLog)
        url = f'/get_file/{ori_filename}?renameto={basename}&filetype={filetype}'
        # print(url)
        response = HttpResponse()
        response['content_type'] = 'application/octet-stream'
        response['X-Accel-Redirect'] = url
        return response

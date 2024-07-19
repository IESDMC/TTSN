
import base64
import datetime
import io
import math
from enum import Enum
from random import randrange
from subprocess import getstatusoutput
from typing import Any, Dict, List, Optional

import strawberry
import strawberry_django
from __backend.models import Data, Station
from PIL import Image
from strawberry.scalars import JSON
from strawberry.types import Info

from .types import dataFileType, dataType, stationType


class resolver:
    @strawberry.enum
    class dataFile_choices(Enum):
        jpg = 0
        zip = 1

    def getStaList(info: Info) -> List[stationType]:
        q = {}
        list = Station.objects.filter(**q)
        return list

    def getDataList(info: Info) -> List[dataType]:
        q = {}
        list = Data.objects.filter(**q)
        return list

    def getDataFile(fileType: Optional[dataFile_choices] = dataFile_choices.jpg,
                    yearObj: Optional[JSON] = strawberry.UNSET) -> List[dataFileType]:
        # ex: yearObj = {'1972':['file1','file2'...]}
        # print(fileType, yearObj)
        dataRootDir = "/data/TTSN/"
        res = []

        if fileType.value == 0:
            def getCompressedImg(imgPath):
                img_byte_arr = io.BytesIO()

                with Image.open(imgPath) as img:
                    # 螢幕寬度大多爲1920
                    ratio = 1920/img.width

                    (width, height) = (math.floor(img.width*ratio), math.floor(img.height*ratio))
                    print('ratio=', ratio, (width, height), (img.width, img.height))
                    img_resized = img.resize((width, height))
                    img_resized.save(img_byte_arr, format='JPEG')

                return img_byte_arr.getvalue()

            for year in yearObj.keys():
                for fileName in yearObj[year]:
                    imgPath = f'{dataRootDir}/{year}/{fileName}'
                    data = getCompressedImg(imgPath)
                    res.append(
                        dataFileType(
                            name=fileName,
                            data=data,
                        )
                    )

        return res


@ strawberry.type
class Query:
    stationList:  List[stationType] = strawberry_django.field(resolver=resolver.getStaList)
    dataList:  List[dataType] = strawberry_django.field(resolver=resolver.getDataList)
    dataFile:  List[dataFileType] = strawberry_django.field(resolver=resolver.getDataFile)

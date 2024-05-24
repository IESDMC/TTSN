import datetime
from typing import List, Optional

import strawberry
from backend import models
from strawberry.scalars import JSON, Base16, Base32, Base64


@strawberry.django.type(models.Station)
class stationType:
    station_code: str
    name_chinese: str
    name_english: str
    lat: float
    lon: float
    elev: float
    gain: float


@strawberry.django.type(models.Data)
class dataType:
    file_name: str
    station: str
    component: str
    date: datetime.date

# 圖片檔案


@ strawberry.type
class dataFileType:
    name: str
    data: Base64


@strawberry.type
class ResType:
    success: bool
    text: str

# input type


@strawberry.django.input(models.DownloadLog, partial=True)
class downloadInput:
    sizeBytes: int


@strawberry.input
class staIDInput:
    id: int

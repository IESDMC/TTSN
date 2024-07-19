import datetime
import numbers
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import requests
import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from __backend.models import DownloadLog, Station
from django.db.models import F
from gqlauth.core.field_ import field as fieldAuth
from gqlauth.core.types_ import GQLAuthError

from .decorater import ApiForIES
from .types import ResType, downloadInput, staIDInput


@strawberry.type
class UpdateDB:
    @strawberry.mutation
    def add_downloadLog(self, downloadInput: downloadInput) -> ResType:
        # print(downloadInput)
        DownloadLog.objects.create(
            size_bytes=downloadInput.sizeBytes,
        )

        return ResType(success=True, text=f'download log updated')

    @strawberry.mutation
    def add_ttsn(self, staIDInput: staIDInput) -> ResType:
        id = staIDInput.id

        station = network_stations.objects.filter(id__exact=id).values().first()

        keys_to_delete = ["id", "sub_network"]
        for key in keys_to_delete:
            del station[key]
        # print(station)

        pgaindb = Station.objects.filter(
            network_code__exact=station['network_code'], station_code__exact=station['station_code']).values()
        # print('pgaindb', pgaindb)
        if pgaindb:
            return ResType(success=False, text=f'data in DB')
        else:
            Station.objects.create(
                **station,
                status=2
            )
            return ResType(success=True, text=f'')

    @strawberry.mutation
    def remove_ttsn(self, staIDInput: staIDInput) -> ResType:
        id = staIDInput.id
        Station.objects.get(id=id).delete()
        return ResType(success=True, text=f'')


@strawberry.type
class Mutation:

    @fieldAuth(directives=[ApiForIES()])
    def auth_IES(self) -> Union[GQLAuthError, UpdateDB]:
        return UpdateDB()

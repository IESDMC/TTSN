import datetime
import numbers
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import requests
import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from backend.models import Station
from django.db.models import F
from gqlauth.core.field_ import field as fieldAuth
from gqlauth.core.types_ import GQLAuthError

from .types import ResType, staIDInput


@strawberry.type
class UpdateDB:
    @strawberry.mutation
    def test(self) -> ResType:
        return ResType(success=True, text=f'')

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

    # @strawberry.mutation
    # def add_PGA(self, PGAInput: PGAInput) -> ResType:
    #     date = PGAInput.date
    #     time_ = PGAInput.time
    #     staCode = PGAInput.staCode

    #     datetime_ = datetime.datetime.combine(date, time_)
    #     print('PGAInput', PGAInput)
    #     # eventID = Event.objects.filter(Date__exact=date, Time__exact=time_).values_list('CWB_ID', flat=True).get()
    #     # # print('eventID', eventID)
    #     # # check input data
    #     # if not eventID:
    #     #     return ResType(success=False, text=f'event is not in DB')
    #     pgaindb = PGA.objects.filter(event__exact=datetime_, staCode__exact=staCode)
    #     # print('pgaindb', pgaindb)
    #     if pgaindb:
    #         return ResType(success=False, text=f'data in DB')
    #     else:
    #         PGA.objects.create(
    #             event=datetime_,
    #             staCode=staCode,
    #             pga=PGAInput.pga if PGAInput.pga is not strawberry.UNSET else None,
    #             pgv=PGAInput.pgv if PGAInput.pgv is not strawberry.UNSET else None,
    #             az=PGAInput.az,
    #             dist=PGAInput.dist,
    #         )

    #         return ResType(success=True, text=f'')


@strawberry.type
class Mutation:
    @strawberry.mutation
    def updateDB(self) -> UpdateDB:
        return UpdateDB()

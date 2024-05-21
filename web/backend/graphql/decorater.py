from abc import ABC, abstractmethod
from typing import Any, List, Optional

import strawberry
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from gqlauth.core.directives import BaseAuthDirective
from gqlauth.core.exceptions import TokenExpired
from gqlauth.core.types_ import GQLAuthError, GQLAuthErrors
from gqlauth.jwt.types_ import TokenType
from gqlauth.settings import gqlauth_settings as app_settings
from jwt import PyJWTError
from strawberry.schema_directive import Location
from strawberry.types import Info

USER_MODEL = get_user_model()


# IES IP 140.109.80 81 82
limitedIP = ['140.109.80', '140.109.81', '140.109.82', '172.23.0']


@strawberry.schema_directive(
    locations=[
        Location.FIELD_DEFINITION,
    ],
    description="only IES ip could use the apis",
)
class ApiForIES(BaseAuthDirective):
    def resolve_permission(self, source: Any, info: Info, args, kwargs):
        # REMOTE_ADDR 會抓到區網ip , HTTP_HOST 抓到對外的ip:port
        IP = info.context.request.META.get('HTTP_HOST')  # REMOTE_ADDR
        a, b, c, _ = IP.split(".")
        ip = f'{a}.{b}.{c}'
        # print(info.context.request.META)
        if ip not in limitedIP:
            return GQLAuthError(code=GQLAuthErrors.UNAUTHENTICATED)
        return None

# gqlauth/jwt/types_.py
import json
from typing import Optional, cast

import requests
import strawberry
from django.conf import settings
from gqlauth.core.constants import Messages
# 不然 gqlauth.core裡面會有 module 'gqlauth.core' has no attribute 'field_' bug
from gqlauth.core.field_ import field
from gqlauth.core.interfaces import OutputInterface
from gqlauth.core.mixins import ArgMixin
from gqlauth.core.utils import inject_fields
from gqlauth.jwt.types_ import ExpectedErrorType
from gqlauth.settings import gqlauth_settings as app_settings
from gqlauth.user.resolvers import BaseMixin
from gqlauth.user.types_ import UserType

# app_settings = settings.GQL_AUTH

# recaptcha


def checkRecaptcha(input_):
    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
    secret = getattr(settings, "GOOGLE_RECAPTCHA_SECRET")
    targetScore = getattr(settings, "GOOGLE_RECAPTCHA_SCORE")
    recaptcha_token = input_.recaptcha
    # print("recaptcha_token", recaptcha_token)
    response = requests.post(recaptcha_url,
                             data={
                                 'secret': secret,
                                 'response': recaptcha_token,
                             })

    content = json.loads(response.text)
    status = not content['success']
    score = content['score']
    # print("recaptcha", status, score)
    if status or score < targetScore:
        return False
    else:
        return True


@strawberry.input  # @inject_fields(app_settings.LOGIN_FIELDS)
class ObtainJSONWebTokenInput:
    # password: str
    if app_settings.LOGIN_REQUIRE_CAPTCHA:
        recaptcha: str


@strawberry.type(
    description="""
    encapsulates token data, and refresh token data if `JWT_LONG_RUNNING_REFRESH_TOKEN` is on.
    with an output interface.
    """
)
class ObtainJSONWebTokenType(OutputInterface):
    success: bool
    user: Optional[UserType] = None
    # token: Optional[TokenType] = None
    # if app_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
    #     refresh_token: Optional[RefreshTokenType] = None
    errors: Optional[ExpectedErrorType] = None


# gqlauth/user/resolvers.py


class ObtainJSONWebTokenMixin(BaseMixin):
    """
    Obtain JSON web token for given user.
    Allow to perform login with different fields,
    The fields are defined on settings.
    Not verified users can log in by default. This
    can be changes on settings.
    If user is archived, make it unarchived and
    return `unarchiving=True` on OutputBase.
    """

    @classmethod
    def resolve_mutation(cls, info, input_: ObtainJSONWebTokenInput) -> ObtainJSONWebTokenType:
        if app_settings.LOGIN_REQUIRE_CAPTCHA:
            try:
                status = checkRecaptcha(input_)
                if status:
                    return ObtainJSONWebTokenType(success=True)
                else:
                    return ObtainJSONWebTokenType(success=False, errors=Messages.UNAUTHENTICATED)
            except:
                return ObtainJSONWebTokenType(success=False, errors=Messages.UNAUTHENTICATED)
        return ObtainJSONWebTokenType(success=True)


# # gqlauth/user/arg_mutations.py
class ObtainJSONWebToken(ObtainJSONWebTokenMixin, ArgMixin):
    __doc__ = ObtainJSONWebTokenMixin.__doc__

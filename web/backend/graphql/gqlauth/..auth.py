# gqlauth/jwt/types_.py
import json
from dataclasses import asdict
from datetime import datetime
from smtplib import SMTPException
from typing import Optional, cast

import requests
import strawberry
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.signing import BadSignature, SignatureExpired
from django.db import transaction
from gqlauth.core.constants import Messages, TokenAction
from gqlauth.core.exceptions import PasswordAlreadySetError, TokenExpired, TokenScopeError, UserAlreadyVerified, \
    UserNotVerified
from gqlauth.core.interfaces import OutputInterface
from gqlauth.core.mixins import ArgMixin
from gqlauth.core.types_ import GQLAuthError, GQLAuthErrors, MutationNormalOutput
from gqlauth.core.utils import get_payload_from_token, get_user_by_email, inject_fields
from gqlauth.jwt.types_ import ExpectedErrorType, RefreshTokenType, TokenType
from gqlauth.models import RefreshToken
from gqlauth.settings import gqlauth_settings as app_settings
from gqlauth.user.forms import EmailForm, PasswordLessRegisterForm, RegisterForm
from gqlauth.user.resolvers import BaseMixin
from gqlauth.user.signals import user_registered, user_verified
from gqlauth.user.types_ import UserType
from strawberry.types import Info

# from .models import CustomUser as users

app_settings = settings.GQL_AUTH
# USER_MODEL = get_user_model()


# recaptcha
def checkRecaptcha(input_):
    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
    secret = getattr(settings, "GOOGLE_RECAPTCHA_SECRET")
    targetScore = getattr(settings, "GOOGLE_RECAPTCHA_SCORE")
    recaptcha_token = input_.recaptcha
    response = requests.post(recaptcha_url,
                             data={
                                 'secret': secret,
                                 'response': recaptcha_token,
                             })

    content = json.loads(response.text)
    status = not content['success']
    score = content['score']
    print("recaptra", status, score)
    if status or score < targetScore:
        return False
    else:
        return True

# recaptcha end

# from gqlauth.jwt.types_ import ObtainJSONWebTokenInput


@strawberry.input
@inject_fields(app_settings.LOGIN_FIELDS)
class ObtainJSONWebTokenInput:
    password: str
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
    token: Optional[TokenType] = None
    if app_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
        refresh_token: Optional[RefreshTokenType] = None
    errors: Optional[ExpectedErrorType] = None

    @classmethod
    def from_user(cls, user: AbstractBaseUser) -> "ObtainJSONWebTokenType":
        """
        creates a new token and possibly a new refresh token based on the user.
        *call this method only for trusted users.*
        """

        ret = ObtainJSONWebTokenType(
            success=True, user=cast(UserType, user), token=TokenType.from_user(user)
        )
        if app_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
            ret.refresh_token = cast(RefreshTokenType, RefreshToken.from_user(user))
        return ret

    @classmethod
    def authenticate(cls, info: Info, input_: ObtainJSONWebTokenInput) -> "ObtainJSONWebTokenType":
        """
        return `ObtainJSONWebTokenType`.
        authenticates against django authentication backends.
        *creates a new token and possibly a refresh token.*
        """
        # only modified here
        # EMAIL_FIELD -> USERNAME_FIELD
        try:
            email = 'aaa'
            username = users.objects.filter(email=email).values_list('username', flat=True)[0]
        except:
            return ObtainJSONWebTokenType(success=False, errors=[{"message": "Invalid email."}])

        args = {
            'user': username,
            "password": input_.password,
        }

        # only modified here end

        try:
            # authenticate against django authentication backends.
            if not (user := authenticate(info.context.request, **args)):
                return ObtainJSONWebTokenType(success=False, errors=Messages.INVALID_CREDENTIALS)
            from gqlauth.models import UserStatus

            status: UserStatus = getattr(user, "status")  # noqa: B009
            # gqlauth logic
            if status.archived is True:  # un-archive on login
                UserStatus.unarchive(user)
            if status.verified or app_settings.ALLOW_LOGIN_NOT_VERIFIED:
                # successful login.
                u = users.objects.filter(email=email)
                loginTime = datetime.now()
                u.update(last_login=loginTime)
                return ObtainJSONWebTokenType.from_user(user)
            else:
                return ObtainJSONWebTokenType(success=False, errors=Messages.NOT_VERIFIED)

        except PermissionDenied:
            # one of the authentication backends rejected the user.
            return ObtainJSONWebTokenType(success=False, errors=Messages.UNAUTHENTICATED)

        except TokenExpired:
            return ObtainJSONWebTokenType(success=False, errors=Messages.EXPIRED_TOKEN)


# gqlauth/user/resolvers.py
# from gqlauth.user.helpers import check_captcha


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
                    return ObtainJSONWebTokenType.authenticate(info, input_)
                else:
                    return ObtainJSONWebTokenType(success=False, errors=Messages.UNAUTHENTICATED)
            except:
                return ObtainJSONWebTokenType(success=False, errors=Messages.UNAUTHENTICATED)
        return ObtainJSONWebTokenType.authenticate(info, input_)


class RefreshTokenMixin(BaseMixin):
    """
    ### refreshToken to generate a new login token:
    *Use this only if `JWT_LONG_RUNNING_REFRESH_TOKEN` is True*
    using the refresh-token you already got during authorization, and
    obtain a brand-new token (and possibly a new refresh token if you revoked the previous).
    This is an alternative to log in when your token expired.
    """

    @strawberry.input(
        description="If `revoke_refresh_token` is true,"
        " revokes to refresh token an creates a new one."
    )
    class RefreshTokenInput:
        refresh_token: str
        revoke_refresh_token: bool = strawberry.field(
            description="revokes the previous refresh token, and will generate new one.",
            default=False,
        )

    @classmethod
    def resolve_mutation(cls, info, input_: RefreshTokenInput) -> ObtainJSONWebTokenType:
        try:
            res = RefreshToken.objects.get(token=input_.refresh_token)
        except RefreshToken.DoesNotExist:
            return ObtainJSONWebTokenType(success=False, errors=Messages.INVALID_TOKEN)
        user = res.user
        if res.is_expired_():
            return ObtainJSONWebTokenType(success=False, errors=Messages.EXPIRED_TOKEN)
        # fields that are determined by if statements are not recognized by mypy.
        ret = ObtainJSONWebTokenType(
            success=True, token=TokenType.from_user(user), refresh_token=res  # type: ignore
        )
        if input_.revoke_refresh_token:
            res.revoke()
            ret.refresh_token = cast(RefreshTokenType, RefreshToken.from_user(user))
        return ret


class RegisterMixin(BaseMixin):
    """Register user with fields defined in the settings. If the email field of
    the user model is part of the registration fields (default), check if there
    is no user with that email.
    If it exists, it does not register the user,
    even if the email field is not defined as unique
    (default of the default django user model).
    When creating the user, it also creates a `UserStatus`
    related to that user, making it possible to track
    if the user is archived / verified.
    Send account verification email.
    If allowed to not verified users login, return token.
    """

    @strawberry.input
    @inject_fields(app_settings.REGISTER_MUTATION_FIELDS)
    class RegisterInput:
        if not app_settings.ALLOW_PASSWORDLESS_REGISTRATION:
            password1: str
            password2: str

        if app_settings.REGISTER_REQUIRE_CAPTCHA:
            recaptcha: str

    form = (
        PasswordLessRegisterForm if app_settings.ALLOW_PASSWORDLESS_REGISTRATION else RegisterForm
    )

    @classmethod
    def resolve_mutation(cls, info, input_: RegisterInput) -> MutationNormalOutput:
        if app_settings.LOGIN_REQUIRE_CAPTCHA:
            status = checkRecaptcha(input_)
            if not status:
                return MutationNormalOutput(success=False, errors=Messages.CAPTCHA_INVALID)
        email = getattr(input_, "email", False)
        try:
            with transaction.atomic():
                f = cls.form(asdict(input_))
                if f.is_valid():
                    user = f.save()
                    if email:
                        send_activation = app_settings.SEND_ACTIVATION_EMAIL is True
                        send_password_set = (
                            app_settings.ALLOW_PASSWORDLESS_REGISTRATION is True
                            and app_settings.SEND_PASSWORD_SET_EMAIL is True
                        )
                        if send_activation:
                            user.status.send_activation_email(info)

                        if send_password_set:
                            user.status.send_password_set_email(info)

                    user_registered.send(sender=cls, user=user)
                    return MutationNormalOutput(success=True)
                else:
                    return MutationNormalOutput(success=False, errors=f.errors.get_json_data())
        except SMTPException:
            return MutationNormalOutput(success=False, errors=Messages.EMAIL_FAIL)


# email for VerifyAccountMixin
def send_email_to_managers(user, **kwargs):
    from django.core.mail import mail_managers
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    _subject = render_to_string('email/wake_up_managers_subject.txt', {'user': user}).replace("\n", " ").strip()
    _html_message = render_to_string('email/wake_up_managers_email.html', {'user': user})
    _message = strip_tags(_html_message)
    mail_managers(
        subject=_subject,
        message=_message,
        html_message=_html_message,
        fail_silently=False,
    )

#########


class VerifyAccountMixin(BaseMixin):
    """Verify user account.
    Receive the token that was sent by email. If the token is valid,
    make the user verified by making the `user.status.verified` field
    true.
    """

    @strawberry.input
    class VerifyAccountInput:
        token: str

    @classmethod
    def resolve_mutation(cls, info: Info, input_: VerifyAccountInput) -> MutationNormalOutput:

        try:
            from gqlauth.models import UserStatus
            UserStatus.verify(input_.token)
            send_email_to_managers("New one")
            return MutationNormalOutput(success=True)
        except UserAlreadyVerified:
            return MutationNormalOutput(success=False, errors=Messages.ALREADY_VERIFIED)
        except SignatureExpired:
            return MutationNormalOutput(success=False, errors=Messages.EXPIRED_TOKEN)
        except (BadSignature, TokenScopeError):
            return MutationNormalOutput(success=False, errors=Messages.INVALID_TOKEN)


# sent email to reset password


class SendPasswordResetEmailMixin(BaseMixin):
    """Send password reset email.
    For non verified users, send an activation
    email instead.
    If there is no user with the requested email,
    a successful response is returned.
    """

    @strawberry.input
    class SendPasswordResetEmailInput:
        email: str
        if app_settings.LOGIN_REQUIRE_CAPTCHA:
            recaptcha: str

    @classmethod
    def resolve_mutation(cls, info, input_: SendPasswordResetEmailInput) -> MutationNormalOutput:
        try:
            if app_settings.LOGIN_REQUIRE_CAPTCHA:
                status = checkRecaptcha(input_)
            if not status:
                return MutationNormalOutput(success=False, errors=Messages.CAPTCHA_INVALID)

            email = input_.email
            f = EmailForm({"email": email})
            if f.is_valid():
                user = get_user_by_email(email)
                user.status.send_password_reset_email(info, [email])
                return MutationNormalOutput(success=True)
            return MutationNormalOutput(success=False, errors=f.errors.get_json_data())
        except ObjectDoesNotExist:
            return MutationNormalOutput(success=True)  # even if user is not registered
        except SMTPException:
            return MutationNormalOutput(success=False, errors=Messages.EMAIL_FAIL)
        except UserNotVerified:
            user = get_user_by_email(input_.email)
            try:
                user.status.resend_activation_email(info)
                return MutationNormalOutput(
                    success=False,
                    errors={"email": Messages.NOT_VERIFIED_PASSWORD_RESET},
                )
            except SMTPException:
                return MutationNormalOutput(success=False, errors=Messages.EMAIL_FAIL)


# reset password


class PasswordResetMixin(BaseMixin):
    """Change user password without old password.
    Receive the token that was sent by email.
    If token and new passwords are valid, update
    user password and in case of using refresh
    tokens, revoke all of them.
    Also, if user has not been verified yet, verify it.
    """

    @strawberry.input
    class PasswordResetInput:
        token: str
        new_password1: str
        new_password2: str
        if app_settings.LOGIN_REQUIRE_CAPTCHA:
            recaptcha: str

    form = SetPasswordForm

    @classmethod
    def resolve_mutation(cls, _, input_: PasswordResetInput) -> MutationNormalOutput:
        try:
            payload = get_payload_from_token(
                input_.token,
                TokenAction.PASSWORD_RESET,
                app_settings.EXPIRATION_PASSWORD_RESET_TOKEN,
            )
            user = 'aaa'
            status: "UserStatus" = getattr(user, "status")  # noqa: B009
            f = cls.form(user, asdict(input_))
            if f.is_valid():
                user = f.save()  # type: ignore
                if status.verified is False:
                    status.verified = True
                    status.save(update_fields=["verified"])
                    user_verified.send(sender=cls, user=user)

                return MutationNormalOutput(success=True)
            return MutationNormalOutput(success=False, errors=f.errors.get_json_data())
        except SignatureExpired:
            return MutationNormalOutput(success=False, errors=Messages.EXPIRED_TOKEN)
        except (BadSignature, TokenScopeError):
            return MutationNormalOutput(success=False, errors=Messages.INVALID_TOKEN)
# reset password end


# gqlauth/user/arg_mutations.py


class ObtainJSONWebToken(ObtainJSONWebTokenMixin, ArgMixin):
    __doc__ = ObtainJSONWebTokenMixin.__doc__


# class RefreshTokenClass(RefreshTokenMixin, ArgMixin):
#     __doc__ = RefreshTokenMixin.__doc__


# class VerifyAccountClass(VerifyAccountMixin, ArgMixin,):
#     __doc__ = VerifyAccountMixin.__doc__


# class Register(RegisterMixin, ArgMixin):
#     __doc__ = RegisterMixin.__doc__


# class SendPasswordResetEmail(SendPasswordResetEmailMixin, ArgMixin):
#     __doc__ = SendPasswordResetEmailMixin.__doc__


# class PasswordReset(PasswordResetMixin, ArgMixin):
#     __doc__ = PasswordResetMixin.__doc__

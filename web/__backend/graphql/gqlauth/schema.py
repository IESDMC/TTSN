
# quickstart.schema.py
import strawberry

from .auth import ObtainJSONWebToken


@strawberry.type
class Mutation:
    token_auth = ObtainJSONWebToken.field

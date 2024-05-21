from typing import List

# import backend.models as model
import strawberry

from .gqlauth.schema import Mutation as AuthMutation
from .mutation import Mutation
from .query import Query


@strawberry.type
class Queries(Query):
    pass


@strawberry.type
class Mutations(AuthMutation, Mutation):
    pass


schema = strawberry.Schema(query=Queries, mutation=Mutations)

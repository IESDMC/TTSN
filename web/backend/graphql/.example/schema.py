from symtable import SymbolTable
from typing import List

import strawberry
import strawberry_django
import strawberry_django.auth as auth
from strawberry_django import mutations

from . import resolver
from .type_ import (Color, ColorInput, ColorPartialInput, Fruit, FruitInput,
                    FruitPartialInput, User, UserInput)


@ strawberry.type
class Query:
    fruit: Fruit = strawberry_django.field()
    fruits: List[Fruit] = strawberry_django.field()

    color: Color = strawberry_django.field()
    colors: List[Color] = strawberry_django.field()

    @ strawberry.field
    def hello(self, info) -> str:
        return "world"

    world: str = strawberry_django.field(resolver=resolver.get_test)


@ strawberry.type
class Mutation:
    createFruit: Fruit = mutations.create(FruitInput)
    createFruits: List[Fruit] = mutations.create(FruitInput)
    updateFruits: List[Fruit] = mutations.update(FruitPartialInput)
    deleteFruits: List[Fruit] = mutations.delete()

    createColor: Color = mutations.create(ColorInput)
    createColors: List[Color] = mutations.create(ColorInput)
    updateColors: List[Color] = mutations.update(ColorPartialInput)
    deleteColors: List[Color] = mutations.delete()

    register: User = auth.register(UserInput)


schema = strawberry.Schema(query=Query, mutation=Mutation)

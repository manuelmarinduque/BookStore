from graphene import Schema, ObjectType, Mutation
from graphql_jwt import ObtainJSONWebToken, Verify

from libro.schema import Query as LibroQuery
from libro.schema import Mutation as LibroMutation
from usuario.schema import Query as UsuarioQuery
from usuario.schema import Mutation as UsuarioMutation


class Query(UsuarioQuery, LibroQuery, ObjectType):
    pass


class Mutation(UsuarioMutation, LibroMutation, ObjectType):
    get_token = ObtainJSONWebToken.Field()
    verificar_token = Verify.Field()


schema = Schema(query=Query, mutation=Mutation)

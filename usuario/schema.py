from django.contrib.auth import get_user_model
from graphene import ObjectType, Field, String, Mutation
from graphene_django import DjangoObjectType


class UsuarioType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CrearUsuario(Mutation):
    usuario = Field(UsuarioType)

    class Arguments:
        username = String(required=True)
        password = String(required=True)
        email = String(required=True)

    def mutate(self, info, username, password, email):
        usuario = get_user_model()(username=username, email=email)
        usuario.set_password(password)
        usuario.save()
        return CrearUsuario(usuario=usuario)


class Query(ObjectType):
    usuario = Field(UsuarioType, username=String(required=True))

    def resolve_usuario(self, info, username):
        return get_user_model().objects.get(username=username)


class Mutation(ObjectType):
    crear_usuario = CrearUsuario.Field()

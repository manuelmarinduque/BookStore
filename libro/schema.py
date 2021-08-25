from graphene import Schema, ObjectType, InputObjectType, List, Field, String, Mutation
from graphene_django import DjangoObjectType

from .models import Editor, Libro, Autor, Categoria
from .schema_auxiliars import SchemaAuxiliarObj


# Definición de los tipos.

class EditorType(DjangoObjectType):
    class Meta():
        model = Editor
        fields = "__all__"


class AutorType(DjangoObjectType):
    class Meta():
        model = Autor
        fields = "__all__"


class CategoriaType(DjangoObjectType):
    class Meta():
        model = Categoria
        fields = "__all__"


class LibroType(DjangoObjectType):
    class Meta():
        model = Libro
        fields = "__all__"


# Definición de las consultas.

class Query(ObjectType):

    libros = List(LibroType, titulo_libro=String())

    def resolve_libros(self, info, titulo_libro: str):
        SchemaAuxiliarObj.ValidarEntrada(titulo_libro)
        libros = Libro.objects.filter(title__icontains=titulo_libro)
        if not len(libros):
            libros_google = SchemaAuxiliarObj.ObtenerLibrosDeGoogle(titulo_libro)
            print(next(libros_google))
        return libros


# Definición de las mutaciones.

# Definición de las entradas.

class EditorInput(InputObjectType):
    name = String()


class AutorInput(InputObjectType):
    name = String()


class CategoriaInput(InputObjectType):
    name = String()


class LibroInput(InputObjectType):
    title = String()
    subtitle = String()
    year_published = String()
    description = String()
    image = String()
    editor = Field(EditorInput)
    autores = List(AutorInput)
    categorias = List(CategoriaInput)


# Definición de las creaciones.

class CrearLibro(Mutation):
    class Arguments:
        datos_libro = LibroInput(required=True)

    libro = Field(LibroType)

    @staticmethod
    def mutate(self, info, datos_libro=None):
        instancia_libro = SchemaAuxiliarObj.CrearLibro(datos_libro)
        return CrearLibro(libro=instancia_libro)


# Definición de las eliminaciones.

class EliminarLibro(Mutation):
    class Arguments:
        titulo = String()

    libro = Field(LibroType)

    @staticmethod
    def mutate(root, info, titulo):
        libros = Libro.objects.filter(title__icontains=titulo)
        for libro in libros:
            libro.delete()
        return None


# Definición de la clase Mutation.

class Mutation(ObjectType):
    crear_libro = CrearLibro.Field()
    eliminar_libro = EliminarLibro.Field()


# Define 'schema' object.

schema = Schema(query=Query, mutation=Mutation)

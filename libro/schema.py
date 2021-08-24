from graphene import Schema, ObjectType, InputObjectType, List, Field, String, Mutation
from graphene_django import DjangoObjectType

from .models import Editor, Libro, Autor, Categoria
from .schema_auxiliars import SchemaAuxiliarObj

from django.db import IntegrityError


# Create your types here.

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


# Create your queries here.

class Query(ObjectType):

    libros = List(LibroType, libro_title=String())

    def resolve_libros(self, info, libro_title):
        return Libro.objects.filter(title__icontains=libro_title)


# Create your mutations here.


# About inputs.

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


# About creations.


class CreateLibro(Mutation):
    class Arguments:
        libro_data = LibroInput(required=True)

    libro = Field(LibroType)

    @staticmethod
    def mutate(root, info, libro_data=None):
        editor_instance = SchemaAuxiliarObj.GetOrCreate(Editor, libro_data.editor.name)
        try:
            libro_instance = Libro.objects.create(
                title=libro_data.title,
                subtitle=libro_data.subtitle,
                editor=editor_instance,
                year_published=libro_data.year_published,
                description=libro_data.description,
                image=libro_data.image
            )
        except IntegrityError:
            raise Exception(f'Ya existe un libro con el título "{libro_data.title}".')
        for autor in libro_data.autores:
            autor_instance = SchemaAuxiliarObj.GetOrCreate(Autor, autor.name)
            libro_instance.autor.add(autor_instance)
        for categoria in libro_data.categorias:
            categoria_instance = SchemaAuxiliarObj.GetOrCreate(Categoria, categoria.name)
            libro_instance.categoria.add(categoria_instance)
        return CreateLibro(libro=libro_instance)


# 'Mutation' class.

class Mutation(ObjectType):
    create_libro = CreateLibro.Field()


# Define 'schema' object.

schema = Schema(query=Query, mutation=Mutation)

from graphene import Schema, ObjectType, InputObjectType, List, Field, String, Mutation
from graphene_django import DjangoObjectType

from .models import Editor, Libro, Autor, Categoria


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

    editores = List(EditorType)
    libros = List(LibroType, libro_title=String())
    autores = List(AutorType)
    categorias = List(CategoriaType)

    def resolve_editores(self, info, **kwargs):
        return Editor.objects.all()

    def resolve_libros(self, info, libro_title):
        return Libro.objects.filter(title__icontains=libro_title)
    
    def resolve_autores(self, info, **kwargs):
        return Autor.objects.all()

    def resolve_categorias(self, info, **kwargs):
        return Categoria.objects.all()


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
        print(libro_data)
        editor_instance = Editor.objects.create(name=libro_data.editor.name)
        libro_instance = Libro.objects.create(
            title=libro_data.title,
            subtitle=libro_data.subtitle,
            editor=editor_instance,
            year_published=libro_data.year_published,
            description=libro_data.description,
            image=libro_data.image,
            )
        for autor in libro_data.autores:
            autor_instance = Autor.objects.create(name=autor.name)
            libro_instance.autor.add(autor_instance)
        for categoria in libro_data.categorias:
            categoria_instance = Categoria.objects.create(name=categoria.name)
            libro_instance.categoria.add(categoria_instance)
        return CreateLibro(libro=libro_instance)


# 'Mutation' class.

class Mutation(ObjectType):
    create_libro = CreateLibro.Field()


# Define 'schema' object.

schema = Schema(query=Query, mutation=Mutation)
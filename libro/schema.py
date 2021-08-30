from graphene import ObjectType, InputObjectType, List, Field, String, Mutation, ID
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

    filtro_entrada = {
        'id':ID(),
        'titulo':String(), 
        'subtitulo':String(), 
        'anio':String(),
        'descripcion':String(),
        'url':String(),
        'editor':String(), 
        'autor':String(), 
        'categoria':String()
    }

    libros = List(LibroType, **filtro_entrada)

    def resolve_libros(self, info, **kwargs):
        SchemaAuxiliarObj.ValidarInicioSesion(info)
        filtro = SchemaAuxiliarObj.GetFiltro(kwargs)
        libros = Libro.objects.filter(**filtro)
        titulo = kwargs['titulo'] if 'titulo' in kwargs.keys() else ''
        autor = kwargs['autor'] if 'autor' in kwargs.keys() else ''
        categoria = kwargs['categoria'] if 'categoria' in kwargs.keys() else ''
        editor = kwargs['editor'] if 'editor' in kwargs.keys() else ''
        if not libros and (titulo or autor or categoria or editor):
            if titulo: SchemaAuxiliarObj.ValidarEntrada(titulo)
            libros_google = SchemaAuxiliarObj.BusquedaDeLibrosEnGoogle(title=titulo, author=autor, subject=categoria, publisher=editor)
            SchemaAuxiliarObj.CrearLibrosEnBD(libros_google)
            libros = Libro.objects.filter(**filtro)
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
    titulo = String()
    subtitulo = String()
    anio = String()
    descripcion = String()
    url = String()
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
        SchemaAuxiliarObj.ValidarInicioSesion(info)
        instancia_libro = SchemaAuxiliarObj.CrearLibro(datos_libro)
        return CrearLibro(libro=instancia_libro)


# Definición de las eliminaciones.

class EliminarLibro(Mutation):
    class Arguments:
        titulo = String()

    libros = List(LibroType)

    @staticmethod
    def mutate(self, info, titulo):
        SchemaAuxiliarObj.ValidarInicioSesion(info)
        libros = Libro.objects.filter(title__icontains=titulo)
        for libro in libros:
            libro.delete()
        return EliminarLibro(libros=libros)


# Definición de la clase Mutation.

class Mutation(ObjectType):
    crear_libro = CrearLibro.Field()
    eliminar_libro = EliminarLibro.Field()

from os import name
from requests import get
from .models import Editor, Autor, Categoria, Libro

# Create your auxiliars here.

class SchemaAuxiliar:

    def __ObtenerOCrearInstancia(self, model, **kwargs):
        instancia, _ = model.objects.get_or_create(**kwargs)
        return instancia

    def ObtenerLibrosDeGoogle(self, nombre_libro: str):
        recurso: str = f'https://www.googleapis.com/books/v1/volumes?q={nombre_libro}'
        datos_peticion = get(recurso).json()
        libros_google = datos_peticion['items']
        libros_google_formato_db = self.__LibrosFormatoBD(libros_google)
        return libros_google_formato_db

    def __LibrosFormatoBD(self, libros_google):
        for libro in libros_google:
            print(type(libro))
            datos_libro = {
                'title': libro['volumeInfo']['title'],
                'subtitle': libro['volumeInfo']['subtitle'],
                'editor': {'name': libro['volumeInfo']['authors'][0]},
                'yearPublished': libro['volumeInfo']['publishedDate'].split('-')[0],
                'description': libro['volumeInfo']['description'],
                'image': libro['volumeInfo']['imageLinks']['thumbnail'],
                'autores': self.__FormatoListaObjetos(libro['volumeInfo']['authors']),
                'categorias': self.__FormatoListaObjetos(libro['volumeInfo']['categories'])
            }
            yield datos_libro
    
    def __FormatoListaObjetos(self, lista):
        lista_objetos = []
        objeto = {}
        for elemento in lista:
            objeto['name'] = elemento
            lista_objetos.append(objeto)
        return lista_objetos


    def CrearLibrosDeGoogle(self, libros_google):
        for libro in libros_google:
            self.CrearLibro(libro)
    
    def CrearLibro(self, libro):
        instancia_editor = self.__ObtenerOCrearInstancia(Editor, name=libro['editor']['name'])
        datos_libro = {
            'title':libro['title'],
            'subtitle':libro['subtitle'],
            'editor':instancia_editor,
            'year_published':libro['year_published'],
            'description':libro['description'],
            'image':libro['image']
        }
        instancia_libro = self.__ObtenerOCrearInstancia(Libro, **datos_libro)
        for autor in libro.autores:
            instancia_autor = self.__ObtenerOCrearInstancia(Autor, name=autor['name'])
            instancia_libro.autor.add(instancia_autor)
        for categoria in libro.categorias:
            instancia_categoria = self.__ObtenerOCrearInstancia(Categoria, name=categoria['name'])
            instancia_libro.categoria.add(instancia_categoria)
        return instancia_libro

    def ValidarEntrada(self, texto_entrada: str):
        if not len(texto_entrada.split(' ')) >= 2:
            raise Exception(f'El título del libro a buscar es muy corto.')

SchemaAuxiliarObj = SchemaAuxiliar()

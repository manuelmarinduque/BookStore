from os import name
from requests import get
from .models import Editor, Autor, Categoria, Libro

# Create your auxiliars here.

class SchemaAuxiliar:

    def __ObtenerOCrearInstancia(self, model, **kwargs):
        instancia, _ = model.objects.get_or_create(**kwargs)
        return instancia

    def ObtenerLibrosDeGoogle(self, nombre_libro: str):
        recurso: str = f'https://www.googleapis.com/books/v1/volumes?q={nombre_libro}&langRestrict=es&maxResults=30&orderBy=relevance&printType=BOOKS&fields=items.volumeInfo.title%2C%20items.volumeInfo.subtitle%2C%20items.volumeInfo.authors%2C%20items.volumeInfo.publishedDate%2C%20items.volumeInfo.description%2C%20items.volumeInfo.categories%2C%20items.volumeInfo.imageLinks.thumbnail'
        datos_peticion = get(recurso).json()
        libros_google = datos_peticion['items']
        libros_google_formato_db = self.__LibrosFormatoBD(libros_google)
        return libros_google_formato_db

    def __LibrosFormatoBD(self, libros_google):
        for libro in libros_google:
            datos_libro = {
                'title': libro['volumeInfo']['title'],
                'subtitle': libro['volumeInfo'].get('subtitle', ''),
                'editor': {'name': libro['volumeInfo'].get('authors', ['no_definido'])[0]},
                'yearPublished': libro['volumeInfo'].get('publishedDate', '').split('-')[0],
                'description': libro['volumeInfo'].get('description', ''),
                'image': libro['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                'autores': self.__FormatoListaObjetos(libro['volumeInfo'].get('authors', ['no_definido'])),
                'categorias': self.__FormatoListaObjetos(libro['volumeInfo'].get('categories', ['no_definido']))
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
        try:
            instancia_editor = self.__ObtenerOCrearInstancia(Editor, name=libro['editor']['name'])
            datos_libro = {
                'title':libro['title'],
                'subtitle':libro['subtitle'],
                'editor':instancia_editor,
                'year_published':libro['yearPublished'],
                'description':libro['description'],
                'image':libro['image']
            }
            instancia_libro = self.__ObtenerOCrearInstancia(Libro, **datos_libro)
            for autor in libro['autores']:
                instancia_autor = self.__ObtenerOCrearInstancia(Autor, name=autor['name'])
                instancia_libro.autor.add(instancia_autor)
            for categoria in libro['categorias']:
                instancia_categoria = self.__ObtenerOCrearInstancia(Categoria, name=categoria['name'])
                instancia_libro.categoria.add(instancia_categoria)
            return instancia_libro
        except Exception:
            pass

    def ValidarEntrada(self, texto_entrada: str):
        if not len(texto_entrada.split(' ')) >= 2:
            raise Exception(f'El título del libro a buscar es muy corto.')

    def GetFiltro(self, valores_busqueda):
        filtro = {key:value for key, value in valores_busqueda.items() if len(value)>1}
        if 'titulo' in filtro.keys(): filtro['title__icontains'] = filtro.pop('titulo') 
        if 'subtitulo' in filtro.keys(): filtro['subtitle__icontains'] = filtro.pop('subtitulo') 
        if 'anio' in filtro.keys(): filtro['year_published'] = filtro.pop('anio')
        if 'description' in filtro.keys(): filtro['description__icontains'] = filtro.pop('description')
        if 'editor' in filtro.keys(): filtro['editor__name__icontains'] = filtro.pop('editor')
        if 'autor' in filtro.keys(): filtro['autor__name__icontains'] = filtro.pop('autor')
        if 'categoria' in filtro.keys(): filtro['categoria__name__icontains'] = filtro.pop('categoria')
        return filtro


SchemaAuxiliarObj = SchemaAuxiliar()

from requests import get
from graphql import GraphQLError

from .models import Editor, Autor, Categoria, Libro


# Create your auxiliars here.

class SchemaAuxiliar:

    def ValidarInicioSesion(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Debes iniciar sesión para acceder a esta funcionalidad.')

    def __ObtenerOCrearInstancia(self, model, **datos):
        instancia, _ = model.objects.get_or_create(**datos)
        return instancia

    def BusquedaDeLibrosEnGoogle(self, **kwargs):
        filtro_google = self.__GetFiltroGoogle(**kwargs)
        recurso: str = f'https://www.googleapis.com/books/v1/volumes?q={filtro_google}&filter=partial&langRestrict=es&maxResults=30&orderBy=relevance&printType=BOOKS&fields=items.volumeInfo.title%2C%20items.volumeInfo.subtitle%2C%20items.volumeInfo.authors%2C%20items.volumeInfo.publishedDate%2C%20items.volumeInfo.description%2C%20items.volumeInfo.categories%2C%20items.volumeInfo.publisher%2C%20items.volumeInfo.imageLinks.thumbnail'
        datos_peticion = get(recurso).json()
        if datos_peticion:
            libros_google = datos_peticion['items']
            libros_google_formato_db = self.__LibrosFormatoBD(libros_google)
            return libros_google_formato_db
        else:
            return []

    def __GetFiltroGoogle(self, **atributos):
        filtro_auxiliar_1 = {key:value for key,value in atributos.items() if value}
        filtro_auxiliar = {f'in{key}':value if key=='title' or key=='author' or key=='publisher' else {key:value} for key,value in filtro_auxiliar_1.items()}
        filtro_google = ''
        for key,value in filtro_auxiliar.items():
            filtro_google += f'{key}:{value}%20'
        return filtro_google

    def __LibrosFormatoBD(self, libros_google):
        for libro in libros_google:
            datos_libro = {
                'titulo': libro['volumeInfo']['title'],
                'subtitulo': libro['volumeInfo'].get('subtitle', ''),
                'editor': {'name': libro['volumeInfo'].get('publisher', ['no_definido'])},
                'anio': libro['volumeInfo'].get('publishedDate', '').split('-')[0],
                'descripcion': libro['volumeInfo'].get('description', ''),
                'url': libro['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
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

    def CrearLibrosEnBD(self, libros):
        for libro in libros:
            self.CrearLibro(libro)
    
    def CrearLibro(self, libro):
        try:
            instancia_editor = self.__ObtenerOCrearInstancia(Editor, name=libro['editor']['name'])
            datos_libro = {
                'title':libro['titulo'],
                'subtitle':libro['subtitulo'],
                'editor':instancia_editor,
                'year_published':libro['anio'],
                'description':libro['descripcion'],
                'image':libro['url']
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
        if not len(texto_entrada) >= 4:
            raise GraphQLError(f'El título del libro a buscar es muy corto.')

    def GetFiltro(self, valores_busqueda):
        filtro = {}
        if 'titulo' in valores_busqueda.keys(): filtro['title__icontains'] = valores_busqueda['titulo']
        if 'subtitulo' in valores_busqueda.keys(): filtro['subtitle__icontains'] = valores_busqueda['subtitulo']
        if 'anio' in valores_busqueda.keys(): filtro['year_published'] = valores_busqueda['anio']
        if 'description' in valores_busqueda.keys(): filtro['description__icontains'] = valores_busqueda['description']
        if 'url' in valores_busqueda.keys(): filtro['image__icontains'] = valores_busqueda['url']
        if 'editor' in valores_busqueda.keys(): filtro['editor__name__icontains'] = valores_busqueda['editor']
        if 'autor' in valores_busqueda.keys(): filtro['autor__name__icontains'] = valores_busqueda['autor']
        if 'categoria' in valores_busqueda.keys(): filtro['categoria__name__icontains'] = valores_busqueda['categoria']
        return filtro


SchemaAuxiliarObj = SchemaAuxiliar()

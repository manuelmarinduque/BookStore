# Proyecto BookStore

## Características

Este proyecto consta de las siguientes carácteristicas:

1. La aplicación se desarolló en Python 3.8.10 mediante el framework Django v3.2.6 y los paquetes que se listan en el archivo _requirements.txt_.

2. Comprende un diseño de base de datos hecho en PostgreSQL.

3. Es una API de tipo GraphQL.

4. Consta de un servicio web para buscar un libro por los atributos de id, titulo, subtítulo, nombre del editor o editorial, año, descripción, nombre de uno de sus autores, nombre de una de sus categorías. Principalmente se realiza la búsqueda del libro dentro de la base de datos y en caso de no existir, se consulta la API de _Google Books_ y la API de _OpenLibrary_, almacenando en la base de datos los libros encontrados en ambas API y mostrándolos como respuesta.

5. Consta de un servicio web para eliminar un libro, mediante el título.

6. Los endpoints están protegidos con el mecanismo de seguridad _JWT_, razón por la cual el usuario quien utiliza la aplicación debe estár registrado y debe haber iniciado sesión para poder consultar un libro.


## Modo de uso

Endpoint único:

```
https://bookstoreappr5.herokuapp.com/api/v1/book
```

1. Registro del usuario:

```
mutation {
  crearUsuario(
    username: "###"
    password: "###"
    email: ""
  )
  {
    usuario {
      username
      password
      email
    }
  }
}
```

2. Inicio de sesión para obtener el token de acceso:

```
mutation {
  getToken(username:"###", password:"###")
  {
    token
  }
}
```

3. Creación de un libro:

```
mutation {
  crearLibro(datosLibro:{
    titulo: "###"
    subtitulo: "###"
    descripcion: "###"
    editor: {
      name: "###"
    }
    autores: [
      {
        name: "###"
      }
    ]
    categorias: [
      {
        name: "###"
      }
    ]
    url: "###"
    anio: "###"
  })
  {
    libro {
      title
      autor {
        name
      }
      categoria {
        name
      }
    }
  }
}
```

4. Consulta de un libro:

```
query {
  libros (titulo: "###"
          autor: "###"
          categoria: "###"
          editor: "###"){
    title,
    autor {
      name
    }
    categoria {
      name
    }
    yearPublished
    editor {
      name
    }
  }
}
```

5. Eliminación de un libro:

```
mutation{
  eliminarLibro(titulo:"###")
  {
    libros {
      title
    }
  }
}
```

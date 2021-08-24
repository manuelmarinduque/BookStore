from django.db import models


# Create your models here.

class Editor(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre del editor', unique=True)

    def __str__(self):
        return self.name


class Autor(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre del autor', unique=True)

    def __str__(self):
        return self.name


class Categoria(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre de la categoría', unique=True)

    def __str__(self):
        return self.name


class Libro(models.Model):
    title = models.CharField(max_length=200, verbose_name='Titulo', unique=True)
    subtitle = models.CharField(max_length=200, verbose_name='Subtitulo')
    year_published = models.CharField(max_length=4, verbose_name='Fecha de publicación')
    description = models.TextField(verbose_name='Descripción')
    image = models.URLField(verbose_name='Url de la imágen')
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, verbose_name='Editor del libro')
    autor = models.ManyToManyField(Autor, verbose_name='Autores del libro')
    categoria = models.ManyToManyField(Categoria, verbose_name='Categorías del libro')

    def __str__(self):
        return self.title

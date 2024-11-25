from django.db import models
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


from .utils import get_movie_data_from_api

import requests
from django.db import models
from django.core.files.base import ContentFile

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)  # Duración en minutos
    language = models.CharField(max_length=50, null=True, blank=True)  # Idioma original
    director = models.CharField(max_length=200, null=True, blank=True)  # Director
    cast = models.TextField(null=True, blank=True)  # Reparto
    tmdb_url = models.URLField(null=True, blank=True)  # Enlace a TMDb
    poster_image = models.ImageField(upload_to='posters/', blank=True, null=True)  # Imagen seleccionada o descargada
    header_image = models.ImageField(upload_to='headers/', blank=True, null=True)  # Imagen del encabezado
    drive_url = models.URLField()  # Enlace a Google Drive
    drive_url = models.URLField()  # Enlace de Google Drive
    genres = models.ManyToManyField('Genre', related_name='movies')  # Relación con géneros
    review = models.TextField(blank=True, null=True)  # Reseña opcional

def save(self, *args, **kwargs):
    # Transformar la URL de Google Drive a formato de previsualización
    if self.drive_url and "drive.google.com" in self.drive_url:
        if "/view" in self.drive_url or "?usp" in self.drive_url:
            # Extraer el ID del archivo
            file_id = self.drive_url.split('/d/')[1].split('/')[0]
            self.drive_url = f"https://drive.google.com/file/d/{file_id}/preview"

    # Solo intenta obtener datos de la API si faltan campos clave
    if not self.description or not self.release_date or not self.rating:
        movie_data = get_movie_data_from_api(self.title)
        if movie_data:
            self.description = movie_data.get('overview', self.description)
            self.release_date = movie_data.get('release_date', self.release_date)
            self.rating = movie_data.get('vote_average', self.rating)
            self.duration = movie_data.get('runtime', self.duration)
            self.language = movie_data.get('original_language', self.language)
            self.tmdb_url = movie_data.get('tmdb_url', self.tmdb_url)
            self.director = movie_data.get('director', self.director)
            self.cast = movie_data.get('cast', self.cast)

            # Descargar la imagen desde la API si no hay una seleccionada
            if not self.poster_image and movie_data.get('poster_path'):
                poster_url = f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}"
                try:
                    response = requests.get(poster_url, timeout=10)
                    response.raise_for_status()
                    # Guardar la imagen descargada en el servidor
                    image_name = f"posters/{self.title.replace(' ', '_')}_poster.jpg"
                    self.poster_image.save(image_name, ContentFile(response.content), save=False)
                except requests.RequestException as e:
                    print(f"Error al descargar la imagen: {e}")

    # Asignar un encabezado predeterminado si no se proporciona uno personalizado
    if not self.header_image:
        default_header_path = 'static/banners/header_default.jpg'
        try:
            with open(default_header_path, 'rb') as f:
                self.header_image.save(
                    'default_header.jpg',
                    ContentFile(f.read()),
                    save=False
                )
        except FileNotFoundError:
            print(f"No se encontró el archivo predeterminado en {default_header_path}")

    # Guardar la instancia del modelo
    super().save(*args, **kwargs)


    
class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.movie.title}'
    




    


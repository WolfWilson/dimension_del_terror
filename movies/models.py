from django.db import models
from django.core.files.base import ContentFile
import requests
from .utils import get_movie_data_from_api
from django.utils.html import strip_tags
from django_ckeditor_5.fields import CKEditor5Field


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


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
    poster_image = models.ImageField(upload_to='posters/', blank=True, null=True)
    header_image = models.ImageField(upload_to='headers/', blank=True, null=True)  # Imagen del encabezado
    drive_url = models.URLField()
    trailer_url = models.URLField(null=True, blank=True)  # Nuevo campo para la URL del tráiler
    genres = models.ManyToManyField('Genre', related_name='movies')
    review = CKEditor5Field('Review', config_name='default', blank=True, null=True)

    def save(self, *args, **kwargs):
        print(f"Iniciando guardado de la película: {self.title}")

        # Validación y limpieza de la reseña
       

        # Transformar la URL de Google Drive
        if self.drive_url and "drive.google.com" in self.drive_url:
            if "/view" in self.drive_url or "?usp" in self.drive_url:
                file_id = self.drive_url.split('/d/')[1].split('/')[0]
                self.drive_url = f"https://drive.google.com/file/d/{file_id}/preview"
                print(f"URL de Google Drive transformada: {self.drive_url}")

        # Intentar obtener datos de la API si los campos clave están vacíos
        if not self.description or not self.release_date or not self.rating or not self.trailer_url:
            print("Intentando obtener datos desde la API...")
            movie_data = get_movie_data_from_api(self.title)
            if movie_data:
                print(f"Datos obtenidos de la API: {movie_data}")

                # Asignar datos obtenidos de la API
                self.description = movie_data.get('overview', self.description)
                self.release_date = movie_data.get('release_date', self.release_date)
                self.rating = movie_data.get('vote_average', self.rating)
                self.duration = movie_data.get('runtime', self.duration)
                self.language = movie_data.get('original_language', self.language)
                self.tmdb_url = movie_data.get('tmdb_url', self.tmdb_url)
                self.director = movie_data.get('director', self.director)

                if not self.cast and movie_data.get('cast'):
                    self.cast = movie_data['cast']

                if not self.trailer_url and movie_data.get('trailer_url'):
                    self.trailer_url = movie_data['trailer_url']

                # Descargar y asignar el póster
                if not self.poster_image and movie_data.get('poster_path'):
                    poster_url = f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}"
                    try:
                        response = requests.get(poster_url, timeout=10)
                        response.raise_for_status()
                        image_name = f"posters/{self.title.replace(' ', '_')}_poster.jpg"
                        self.poster_image.save(image_name, ContentFile(response.content), save=False)
                        print(f"Póster descargado y asignado: {image_name}")
                    except requests.RequestException as e:
                        print(f"Error al descargar el póster: {e}")

        # Asignar un header predeterminado si no se proporciona uno personalizado
        if not self.header_image:
            default_header_path = 'static/banners/header_default.jpg'
            print(f"Intentando asignar header predeterminado desde {default_header_path}")
            try:
                with open(default_header_path, 'rb') as f:
                    self.header_image.save('default_header.jpg', ContentFile(f.read()), save=False)
                    print("Header predeterminado asignado correctamente.")
            except FileNotFoundError:
                print(f"No se encontró el archivo predeterminado en {default_header_path}")

        # Llamar al método `save` original para guardar los datos
        super().save(*args, **kwargs)
        print(f"Película guardada correctamente: {self.title}")

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name='comments')
    nick = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.nick} on {self.movie.title}"
    

class MovieRequest(models.Model):
    name = models.CharField(max_length=100)  # Nombre del usuario
    email = models.EmailField()  # Correo electrónico del usuario
    message = models.TextField(max_length=150)  # Mensaje con el pedido (máximo 150 caracteres)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return f"{self.name} - {self.email} - {self.created_at.strftime('%d-%m-%Y')}"
    

#para agregar generos
'''from movies.models import Genre

# Agrega nuevos géneros
new_genres = ['Home Invasion', 'Body Horror', 'Acción'] 
for genre_name in new_genres:
    Genre.objects.get_or_create(name=genre_name)  # Evita duplicados

print("Géneros agregados exitosamente.")'''

    


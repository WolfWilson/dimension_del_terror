from django.db import models
from django.core.files.base import ContentFile
import requests
from .utils import get_movie_data_from_api
from django.utils.html import strip_tags
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
import io
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


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

    # Nuevo: Calificación personal del usuario (opcional, puede ser null)
    user_ratings = models.ManyToManyField(
        User,
        through='MovieRating',
        related_name='rated_movies',
        blank=True
    )

    # Nuevo: Lista de favoritos (puede estar vacía)
    favorite_by_users = models.ManyToManyField(
        User,
        related_name='favorite_movies',
        blank=True
    )

    # Nuevo: Lista de "Por Ver" (puede estar vacía)
    watchlist_by_users = models.ManyToManyField(
        User,
        related_name='watchlist_movies',
        blank=True
    )

    def save(self, *args, **kwargs):
        print(f"Iniciando guardado de la película: {self.title}")

        # Transformar la URL de Google Drive
        if self.drive_url and "drive.google.com" in self.drive_url:
            if "/view" in self.drive_url or "?usp" in self.drive_url:
                file_id = self.drive_url.split('/d/')[1].split('/')[0]
                self.drive_url = f"https://drive.google.com/file/d/{file_id}/preview"
                print(f"URL de Google Drive transformada: {self.drive_url}")

        # Intentar obtener datos de la API si faltan
        if not self.description or not self.release_date or not self.rating or not self.trailer_url:
            print("Intentando obtener datos desde la API...")

            movie_data = None

            # Prioridad al enlace de TMDb si está presente
            if self.tmdb_url:
                print(f"Usando TMDb URL para buscar la película: {self.tmdb_url}")
                movie_id = self.tmdb_url.rstrip('/').split('/')[-1]  # Extraer el ID de la película
                movie_data = get_movie_data_from_api(movie_id=movie_id)
            else:
                print(f"Usando el título para buscar la película: {self.title}")
                movie_data = get_movie_data_from_api(title=self.title)

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

                # Descargar y redimensionar el póster
                if not self.poster_image and movie_data.get('poster_path'):
                    poster_url = f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}"
                    try:
                        response = requests.get(poster_url, timeout=10)
                        response.raise_for_status()
                        img = Image.open(BytesIO(response.content))
                        img = img.resize((667, 1000))  # Redimensionar a 667x1000
                        buffer = BytesIO()
                        img.save(buffer, format='JPEG', quality=100)
                        buffer.seek(0)
                        image_name = f"posters/{self.title.replace(' ', '_')}_poster.jpg"
                        self.poster_image.save(image_name, ContentFile(buffer.read()), save=False)
                        print(f"Póster descargado y asignado: {image_name}")
                    except requests.RequestException as e:
                        print(f"Error al descargar el póster: {e}")

        # Llamar al método `save` original para guardar los datos
        super().save(*args, **kwargs)
        print(f"Película guardada correctamente: {self.title}")

    def __str__(self):
        return self.title


# Nueva tabla intermedia para almacenar las calificaciones personales de los usuarios (opcional)
class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(
        choices=[(i / 2, f'{i / 2} ⭐') for i in range(1, 11)],  # De 0.5 a 5.0 estrellas
        null=True, blank=True  # Opcional, el usuario no está obligado a calificar
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')  # Evita que un usuario califique la misma película más de una vez

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}: {self.rating} ⭐" if self.rating else f"{self.user.username} - {self.movie.title}: Sin calificación"


    
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

    



from django.db import models
from django.core.files.base import ContentFile
from .utils import get_series_data_from_api
from io import BytesIO
import requests


class Series(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    tmdb_url = models.URLField(null=True, blank=True)
    poster_image = models.ImageField(upload_to='series_posters/', blank=True, null=True)
    header_image = models.ImageField(upload_to='series_headers/', blank=True, null=True)
    genres = models.ManyToManyField("Genre", related_name='series')

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para obtener datos de TMDb y poblar los campos automáticamente.
        """
        # Guardar inicialmente para garantizar un ID válido
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.tmdb_url:
            # Obtener datos de la API
            series_data = get_series_data_from_api(self.tmdb_url)
            if series_data:
                # Poblar campos con datos de la API si están vacíos
                self.description = series_data.get('description', self.description)
                self.release_date = series_data.get('release_date', self.release_date)
                self.rating = series_data.get('rating', self.rating)
                self.language = series_data.get('language', self.language)

                # Descargar imágenes del póster y encabezado
                if not self.poster_image and series_data.get('poster_path'):
                    self.poster_image = self.download_image(
                        series_data['poster_path'],
                        f"series_posters/{self.title.replace(' ', '_')}.jpg"
                    )

                if not self.header_image and series_data.get('header_path'):
                    self.header_image = self.download_image(
                        series_data['header_path'],
                        f"series_headers/{self.title.replace(' ', '_')}_header.jpg"
                    )

                # Guardar nuevamente los cambios
                super().save(update_fields=['description', 'release_date', 'rating', 'language', 'poster_image', 'header_image'])

                # Crear temporadas y episodios
                self.create_seasons_and_episodes(series_data)

    def create_seasons_and_episodes(self, series_data):
        """
        Crea temporadas y episodios basados en los datos obtenidos de la API.
        """
        for season_data in series_data.get('seasons', []):
            season, created = Season.objects.get_or_create(
                series=self,
                season_number=season_data['season_number'],
                defaults={
                    'title': season_data['title'],
                    'description': season_data['description'],
                }
            )
            for episode_data in season_data.get('episodes', []):
                Episode.objects.get_or_create(
                    season=season,
                    episode_number=episode_data['episode_number'],
                    defaults={
                        'title': episode_data['title'],
                        'description': episode_data['description'],
                        'air_date': episode_data['air_date'],
                        'duration': episode_data.get('runtime'),  # Obtener la duración desde la API
                        'screenshot': self.download_image(
                            episode_data['screenshot_path'],
                            f"episode_screenshots/{self.title.replace(' ', '_')}_T{season.season_number}_E{episode_data['episode_number']}.jpg"
                        ) if episode_data.get('screenshot_path') else None
                    }
                )


    @staticmethod
    def download_image(url, file_name):
        """
        Descarga una imagen desde una URL y la retorna como un archivo ContentFile.
        """
        try:
            response = requests.get(f"https://image.tmdb.org/t/p/original{url}", timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            buffer.seek(0)
            return ContentFile(buffer.read(), name=file_name)
        except requests.RequestException as e:
            print(f"Error al descargar imagen: {e}")
            return None

    def __str__(self):
        return self.title


class Season(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="seasons")
    season_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.series.title} - Temporada {self.season_number}"


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    air_date = models.DateField(null=True, blank=True)
    screenshot = models.ImageField(upload_to="episode_screenshots/", blank=True, null=True)
    drive_url = models.URLField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)  # Duración en minutos

    def get_drive_preview_url(self):
        """
        Devuelve la URL en formato de vista previa de Google Drive si la URL original es válida.
        Si no es una URL de Google Drive, devuelve la URL tal como está.
        """
        if self.drive_url and "drive.google.com" in self.drive_url:
            # Extraer el file_id de la URL
            if "id=" in self.drive_url:
                file_id = self.drive_url.split("id=")[-1]
                return f"https://drive.google.com/file/d/{file_id}/preview"
            elif "/file/d/" in self.drive_url:
                file_id = self.drive_url.split("/file/d/")[1].split("/")[0]
                return f"https://drive.google.com/file/d/{file_id}/preview"
        return self.drive_url

    def __str__(self):
        return f"{self.season.series.title} - T{self.season.season_number}E{self.episode_number}: {self.title}"



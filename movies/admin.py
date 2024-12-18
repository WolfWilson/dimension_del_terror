# Register your models here.
from django.contrib import admin
from .models import Movie, Comment
from .models import Genre
from .models import MovieRequest

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    ordering = ['name']  # Ordenar alfabéticamente en el administrador

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating')
    search_fields = ('title',)
    list_filter = ('genres', 'release_date')
    fields = (
        'title',
        'description',
        'release_date',
        'rating',
        'duration',
        'language',
        'director',
        'cast',
        'tmdb_url',
        'trailer_url', #enlace a youtube
        'poster_image',
        'header_image',  # Campo para el encabezado personalizado
        'drive_url',
        'genres',
        'review'
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('movie', 'created_at')
    search_fields = ('movie__title',)

@admin.register(MovieRequest)
class MovieRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')  # Campos a mostrar en la lista
    search_fields = ('name', 'email', 'message')  # Campos por los que se puede buscar
    list_filter = ('created_at',)  # Agrega un filtro por fecha
    ordering = ('-created_at',)  # Ordena los resultados de forma descendente por fecha

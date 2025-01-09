"""
admin.py

Este archivo define cómo se mostrarán y administrarán los modelos 
en el panel de administración de Django.
"""

from django.contrib import admin

# Importa todos los modelos que usarás en el admin
from .models import (
    Movie,
    Comment,
    Genre,
    MovieRequest,
    Series,
    Season,
    Episode
)

# Si usas formularios personalizados para algunos modelos
from .forms import SeriesForm, EpisodeForm

# :::::::::::::: GENRE ::::::::::::::
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Genre.
    """
    ordering = ['name']  # Ordenar alfabéticamente en el admin

# :::::::::::::: MOVIE ::::::::::::::
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Movie.
    """
    list_display = ('title', 'release_date', 'rating')   # Columnas en el listado
    search_fields = ('title',)                            # Barra de búsqueda
    list_filter = ('genres', 'release_date')              # Filtros laterales

    # Campos que aparecen en el formulario de detalle/edición
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
        'trailer_url',   # Enlace a YouTube
        'poster_image',
        'header_image',  # Campo para el encabezado personalizado
        'drive_url',
        'genres',
        'review',
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

# :::::::::::::: SERIES ::::::::::::::
@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Series.
    """
    form = SeriesForm  # Si deseas usar un formulario personalizado
    list_display = ('title', 'release_date', 'rating')
    search_fields = ('title',)
    list_filter = ('genres', 'release_date')
    fields = (
        'title',
        'description',
        'release_date',
        'rating',
        'language',
        'tmdb_url',
        'poster_image',
        'header_image',
        'genres',
    )

# :::::::::::::: EPISODE (Inline y Admin) ::::::::::::::
class EpisodeInline(admin.TabularInline):
    """
    Muestra los episodios de forma inline dentro de la vista de Season.
    """
    model = Episode
    form = EpisodeForm
    extra = 1  # Formularios vacíos para crear nuevos episodios
    fields = [
        'episode_number',
        'title',
        'duration',      # Campo para editar la duración manualmente
        'air_date',
        'description',
        'drive_url',
        'screenshot',
    ]

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    """
    Admin independiente para el modelo Episode.
    """
    form = EpisodeForm
    list_display = ('title', 'season', 'episode_number', 'duration')
    list_filter = ('season',)
    search_fields = ('title',)

# :::::::::::::: SEASON ::::::::::::::
@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Season.
    """
    list_display = ('series', 'season_number', 'title')
    inlines = [EpisodeInline]

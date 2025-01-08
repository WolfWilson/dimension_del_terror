# Register your models here.
from django.contrib import admin
from .models import Movie, Comment, Genre, MovieRequest, Series

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
        'trailer_url',  # Enlace a YouTube
        'poster_image',
        'header_image',  # Campo para el encabezado personalizado
        'drive_url',
        'genres',
        'review',
    )

# :::::::::::::: Series ::::::::::::::
from .models import Series, Season, Episode, Genre

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
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

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'season_number', 'title')
    search_fields = ('series__title', 'title')
    list_filter = ('series',)

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'episode_number', 'title', 'air_date')
    search_fields = ('season__series__title', 'title')
    list_filter = ('season__series', 'air_date')

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

#:::::::::::::::::::: COLECCIONES :::::::::::::::::::::::::
from django import forms
from django.contrib import admin
from .models import Collection, Movie

class CollectionAdminForm(forms.ModelForm):
    """
    Formulario personalizado para agregar películas a una colección desde una lista o por ID.
    """
    movie_ids = forms.CharField(
        required=False,
        help_text="IDs de películas separados por comas. Las películas ingresadas se añadirán a las existentes.",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 12, 45, 78'})
    )

    class Meta:
        model = Collection
        fields = '__all__'

    def clean_movie_ids(self):
        """
        Convierte los IDs ingresados en una lista de objetos Movie sin eliminar las películas actuales.
        """
        ids_str = self.cleaned_data.get('movie_ids', '').strip()
        if not ids_str:
            return []

        # Extraer solo los números y convertir a enteros
        movie_ids = [int(id.strip()) for id in ids_str.split(',') if id.strip().isdigit()]

        # Filtrar solo películas que existen
        valid_movies = Movie.objects.filter(id__in=movie_ids)

        return valid_movies

    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario mostrando los IDs de las películas **ya existentes** en la colección.
        """
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            existing_ids = ", ".join(str(movie.id) for movie in self.instance.movies.all())
            self.fields['movie_ids'].initial = existing_ids  # ✅ Muestra los IDs ya agregados


class CollectionAdmin(admin.ModelAdmin):
    form = CollectionAdminForm
    list_display = ('title', 'get_movies_list')
    fields = ('title', 'description', 'cover_image', 'movies', 'movie_ids')

    filter_horizontal = ('movies',)  # ✅ Permite selección manual en admin

    def save_model(self, request, obj, form, change):
        """
        Guarda la colección y **agrega** nuevas películas sin eliminar las ya existentes.
        """
        obj.save()  # Guardamos primero la colección

        # Películas seleccionadas manualmente desde la lista en el admin
        selected_movies = list(form.cleaned_data.get('movies', []))

        # Películas agregadas por ID **sin eliminar las ya existentes**
        movies_by_id = list(form.cleaned_data.get('movie_ids', []))

        # ✅ **Agregamos nuevas películas sin sobrescribir las ya existentes**
        for movie in movies_by_id:
            if movie not in obj.movies.all():
                obj.movies.add(movie)  # ✅ Usamos `add()` para agregar sin eliminar

        obj.save()  # Guardamos nuevamente para actualizar la relación ManyToMany


    def get_movies_list(self, obj):
        """Muestra los títulos de las películas en la lista de admin, ordenados por el orden de agregado."""
        if not obj.movies.exists():
            return "Sin películas en la colección"

        # Ordenamos por la clave primaria de la relación ManyToMany, que refleja el orden de agregado
        sorted_movies = obj.movies.through.objects.filter(collection=obj).order_by("id")

        return ", ".join([
            f"{entry.movie.id} - {entry.movie.title}"
            for entry in sorted_movies
        ])

    get_movies_list.short_description = "Películas en la Colección"


""""
    def get_movies_list(self, obj):
   
        if not obj.movies.exists():
            return "Sin películas en la colección"

        # Ordenamos manualmente por el campo 'release_date' sin alterar el modelo
        sorted_movies = sorted(
            obj.movies.all(),
            key=lambda movie: movie.release_date.year if movie.release_date else 9999
        )

        return ", ".join([
            f"{movie.id} - {movie.title} ({movie.release_date.year if movie.release_date else 'Sin fecha'})"
            for movie in sorted_movies
        ])

    get_movies_list.short_description = "Películas en la Colección"

"""

admin.site.register(Collection, CollectionAdmin)






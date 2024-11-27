from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Movie
from django.shortcuts import render, redirect
from .forms import MovieForm
from .utils import get_movie_data_from_api
from .models import Genre


def movie_list(request):
    query = request.GET.get('q', '')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()

    paginator = Paginator(movies, 12) # cantidad de pelis en la grilla
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'movies/index.html', {
        'movies': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'query': query,
    })

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Procesar el reparto como una lista de actores
    cast_list = movie.cast.split(', ') if movie.cast else []  # Dividir el reparto por comas

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'cast_list': cast_list,  # Pasar la lista al contexto
    })

def search_movies(request):
    query = request.GET.get('q', '')  # Captura el término de búsqueda
    results = Movie.objects.filter(title__icontains=query) if query else []
    return render(request, 'movies/resultados.html', {
        'results': results,
        'query': query,
    })

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)  # No guardar aún en la base de datos

            # Obtener datos desde la API
            movie_data = get_movie_data_from_api(movie.title)
            if movie_data:
                movie.description = movie_data.get('overview', movie.description)
                movie.release_date = movie_data.get('release_date', movie.release_date)
                movie.rating = movie_data.get('vote_average', movie.rating)
                poster_path = movie_data.get('poster_path')
                if poster_path and not movie.poster_image:
                    movie.poster_image = f"https://image.tmdb.org/t/p/w500{poster_path}"
            movie.save()  # Guarda la película sin géneros
            form.save_m2m()  # Guarda los géneros seleccionados en el formulario
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Movie, Genre

def movies_by_genre(request, genre_name):
    # Buscar el género por nombre (o devolver un 404 si no existe)
    genre = get_object_or_404(Genre, name=genre_name)

    # Filtrar películas relacionadas con ese género
    movies = Movie.objects.filter(genres=genre)

    # Contexto para la plantilla
    context = {
        'genre': genre,
        'movies': movies,
    }

    return render(request, 'movies/movies_by_genre.html', context)

from .models import Movie

def movies_by_tag(request, tag_type, tag):
    # Filtrar películas por el director o reparto basado en el tag_type
    if tag_type == "director":
        movies = Movie.objects.filter(director__iexact=tag)  # Asegura que la búsqueda sea insensible a mayúsculas
    elif tag_type == "cast":
        movies = Movie.objects.filter(cast__icontains=tag.strip())

    else:
        movies = Movie.objects.none()

    # Pasar el tipo de etiqueta (director o cast) y el valor del tag al contexto
    context = {
        'movies': movies,
        'tag_type': tag_type,
        'tag': tag,
    }
    print(f"Tag Type: {tag_type}, Tag: {tag}")

    return render(request, 'movies/movies_by_tag.html', context)
    

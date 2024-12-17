from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Movie
from django.shortcuts import render, redirect
from .forms import MovieForm
from .utils import get_movie_data_from_api
from .models import Genre
from .models import Movie, Comment
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from .models import Genre, Movie
from .forms import MovieRequestForm

def dynamic_genre_movies(request):
    # Ordena los géneros alfabéticamente
    genres = Genre.objects.all().order_by('name')  # Orden por nombre alfabético
    
    selected_genre_id = request.GET.get('genre')  # Captura el ID del género seleccionado desde la URL

    # Si hay un género seleccionado, filtra las películas; de lo contrario, muestra todas
    if selected_genre_id:
        selected_genre = get_object_or_404(Genre, id=selected_genre_id)
        movies = Movie.objects.filter(genres=selected_genre).order_by('-id')  # Orden descendente por ID
    else:
        selected_genre = None
        movies = Movie.objects.all().order_by('-id')  # Orden descendente por ID

    context = {
        'genres': genres,
        'selected_genre': selected_genre,
        'movies': movies,
    }
    return render(request, 'movies/dynamic_genre_movies.html', context)



def movie_list(request):
    query = request.GET.get('q', '')  # Captura el término de búsqueda
    page_number = request.GET.get('page')  # Captura el número de página actual
    request_success = request.session.pop('request_success', False)  # Recupera la variable de sesión

    # Filtra las películas si hay búsqueda, o muestra todas
    if query:
        movies = Movie.objects.filter(title__icontains=query).order_by('-id')
    else:
        movies = Movie.objects.all().order_by('-id')

    # Paginador para mostrar 16 películas por página
    paginator = Paginator(movies, 16)
    page_obj = paginator.get_page(page_number)

    # Procesar el formulario de contacto
    if request.method == "POST":
        form = MovieRequestForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['request_success'] = True  # Guarda el éxito en la sesión
            # Redirige pasando también los parámetros actuales (query y page)
            return redirect(f'{request.path}?q={query}&page={page_number}')
    else:
        form = MovieRequestForm()

    # Contexto para la plantilla
    return render(request, 'movies/index.html', {
        'movies': page_obj,              # Pasa las películas paginadas
        'is_paginated': page_obj.has_other_pages(),  # Indica si hay paginación
        'page_obj': page_obj,            # Objeto de la página actual
        'query': query,                  # Valor del campo de búsqueda
        'form': form,                    # Formulario de contacto
        'request_success': request_success,  # Variable para mostrar el modal
    })

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comments = movie.comments.order_by('-created_at')  # Ordenar los comentarios por fecha descendente
    comment_success = False  # Bandera para confirmar el envío del comentario

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie = movie
            comment.save()
            comment_success = True  # Se envió el comentario correctamente
    else:
        form = CommentForm()

    # Procesar el reparto como una lista de actores
    cast_list = movie.cast.split(', ') if movie.cast else []

    context = {
        'movie': movie,
        'comments': comments,
        'form': form,
        'cast_list': cast_list,
        'comment_success': comment_success,  # Pasar la bandera al contexto
    }
    return render(request, 'movies/movie_detail.html', context)



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

# ::::::::::::::::::: VISTA PARA LA PAGINA QUE FILTRA LAS PELICULAS POR GÉNEROS ::::::::::::::::::::::::::::::: #

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

# ::::::::::::::::::: VISTA PARA LA PAGINA QUE FILTRA LAS PELICULAS POR ETIQUETAS DE ACTORES Y DIRECTORES ::::::::::::::::::::::::::::::: #

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


from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import MovieForm

# Función para verificar si el usuario es superusuario
def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser, login_url='/admin/login/')  # Redirige al login de admin si no es superuser
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')  # Redirige a la lista de películas después de guardar
    else:
        form = MovieForm()

    return render(request, 'movies/add_movie.html', {'form': form})


    

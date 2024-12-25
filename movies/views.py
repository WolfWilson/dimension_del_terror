# views.py

from django.shortcuts import (
    render, 
    get_object_or_404, 
    redirect
)
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

# Modelos y formularios propios
from .models import Movie, Genre, Comment
from .forms import (
    MovieForm,
    CommentForm,
    MovieRequestForm
)
from .utils import get_movie_data_from_api

# ------------------------------------------------------------------------------
#                                  UTILIDADES
# ------------------------------------------------------------------------------
def is_superuser(user):
    """
    Verifica si el usuario es superusuario.
    Se utiliza con el decorador @user_passes_test.
    """
    return user.is_authenticated and user.is_superuser


def get_display_pages(page_obj, max_pages=6):
    """
    Genera una lista con un máximo de 'max_pages' páginas,
    centradas alrededor de la página actual, sin forzar siempre
    la inclusión de la primera y la última. 
    Incluye '...' y 1 o la página final cuando hay un hueco.
    
    :param page_obj: Objeto de la página actual (paginador).
    :param max_pages: Cantidad máxima de números de páginas a mostrar.
    :return: Lista de números de página y/o '...' para elipsis.
    """
    total_pages = page_obj.paginator.num_pages
    current_page = page_obj.number

    # Si el total de páginas no excede max_pages, se muestran todas
    if total_pages <= max_pages:
        return list(range(1, total_pages + 1))

    half = max_pages // 2
    start_page = current_page - half
    end_page = current_page + half - 1

    # Ajustes para no salirse de los límites [1, total_pages]
    if start_page < 1:
        start_page = 1
        end_page = max_pages
    if end_page > total_pages:
        end_page = total_pages
        start_page = total_pages - max_pages + 1
    if start_page < 1:
        start_page = 1

    # Se construye la ventana central
    pages = list(range(start_page, end_page + 1))

    # Agrega la página 1 y elipsis al inicio si hay hueco
    if start_page > 2:
        pages.insert(0, '...')
        pages.insert(0, 1)
    elif start_page == 2:
        # Si empieza en 2, se añade solo 1
        pages.insert(0, 1)

    # Agrega la última página y elipsis al final si hay hueco
    if end_page < total_pages - 1:
        pages.append('...')
        pages.append(total_pages)
    elif end_page == total_pages - 1:
        # Si termina en la penúltima, se añade solo la última
        pages.append(total_pages)

    return pages


# ------------------------------------------------------------------------------
#                         VISTAS PRINCIPALES
# ------------------------------------------------------------------------------

def dynamic_genre_movies(request):
    """
    Vista para filtrar películas dinámicamente por géneros.
    Si se selecciona un género, filtra; sino, muestra todas.
    """
    genres = Genre.objects.all().order_by('name')  # Orden alfabético
    selected_genre_id = request.GET.get('genre')

    if selected_genre_id:
        selected_genre = get_object_or_404(Genre, id=selected_genre_id)
        movies = Movie.objects.filter(genres=selected_genre).order_by('-id')
    else:
        selected_genre = None
        movies = Movie.objects.all().order_by('-id')

    context = {
        'genres': genres,
        'selected_genre': selected_genre,
        'movies': movies,
    }
    return render(request, 'movies/dynamic_genre_movies.html', context)


def movie_list(request):
    """
    Vista principal (index) que muestra la lista de películas.
    - Soporta búsqueda por 'title__icontains' si se manda 'q'.
    - Paginación de 20 películas por página.
    - Formulario de MovieRequest (peticiones) en la misma página.
    - Genera una lista de páginas (display_pages) para la paginación.
    """
    query = request.GET.get('q', '')
    page_number = request.GET.get('page')
    request_success = request.session.pop('request_success', False)

    # Búsqueda opcional
    if query:
        movies = Movie.objects.filter(title__icontains=query).order_by('-id')
    else:
        movies = Movie.objects.all().order_by('-id')

    # Paginación: 20 por página
    paginator = Paginator(movies, 20)
    page_obj = paginator.get_page(page_number)

    total_movies = Movie.objects.count()

    # Generar la lista de páginas con la lógica de display_pages
    display_pages = get_display_pages(page_obj, max_pages=8)

    # Procesar el formulario de solicitud (MovieRequestForm)
    if request.method == "POST":
        form = MovieRequestForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['request_success'] = True
            # Redirigir conservando parámetros de búsqueda y paginación
            return redirect(f'{request.path}?q={query}&page={page_number}')
    else:
        form = MovieRequestForm()

    context = {
        'movies': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'query': query,
        'form': form,
        'request_success': request_success,
        'total_movies': total_movies,
        'display_pages': display_pages,
    }
    return render(request, 'movies/index.html', context)


def movie_detail(request, movie_id):
    """
    Vista detallada de una película, con comentarios asociados.
    - Procesa formulario de comentarios (CommentForm).
    - Muestra películas similares basadas en géneros en común.
    """
    movie = get_object_or_404(Movie, id=movie_id)
    comments = movie.comments.order_by('-created_at')  # Comentarios más nuevos primero
    comment_success = False

    # Procesar el formulario de comentarios
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.movie = movie
            new_comment.save()
            comment_success = True
    else:
        form = CommentForm()

    # El reparto como lista separada por comas
    cast_list = movie.cast.split(', ') if movie.cast else []

    # Géneros de la película
    movie_genres = movie.genres.all()

    # Películas similares por géneros compartidos
    similar_movies = (
        Movie.objects.filter(genres__in=movie_genres)
        .exclude(id=movie.id)
        .annotate(shared_genres=Count('genres'))
        .order_by('-shared_genres', '-rating')[:4]
    )

    context = {
        'movie': movie,
        'comments': comments,
        'form': form,
        'cast_list': cast_list,
        'comment_success': comment_success,
        'similar_movies': similar_movies,
    }
    return render(request, 'movies/movie_detail.html', context)


def search_movies(request):
    """
    Vista para manejar una búsqueda simple en un template aparte (resultados.html).
    """
    query = request.GET.get('q', '')
    results = Movie.objects.filter(title__icontains=query) if query else []

    return render(request, 'movies/resultados.html', {
        'results': results,
        'query': query,
    })


# ------------------------------------------------------------------------------
#                      VISTAS PARA AGREGAR MOVIES
# ------------------------------------------------------------------------------

@user_passes_test(is_superuser, login_url='/admin/login/')
def add_movie(request):
    """
    Vista para añadir una nueva película (sólo superusuario).
    - Usa MovieForm.
    - Si se guarda, redirige a la lista de películas.
    """
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()

    return render(request, 'movies/add_movie.html', {'form': form})


def add_movie_with_api(request):
    """
    Ejemplo de vista que obtiene datos desde la API (TMDb),
    rellena los campos y luego guarda. 
    (Si la utilizas en tu proyecto, renombra para no chocar con la otra add_movie.)
    """
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie_data = get_movie_data_from_api(movie.title)
            if movie_data:
                movie.description = movie_data.get('overview', movie.description)
                movie.release_date = movie_data.get('release_date', movie.release_date)
                movie.rating = movie_data.get('vote_average', movie.rating)
                poster_path = movie_data.get('poster_path')
                if poster_path and not movie.poster_image:
                    movie.poster_image = f"https://image.tmdb.org/t/p/w500{poster_path}"
            movie.save()
            form.save_m2m()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})

# ------------------------------------------------------------------------------
#                         VISTAS DE FILTRADO ADICIONAL
# ------------------------------------------------------------------------------

def movies_by_genre(request, genre_name):
    """
    Muestra todas las películas asociadas a un género específico
    (pasado por su nombre en la URL).
    """
    genre = get_object_or_404(Genre, name=genre_name)
    movies = Movie.objects.filter(genres=genre)

    return render(request, 'movies/movies_by_genre.html', {
        'genre': genre,
        'movies': movies,
    })


def movies_by_tag(request, tag_type, tag):
    """
    Filtra películas por director o reparto según 'tag_type'.
    - tag_type = 'director' => director__iexact=tag
    - tag_type = 'cast' => cast__icontains=tag
    """
    if tag_type == "director":
        movies = Movie.objects.filter(director__iexact=tag)
    elif tag_type == "cast":
        movies = Movie.objects.filter(cast__icontains=tag.strip())
    else:
        movies = Movie.objects.none()

    # Log para debug
    print(f"Tag Type: {tag_type}, Tag: {tag}")

    return render(request, 'movies/movies_by_tag.html', {
        'movies': movies,
        'tag_type': tag_type,
        'tag': tag,
    })

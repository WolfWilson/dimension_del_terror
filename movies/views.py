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
from .forms import MovieForm, MovieFrontendForm, CommentForm, MovieRequestForm
from django.contrib.auth.decorators import login_required #para proteger las vistas con inicio de sesión requerido

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

@login_required(login_url='login_view')
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

@login_required(login_url='login_view')
def movie_list(request):
    """
    Vista principal con soporte para múltiples filtros combinados: género, año, y ordenamiento.
    """
    query = request.GET.get('q', '')  # Filtro por búsqueda
    page_number = request.GET.get('page')  # Paginación
    request_success = request.session.pop('request_success', False)

    # Filtros adicionales
    year_segment = request.GET.get('year_segment', 'Todos')  # Filtro por año
    sort_by = request.GET.get('sort_by', 'reciente')  # Orden
    genre_id = request.GET.get('genre_id', 'Todos')  # Género seleccionado

    # Base queryset (todas las películas)
    movies = Movie.objects.all()

    # 1. FILTRAR POR BÚSQUEDA
    if query:
        movies = movies.filter(title__icontains=query)

    # 2. FILTRAR POR GÉNERO
    if genre_id != 'Todos':
        try:
            genre_id_int = int(genre_id)
            movies = movies.filter(genres__id=genre_id_int)
        except ValueError:
            pass  # Si no es un número válido, ignora el filtro

    # 3. FILTRAR POR AÑO/SEGMENTO
    if year_segment != 'Todos':
        if year_segment.isdigit():
            # Año exacto
            movies = movies.filter(release_date__year=int(year_segment))
        elif '-' in year_segment:
            try:
                # Rango de años (e.g., "2000-2009")
                start_year, end_year = map(int, year_segment.split('-'))
                movies = movies.filter(
                    release_date__year__gte=start_year,
                    release_date__year__lte=end_year
                )
            except ValueError:
                pass  # Si el rango no es válido, ignora el filtro
      

    # 4. ORDENAMIENTO
    if sort_by == 'alf_asc':
        movies = movies.order_by('title')
    elif sort_by == 'alf_desc':
        movies = movies.order_by('-title')
    elif sort_by == 'antiguo':
        movies = movies.order_by('release_date')  # Películas más antiguas
    elif sort_by == 'rating':
        movies = movies.order_by('-rating')  # Puntuación TMDb descendente
    else:
        # Default: "reciente" (películas más nuevas primero)
        movies = movies.order_by('-id')

    # 5. PAGINACIÓN
    paginator = Paginator(movies, 20)  # Mostrar 20 películas por página
    page_obj = paginator.get_page(page_number)

    # Total de películas (para mostrar en el contador)
    total_movies = Movie.objects.count()

    # Lógica para páginas dinámicas (paginación)
    display_pages = get_display_pages(page_obj, max_pages=8)

    # Procesar formulario de peticiones
    if request.method == "POST":
        form = MovieRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'{request.path}?q={query}&page={page_number}'
                            f'&year_segment={year_segment}&sort_by={sort_by}'
                            f'&genre_id={genre_id}')
    else:
        form = MovieRequestForm()

    # Lista de géneros (para popular el dropdown)
    all_genres = Genre.objects.all().order_by('name')

    context = {
        'movies': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'query': query,
        'form': form,
        'request_success': request_success,
        'total_movies': total_movies,
        'display_pages': display_pages,

        # Valores actuales para no perder selección
        'current_year_segment': year_segment,
        'current_sort_by': sort_by,
        'current_genre_id': genre_id,

        # Lista de géneros para el select
        'all_genres': all_genres,
    }
    return render(request, 'movies/index.html', context)






@login_required(login_url='login_view')
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
        .order_by('-shared_genres', '-rating')[:6]
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

@login_required(login_url='login_view')
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

from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    """
    Verifica si el usuario es superusuario.
    """
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser, login_url='/admin/login/')
def add_movie(request):
    """
    Vista para añadir una nueva película (sólo superusuario).
    Usa MovieForm.
    """
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()

    return render(request, 'movies/add_movie.html', {'form': form})

from django.contrib import messages

@user_passes_test(is_superuser, login_url='/admin/login/')
def add_movie_frontend(request):
    """
    Vista para añadir una nueva película (solo para usuarios superusuarios).
    Usa el formulario simplificado (MovieFrontendForm).
    """
    if request.method == 'POST':
        form = MovieFrontendForm(request.POST)
        if form.is_valid():
            try:
                # Guardar la película
                movie = form.save(commit=False)  # Guarda el objeto sin enviarlo todavía a la BD
                movie.save()
                form.save_m2m()  # Guarda las relaciones de muchos a muchos
                messages.success(
                    request,
                    f'¡Película "{movie.title}" agregada exitosamente! Puedes continuar agregando más.'
                )
                # Resetear el formulario después de un envío exitoso
                form = MovieFrontendForm()
            except Exception as e:
                messages.error(request, f'Error al agregar la película: {e}')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = MovieFrontendForm()

    return render(request, 'movies/add_movie_frontend.html', {'form': form})





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
@login_required(login_url='login_view')
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

@login_required(login_url='login_view')
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



from django.db.models import Q
#VISTA PARA FILTRAR PELIS CON RESEÑAS
@login_required(login_url='login_view')
def reviews(request):
    """
    Vista que muestra las películas con reseñas escritas válidas.
    """
    query = request.GET.get('q', '')  # Filtro por búsqueda
    page_number = request.GET.get('page')  # Paginación
    year_segment = request.GET.get('year_segment', 'Todos')  # Filtro por año
    sort_by = request.GET.get('sort_by', 'reciente')  # Orden
    genre_id = request.GET.get('genre_id', 'Todos')  # Género seleccionado

    # Base queryset: Películas con reseñas válidas
    movies_with_reviews = Movie.objects.filter(
        review__isnull=False
    ).exclude(
        Q(review__regex=r'^\s*$') |  # Excluye reseñas vacías
        Q(review__regex=r'^(&nbsp;|\s|<[^>]*>)*$')  # Excluye contenido vacío o con solo etiquetas
    )

    # Filtro por búsqueda
    if query:
        movies_with_reviews = movies_with_reviews.filter(title__icontains=query)

    # Filtro por género
    if genre_id != 'Todos':
        try:
            genre_id_int = int(genre_id)
            movies_with_reviews = movies_with_reviews.filter(genres__id=genre_id_int)
        except ValueError:
            pass

    # Filtro por año
    if year_segment != 'Todos':
        if year_segment.isdigit():
            movies_with_reviews = movies_with_reviews.filter(release_date__year=int(year_segment))
        elif '-' in year_segment:
            try:
                start_year, end_year = map(int, year_segment.split('-'))
                movies_with_reviews = movies_with_reviews.filter(
                    release_date__year__gte=start_year,
                    release_date__year__lte=end_year
                )
            except ValueError:
                pass

    # Ordenamiento
    if sort_by == 'alf_asc':
        movies_with_reviews = movies_with_reviews.order_by('title')
    elif sort_by == 'alf_desc':
        movies_with_reviews = movies_with_reviews.order_by('-title')
    elif sort_by == 'antiguo':
        movies_with_reviews = movies_with_reviews.order_by('release_date')
    elif sort_by == 'rating':
        movies_with_reviews = movies_with_reviews.order_by('-rating')
    else:
        movies_with_reviews = movies_with_reviews.order_by('-id')

    # Paginación
    paginator = Paginator(movies_with_reviews, 20)
    page_obj = paginator.get_page(page_number)

    # Géneros para el dropdown
    all_genres = Genre.objects.all().order_by('name')

    context = {
        'movies': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'query': query,
        'total_movies': movies_with_reviews.count(),
        'all_genres': all_genres,
        'current_year_segment': year_segment,
        'current_sort_by': sort_by,
        'current_genre_id': genre_id,
    }

    return render(request, 'movies/reviews.html', context)


#:::::::::::::::::::::::VISTA DE SERIES :::::::::::::::::::::::::::::


from .models import Series  # Importa el modelo de series
@login_required(login_url='login_view')
def series_list(request):
    """
    Vista principal para listar y filtrar series.
    Soporta:
      - Búsqueda por título (q)
      - Filtro por género (genre_id)
      - Filtro por año o rango de años (year_segment)
      - Ordenamiento (sort_by)
      - Paginación
      - Formulario 'MovieRequestForm' para solicitudes (opcional)
    """
    query = request.GET.get('q', '')
    page_number = request.GET.get('page')
    request_success = request.session.pop('request_success', False)

    # Filtros
    year_segment = request.GET.get('year_segment', 'Todos')
    sort_by = request.GET.get('sort_by', 'reciente')
    genre_id = request.GET.get('genre_id', 'Todos')

    # Base queryset (todas las series)
    series_qs = Series.objects.all()

    # 1. FILTRAR POR BÚSQUEDA (título)
    if query:
        series_qs = series_qs.filter(title__icontains=query)

    # 2. FILTRAR POR GÉNERO
    if genre_id != 'Todos':
        try:
            genre_id_int = int(genre_id)
            series_qs = series_qs.filter(genres__id=genre_id_int)
        except ValueError:
            pass  # Si no es un número válido, ignora

    # 3. FILTRAR POR AÑO/SEGMENTO
    if year_segment != 'Todos':
        if year_segment.isdigit():
            # Año exacto
            series_qs = series_qs.filter(release_date__year=int(year_segment))
        elif '-' in year_segment:
            # Rango de años (p.e. "2000-2009")
            try:
                start_year, end_year = map(int, year_segment.split('-'))
                series_qs = series_qs.filter(
                    release_date__year__gte=start_year,
                    release_date__year__lte=end_year
                )
            except ValueError:
                pass

    # 4. ORDENAMIENTO
    if sort_by == 'alf_asc':
        series_qs = series_qs.order_by('title')
    elif sort_by == 'alf_desc':
        series_qs = series_qs.order_by('-title')
    elif sort_by == 'antiguo':
        # Series más antiguas primero
        series_qs = series_qs.order_by('release_date')
    elif sort_by == 'rating':
        # Puntuación desc
        series_qs = series_qs.order_by('-rating')
    else:
        # Default: más reciente (ID más alto primero)
        series_qs = series_qs.order_by('-id')

    # 5. PAGINACIÓN
    paginator = Paginator(series_qs, 20)  # 20 series por página
    page_obj = paginator.get_page(page_number)

    # Total de series (para el contador)
    total_series = Series.objects.count()

    # Paginación dinámica (si usas get_display_pages como en movies)
    display_pages = get_display_pages(page_obj, max_pages=8)

    # Procesar formulario "Pídeme una serie" (reusando MovieRequestForm)
    if request.method == "POST":
        form = MovieRequestForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir para que no se duplique el post en caso de refrescar
            return redirect(f'{request.path}?q={query}'
                            f'&page={page_number}'
                            f'&year_segment={year_segment}'
                            f'&sort_by={sort_by}'
                            f'&genre_id={genre_id}')
    else:
        form = MovieRequestForm()

    # Lista de géneros
    all_genres = Genre.objects.all().order_by('name')

    context = {
        'series_list': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'query': query,
        'form': form,
        'request_success': request_success,
        'total_series': total_series,
        'display_pages': display_pages,

        # Mantener los valores seleccionados en la interfaz
        'current_year_segment': year_segment,
        'current_sort_by': sort_by,
        'current_genre_id': genre_id,

        # Géneros para el dropdown
        'all_genres': all_genres,
    }
    return render(request, 'movies/series_list.html', context)

@login_required(login_url='login_view')
def series_detail(request, series_id):
    """
    Vista detallada de una serie.
    - Muestra los detalles de la serie, sus temporadas y episodios.
    """
    series = get_object_or_404(Series, id=series_id)
    
    # Temporadas de la serie
    seasons = series.seasons.all().order_by('season_number')

    # Géneros de la serie
    series_genres = series.genres.all()

    # Formulario de comentarios (opcional, si se implementa)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.series = series
            new_comment.save()
    else:
        form = CommentForm()

    context = {
        'series': series,
        'seasons': seasons,
        'form': form,
        'series_genres': series_genres,
    }

    return render(request, 'movies/series_detail.html', context)


# views.py (extracto final)
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('movie_list')  # O la vista que quieras como "index"
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"¡Bienvenido/a {user.username}!")
            return redirect('movie_list')  # Asegúrate de que 'index' exista en tus urls
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, 'movies/login.html')



def logout_view(request):
    """
    Cierra la sesión actual y redirige a la página de login o donde desees.
    """
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login_view')






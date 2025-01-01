from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),  # Lista de películas
    path('search/', views.search_movies, name='search_movies'),  # Búsqueda
    path('add/', views.add_movie, name='add_movie'),  # Agregar películas
    path('genre/<str:genre_name>/', views.movies_by_genre, name='movies_by_genre'),  # Filtrar por género
    path('<str:tag_type>/<str:tag>/', views.movies_by_tag, name='movies_by_tag'),  # Filtrar por etiqueta
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),  # Detalles de película
    path('dynamic-genres/', views.dynamic_genre_movies, name='dynamic_genre_movies'),
    path('reviews/', views.reviews, name='reviews'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search_movies, name='search_movies'),
    path('add/', views.add_movie, name='add_movie'),  # Nueva ruta para cargar películas
    path('genre/<str:genre_name>/', views.movies_by_genre, name='movies_by_genre'),

]
from django.urls import path
from .views import toggle_favorite, toggle_watchlist
from . import views
from .views import favorite_movies
from .views import user_panel

urlpatterns = [
    path('', views.movie_list, name='movie_list'),  # Lista de películas
    path('search/', views.search_movies, name='search_movies'),  # Búsqueda
    path('add-movie/', views.add_movie_frontend, name='add_movie_frontend'),
    path('add/', views.add_movie, name='add_movie'),  # Agregar películas
    path('genre/<str:genre_name>/', views.movies_by_genre, name='movies_by_genre'),  # Filtrar por género
    path('dynamic-genres/', views.dynamic_genre_movies, name='dynamic_genre_movies'),
    path('reviews/', views.reviews, name='reviews'),

    # Series - rutas para series
    path('series/', views.series_list, name='series_list'),  # Vista de la lista de series
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),  # Vista de detalles de series

    # Películas - asegúrate de que esta ruta esté después de las rutas específicas
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),  # Detalles de película
    path('<str:tag_type>/<str:tag>/', views.movies_by_tag, name='movies_by_tag'),  # Filtrar por etiqueta

    # Rutas para login/logout
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    #Rutas para botones de favoritos y watchlist
    path("toggle-favorite/", toggle_favorite, name="toggle_favorite"),
    path("toggle-watchlist/", toggle_watchlist, name="toggle_watchlist"),
    path("mis-favoritos/", favorite_movies, name="favorite_movies"),
    path("mi-panel/", user_panel, name="user_panel"),



]

    


from django.urls import path
from .views import (
    toggle_favorite,
    toggle_watchlist,
    favorite_movies,
    user_panel,
    rate_movie,
)
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),               # Lista de películas
    path('search/', views.search_movies, name='search_movies'),  # Búsqueda
    path('add-movie/', views.add_movie_frontend, name='add_movie_frontend'),
    path('colecciones/<int:collection_id>/add-by-id/', views.add_movies_by_id, name='add_movies_by_id'),
    path('add/', views.add_movie, name='add_movie'),             # Agregar películas
    path('genre/<str:genre_name>/', views.movies_by_genre, name='movies_by_genre'),
    path('dynamic-genres/', views.dynamic_genre_movies, name='dynamic_genre_movies'),
    path('reviews/', views.reviews, name='reviews'),

    # Series - rutas para series
    path('series/', views.series_list, name='series_list'),          # Vista de la lista de series
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),  # Vista de detalles de series

     # COLECCIONES
    path('colecciones/', views.collections_list, name='collections_list'),
    path('colecciones/<int:collection_id>/', views.collection_detail, name='collection_detail'),

    # Rutas de login/logout
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),

    # Rutas para botones de favoritos y watchlist
    path('toggle-favorite/', toggle_favorite, name='toggle_favorite'),
    path('toggle-watchlist/', toggle_watchlist, name='toggle_watchlist'),
    path('mis-favoritos/', favorite_movies, name='favorite_movies'),
    path('mi-panel/', user_panel, name='user_panel'),

    # RATING - Lo ponemos antes de la ruta de "<int:movie_id>/" o "<str:tag_type>/..."
    path('rate-movie/<int:movie_id>/', rate_movie, name='rate_movie'),

    # Películas - asegúrate de que esta ruta esté después de las rutas específicas
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),  # Detalles de película

    # Filtrar por etiqueta (ruta genérica). IMPORTANTE: esta va al final
    path('<str:tag_type>/<str:tag>/', views.movies_by_tag, name='movies_by_tag'),
]

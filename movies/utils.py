import os
import requests
import certifi
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

def get_movie_data_from_api(title=None, movie_id=None):
    """
    Obtiene datos de una película desde la API de TMDb, incluyendo director, reparto y tráiler de YouTube.
    Si se proporciona un `movie_id`, tiene prioridad sobre el `title`.
    """
    # Cargar la clave API desde las variables de entorno
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        raise ValueError("La clave API no está configurada. Asegúrate de tener TMDB_API_KEY en tu archivo .env")

    # Determinar si estamos en desarrollo (DEV_MODE=true en el archivo .env)
    is_dev = os.getenv("DEV_MODE", "false").lower() == "true"
    verify_ssl = not is_dev  # Si está en desarrollo, desactiva la verificación SSL

    # URLs de la API de TMDb
    search_url = "https://api.themoviedb.org/3/search/movie"
    details_url_template = "https://api.themoviedb.org/3/movie/{movie_id}"
    credits_url_template = "https://api.themoviedb.org/3/movie/{movie_id}/credits"
    videos_url_template = "https://api.themoviedb.org/3/movie/{movie_id}/videos"

    try:
        # Si se proporciona `movie_id`, buscar directamente por ID
        if movie_id:
            print(f"Usando ID de película: {movie_id}")

            # 1. Obtener detalles completos de la película
            details_url = details_url_template.format(movie_id=movie_id)
            details_response = requests.get(details_url, params={"api_key": api_key, "language": "es-ES"}, verify=certifi.where() if verify_ssl else False)
            details_response.raise_for_status()
            details_data = details_response.json()

            # 2. Obtener créditos (director y reparto)
            credits_url = credits_url_template.format(movie_id=movie_id)
            credits_response = requests.get(credits_url, params={"api_key": api_key}, verify=certifi.where() if verify_ssl else False)
            credits_response.raise_for_status()
            credits_data = credits_response.json()

            # Extraer director y reparto
            director = next((member['name'] for member in credits_data['crew'] if member['job'] == 'Director'), None)
            cast = ", ".join([actor['name'] for actor in credits_data['cast'][:5]])  # Los 5 principales

            # 3. Obtener el tráiler desde la sección de videos
            videos_url = videos_url_template.format(movie_id=movie_id)
            videos_response = requests.get(videos_url, params={"api_key": api_key, "language": "en-US"}, verify=certifi.where() if verify_ssl else False)
            videos_response.raise_for_status()
            videos_data = videos_response.json()

            # Buscar el primer tráiler en YouTube
            trailer_url = None
            for video in videos_data.get('results', []):
                if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                    trailer_url = f"https://www.youtube.com/embed/{video['key']}"
                    break

            # Devolver todos los datos necesarios
            return {
                "overview": details_data.get('overview'),
                "release_date": details_data.get('release_date'),
                "vote_average": details_data.get('vote_average'),
                "runtime": details_data.get('runtime'),
                "original_language": details_data.get('original_language'),
                "poster_path": details_data.get('poster_path'),
                "tmdb_url": f"https://www.themoviedb.org/movie/{movie_id}",
                "director": director,
                "cast": cast,
                "trailer_url": trailer_url,  # Nueva clave para la URL del tráiler
            }

        # Si no hay `movie_id`, buscar por título
        if title:
            print(f"Realizando búsqueda para: {title}")
            params = {
                "api_key": api_key,
                "query": title,
                "language": "es-ES"  # Idioma español
            }
            search_response = requests.get(search_url, params=params, verify=certifi.where() if verify_ssl else False)
            search_response.raise_for_status()
            search_data = search_response.json()

            if search_data['results']:
                # Obtener el ID de la primera coincidencia
                movie_id = search_data['results'][0]['id']
                print(f"ID de película encontrado: {movie_id}")

                # Recursivamente usar `movie_id` para obtener los detalles
                return get_movie_data_from_api(movie_id=movie_id)
            else:
                print(f"No se encontraron resultados para '{title}'")
                return None

        # Si no se proporciona ni `title` ni `movie_id`, no hay nada que buscar
        print("Se requiere un título o un ID de película para realizar la búsqueda.")
        return None

    except requests.exceptions.SSLError as ssl_error:
        print(f"Error SSL: {ssl_error}")
        return None
    except requests.RequestException as e:
        print(f"Otro error de solicitud: {e}")
        return None


def get_series_data_from_api(tmdb_url):
    """
    Obtiene datos de una serie desde la API de TMDb, incluyendo temporadas y episodios.
    """
    # Cargar la clave API desde las variables de entorno
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        raise ValueError("La clave API no está configurada. Asegúrate de tener TMDB_API_KEY en tu archivo .env")

    # Determinar si estamos en desarrollo
    is_dev = os.getenv("DEV_MODE", "false").lower() == "true"
    verify_ssl = not is_dev

    # Extraer el ID de la serie desde la URL de TMDb
    try:
        series_id = tmdb_url.rstrip('/').split('/')[-1]
        print(f"ID de la serie extraído: {series_id}")

        # 1. Obtener detalles generales de la serie
        details_url = f"https://api.themoviedb.org/3/tv/{series_id}"
        details_response = requests.get(details_url, params={"api_key": api_key, "language": "es-ES"}, verify=certifi.where() if verify_ssl else False)
        details_response.raise_for_status()
        details_data = details_response.json()

        # Formatear datos básicos de la serie
        series_data = {
            "title": details_data.get("name"),
            "description": details_data.get("overview"),
            "release_date": details_data.get("first_air_date"),
            "rating": details_data.get("vote_average"),
            "language": details_data.get("original_language"),
            "poster_path": details_data.get("poster_path"),
            "header_path": details_data.get("backdrop_path"),
            "seasons": []
        }

        # 2. Obtener las temporadas de la serie
        for season in details_data.get("seasons", []):
            season_number = season.get("season_number")
            season_details_url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}"
            season_response = requests.get(season_details_url, params={"api_key": api_key, "language": "es-ES"}, verify=certifi.where() if verify_ssl else False)
            season_response.raise_for_status()
            season_data = season_response.json()

            # Formatear datos de la temporada
            formatted_season = {
                "season_number": season_data.get("season_number"),
                "title": season_data.get("name"),
                "description": season_data.get("overview"),
                "episodes": []
            }

            # 3. Obtener los episodios de la temporada
            for episode in season_data.get("episodes", []):
                formatted_episode = {
                    "episode_number": episode.get("episode_number"),
                    "title": episode.get("name"),
                    "description": episode.get("overview"),
                    "air_date": episode.get("air_date"),
                    "screenshot_path": episode.get("still_path")
                }
                formatted_season["episodes"].append(formatted_episode)

            series_data["seasons"].append(formatted_season)

        return series_data

    except requests.RequestException as e:
        print(f"Error al obtener datos de la serie: {e}")
        return None

import os
import requests
import certifi
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

def get_movie_data_from_api(title):
    """
    Obtiene datos de una película desde la API de TMDb, incluyendo director, reparto y tráiler de YouTube.
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

    params = {
        "api_key": api_key,
        "query": title,
        "language": "es-ES"  # Idioma español
    }

    try:
        # 1. Buscar la película por título
        print(f"Realizando búsqueda para: {title}")
        search_response = requests.get(search_url, params=params, verify=certifi.where() if verify_ssl else False)
        search_response.raise_for_status()
        search_data = search_response.json()

        if search_data['results']:
            # Obtener el ID de la primera coincidencia
            movie_id = search_data['results'][0]['id']
            print(f"ID de película encontrado: {movie_id}")

            # 2. Obtener detalles completos de la película
            details_url = details_url_template.format(movie_id=movie_id)
            details_response = requests.get(details_url, params={"api_key": api_key, "language": "es-ES"}, verify=certifi.where() if verify_ssl else False)
            details_response.raise_for_status()
            details_data = details_response.json()

            # 3. Obtener créditos (director y reparto)
            credits_url = credits_url_template.format(movie_id=movie_id)
            credits_response = requests.get(credits_url, params={"api_key": api_key}, verify=certifi.where() if verify_ssl else False)
            credits_response.raise_for_status()
            credits_data = credits_response.json()

            # Extraer director y reparto
            director = next((member['name'] for member in credits_data['crew'] if member['job'] == 'Director'), None)
            cast = ", ".join([actor['name'] for actor in credits_data['cast'][:5]])  # Los 5 principales

            # 4. Obtener el tráiler desde la sección de videos
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

            # 5. Devolver todos los datos necesarios
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
        else:
            print(f"No se encontraron resultados para '{title}'")
            return None

    except requests.exceptions.SSLError as ssl_error:
        print(f"Error SSL: {ssl_error}")
        return None
    except requests.RequestException as e:
        print(f"Otro error de solicitud: {e}")
        return None

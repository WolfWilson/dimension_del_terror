import os
import requests
import certifi
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

def get_movie_data_from_api(title):
    """
    Obtiene datos de una película desde la API de TMDb, incluyendo director y reparto.
    """
    # Cargar la clave API desde las variables de entorno
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        raise ValueError("La clave API no está configurada. Asegúrate de tener TMDB_API_KEY en tu archivo .env")

    # Determinar si estamos en desarrollo (DEV_MODE=true en el archivo .env)
    is_dev = os.getenv("DEV_MODE", "false").lower() == "true"
    verify_ssl = not is_dev  # Si está en desarrollo, desactiva la verificación SSL

    search_url = "https://api.themoviedb.org/3/search/movie"
    details_url_template = "https://api.themoviedb.org/3/movie/{movie_id}"
    credits_url_template = "https://api.themoviedb.org/3/movie/{movie_id}/credits"
    params = {
        "api_key": api_key,
        "query": title,
        "language": "es-ES"  # Idioma español
    }

    try:
        # Buscar la película por título
        print(f"Realizando búsqueda para: {title}")
        search_response = requests.get(search_url, params=params, verify=certifi.where() if verify_ssl else False)
        search_response.raise_for_status()
        search_data = search_response.json()

        if search_data['results']:
            # Obtener el ID de la primera coincidencia
            movie_id = search_data['results'][0]['id']
            print(f"ID de película encontrado: {movie_id}")
            
            # Obtener detalles completos de la película
            details_url = details_url_template.format(movie_id=movie_id)
            details_response = requests.get(details_url, params={"api_key": api_key, "language": "es-ES"}, verify=certifi.where() if verify_ssl else False)
            details_response.raise_for_status()
            details_data = details_response.json()

            # Obtener créditos (director y reparto)
            credits_url = credits_url_template.format(movie_id=movie_id)
            credits_response = requests.get(credits_url, params={"api_key": api_key}, verify=certifi.where() if verify_ssl else False)
            credits_response.raise_for_status()
            credits_data = credits_response.json()

            # Extraer director y reparto
            director = next((member['name'] for member in credits_data['crew'] if member['job'] == 'Director'), None)
            cast = ", ".join([actor['name'] for actor in credits_data['cast'][:5]])  # Los 5 principales

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

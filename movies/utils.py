import requests

def get_movie_data_from_api(title):
    """
    Obtiene datos de una película desde la API de TMDb, incluyendo director y reparto.
    """
    api_key = "5758c3a5300652103ce452a959e52b42"  # Clave API
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
        search_response = requests.get(search_url, params=params, verify=False)
        search_response.raise_for_status()
        search_data = search_response.json()

        if search_data['results']:
            # Obtener el ID de la primera coincidencia
            movie_id = search_data['results'][0]['id']
            
            # Obtener detalles completos de la película
            details_url = details_url_template.format(movie_id=movie_id)
            details_response = requests.get(details_url, params={"api_key": api_key, "language": "es-ES"}, verify=False)
            details_response.raise_for_status()
            details_data = details_response.json()

            # Obtener créditos (director y reparto)
            credits_url = credits_url_template.format(movie_id=movie_id)
            credits_response = requests.get(credits_url, params={"api_key": api_key}, verify=False)
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
    except requests.RequestException as e:
        print(f"Error al comunicarse con TMDb: {e}")
        return None

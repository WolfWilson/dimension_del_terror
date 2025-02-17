function toggleFavorite(movieId) {
    fetch('/toggle_favorite/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken() // Asegurar que el token CSRF está correctamente definido
        },
        body: `movie_id=${movieId}`
    })
    .then(response => response.json())  // Asegurar que la respuesta se convierte en JSON
    .then(data => {
        const icon = document.getElementById(`fav-icon-${movieId}`);
        if (data.status === "added") {
            icon.textContent = "favorite";
        } else {
            icon.textContent = "favorite_border";
        }
    })
    .catch(error => console.error("Error al actualizar favoritos:", error));
}

function toggleWatchlist(movieId) {
    fetch('/toggle_watchlist/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },
        body: `movie_id=${movieId}`
    })
    .then(response => response.json())
    .then(data => {
        const icon = document.getElementById(`watchlist-icon-${movieId}`);
        if (data.status === "added") {
            icon.textContent = "visibility";
        } else {
            icon.textContent = "visibility_off";
        }
    })
    .catch(error => console.error("Error al actualizar 'Por Ver':", error));
}

// Obtener el token CSRF correctamente
function getCSRFToken() {
    const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    return tokenElement ? tokenElement.value : '';
}

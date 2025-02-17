document.addEventListener("DOMContentLoaded", function () {
    console.log("🚀 scripts.js ha sido cargado correctamente.");

    function setupMovieActions() {
        console.log("🎬 Configurando botones de favoritos y 'Por Ver'...");

        const favoriteButtons = document.querySelectorAll(".favorite-btn");
        const watchlistButtons = document.querySelectorAll(".watchlist-btn");

        favoriteButtons.forEach(button => {
            button.addEventListener("click", function () {
                const movieId = this.dataset.movieId;
                console.log(`🖤 Click en botón de favorito para la película ID: ${movieId}`);
                toggleFavorite(movieId);
            });
        });

        watchlistButtons.forEach(button => {
            button.addEventListener("click", function () {
                const movieId = this.dataset.movieId;
                console.log(`👀 Click en botón de 'Por Ver' para la película ID: ${movieId}`);
                toggleWatchlist(movieId);
            });
        });
    }

    function toggleFavorite(movieId) {
        console.log(`🔄 Enviando solicitud para agregar/quitar favorito a la película ${movieId}`);

        fetch(`/toggle-favorite/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ movie_id: movieId }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("✅ Respuesta del servidor:", data);
            const icon = document.getElementById(`fav-icon-${movieId}`);
            icon.textContent = data.is_favorite ? "favorite" : "favorite_border";
        })
        .catch(error => console.error("❌ Error en la petición:", error));
    }

    function toggleWatchlist(movieId) {
        console.log(`🔄 Enviando solicitud para agregar/quitar de 'Por Ver' la película ${movieId}`);

        fetch(`/toggle-watchlist/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ movie_id: movieId }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("✅ Respuesta del servidor:", data);
            const icon = document.getElementById(`watchlist-icon-${movieId}`);
            icon.textContent = data.is_watchlist ? "visibility" : "visibility_off";
        })
        .catch(error => console.error("❌ Error en la petición:", error));
    }

    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith("csrftoken=")) {
                    cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                    break;
                }
            }
        }
        return cookieValue;
    }

    setupMovieActions();
});

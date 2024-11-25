// js/resultados.js

// Array de todas las películas disponibles
const allMovies = [
    { title: "The Thing", title_es: "La Cosa", year: 1982, genre: ["Sci-fi", "Terror", "Criaturas", "Aliens"], poster: "posters/thing.jpg", link: "movies1/thing.html" },
    { title: "Night of the Living Dead", title_es: "La Noche de los Muertos Vivientes", year: 1990, genre: ["Terror", "Zombies"], poster: "posters/nightofthelivingdead.jpg", link: "movies1/nightofthelivingdead.html" },
    { title: "The Empty Man", title_es: "El mensajero del último día", year: 2020, genre: ["Terror", "Psicológico", "Suspenso", "Misterio", "Sectas"], poster: "posters/TheEmptyMan_Poster.jpg", link: "movies1/the_empty_man.html" },
    { title: "Incantation", title_es: "Maleficio", year: 2022, genre: ["Found Footage", "Terror sobrenatural", "Maldiciones"], poster: "posters/incantation.jpg", link: "movies1/incantation.html" },
    { title: "The Dark and the Wicked", title_es: "Lo Oscuro y lo Malvado", year: 2020, genre: ["Terror", "Drama", "Maldiciones", "Psicológico"], poster: "posters/thedarkandthewicked.jpg", link: "movies1/the_dark_and_the_wicked.html" },
    { title: "Martyrs", title_es: "Mártires", year: 2008, genre: ["Terror", "Sectas", "Gore", "Drama", "Psicológico"], poster: "posters/martyrs.jpg", link: "movies1/martyrs.html" },
    { title: "Cuando acecha la maldad", title_es: "Cuando Acecha la Maldad", year: 2023, genre: ["Terror", "Maldiciones", "Folk"], poster: "posters/Cuando_acecha_la_maldad.jpg", link: "movies1/cuando_acecha_la_maldad.html" },
    { title: "Color Out of Space", title_es: "El Color que Cayó del Espacio", year: 2019, genre: ["Sci-Fi", "Terror"], poster: "posters/colors.jpg", link: "movies1/color_out_of_space.html" },
    { title: "The Descent", title_es: "El Descenso", year: 2009, genre: ["Terror", "Criaturas"], poster: "posters/descent.jpg", link: "movies1/the_descent.html" },
    { title: "Los Sin Nombre", title_es: "Los Sin Nombre", year: 1999, genre: ["Terror", "Thriller", "Sectas", "Drama", "Misterio"], poster: "posters/lossinnombre.jpg", link: "movies1/los_sin_nombre.html" },
    { title: "The Relic", title_es: "La Reliquia", year: 1995, genre: ["Terror", "Criaturas", "Humor Negro"], poster: "posters/THERELIC.jpg", link: "movies1/the_relic.html" },
    { title: "30 Days of Night", title_es: "30 Días de Noche", year: 2007, genre: ["Terror", "Vampiros", "Gore", "Slasher"], poster: "posters/30 days of night poster.jpg", link: "movies1/30_days_of_night.html" },

    // Nuevas películas agregadas movies2
    { title: "Unfriended Dark Web", title_es: "Eliminado: Dark Web", year: 2018, genre: ["Found Footage", "Terror", "Thriller"], poster: "posters2/unfriended.jpg", link: "movies2/unfriended.html" },
    { title: "The Superdeep", title_es: "Superprofundo", year: 2020, genre: ["Terror", "Sci-fi", "Criaturas"], poster: "posters2/superdeep.jpg", link: "movies2/superdeep.html" },
    { title: "The Hunt", title_es: "La Caza", year: 2020, genre: ["Thriller", "Acción", "Slasher", "Humor Negro", "Gore"], poster: "posters2/hunt.jpg", link: "movies2/hunt.html" },
    { title: "The Crimson Rivers", title_es: "Los ríos de color púrpura", year: 2000, genre: ["Misterio", "Crimen", "Drama", "Thriller"], poster: "posters2/crimsonrivers.jpg", link: "movies2/crimsonrivers.html" },
    { title: "Ready Or Not", title_es: "Boda Sangrienta", year: 2019, genre: ["Terror", "Humor Negro", "Thriller", "Sectas", "Vampiros"], poster: "posters2/readyornot.jpg", link: "movies2/readyornot.html" },
    { title: "Phantoms", title_es: "Fantasmas", year: 1998, genre: ["Terror", "Misterio", "Sci-fi", "Criaturas"], poster: "posters2/phantoms.jpg", link: "movies2/phantoms.html" },
    { title: "Necronomicon Book Of The Dead", title_es: "Necronomicon: El Libro de los Muertos", year: 1994, genre: ["Terror", "Fantasía", "Misterio", "Criaturas"], poster: "posters2/necronomicon.jpg", link: "movies2/necronomicon.html" },
    { title: "Lifeforce", title_es: "Fuerza Vital", year: 1985, genre: ["Sci-fi", "Terror", "Aliens", "Zombies"], poster: "posters2/lifeforce.jpg", link: "movies2/lifeforce.html" },
    { title: "Lake Mungo", title_es: "El Lago Mungo", year: 2008, genre: ["Terror", "Misterio", "Falso Documental", "Found Footage", "Terror sobrenatural"], poster: "posters2/lakemungo.jpg", link: "movies2/lakemungo.html" },
    { title: "Forbidden Siren", title_es: "Forbidden Siren", year: 2006, genre: ["Terror", "Terror sobrenatural", "Misterio", "Thriller", "Maldiciones"], poster: "posters2/forbiddensiren.jpg", link: "movies2/forbiddensiren.html" },
    { title: "No One Will Save You", title_es: "Nadie podrá salvarte", year: 2023, genre: ["Aliens", "Sci-fi", "Terror", "Thriller"], poster: "posters2/noonewillsaveyou.jpg", link: "movies2/noonewillsaveyou.html" },
    { title: "Gekijoban Rei Zero", title_es: "Fatal Frame", year: 2008, genre: ["Terror", "Misterio", "Thriller", "Terror sobrenatural", "Maldiciones"], poster: "posters2/gekijobanrei.jpg", link: "movies2/gekijoban.html" },

    // Nuevas películas agregadas movies3
    { title: "Speak No Evil", title_es: "No hables con extraños", year: 2024, genre: ["Terror", "Psicológico", "Crimen", "Drama", "Thriller"], poster: "posters3/speaknoevil.jpg", link: "movies3/speaknoevil.html" },
    { title: "Slither", title_es: "La Plaga", year: 2006, genre: ["Terror", "Criaturas", "Humor Negro", "Aliens", "Sci-fi"], poster: "posters3/slither.jpg", link: "movies3/slither.html" },
    { title: "Longlegs", title_es: "Piernas Largas", year: 2024, genre: ["Terror", "Misterio", "Suspenso", "Sectas"], poster: "posters3/longlegs.jpg", link: "movies3/longlegs.html" },
    { title: "The First Omen", title_es: "La Primer Profecia", year: 2024, genre: ["Terror", "Psicológico", "Terror sobrenatural", "Misterio", "Sectas"], poster: "posters3/firtsomen.jpg", link: "movies3/firstomen.html" },
    { title: "The Taking of Deborah Logan", title_es: "La posesión de Deborah Logan.", year: 2014, genre: ["Terror", "Found Footage", "Terror sobrenatural", "Falso Documental"], poster: "posters3/the-taking-of-deborah-logan.jpg", link: "movies3/the-taking-of-deborah-logan.html" },
    { title: "The Substance", title_es: "La Sustancia", year: 2024, genre: ["Terror", "Ciencia Ficción", "Misterio", "Drama"], poster: "posters3/substance.jpg", link: "movies3/the_substance.html" },
    { title: "Alien: Romulus", title_es: "Alien: Romulus", year: 2024, genre: ["Terror", "Ciencia Ficción", "Aliens"], poster: "posters3/aliens_romulus.jpg", link: "movies3/alien_romulus.html" },
    { title: "V/H/S BEYOND", title_es: "V/H/S Más Allá", year: 2024, genre: ["Terror", "Antología", "Found Footage"], poster: "posters3/vhs_beyond.jpg", link: "movies3/vhs_beyond.html" },
    { title: "The Blob", title_es: "La Mancha Voraz", year: 1988, genre: ["Terror", "Ciencia Ficción", "Criaturas"], poster: "posters3/blob1.jpg", link: "movies3/the_blob.html" },
    { title: "Little Shop of Horrors: Director's Cut", title_es: "La Tiendita del Horror: Versión del Director", year: 1986, genre: ["Humor Negro", "Criaturas", "Ciencia Ficción"], poster: "posters3/little_shop.jpg", link: "movies3/little_shop_of_horrors.html" },
    { title: "Return of the Living Dead 3", title_es: "El Regreso de los Muertos Vivientes 3", year: 1993, genre: ["Terror", "Zombies", "Culto"], poster: "posters3/return_of_the_living_dead_3.jpg", link: "movies3/return_of_the_living_dead3.html" }, 
    { title: "Late Night with the Devil", title_es: "Late Night con el Diablo", year: 2023, genre: ["Terror", "Suspenso",  "Terror sobrenatural", "Misterio"], poster: "posters3/late_night_with_the_devil.jpg", link: "movies3/late_night_with_the_devil.html" }

    

];


// Obtener el término de búsqueda desde localStorage
const searchQuery = localStorage.getItem('searchQuery').toLowerCase();

// Filtrar las películas que coincidan con el término de búsqueda en título en inglés, español o año
const filteredMovies = allMovies.filter(movie => {
    // Comparar el título en inglés, español y el año con la búsqueda
    return movie.title.toLowerCase().includes(searchQuery) || 
           movie.title_es.toLowerCase().includes(searchQuery) || 
           movie.year.toString().includes(searchQuery);
});

// Contenedor donde se mostrarán los resultados
const resultsContainer = document.getElementById('results-container');

// Verificar si se encontraron resultados
if (filteredMovies.length > 0) {
    filteredMovies.forEach(movie => {
        const movieElement = `
            <div class="poster-box">
                <div class="poster-content">
                    <img src="${movie.poster}" alt="${movie.title}">
                    <div class="hover-overlay">
                        <a href="${movie.link}" class="details-button">Ver</a>
                    </div>
                </div>
                <div class="poster-info">
                    <p>${movie.title} (${movie.year})</p>
                </div>        
            </div>
        `;
        resultsContainer.innerHTML += movieElement;
    });
} else {
    // Si no se encontraron resultados, muestra un mensaje
    resultsContainer.innerHTML = `<p>No se encontraron resultados para "${searchQuery}".</p>`;
}
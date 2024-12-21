// js/search.js

// Capturar el evento del botón de búsqueda
document.getElementById('search-button').addEventListener('click', function(event) {
    event.preventDefault(); // Evitar la recarga de la página

    // Obtener el valor del cuadro de búsqueda
    const query = document.getElementById('search-input').value.trim().toLowerCase();

    if (query) {
        // Guardar el término de búsqueda en localStorage
        localStorage.setItem('searchQuery', query);
        // Redirigir a la página de resultados
        window.location.href = 'resultados.html';
    } else {
        alert("Por favor, ingrese un término de búsqueda.");
    }
});

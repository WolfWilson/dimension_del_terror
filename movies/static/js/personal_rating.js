document.addEventListener("DOMContentLoaded", function () {
    // Seleccionar cada contenedor .star-rating
    document.querySelectorAll(".star-rating").forEach(ratingEl => {
      const movieId = ratingEl.getAttribute("data-movie-id");
      const stars = ratingEl.querySelectorAll(".star");
  
      // NUEVO: Leer la calificación inicial del atributo data-initial-rating
      let initialRating = parseFloat(ratingEl.getAttribute("data-initial-rating")) || 0;
  
      // Resaltar estrellas según la calificación inicial
      highlightStars(stars, initialRating);
  
      // También actualiza el texto, si existe #user-rating-display
      let display = ratingEl.parentNode.querySelector("#user-rating-display");
      if (display) {
        display.textContent = initialRating.toFixed(1);
      }
  
      // Manejar eventos en cada estrella
      stars.forEach(star => {
        // Hover (previsualización de media estrella)
        star.addEventListener("mousemove", function (e) {
          const rect = star.getBoundingClientRect();
          const offsetX = e.clientX - rect.left;
          const half = rect.width / 2;
          let starIndex = parseInt(star.getAttribute("data-index"));
  
          // Cálculo para media estrella
          let rating = (offsetX < half) ? starIndex + 0.5 : starIndex + 1;
          highlightStars(stars, rating);
        });
  
        // Click (guardar calificación)
        star.addEventListener("click", function (e) {
          const rect = star.getBoundingClientRect();
          const offsetX = e.clientX - rect.left;
          const half = rect.width / 2;
          let starIndex = parseInt(star.getAttribute("data-index"));
  
          // Cálculo final de la calificación (0.5 / 1)
          let rating = (offsetX < half) ? starIndex + 0.5 : starIndex + 1;
  
          saveRating(movieId, rating);
  
          // Actualizar texto y resaltar estrellas
          if (display) {
            display.textContent = rating.toFixed(1);
          }
          highlightStars(stars, rating);
        });
  
        // Quitar la previsualización al salir
        star.addEventListener("mouseleave", function () {
          // Al salir, podrías restaurar el rating actual si quieres.
          highlightStars(stars, parseFloat(display.textContent) || 0);
        });
      });
    });
  
    // Función para resaltar las estrellas
    function highlightStars(stars, rating) {
      stars.forEach(star => {
        const starValue = parseFloat(star.getAttribute("data-index")) + 1;
        // Si starValue <= rating => la estrella se marca como 'active'
        star.classList.toggle("active", starValue <= rating);
      });
    }
  
    // Guardar rating en el backend
    function saveRating(movieId, ratingValue) {
      fetch(`/rate-movie/${movieId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": getCSRFToken()
        },
        body: `rating=${ratingValue}`
      })
      .then(res => res.json())
      .then(data => {
        if (!data.success) {
          console.error("Fallo al guardar rating");
        }
      })
      .catch(err => console.error("Error rating:", err));
    }
  
    // Obtener CSRF token
    function getCSRFToken() {
      return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
  });
  
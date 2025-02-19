document.addEventListener("DOMContentLoaded", function () {
    // 1. Seleccionar contenedores de rating
    document.querySelectorAll(".star-rating").forEach(ratingEl => {
      const movieId = ratingEl.getAttribute("data-movie-id");
      const stars = ratingEl.querySelectorAll(".star");
  
      // 2. Agregar eventos a cada estrella
      stars.forEach(star => {
        star.addEventListener("mousemove", function (e) {
          // Detectar mitad izquierda/derecha
          const rect = star.getBoundingClientRect();
          const offsetX = e.clientX - rect.left; // Posición X del cursor sobre la estrella
          const half = rect.width / 2;           // Mitad de la estrella
          let starIndex = parseInt(star.getAttribute("data-index"));
  
          // => ratingValue = starIndex + 1 si clic en mitad derecha
          // => ratingValue = starIndex + 0.5 si clic en mitad izquierda
          let rating = (offsetX < half) ? starIndex + 0.5 : starIndex + 1;
  
          // Previsualizar en pantalla (hover)
          highlightStars(stars, rating);
        });
  
        star.addEventListener("click", function (e) {
          const rect = star.getBoundingClientRect();
          const offsetX = e.clientX - rect.left;
          const half = rect.width / 2;
          let starIndex = parseInt(star.getAttribute("data-index"));
          let rating = (offsetX < half) ? starIndex + 0.5 : starIndex + 1;
  
          // Llamar API para enviar rating
          saveRating(movieId, rating);
  
          // Actualizar texto
          let display = ratingEl.parentNode.querySelector("#user-rating-display");
          if (display) {
            display.textContent = rating.toFixed(1);
          }
  
          // Destacar las estrellas de forma permanente
          highlightStars(stars, rating);
        });
  
        // Quitar la previsualización al salir
        star.addEventListener("mouseleave", function () {
          // Podrías restaurar al rating actual si lo tienes almacenado
        });
      });
    });
  
    // 3. Función para resaltar las estrellas
    function highlightStars(stars, rating) {
      stars.forEach(star => {
        const starValue = parseFloat(star.getAttribute("data-index")) + 1;
        const starHalfValue = parseFloat(star.getAttribute("data-index")) + 0.5;
        // Si rating >= starValue => estrella completa
        // Si rating >= starHalfValue pero < starValue => media
        // Para simplificar: si starValue <= rating => active
        star.classList.toggle("active", starValue <= rating);
      });
    }
  
    // 4. Guardar rating en el backend
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
  
    // 5. Función para obtener CSRF token
    function getCSRFToken() {
      return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
  });
  
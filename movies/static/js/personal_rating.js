document.addEventListener("DOMContentLoaded", function () {
    // Seleccionar cada contenedor .star-rating
    document.querySelectorAll(".star-rating").forEach(ratingEl => {
      const movieId = ratingEl.getAttribute("data-movie-id");
      const stars = ratingEl.querySelectorAll(".star");
  
      // Leer la calificación inicial desde el atributo data-initial-rating
      let initialRating = parseFloat(ratingEl.getAttribute("data-initial-rating")) || 0;
  
      // Pintar estrellas según la calificación inicial
      highlightStars(stars, initialRating);
  
      // Actualizar el texto, si existe #user-rating-display
      let display = ratingEl.parentNode.querySelector("#user-rating-display");
      if (display) {
        display.textContent = initialRating.toFixed(1);
      }
  
      // Manejo de eventos en cada estrella
      stars.forEach(star => {
        // Hover (previsualizar media estrella)
        star.addEventListener("mousemove", function (e) {
          const rect = star.getBoundingClientRect();
          const offsetX = e.clientX - rect.left;
          const half = rect.width / 2;
          let starIndex = parseInt(star.getAttribute("data-index"));
  
          // Si el cursor está en la mitad izquierda => +0.5
          // Sino => +1
          let rating = (offsetX < half) ? starIndex + 0.5 : starIndex + 1;
  
          highlightStars(stars, rating);
        });
  
        // Click (guardar calificación en el backend)
        star.addEventListener("click", function (e) {
          const rect = star.getBoundingClientRect();
          const offsetX = e.clientX - rect.left;
          const half = rect.width / 2;
          let starIndex = parseInt(star.getAttribute("data-index"));
          let rating = (offsetX < half) ? starIndex + 0.5 : starIndex + 1;
  
          // Llamar backend
          saveRating(movieId, rating);
  
          // Actualizar texto y resaltar en pantalla
          if (display) {
            display.textContent = rating.toFixed(1);
          }
          highlightStars(stars, rating);
        });
  
        // Al salir con el mouse, vuelve a la calificación actual
        star.addEventListener("mouseleave", function () {
          let currentVal = parseFloat(display ? display.textContent : 0) || 0;
          highlightStars(stars, currentVal);
        });
      });
    });
  
 // :::::::::::::: Función para resaltar estrellas ::::::::::::::
function highlightStars(stars, rating) {
    // 1) Limpiar la clase "clicked" de todas las estrellas
    stars.forEach(star => star.classList.remove("clicked"));
  
    // 2) Pintar cada estrella
    stars.forEach(star => {
      const starIndex = parseInt(star.getAttribute("data-index"));
      const starNumber = starIndex + 1; // 1..5
  
      // Restablecer la estrella a su estado vacío por defecto (gris)
      star.classList.remove("fa-star", "fa-star-half-alt", "active");
      star.classList.add("fa-star"); // Siempre muestra la estrella
      star.style.color = "#ccc";     // Gris por defecto
  
      if (rating >= starNumber) {
        // Estrella completa
        star.classList.add("active");
        star.style.color = getStarColor(rating);
      } else if (rating >= starIndex + 0.5) {
        // Media estrella
        star.classList.remove("fa-star"); // Quitar estrella completa
        star.classList.add("fa-star-half-alt", "active");
        star.style.color = getStarColor(rating);
      }
    });
  
    // 3) Determinar sobre qué estrella ocurre el click
    //    - p.ej. si rating=3.5, la estrella "central" es starIndex=2 => 3ra estrella
    //    - Si rating=4 => starIndex=3 => 4ta estrella
    if (rating > 0) {
      let clickedIndex = Math.floor(rating - 0.5);
      // Controlar límites (por si rating<1)
      if (clickedIndex < 0) {
        clickedIndex = 0;
      } else if (clickedIndex > 4) {
        clickedIndex = 4;
      }
  
      // 4) Agregar la clase "clicked" sólo a la estrella correspondiente
      stars[clickedIndex].classList.add("clicked");
    }
  }
  
  // ✅ Función para obtener el color dinámico según la calificación seleccionada
  function getStarColor(rating) {
    if (rating >= 0.5 && rating <= 1) {
      return "red";      // 0.5 - 1 (Rojo)
    } else if (rating > 1 && rating <= 2.5) {
      return "orange";   // 1.5 - 3 (Naranja)
    } else if (rating > 3 && rating <= 4.5) {
     return "gold";     // 3.5  - 4 .5(Dorado)  
    } else if (rating === 5) {
      return "purple";   // 5 (Morado)
    }
    return "gold";       // Por defecto
  }
  
  
    // :::::::::::::: Guardar rating en el servidor ::::::::::::::
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
          console.error("Fallo al guardar rating:", data);
        }
      })
      .catch(err => console.error("Error rating:", err));
    }
  
    // :::::::::::::: Obtener CSRF token ::::::::::::::
    function getCSRFToken() {
      const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");
      return csrfInput ? csrfInput.value : "";
    }
  });
  
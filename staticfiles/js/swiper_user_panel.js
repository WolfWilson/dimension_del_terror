document.addEventListener("DOMContentLoaded", function () {
    new Swiper(".favorites-carousel", {
      slidesPerView: 7,  // Por defecto en PC
      spaceBetween: 20,
      loop: true,
      navigation: {
        nextEl: ".favorites-next",
        prevEl: ".favorites-prev",
      },
      breakpoints: {
        1440: { slidesPerView: 7 },
        1024: { slidesPerView: 5 },
        768:  { slidesPerView: 4 },
        600:  { slidesPerView: 3 },
        450:  { slidesPerView: 2 }  // Muestra solo 2 en pantallas pequeñas
      }
    });
  
    new Swiper(".watchlist-carousel", {
      slidesPerView: 7,
      spaceBetween: 20,
      loop: true,
      navigation: {
        nextEl: ".watchlist-next",
        prevEl: ".watchlist-prev",
      },
      breakpoints: {
        1440: { slidesPerView: 7 },
        1024: { slidesPerView: 5 },
        768:  { slidesPerView: 4 },
        600:  { slidesPerView: 3 },
        450:  { slidesPerView: 2 }
      }
    });
  });
  
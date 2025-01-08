// Asegurarse de que el DOM esté completamente cargado antes de ejecutar cualquier script
$(document).ready(function () {
    /**
     * Inicializa Fancybox para los elementos que contienen el atributo `data-fancybox`.
     * Configuración específica para manejar iframes.
     */
    $('[data-fancybox]').fancybox({
        iframe: {
            css: {
                width: '80%',  // Ancho del iframe dentro del popup
                height: '80%'  // Altura del iframe dentro del popup
            },
        },
        transitionEffect: "zoom-in-out", // Efecto de transición al abrir/cerrar
        transitionDuration: 400,        // Duración del efecto de transición en milisegundos

        // Evento que se ejecuta antes de mostrar el popup
        beforeShow: function (instance, slide) {
            $(".fancybox-content").addClass("open"); // Agrega la clase personalizada `open` para efectos visuales
        },

        // Evento que se ejecuta antes de cerrar el popup
        beforeClose: function (instance, slide) {
            $(".fancybox-content").removeClass("open").addClass("close"); // Cambia la clase para animaciones de cierre
        },
    });
});

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


// Configura dinámicamente la imagen de fondo del encabezado usando el atributo `data-bg-url`
document.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector(".series-header");
    if (header) {
        const bgUrl = header.getAttribute("data-bg-url");
        if (bgUrl) {
            header.style.backgroundImage = `url('${bgUrl}')`;
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    setupThemeToggle();

    // Configuración del botón de Modo Oscuro/Claro
    function setupThemeToggle() {
        // Crear el botón y el icono
        const toggleButton = document.createElement("button");
        const toggleIcon = document.createElement("span");

        // Configuración del botón
        toggleButton.classList.add("theme-toggle-button"); // Agregar clase CSS
        toggleIcon.classList.add("material-icons");
        toggleIcon.textContent = "dark_mode"; // Icono inicial
        toggleButton.appendChild(toggleIcon);

        // Añadir el botón al body
        document.body.appendChild(toggleButton);

        // Comprobar el modo actual en localStorage
        const currentTheme = localStorage.getItem("theme");
        if (currentTheme === "dark") {
            document.body.classList.add("dark-mode");
            toggleIcon.textContent = "light_mode"; // Cambiar icono a "light_mode"
        }

        // Alternar entre modos
        toggleButton.addEventListener("click", function () {
            if (document.body.classList.contains("dark-mode")) {
                document.body.classList.remove("dark-mode");
                localStorage.setItem("theme", "light"); // Guardar preferencia en localStorage
                toggleIcon.textContent = "dark_mode"; // Cambiar icono a "dark_mode"
            } else {
                document.body.classList.add("dark-mode");
                localStorage.setItem("theme", "dark"); // Guardar preferencia en localStorage
                toggleIcon.textContent = "light_mode"; // Cambiar icono a "light_mode"
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    // Modal de Confirmación
    function setupModal() {
        const closeModal = document.getElementById("closeModal");
        const modal = document.getElementById("requestModal");

        if (closeModal && modal) {
            closeModal.addEventListener("click", function () {
                modal.classList.add("hidden"); // Oculta el modal
            });
        }
    }

    // Botón de Modo Oscuro/Claro
    function setupThemeToggle() {
        const toggleButton = document.createElement("button");
        const toggleIcon = document.createElement("span");

        // Configuración del botón
        toggleButton.style.position = "fixed";
        toggleButton.style.bottom = "10px";
        toggleButton.style.right = "10px";
        toggleButton.style.zIndex = "1000";
        toggleButton.style.padding = "10px";
        toggleButton.style.border = "none";
        toggleButton.style.backgroundColor = "var(--accent-color)";
        toggleButton.style.color = "var(--text-color)";
        toggleButton.style.borderRadius = "50%";
        toggleButton.style.cursor = "pointer";
        toggleButton.style.display = "flex";
        toggleButton.style.justifyContent = "center";
        toggleButton.style.alignItems = "center";
        toggleButton.style.width = "50px";
        toggleButton.style.height = "50px";
        toggleButton.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.3)";

        // Configuración del icono
        toggleIcon.classList.add("material-icons");
        toggleIcon.style.fontSize = "24px";
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

    // Botón para Alternar el Formulario de Contacto
    function setupContactFormToggle() {
        const toggleFormButton = document.getElementById("toggleFormButton");
        const contactForm = document.getElementById("contact-form");

        if (toggleFormButton && contactForm) {
            toggleFormButton.addEventListener("click", function () {
                contactForm.classList.toggle("hidden");
            });
        }
    }

    // Abrir Formulario desde el Enlace
    function setupOpenFormLink() {
        const openFormLink = document.getElementById("openFormLink");
        const contactForm = document.getElementById("contact-form");

        if (openFormLink && contactForm) {
            openFormLink.addEventListener("click", function (e) {
                e.preventDefault(); // Previene el comportamiento predeterminado del enlace
                contactForm.classList.remove("hidden"); // Muestra el formulario
                contactForm.scrollIntoView({ behavior: "smooth" }); // Hace scroll hacia el formulario
            });
        }
    }

    // Inicializar todas las funciones
    setupModal();
    setupThemeToggle();
    setupContactFormToggle();
    setupOpenFormLink();
});

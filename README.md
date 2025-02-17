# 🎬 **Dimensión del Terror**  

![Licencia](https://img.shields.io/badge/Licencia-MIT-green.svg) ![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg) ![Django](https://img.shields.io/badge/Framework-Django-orange.svg) ![Estado](https://img.shields.io/badge/Estado-Estable-success.svg)  

**Dimensión del Terror** es una plataforma web para **amantes del cine de terror y ciencia ficción**. Con ella puedes **gestionar, explorar y buscar películas** de manera sencilla y eficiente. 🚀  

---

## 🎥 **Características Principales**  

### 🎞️ **Gestión de Películas**  
✔️ Agrega películas con información detallada:  
   - 🎬 **Título**  
   - 📝 **Descripción**  
   - 🎭 **Reparto**  
   - 📅 **Fecha de Lanzamiento**  
   - 🎛️ **Géneros**  
   - 🎞️ **Duración**  
   - 🌐 **Idioma**  
   - ⭐ **Calificación**  
✔️ **Sube posters** manualmente o permite que el sistema autocomplete la información usando la **API de TMDb**.  

### 🔍 **Búsqueda y Filtrado**  
🔹 Búsqueda rápida por **título**.  
🔹 Filtrado de películas por **género**.  

### 🖥️ **Frontend Dinámico y Responsive**  
✔️ Listado con paginación y buscador interactivo.  
✔️ Página de detalles con información completa.  
✔️ **Diseño responsive** optimizado para móviles y escritorio.  

### ⚙️ **Gestión desde Django Admin**  
🔹 Control total de películas y datos desde el panel de administración.  

### 📂 **Soporte de Archivos**  
✔️ Subida de **imágenes personalizadas** para los posters y headers.  

---

## 🛠️ **Instalación y Configuración**  

### 🔽 **1. Clonar el Repositorio**  
```bash
git clone https://github.com/tu_usuario/black-cat-cinema.git
cd black-cat-cinema

🏗️ 2. Crear un Entorno Virtual
python -m venv venv  
source venv/bin/activate  # macOS/Linux  
venv\Scripts\activate     # Windows

📦 3. Instalar Dependencias
pip install -r requirements.txt

⚙️ 4. Configurar Variables de Entorno
Crea un archivo .env en la raíz del proyecto con el siguiente contenido:
DEBUG=True
SECRET_KEY=tu_clave_secreta
TMDB_API_KEY=tu_api_key_de_tmdb

📀 5. Aplicar Migraciones y Ejecutar el Servidor
python manage.py migrate
python manage.py runserver

🔗 Accede a la aplicación en tu navegador:
http://127.0.0.1:8000/


📂## Estructura del Proyecto

blackcatcinema/
├── blackcatcinema/        # Configuración principal de Django
├── movies/                # Aplicación principal
│   ├── templates/         # Plantillas HTML
│   ├── static/            # Archivos estáticos (CSS, JS, imágenes)
│   ├── models.py          # Modelos de la base de datos
│   ├── views.py           # Lógica de las vistas
│   ├── utils.py           # Funciones auxiliares (API de TMDb, etc.)
├── media/                 # Directorio para archivos subidos
├── static/                # Archivos estáticos generales
├── manage.py              # Herramienta de administración de Django
└── requirements.txt       # Dependencias del proyecto

🚀 Tecnologías Utilizadas
🔹 Backend: Django 5.x
🔹 Frontend: HTML, CSS, JavaScript
🔹 Base de Datos: SQLite
🔹 Framework UI: PyQt5
🔹 APIs Externas: The Movie Database (TMDb)


📌 Estado del Proyecto
🔸 Estado: 🔵 En desarrollo | 🟢 Estable | 🔴 En mantenimiento
🔸 Próximas mejoras:

📌 Integración de usuarios y comentarios
📌 Soporte para más idiomas
📌 Mejoras en rendimiento


📜 Licencia
Este proyecto está bajo la licencia MIT. ¡Úsalo, modifícalo y compártelo libremente!


📢 Si te gusta este proyecto, considera darle una ⭐ en GitHub.


### **🔹 ¿A futuro?**
✅ Mejor organización** creación de sección de colecciones para agrupas sagas de peliculas.  
✅ Listas de favoritos y por ver 
✅ .Agregar calificicación personalizada para cada usuario en formato 5 estrellas debajo de cada poster
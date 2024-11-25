# 🎬 Black Cat Cinema

**Black Cat Cinema** es una aplicación web para amantes del terror y la ciencia ficción. Con esta plataforma, puedes gestionar películas, buscar por géneros, y disfrutar de un diseño intuitivo con potentes funcionalidades. 🐾🎥

---

## 🚀 **Características Principales**

### 🎥 **Gestión de Películas**
- Agrega películas con información detallada: 🎬 **Título**, 📝 **Descripción**, 🎭 **Reparto**, 📅 **Fecha de Lanzamiento**, 🎛️ **Géneros**, 🎞️ **Duración**, 🌐 **Idioma**, ⭐ **Calificación**, y más.
- **Sube posters** de películas o deja que se autocompleten con datos de la API de TMDb. 🖼️
- **Generación automática** de datos opcionales desde la API de TMDb, como duración, idioma, director y más.

### 🔎 **Búsqueda y Filtrado**
- Búsqueda de películas por título. 🔤
- Filtrado de películas por género (etiquetas o tags). 🏷️

### 🖼️ **Frontend Dinámico**
- Página principal que lista películas con paginación y buscador. 🧭
- Página de detalles de películas con información completa y enlace directo para visualización. 🎞️
- Diseño **responsive** para una experiencia óptima en dispositivos móviles y de escritorio. 📱💻
♦
### ⚙️ **Gestión desde el Administrador de Django**
- Control total de películas, géneros, y otros datos desde el panel de administración. 🔐

### 📁 **Soporte para Archivos**
- Subida de imágenes de posters y headers personalizados al directorio configurado. 🖼️

---

## 🛠️ **Instalación**

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/black-cat-cinema.git
   cd black-cat-cinema

2. Crea un entorno virtual:

python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate    # Windows

3.Instala las dependencias:
pip install -r requirements.txt

4.Configura el entorno:
Crea un archivo .env con las siguientes variables:
DEBUG=True
SECRET_KEY=tu_clave_secreta
TMDB_API_KEY=tu_api_key_de_tmdb

5. Ejecuta migraciones y levanta el servidor:
python manage.py migrate
python manage.py runserver


6. Abre tu navegador en: http://127.0.0.1:8000/


📚 Estructura del Proyecto


blackcatcinema/
├── blackcatcinema/         # Configuración principal del proyecto Django
├── movies/                 # Aplicación principal
│   ├── templates/          # Plantillas HTML
│   ├── static/             # Archivos estáticos (CSS, JS, imágenes)
│   ├── models.py           # Modelos de la base de datos
│   ├── views.py            # Lógica de las vistas
│   ├── utils.py            # Funciones auxiliares (API de TMDb, etc.)
├── media/                  # Directorio para archivos subidos
├── static/                 # Archivos estáticos generales
├── manage.py               # Herramienta de administración de Django
└── requirements.txt        # Dependencias del proyecto



¡Claro! Aquí tienes un ejemplo de un archivo README.md bien formateado para tu proyecto en GitHub. Incluye emojis, encabezados claros y un formato profesional para hacerlo atractivo y funcional.

markdown
Copiar código
# 🎬 Black Cat Cinema

**Black Cat Cinema** es una aplicación web para amantes del terror y la ciencia ficción. Con esta plataforma, puedes gestionar películas, buscar por géneros, y disfrutar de un diseño intuitivo con potentes funcionalidades. 🐾🎥

---

## 🚀 **Características Principales**

### 🎥 **Gestión de Películas**
- Agrega películas con información detallada: 🎬 **Título**, 📝 **Descripción**, 🎭 **Reparto**, 📅 **Fecha de Lanzamiento**, 🎛️ **Géneros**, 🎞️ **Duración**, 🌐 **Idioma**, ⭐ **Calificación**, y más.
- **Sube posters** de películas o deja que se autocompleten con datos de la API de TMDb. 🖼️
- **Generación automática** de datos opcionales desde la API de TMDb, como duración, idioma, director y más.

### 🔎 **Búsqueda y Filtrado**
- Búsqueda de películas por título. 🔤
- Filtrado de películas por género (etiquetas o tags). 🏷️

### 🖼️ **Frontend Dinámico**
- Página principal que lista películas con paginación y buscador. 🧭
- Página de detalles de películas con información completa y enlace directo para visualización. 🎞️
- Diseño **responsive** para una experiencia óptima en dispositivos móviles y de escritorio. 📱💻

### ⚙️ **Gestión desde el Administrador de Django**
- Control total de películas, géneros, y otros datos desde el panel de administración. 🔐

### 📁 **Soporte para Archivos**
- Subida de imágenes de posters y headers personalizados al directorio configurado. 🖼️

---

## 🛠️ **Instalación**

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/black-cat-cinema.git
   cd black-cat-cinema
Crea un entorno virtual:

bash
Copiar código
python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate    # Windows
Instala las dependencias:

bash
Copiar código
pip install -r requirements.txt
Configura el entorno:

Crea un archivo .env con las siguientes variables:
env
Copiar código
DEBUG=True
SECRET_KEY=tu_clave_secreta
TMDB_API_KEY=tu_api_key_de_tmdb
Ejecuta migraciones y levanta el servidor:

bash
Copiar código
python manage.py migrate
python manage.py runserver
Abre tu navegador en: http://127.0.0.1:8000/

📚 Estructura del Proyecto
php
Copiar código
blackcatcinema/
├── blackcatcinema/         # Configuración principal del proyecto Django
├── movies/                 # Aplicación principal
│   ├── templates/          # Plantillas HTML
│   ├── static/             # Archivos estáticos (CSS, JS, imágenes)
│   ├── models.py           # Modelos de la base de datos
│   ├── views.py            # Lógica de las vistas
│   ├── utils.py            # Funciones auxiliares (API de TMDb, etc.)
├── media/                  # Directorio para archivos subidos
├── static/                 # Archivos estáticos generales
├── manage.py               # Herramienta de administración de Django
└── requirements.txt        # Dependencias del proyecto


🖼️ Capturas de Pantalla

🎬 Página Principal

🖥️ Detalle de una Película


🤝 Contribuciones
¡Contribuciones son bienvenidas! 🌟 Si tienes ideas para mejorar el proyecto, sigue estos pasos:

Haz un fork del repositorio.
Crea una rama para tus cambios: git checkout -b feature/mi-mejora.
Haz un commit con tus cambios: git commit -m 'Descripción de mi mejora'.
Haz un push a tu rama: git push origin feature/mi-mejora.
Abre un Pull Request.


🛡️ Licencia
Este proyecto está licenciado bajo la MIT License. 📜

📧 Contacto
Autor: Tu Nombre
LinkedIn: Tu LinkedIn
Twitter: @TuUsuario

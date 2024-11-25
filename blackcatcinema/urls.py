from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include  # Importa include para incluir rutas de otras apps

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('', include('movies.urls')),  # Incluye las rutas de la app "movies"
]

# Configuración para servir archivos estáticos en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

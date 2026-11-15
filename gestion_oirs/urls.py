# gestion_oirs/urls.py (o el archivo urls.py de tu app)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SolicitudOIRSViewSet, crear_solicitud_oirs

router = DefaultRouter()
router.register(r'solicitudes-oirs', SolicitudOIRSViewSet, basename='solicitud-oirs')

urlpatterns = [
    # Ahora el formulario estará en la raíz: http://127.0.0.1:8000/
    path('', crear_solicitud_oirs, name='crear_solicitud_oirs'),
    
    # Rutas de la API REST
    path('api/', include(router.urls)),
]
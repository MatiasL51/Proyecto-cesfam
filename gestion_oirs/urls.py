from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SolicitudOIRSViewSet, crear_solicitud_oirs, listar_solicitudes_admin, probar_conexion_mongo

router = DefaultRouter()
router.register(r'solicitudes-oirs', SolicitudOIRSViewSet, basename='solicitud-oirs')

urlpatterns = [
    # Formulario web público
    path('', crear_solicitud_oirs, name='crear_solicitud_oirs'),
    
    # RUTA CORREGIDA: Cambiamos 'admin/' por 'panel-admin/' para evitar el conflicto
    path('panel-admin/solicitudes/', listar_solicitudes_admin, name='listar_solicitudes_admin'),
    
    # Rutas de la API REST
    path('api/', include(router.urls)),

    # Ruta de la Base De Datos No Relacionales
    path('probar-mongo/', probar_conexion_mongo, name='probar_mongo'),
]
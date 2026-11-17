from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from .models import SolicitudOIRS
from .serializers import SolicitudOIRSSerializer
from .forms import SolicitudOIRSForm
from .mongo_conector import mongo_db


# 1. Vista de la API REST (para la app o administración externa)
class SolicitudOIRSViewSet(viewsets.ModelViewSet):
    queryset = SolicitudOIRS.objects.all().order_by('-fecha_creacion')
    serializer_class = SolicitudOIRSSerializer

    def get_permissions(self):
        """
        Permite crear solicitudes a cualquier usuario, 
        pero restringe la lectura/gestión a administradores.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        
        return [permission() for permission in permission_classes]


# 2. Vista web tradicional (para el formulario HTML en el navegador)
def crear_solicitud_oirs(request):
    if request.method == 'POST':
        form = SolicitudOIRSForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Su solicitud OIRS ha sido enviada exitosamente! Nos pondremos en contacto pronto.')
            return redirect('crear_solicitud_oirs')
    else:
        form = SolicitudOIRSForm()
    
    return render(request, 'formulario_oirs.html', {'form': form})


@staff_member_required
def listar_solicitudes_admin(request):
    # Obtiene todas las solicitudes ordenadas de la más nueva a la más antigua
    solicitudes = SolicitudOIRS.objects.all().order_by('-fecha_creacion')
    return render(request, 'listar_solicitudes.html', {'solicitudes': solicitudes})


# 3. Vista de prueba para la Base de Datos No Relacional (MongoDB)
def probar_conexion_mongo(request):
    """
    Inserta un documento de trazabilidad/auditoría en la nueva colección 
    'logs_auditoria_oirs' de MongoDB desde el backend Django.
    """
    documento_prueba = {
        "origen": "Backend Django 5.2.19 (Unidad 3)",
        "evento": "INGRESO_SOLICITUD_OIRS",
        "folio_relacionado_mysql": 1,
        "establecimiento": "CESFAM Temuco",
        "detalle_operacion": "Validación de persistencia híbrida MySQL + MongoDB",
        "metadatos_cliente": {
            "navegador": request.META.get('HTTP_USER_AGENT', 'Desconocido')[:50],
            "metodo_http": request.method
        }
    }
    
    inserted_id = mongo_db.registrar_evento_implementacion(documento_prueba)
    
    return JsonResponse({
        "status": "success",
        "coleccion": "logs_auditoria_oirs",
        "mensaje": "Documento NoSQL de Unidad 3 guardado exitosamente en MongoDB",
        "mongo_id": inserted_id
    })
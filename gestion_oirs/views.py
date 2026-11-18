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
    Ejecuta pruebas de persistencia híbrida en MongoDB:
    1. Inserción de un registro de auditoría (Camino feliz).
    2. Consulta con filtros inexistentes o valores nulos (Escenario de borde).
    """
    try:
        # 1. Prueba de inserción exitosa (Camino feliz)
        documento_prueba = {
            "establecimiento": "CESFAM Padre Las Casas",
            "evento": "INGRESO_SOLICITUD_OIRS",
            "folio_relacionado_mysql": 1,
            "detalle_operacion": "Validación de persistencia híbrida MySQL + MongoDB",
            "metadatos_cliente": {
                "navegador": request.META.get('HTTP_USER_AGENT', 'Desconocido')[:50],
                "metodo_http": request.method
            }
        }
        
        mongo_id = mongo_db.registrar_log_auditoria(documento_prueba)

        # 2. PRUEBA DE ESCENARIO NEGATIVO / DATOS NULOS
        # Buscamos un folio fantasma o con valor nulo para probar el manejo de vacíos
        resultado_nulo = mongo_db.consultar_log_por_criterio({
            "folio_relacionado_mysql": 99999,
            "calificacion_global": None
        })

        # Respuesta consolidada para el navegador
        respuesta_json = {
            "status": "success",
            "coleccion": "logs_auditoria_oirs",
            "prueba_1_insercion": {
                "mensaje": "Documento NoSQL guardado exitosamente en MongoDB",
                "mongo_id": mongo_id
            },
            "prueba_2_consulta_nula": {
                "descripcion": "Escenario de borde / consulta con datos nulos o inexistentes",
                "resultado": resultado_nulo
            }
        }
        
        return JsonResponse(respuesta_json, json_dumps_params={'ensure_ascii': False, 'indent': 4})

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "mensaje": f"Ocurrió un error en la prueba: {str(e)}"
        }, status=500)
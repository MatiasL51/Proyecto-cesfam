from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from gestion_oirs.models import SolicitudOIRS

class SolicitudOIRSTestCase(TestCase):
    
    def setUp(self):
        """
        Configuración inicial de datos de prueba (fixtures) 
        para los casos de uso de la OIRS del CESFAM.
        """
        self.solicitud_valida = SolicitudOIRS.objects.create(
            nombre="Juan",
            apellido_paterno="Pérez",
            apellido_materno="González",
            rut="12345678-9",
            local_atencion="cesfam_padre_las_casas",
            motivo="reclamo",
            detalle="Demora en la asignación de hora médica con especialista en policlínico.",
            correo_electronico="juan.perez@correo.cl"
        )

    def test_creacion_solicitud_y_calculo_vencimiento(self):
        """
        Caso de Prueba 1: Verifica que al crear una solicitud OIRS se asigne 
        correctamente la fecha de creación y se calcule automáticamente 
        la fecha de vencimiento sumando los días correspondientes (SLA).
        """
        s = self.solicitud_valida
        self.assertIsNotNone(s.pk)
        self.assertEqual(s.rut, "12345678-9")
        self.assertEqual(s.motivo, "reclamo")
        
        # Verificar que la fecha de vencimiento fue calculada y asignada tras el guardado
        self.assertIsNotNone(s.fecha_vencimiento)
        
        # Comprobar que la diferencia aproximada sea de 15 días respecto a la creación
        diferencia = s.fecha_vencimiento - s.fecha_creacion
        self.assertGreaterEqual(diferencia.days, 14) # Margen seguro por horas/minutos

    def test_opciones_choices_validas(self):
        """
        Caso de Prueba 2: Valida que los centros de atención y motivos 
        correspondan exactamente a los establecimientos y normativas definidos.
        """
        s = self.solicitud_valida
        
        # Verificar despliegue correcto mediante los métodos get_FOO_display de Django
        self.assertEqual(s.get_local_atencion_display(), "CESFAM Padre Las Casas")
        self.assertEqual(s.get_motivo_display(), "Reclamo")

    def test_representacion_string_modelo(self):
        """
        Caso de Prueba 3: Comprueba que el método __str__ devuelva 
        el formato esperado para la trazabilidad y logs del sistema.
        """
        s = self.solicitud_valida
        esperado = "12345678-9 - Reclamo (CESFAM Padre Las Casas)"
        self.assertEqual(str(s), esperado)
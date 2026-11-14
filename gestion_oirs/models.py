from django.db import models

class SolicitudOIRS(models.Model):
    LOCAL_CHOICES = [
        ('cesfam_padre_las_casas', 'CESFAM Padre Las Casas'),
        ('cesfam_temuco', 'CESFAM Temuco'),
    ]
    
    MOTIVO_CHOICES = [
        ('informacion', 'Información'),
        ('reclamo', 'Reclamo'),
        ('sugerencia', 'Sugerencia'),
    ]

    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)  # Ejemplo: 12.345.678-9
    local_atencion = models.CharField(max_length=50, choices=LOCAL_CHOICES)
    motivo = models.CharField(max_length=30, choices=MOTIVO_CHOICES)
    detalle = models.TextField(max_length=500)
    correo_electronico = models.EmailField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rut} - {self.get_motivo_display()} ({self.get_local_atencion_display()})"
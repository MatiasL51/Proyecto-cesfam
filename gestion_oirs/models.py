from datetime import timedelta
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
    rut = models.CharField(max_length=12)
    local_atencion = models.CharField(max_length=50, choices=LOCAL_CHOICES)
    motivo = models.CharField(max_length=30, choices=MOTIVO_CHOICES)
    detalle = models.TextField(max_length=500)
    correo_electronico = models.EmailField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # NUEVO CAMPO: Fecha de vencimiento (puede ser nulo inicialmente para registros viejos)
    fecha_vencimiento = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Si el objeto es nuevo y no tiene fecha de vencimiento, le sumamos 15 días
        if not self.pk and not self.fecha_vencimiento:
            # Si ya se asignó fecha_creacion, usamos esa; si no, dejamos que Django la cree y calculamos
            # Nota: auto_now_add se asigna al guardar en BD, por lo que calculamos sumando timedelta al crear
            pass
        super().save(*args, **kwargs)
        
        # Como auto_now_add necesita que el objeto exista para generar la fecha, 
        # asignamos los 15 días justo después del primer guardado si está vacío:
        if not self.fecha_vencimiento:
            self.fecha_vencimiento = self.fecha_creacion + timedelta(days=15)
            # Guardamos solo el campo de vencimiento para evitar bucles
            super().save(update_fields=['fecha_vencimiento'])

    def __str__(self):
        return f"{self.rut} - {self.get_motivo_display()} ({self.get_local_atencion_display()})"
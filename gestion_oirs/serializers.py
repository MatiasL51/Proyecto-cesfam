from rest_framework import serializers
from .models import SolicitudOIRS

class SolicitudOIRSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudOIRS
        fields = [
            'id', 
            'nombre', 
            'apellido_paterno', 
            'apellido_materno', 
            'rut', 
            'local_atencion', 
            'motivo', 
            'detalle', 
            'correo_electronico', 
            'fecha_creacion'
        ]
        read_only_fields = ['id', 'fecha_creacion']

    def validate_detalle(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("El detalle no puede superar los 500 caracteres.")
        return value
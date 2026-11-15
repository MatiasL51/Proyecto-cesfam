from django import forms
from .models import SolicitudOIRS

class SolicitudOIRSForm(forms.ModelForm):
    class Meta:
        model = SolicitudOIRS
        fields = [
            'nombre', 
            'apellido_paterno', 
            'apellido_materno', 
            'rut', 
            'local_atencion', 
            'motivo', 
            'detalle', 
            'correo_electronico'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pérez'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. González'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 12345678-9'}),
            'local_atencion': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Select(attrs={'class': 'form-select'}),
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': '500', 'placeholder': 'Escriba su mensaje aquí (máximo 500 caracteres)...'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        }
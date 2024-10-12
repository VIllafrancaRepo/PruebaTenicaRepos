from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
import re

def validateUser(data, tipo):

    if tipo == 'create':
        required_fields = ["nombre", "apellido_paterno", "apellido_materno", "edad", "email", "telefono"]
        for field in required_fields:
            if field not in data:
                return (1, {"status": status.HTTP_400_BAD_REQUEST, "message": f"El campo '{field}' es obligatorio."})
    
    email = data.get('email')
    if Usuario.objects.filter(email=email).exists():
        return (1, {"status": status.HTTP_400_BAD_REQUEST, "message": "El email ya está en uso por otro usuario."})
    
    telefono = data.get('telefono')
    if not isinstance(telefono, str):
        return (1, {"status": status.HTTP_400_BAD_REQUEST, "message": "El campo 'telefono' debe ser una cadena de texto."})
    
    if not re.match(r'^\d{10}$', telefono):
        return (1, {"status": status.HTTP_400_BAD_REQUEST, "message": "El número de teléfono debe tener exactamente 10 dígitos."})

    
    # Si todas las validaciones pasan, retorna un estado exitoso
    return (0, {"status": status.HTTP_200_OK, "message": "Validación exitosa"})

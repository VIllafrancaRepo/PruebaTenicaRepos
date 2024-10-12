# my_crud/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework.parsers import JSONParser
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from .util import validateUser

class UsuarioVista(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        usuarios = list(Usuario.objects.all())
        ordenar_por = request.data.get('ordenar_por')

        if ordenar_por not in ['edad', 'apellido']:
            return Response({"mensaje": "El parámetro 'ordenar_por' debe ser 'edad' o 'apellido'."}, status=status.HTTP_400_BAD_REQUEST)

        #ordenar usuarios
        def ordenar_usuarios(usuarios, clave):
            n = len(usuarios)
            for i in range(n):
                for j in range(0, n-i-1):
                    if clave(usuarios[j]) > clave(usuarios[j + 1]):
                        # Intercambiar
                        usuarios[j], usuarios[j + 1] = usuarios[j + 1], usuarios[j]

        if ordenar_por == 'edad':
            # Ordenar usuarios por edad (menor a mayor)
            ordenar_usuarios(usuarios, lambda u: u.edad)
        elif ordenar_por == 'apellido':
            # Ordenar usuarios por apellido paterno (alfabéticamente)
            ordenar_usuarios(usuarios, lambda u: u.apellido_paterno)

        
        if usuarios:
            serializer = UsuarioSerializer(usuarios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"mensaje": "No hay usuarios registrados."}, status=status.HTTP_200_OK)


    def post(self, request):
        # Validaciones de informacion
        status_code, validation_response = validateUser(request.data, 'create')
        if status_code == 1:
            return Response(validation_response, status=validation_response["status"])

        data = {
            "nombre": request.data.get('nombre').capitalize(),
            "apellido_paterno": request.data.get('apellido_paterno').capitalize(),
            "apellido_materno": request.data.get('apellido_materno').capitalize(),
            "edad": request.data.get('edad'),
            "email": request.data.get('email'),
            "telefono": request.data.get('telefono')
        }
        
        serializer = UsuarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        
        email = request.data.get('email')

        if not email:
            return Response({"mensaje": "Por favor, proporcione un email."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = Usuario.objects.get(email=email)
            usuario.delete()
            return Response({"mensaje": "Usuario eliminado correctamente."}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({"mensaje": "No se encontró un usuario con ese email."}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        usuario_id = request.data.get('id')
        if not usuario_id:
            return Response({"mensaje": "Por favor, proporcione el ID del usuario a editar."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(id=usuario_id)
            nuevo_email = request.data.get('email')

            # Validaciones de informacion
            status_code, validation_response = validateUser(request.data, 'edit')
            if status_code == 1:
                return Response(validation_response, status=validation_response["status"])


            if nuevo_email and nuevo_email != usuario.email and Usuario.objects.filter(email=nuevo_email).exists():
                return Response({"mensaje": "El email ya está en uso por otro usuario."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Usuario.DoesNotExist:
            return Response({"mensaje": "No se encontró un usuario con ese ID."}, status=status.HTTP_404_NOT_FOUND)

class UsuarioPdfVista(APIView):

    def get(self, request):
        return self.get_pdf(request)

    def get_pdf(self, request):
        # Crear un buffer en memoria
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Agregar título
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 50, "Lista de Usuarios")

        # Obtener todos los usuarios
        usuarios = Usuario.objects.all()

        # titulos
        data = [["Nombre", "Apellido P.", "Apellido M.", "Edad", "Email", "Teléfono"]]

        # Añadir las filas
        for usuario in usuarios:
            data.append([usuario.nombre, usuario.apellido_paterno, usuario.apellido_materno, usuario.edad, usuario.email, usuario.telefono])

        # Ajustar los anchos de las columnas
        table = Table(data, colWidths=[60, 60, 60, 30, 100, 60])

        # Estilo de la tabla con tamaño de letra más pequeño
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),  # tama;o de la letra en titulo
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),  # tama;o letra contendio de la tabla
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),  # padding inferior
            ('TOPPADDING', (0, 1), (-1, -1), 2),  # padding superior
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # lineas de la tabla ancho
        ])
        table.setStyle(style)

        # Obtener las dimensiones de la tabla
        table_width, table_height = table.wrap(0, 0)

        # Ajustar la posición de la tabla en el PDF
        x_position = 50
        y_position = height - 100

        # Dibujar la tabla
        table.drawOn(p, x_position, y_position - table_height)

        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="usuarios.pdf"'
        return response
from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)          
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    edad = models.PositiveIntegerField()
    email = models.EmailField(unique=True)    
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    telefono = models.CharField(max_length=20, blank=True)

    licencia = models.CharField(max_length=30, blank=True)

    foto = models.ImageField(
        upload_to='usuarios/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.usuario.username
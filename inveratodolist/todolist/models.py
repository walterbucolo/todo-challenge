from django.db import models
from django.contrib.auth.models import AbstractUser


class Status(models.IntegerChoices):
    PENDIENTE = 1
    COMPLETADO = 2


class User(AbstractUser):
    pass


class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    date = models.DateTimeField()
    status = models.IntegerField(choices=Status.choices, default=Status.PENDIENTE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

# Create your models here.

class User(AbstractUser):
    is_empresa = models.BooleanField(default = False)
    is_cliente = models.BooleanField(default = False)

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(unique = True, max_length=11)
    nome = models.CharField(max_length=40)
    sobrenome = models.CharField(max_length=100)
    tel = models.CharField(unique = True)
    nascimento = models.DateField()
    email = models.EmailField(unique = True)

class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    razao_social = models.CharField()
    cnpj = models.IntegerField(unique = True)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    email = models.EmailField(unique = True)
    tel = models.CharField(unique = True)
    endereco = models.CharField(max_length=150)
    nome_empresa = models.CharField(max_length=50)
    dom = models.BooleanField(default = False)
    seg = models.BooleanField(default = False)
    ter = models.BooleanField(default = False)
    qua = models.BooleanField(default = False)
    qui = models.BooleanField(default = False)
    sex = models.BooleanField(default = False)
    sab = models.BooleanField(default = False)
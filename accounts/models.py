from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_empresa = models.BooleanField(default = False)
    is_cliente = models.BooleanField(default = False)

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(unique = True, max_length=11)
    nome = models.CharField(max_length=40)
    sobrenome = models.CharField(max_length=100)
    tel = models.CharField(unique = True,max_length=11)
    nascimento = models.DateField()
    email = models.EmailField(unique = True)
    image = models.URLField()

class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    razao_social = models.CharField(max_length= 200)
    cnpj = models.IntegerField(unique = True)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    email = models.EmailField(unique = True)
    tel = models.CharField(unique = True,max_length=11)
    endereco = models.CharField(max_length=150)
    nome_fantasia = models.CharField(max_length=50)
    image = models.URLField()
    dom = models.BooleanField(default = False)
    seg = models.BooleanField(default = False)
    ter = models.BooleanField(default = False)
    qua = models.BooleanField(default = False)
    qui = models.BooleanField(default = False)
    sex = models.BooleanField(default = False)
    sab = models.BooleanField(default = False)
    desc = models.CharField(max_length=200, default='')

class Tags(models.Model):
    name = models.CharField(max_length=250)
    empresa = models.ManyToManyField(Empresa)
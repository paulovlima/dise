from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_empresa = models.BooleanField(default = False)
    is_cliente = models.BooleanField(default = False)

class Tags(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return '#{}'.format(self.name)

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(unique = True, max_length=11)
    nome = models.CharField(max_length=40)
    sobrenome = models.CharField(max_length=100)
    tel = models.CharField(unique = True,max_length=11)
    nascimento = models.DateField()
    email = models.EmailField(unique = True)
    image = models.URLField()

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    razao_social = models.CharField(max_length= 200)
    cnpj = models.CharField(max_length=14,unique = True)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    email = models.EmailField(unique = True)
    tel = models.CharField(unique = True,max_length=11)
    endereco = models.CharField(max_length=150)
    nome_fantasia = models.CharField(max_length=50)
    image = models.URLField()
    dom = models.BooleanField(default = False, blank= True)
    seg = models.BooleanField(default = False, blank= True)
    ter = models.BooleanField(default = False, blank= True)
    qua = models.BooleanField(default = False, blank= True)
    qui = models.BooleanField(default = False, blank= True)
    sex = models.BooleanField(default = False, blank= True)
    sab = models.BooleanField(default = False, blank= True)
    desc = models.CharField(max_length=200, default='')
    tags = models.ManyToManyField(Tags)
    
    def __str__(self):
        return f"{self.nome_fantasia}"
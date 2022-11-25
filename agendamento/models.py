from django.db import models
from accounts.models import User, Cliente, Empresa
from django.conf import settings
from datetime import date
# Create your models here.

class Servico(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    data_agendada = models.DateField(default=date.today())
    hora_agendada = models.TimeField()
    endereco_agendado = models.CharField(max_length = 200)
    status = models.CharField(max_length = 200)
    desc = models.CharField(max_length= 500,default='')

    def __str__(self):
        return f'Serviço de {self.empresa} para {self.cliente}'
        
class Pagamento(models.Model):
    valor_pagar = models.DecimalField(max_digits=6,decimal_places=2, default=0)
    servico = models.OneToOneField(Servico, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    status = models.CharField(max_length = 200)

class CommentCliente(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.DecimalField(max_digits=2,decimal_places=1,default=5)
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)

class CommentEmpresa(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.DecimalField(max_digits=2,decimal_places=1,default=5)
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
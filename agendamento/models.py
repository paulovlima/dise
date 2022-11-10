from django.db import models
from ..agendamento.models import User, Cliente, Empresa
# Create your models here.

class Servico(models.Model):
    orcamento = models.DecimalField(decimal_places=2, default=0)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    hora_agendada = models.DateTimeField()
    endereco_agendado = models.CharField(max_length = 200)
    status = models.CharField()

class Pagamento(models.Model):
    valor_pagar = models.DecimalField(decimal_places=2, default=0)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    status = models.CharField()
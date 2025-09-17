from django.db import models

# Create your models here.
class Despesa(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=60)
    descricao = models.TextField(null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - R$ {self.valor}"

from django.db import models

# Create your models here.
class Despesa(models.Model):
    FREQUENCIA_CHOICES = [
        ('D', 'Diária'), 
        ('S', 'Semanal'),
        ('M', 'Mensal'),
        ('SM', 'Semestral'),
        ('A', 'Anual'),         
    ]

    TIPO_CHOICES = [
        ('GF', 'Gasto Formiga'),
        ('FX', 'Fixa'),
        ('V', 'Variável'),
        ('I', 'Investimento'),
    ]

    nome = models.CharField(max_length=100, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    frequencia = models.CharField(max_length=2, choices=FREQUENCIA_CHOICES, default='M')
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='V')
    data_pagamento = models.DateField(null=True, blank=True)
    pago = models.BooleanField(default=False)
    

    def __str__(self):
        return self.nome

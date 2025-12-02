from django.db import models
from django.conf import settings
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

LIMITE_MINIMO_DATA = date(2000,1,1)

class Despesa(models.Model):
    MES_CHOICES = [
        ('01', 'Janeiro'),
        ('02', 'Fevereiro'),
        ('03', 'Março'),
        ('04', 'Abril'),
        ('05', 'Maio'),
        ('06', 'Junho'),
        ('07', 'Julho'),
        ('08', 'Agosto'),
        ('09', 'Setembro'),
        ('10', 'Outubro'),
        ('11', 'Novembro'),
        ('12', 'Dezembro'),
    ]

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

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='despesas',
        null=True,
        blank=True,
    )

    mes = models.CharField(
        max_length=60,
        choices=MES_CHOICES,
        verbose_name='Mês'
    )

    nome = models.CharField(
        'Nome da despesa',
        max_length=100,
        null=True,
        blank=True
    )

    valor = models.DecimalField(
        'Valor',
        max_digits=10,
        decimal_places=2
    )

    frequencia = models.CharField(
        'Frequência',
        max_length=2,
        choices=FREQUENCIA_CHOICES,
        default='M'
    )

    tipo = models.CharField(
        'Tipo',
        max_length=2,
        choices=TIPO_CHOICES,
        default='V'
    )

    data_vencimento = models.DateField(
        'Data de vencimento',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(LIMITE_MINIMO_DATA),
            MaxValueValidator(date.today),
        ]
    )

    data_pagamento = models.DateField(
        'Data de pagamento',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(LIMITE_MINIMO_DATA),
            MaxValueValidator(date.today),
        ]
    )

    pago = models.BooleanField(
        'Pago?',
        default=False
    )

    def __str__(self):
        return f"{self.nome or 'Despesa sem nome'} - {self.get_mes_display()}"

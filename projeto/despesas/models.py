from django.db import models

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
        blank=True
    )

    data_pagamento = models.DateField(
        'Data de pagamento',
        null=True,
        blank=True
    )

    pago = models.BooleanField(
        'Pago?',
        default=False
    )

    def __str__(self):
        return f"{self.nome or 'Despesa sem nome'} - {self.get_mes_display()}"

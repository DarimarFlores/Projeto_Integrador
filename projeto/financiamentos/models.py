from django.db import models
from django.conf import settings
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

LIMITE_MINIMO_DATA = date(2000,1,1)


class Financiamento(models.Model):
    MES_CHOICES = [
        ('01', 'Janeiro'), ('02', 'Fevereiro'), ('03', 'Março'),
        ('04', 'Abril'), ('05', 'Maio'), ('06', 'Junho'),
        ('07', 'Julho'), ('08', 'Agosto'), ('09', 'Setembro'),
        ('10', 'Outubro'), ('11', 'Novembro'), ('12', 'Dezembro'),
    ]

    TIPO_CHOICES = [
        ('EMP', 'Empréstimo Pessoal'),
        ('CAR', 'Financiamento de Carro'),
        ('CASA', 'Financiamento Imobiliário'),
        ('CARTAO', 'Cartão de Crédito'),
        ('OUTRO', 'Outro'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='financiamentos',
        null=True,
        blank=True,
    )


    mes = models.CharField(max_length=60, choices=MES_CHOICES, verbose_name='Mês')
    credor = models.CharField(max_length=100, verbose_name='Credor')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='OUTRO', verbose_name='Tipo')      
    
    # valores
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor da Parcela', null=True, blank=True)    
        
    # datas
    data_vencimento= models.DateField(
        'Data de vencimento',
        null=True,
        blank=True, 
        validators=[
            MinValueValidator(LIMITE_MINIMO_DATA),
            MaxValueValidator(date.today),
        ]
    )

    data_pagamento= models.DateField(
        'Data de pagamento',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(LIMITE_MINIMO_DATA),
            MaxValueValidator(date.today),
        ]
    )
    
    pago = models.BooleanField(default=False, verbose_name='Pago')

    def clean(self):
        super().clean()

        # só valida se os dois campos estiverem preenchidos
        if self.mes:
            mes_do_registro = int(self.mes)

            # validar data de vencimento
            if self.data_vencimento:
                mes_da_data_vencimento = self.data_vencimento.month
                ano_da_data_vencimento = self.data_vencimento.year

                # validar mês
                if mes_da_data_vencimento != mes_do_registro:
                    raise ValidationError({
                        'data_vencimento': 'A data de vencimento deve ser do mês selecionado.'
                    })
                
                # bloquear ano futuro
                ano_atual = date.today().year
                if ano_da_data_vencimento > ano_atual:
                    raise ValidationError({
                        'data_vencimento': 'A data de vencimento não pode ser de um ano futuro.'
                    })

    def __str__(self):
        return f"{self.credor} - {self.get_tipo_display()} ({self.get_mes_display()})"
from django.db import models

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

    mes = models.CharField(max_length=60, choices=MES_CHOICES, verbose_name='Mês')
    credor = models.CharField(max_length=100, verbose_name='Credor')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='OUTRO', verbose_name='Tipo')      
    
    # valores
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor da Parcela', null=True, blank=True)    
        
    # datas
    data_inicio = models.DateField(verbose_name='Data de Início', null=True, blank=True)
    data_fim = models.DateField(verbose_name='Data de Término', null=True, blank=True)
    data_vencimento= models.DateField(verbose_name='Vencimento da parcela', null=True, blank=True)
    
    pago = models.BooleanField(default=False, verbose_name='Pago')

    def __str__(self):
        return f"{self.credor} - {self.get_tipo_display()} ({self.get_mes_display()})"
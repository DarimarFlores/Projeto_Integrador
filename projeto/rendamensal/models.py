from django.db import models
from django.utils import timezone

# Create your models here.
class Renda(models.Model):
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

    TIPO_CHOICES = [
        ('S', 'Salário'),
        ('F', 'Férias'),
        ('D', 'Décimo Terceiro'),
        ('RE', 'Renda Extra'),
        ('O', 'Outras'),
    ]

    mes = models.CharField('Mês', max_length=60, choices=MES_CHOICES) 
    tipo = models.CharField('Tipo de renda', max_length=2, choices=TIPO_CHOICES, default='S')
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)    
    data_recebimento = models.DateField('Data de recebimento', default=timezone.now)

    def __str__(self):        
        return f"{self.get_mes_display()} - {self.get_tipo_display()} - R$ {self.valor}"


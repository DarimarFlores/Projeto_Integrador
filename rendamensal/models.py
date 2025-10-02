from django.db import models
import datetime

# Create your models here.
class Renda(models.Model):
    TIPO_RENDA_CHOICES = [
    ('S', 'Salário'),
    ('F', 'Férias'),
    ('D', 'Décimo Terceiro'),
    ('RE', 'Renda extar'),
    ('O', 'Outras'),
    ]    

    mes = models.CharField(max_length=60, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=2, choices=TIPO_RENDA_CHOICES, default='S')
    data_recebimento = models.DateField(default=datetime.date.today)
    

    def __str__(self):
        return f"{self.mes or 'Sem mês'} ({self.get_tipo_display()}) - {self.valor}"


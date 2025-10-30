from django.db import models

# Create your models here.
class Renda(models.Model):

    TIPO_CHOICES = [
        ('S', 'Salario'),
        ('F', 'Férias'),
        ('D', 'Décimo Terceiro'),
        ('RE', 'Renda Extra'),
        ('O', 'Outras'),
    ]
    mes = models.CharField(max_length=60, null=True, blank=True)
    nome = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default= 'S')
    valor = models.DecimalField(max_digits=10, decimal_places=2)    
    data_recebimento = models.DateField()
    
    def __str__(self):
        return f"{self.mes} - {self.nome} - R$ {self.valor}"


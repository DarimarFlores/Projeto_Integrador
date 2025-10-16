from django.db import models

# Create your models here.
class Renda(models.Model):
    mes = models.CharField(max_length=60, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.mes


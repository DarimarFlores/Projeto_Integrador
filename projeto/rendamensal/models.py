from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

LIMITE_MINIMO_DATA = date(2000,1,1)

class Renda(models.Model):
    MES_CHOICES = [
        ('01', 'Janeiro'), ('02', 'Fevereiro'), ('03', 'Março'),
        ('04', 'Abril'), ('05', 'Maio'), ('06', 'Junho'),
        ('07', 'Julho'), ('08', 'Agosto'), ('09', 'Setembro'),
        ('10', 'Outubro'), ('11', 'Novembro'), ('12', 'Dezembro'),
    ]

    TIPO_CHOICES = [
        ('S', 'Salário'),
        ('F', 'Férias'),
        ('D', 'Décimo Terceiro'),
        ('RE', 'Renda Extra'),
        ('O', 'Outras'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rendas',
        null=True,
        blank=True,
    )

    mes = models.CharField(
        max_length=60,
        choices=MES_CHOICES,
        verbose_name='Mês'
    ) 

    tipo = models.CharField(
        'Tipo de renda',
        max_length=2,
        choices=TIPO_CHOICES,
        default='S'
    )

    valor = models.DecimalField(
        'Valor',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    data_recebimento = models.DateField(
        'Data de recebimento',
        default=timezone.now,
        validators=[
            MinValueValidator(LIMITE_MINIMO_DATA),
            MaxValueValidator(date.today),
        ]
    )

    def clean(self):
        # chama a validação padrão de django
        super().clean()

        # só valida se a data_recebimento estiver preenchido
        if self.mes and self.data_recebimento:
            mes_do_registro = int(self.mes)
            mes_recebimento = self.data_recebimento.month
            ano_recebimento = self.data_recebimento.year
            ano_atual = date.today().year

            # validar mês
            if mes_recebimento != mes_do_registro:
                raise ValidationError({
                    'data_recebimento':'A data de recebimento deve ser do mês selecionado.'
                })
            
            # validar o ano
            if ano_recebimento != ano_atual:
                raise ValidationError({
                    'data_recebimento': 'A data de recebimento deve ser do ano atual.'
                })    

    def __str__(self):        
        return f"{self.get_mes_display()} - {self.get_tipo_display()} - R$ {self.valor}"


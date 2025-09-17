from django import forms
from .models import Despesa

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields =['nome','valor','categoria','descricao','data_pagamento','pago']
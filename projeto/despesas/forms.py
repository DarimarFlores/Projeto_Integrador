from django import forms
from .models import Despesa

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields =['nome','valor','frequencia','tipo','data_pagamento','pago']
        widgets = {
            'data_pagamento': forms.DateInput(attrs={'type':'date'}),
        }
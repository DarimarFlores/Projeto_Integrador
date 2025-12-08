from django import forms
from .models import Despesa

class DespesaForm(forms.ModelForm):   
    class Meta:
        model = Despesa
        fields = [
            'mes',
            'nome',
            'valor',
            'frequencia',
            'tipo',
            'data_vencimento',
            'data_pagamento',
            'pago',
        ]

        widgets = {
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

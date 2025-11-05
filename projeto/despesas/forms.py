from django import forms
from .models import Despesa

class DespesaForm(forms.ModelForm):
    # Campos de data com formato compatível com <input type="date">
    data_vencimento = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d'],
    )

    data_pagamento = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d'],
    )

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
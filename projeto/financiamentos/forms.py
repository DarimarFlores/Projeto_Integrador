from django import forms
from .models import Financiamento

class FinanciamentoForm(forms.ModelForm):
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d'],
    )

    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Financiamento
        fields = [
            'mes',
            'credor',
            'tipo',
            'valor_total',
            'numero_parcelas',
            'valor_parcela',
            'taxa_juros',
            'data_inicio',
            'data_fim',
            'pago',
        ]
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_fim': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_inicio'].input_formats = ['%Y-%m-%d']
        self.fields['data_fim'].input_formats = ['%Y-%m-%d']
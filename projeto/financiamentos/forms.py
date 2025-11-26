from django import forms
from .models import Financiamento

class FinanciamentoForm(forms.ModelForm):
    data_vencimento = forms.DateField(
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
            'valor_parcela',                                  
            'data_vencimento',
            'pago',
        ]
        widgets = {
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_vencimento'].input_formats = ['%Y-%m-%d']
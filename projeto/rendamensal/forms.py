from django import forms
from .models import Renda

class RendaForm(forms.ModelForm):
    data_recebimento = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Renda
        fields = ['mes', 'tipo', 'valor', 'data_recebimento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_recebimento'].input_formats = ['%Y-%m-%d']

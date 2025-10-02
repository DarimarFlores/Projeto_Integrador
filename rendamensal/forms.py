from django import forms
from .models import Renda

class RendaForm(forms.ModelForm):
    class Meta:
        model = Renda
        fields = ['mes','valor', 'tipo', 'data_recebimento']
        widgets = {
            'data_recebimento': forms.DateInput(attrs={'type': 'date'}),
        }

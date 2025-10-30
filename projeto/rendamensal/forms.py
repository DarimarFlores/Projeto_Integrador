from django import forms
from .models import Renda

class RendaForm(forms.ModelForm):
    class Meta:
        model = Renda
        fields = '__all__'
        widgets = {
            'data_recebimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
    
    def __init_(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_recibimento'].input_formats = ['%Y-%m-%d']

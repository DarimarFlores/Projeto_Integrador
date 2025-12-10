from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
import re

class CadastroForm (UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nome de usuário',
            'password1': 'Senha',
            'password2': 'Confirme a senha',
        }

    # validar nome de usuário único
    def clean_username(self):
        username = self.cleaned_data.get("username")
        
        if not username:
            raise forms.ValidationError("Escreva um nome de usuário")
        
        # verifica se já existe algum usuário com esse username
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Esse nome de usuário já está sendo usado.")
        return username

    # validar email único
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            raise forms.ValidationError("Escreva um e-mail válido.")
        
        # verifica se existe algum usuário com esse mesmo email
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe um usuário com este e-mail.")
        return email

    
    def clean_password1(self):
        senha = self.cleaned_data.get("password1") 

        if not senha:
            raise forms.ValidationError("Digite uma senha válida.")

        # a senha deve ter mínimo 8 caracteres
        if len(senha) < 8:
            raise forms.ValidationError("A senha deve conter pelo menos 8 caracteres.")
        
        # a senha deve ter pelo menos uma letra maiúscula
        if not re.search(r"[A-Z]", senha):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
        
        # a senha deve ter pelo menos uma letra minúscula
        if not re.search(r"[a-z]", senha):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra minúscula.")
        
        # a senha deve ter pelo menos um número
        if not re.search(r"\d", senha):
            raise forms.ValidationError("A senha deve conter pelo um número.")

        # a senha deve ter pelo um caracter especial
        if not re.search(r"[@$!%*#?&.,;:_+=-]", senha):
            raise forms.ValidationError("A senha deve conter pelo menos um caracter especial (@, #, !, $, %, etc.).")
        
        validate_password(senha)
    
        return senha




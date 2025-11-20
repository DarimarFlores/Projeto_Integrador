from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as auth_logout, login
from .forms import CadastroForm
from django.contrib.auth.models import User
import math 
import secrets
import string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required

class LoginCustomView(LoginView):
    template_name = 'contas/login.html'
    redirect_authenticated_user = True    # se ja estiver logado manda para o inicio
    
# cadastro de usuário
def registrar(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()           
            return redirect('contas:login')
    else:
        form = CadastroForm()
    return render(request, 'contas/cadastro_usuario.html', {'form': form})

def logout_view(request):
    auth_logout(request)  
    return redirect('contas:login')

def gerar_senha_temporaria(tamanho=8):
    #letras + números
    alfabeto = string.ascii_letters + string.digits
    senha = ''.join(secrets.choice(alfabeto) for _ in range (tamanho -2))
    # garante pelo menos 1 maiúscula e 1 caracter espacial
    senha += 'A!'
    return senha

def esqueci_senha(request):
    nova_senha = None
    erro = None

    if  request.method == 'POST':
        identificador = request.POST.get('identificador', '').strip()

        if not identificador:
            erro = 'Informe seu nome de usuário ou e-mail.'
        else:
            try:
                # se tiver @ procura por e-mail senão por username
                if '@' in identificador:
                    user = User.objects.get(email__iexact=identificador)
                else:
                    user = User.objects.get(username__iexact=identificador)

                nova_senha = get_random_string(10)
                user.set_password(nova_senha)
                user.save()

                # Loga o usuário com a senha nova temporária
                login(request, user)

                messages.info(
                request,
                f"Sua senha temporária é: {nova_senha}. "
                "Use-a como senha atual e em seguida defina uma nova senha pessoal."
                )

                # manda direto para a tela de trocar senha
                return redirect('contas:trocar_senha')

            except User.DoesNotExist:
                erro = 'Usuário ou e-mail não encontrado.'

    contexto = {
        'nova_senha': nova_senha,
        'erro': erro,
    }

    return render(request, 'contas/esqueci_senha.html', contexto)

@login_required
def trocar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('inicio')

    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'contas/trocar_senha.html', {'form':form})

    
   


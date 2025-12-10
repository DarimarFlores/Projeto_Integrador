from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import secrets
import string
from .forms import CadastroForm


class LoginCustomView(LoginView):
    template_name = 'contas/login.html'
    redirect_authenticated_user = False  # # sempre mostra a tela de login


# ---------- CADASTRO ----------
def registrar(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()

            # não fica logado depois do cadastro
            logout(request)

            # mensaagem que aparece na tela do login
            messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
            return redirect('contas:login')
    else:
        form = CadastroForm()

    return render(request, 'contas/cadastro_usuario.html', {'form': form})


# ---------- LOGOUT ----------
def logout_view(request):
    # limpa a flag de senha temporária (se existir)
    request.session.pop('senha_temporaria', None)
    logout(request)
    return redirect('contas:login')


# ---------- GERAR SENHA TEMPORÁRIA ----------
def gerar_senha_temporaria(tamanho=10):
    # letras + números
    alfabeto = string.ascii_letters + string.digits
    senha_base = ''.join(secrets.choice(alfabeto) for _ in range(tamanho - 2))
    # garante pelo menos 1 maiúscula e 1 caractere especial
    senha = senha_base + 'A!'
    return senha


# ---------- ESQUECI SENHA ----------
def esqueci_senha(request):
    nova_senha = None
    erro = None

    if request.method == 'POST':
        identificador = request.POST.get('identificador', '').strip()

        if not identificador:
            erro = 'Informe seu nome de usuário ou e-mail.'
        else:
            try:
                # se tiver @ procura por e-mail, senão por username
                if '@' in identificador:
                    user = User.objects.get(email__iexact=identificador)
                else:
                    user = User.objects.get(username__iexact=identificador)

                # gera senha temporária forte
                nova_senha = gerar_senha_temporaria()
                user.set_password(nova_senha)
                user.save()

                # NÃO loga o usuário aqui
                # NÃO coloca nada na sessão

                messages.info(
                    request,
                    "Senha temporária gerada com sucesso. "
                    "Use essa senha para fazer login e depois troque por uma senha definitiva."
                )

                # em vez de redirecionar, vamos renderizar a mesma página
                # para mostrar a senha no card (nova_senha)
                # return redirect('contas:login')  # se quiser, pode usar isso e tirar o card do template

            except User.DoesNotExist:
                erro = 'Usuário ou e-mail não encontrado.'

    contexto = {
        'nova_senha': nova_senha,
        'erro': erro,
    }
    return render(request, 'contas/esqueci_senha.html', contexto)


# ---------- TROCAR SENHA ----------
@login_required
def trocar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # mantém o usuário logado depois de trocar a senha
            update_session_auth_hash(request, user)

            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('inicio')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'contas/trocar_senha.html', {'form': form})



    
   


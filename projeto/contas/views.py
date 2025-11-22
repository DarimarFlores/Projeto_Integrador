from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import secrets
import string
from .forms import CadastroForm


class LoginCustomView(LoginView):
    template_name = 'contas/login.html'
    redirect_authenticated_user = True  # se já estiver logado, manda pro início


# ---------- CADASTRO ----------
def registrar(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
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

                # loga o usuário com a senha temporária
                login(request, user)

                # marca na sessão que essa senha é temporária
                request.session['senha_temporaria'] = True

                messages.info(
                    request,
                    f"Sua senha temporária é: {nova_senha}. "
                    "Use-a para acessar agora e em seguida defina uma nova senha."
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


# ---------- TROCAR SENHA ----------
@login_required
def trocar_senha(request):
    # se o usuário estiver usando senha temporaria o sistema usa SetPasswordForm, caso contrário usa PasswordChangeForm
    usando_senha_temporaria = bool(request.session.get('senha_temporaria'))
    
    # escolhe qual formulário usar
    if usando_senha_temporaria:
        FormClass = SetPasswordForm
    else:
        FormClass = PasswordChangeForm

    if request.method == 'POST':
        form = FormClass(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # mantém o usuário logado depois de trocar a senha
            update_session_auth_hash(request, user)

            # se era senha temporaria remove a flag de senha temporária
            if usando_senha_temporaria:
                request.session.pop('senha_temporaria', None)

            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('inicio')
    else:
        form = FormClass(request.user)

    return render(request, 'contas/trocar_senha.html', {'form': form})


    
   


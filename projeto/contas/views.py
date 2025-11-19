from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as auth_logout
from .forms import CadastroForm

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
    
   


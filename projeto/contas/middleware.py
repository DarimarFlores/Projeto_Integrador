from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class ForcarTrocaSenhaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        caminho_atual = request.path  # URL atual

        #  libera arquivos estáticos (CSS, JS, imagens)
        if caminho_atual.startswith(settings.STATIC_URL):
            return self.get_response(request)

        # se o usuário não estiver logado, não precisa forçar troca de senha
        if not request.user.is_authenticated:
            return self.get_response(request)

        # se estiver com senha temporária, restringe o acesso
        if request.session.get('senha_temporaria'):

            # urls que o usuário pode acessar mesmo com senha temporária
            urls_permitidas = [
                reverse('contas:trocar_senha'),
                reverse('contas:login'),
                reverse('contas:esqueci_senha'),
                reverse('contas:logout'),  
            ]

            # se tentar acessar qualquer outra URL, bloqueia
            if not any(caminho_atual.startswith(url) for url in urls_permitidas):
                return redirect('contas:trocar_senha')

        # se estiver tudo certo, segue o fluxo normal
        return self.get_response(request)
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .forms import RendaForm
from .models import Renda


# Create your views here.
def cadastroRenda(request):
    mes_param = request.GET.get('mes')          # None, '', ou '01'...'12'
    mes_corrente = date.today().strftime('%m')  # mês atual do sistema

    if mes_param:
        # Quando um mês foi escolhido no filtro
        rendas = Renda.objects.filter(mes=mes_param).order_by('data_recebimento')
        total_mes = rendas.aggregate(total=Sum('valor'))['total'] or 0
        mostrar_total_mes = True
    else:
        # Quando o filtro está em "Todos os meses" (ou sem parâmetro)
        rendas = Renda.objects.all().order_by('mes', 'data_recebimento')
        total_mes = None
        mostrar_total_mes = False

    # Botões só aparecem quando está vendo o mês atual
    mostrar_botoes = bool(mes_param and mes_param == mes_corrente)

    contexto = {
        'rendas': rendas,
        'meses': Renda.MES_CHOICES,
        'mes_atual': mes_param,           # valor selecionado no filtro
        'total_mes_atual': total_mes,     # total do mês escolhido
        'mostrar_total_mes': mostrar_total_mes,
        'mostrar_botoes': mostrar_botoes,
    }

    return render(request, 'rendamensal/cadastro_renda.html', contexto)

def nova_renda(request):
    mes_param = request.GET.get('mes')  # opcional, pra voltar pro mesmo mês depois

    if request.method == 'POST':
        form = RendaForm(request.POST)
        if form.is_valid():
            renda = form.save()
            # depois de salvar, volta pra lista filtrada pelo mês da renda
            redirect_mes = renda.mes or mes_param
            if redirect_mes:
                return redirect(f'/rendamensal/?mes={redirect_mes}')
            return redirect('rendamensal:cadastro_renda')
    else:
        # se vier ?mes=02 na URL, já deixa o campo "mes" preenchido
        initial = {'mes': mes_param} if mes_param else None
        form = RendaForm(initial=initial)

    return render(request, 'rendamensal/nova_renda.html', {'form': form})

def editar_renda(request, id):
    renda = get_object_or_404(Renda, id=id)

    # Descobre o mês dessa renda para voltar para o mesmo filtro depois
    mes_param = renda.mes or date.today().strftime('%m')

    if request.method == 'POST':
        form = RendaForm(request.POST, instance=renda)
        if form.is_valid():
            form.save()
            return redirect(f'/rendamensal/?mes={mes_param}')
    else:
        form = RendaForm(instance=renda)

    return render(request, 'rendamensal/editar_renda.html', {'form': form, 'renda': renda})

def remover_renda(request, id):
    renda = get_object_or_404(Renda, id=id)
    mes_param = renda.mes or date.today().strftime('%m')
    renda.delete()
    return redirect(f'/rendamensal/?mes={mes_param}')
#prova do que gitignore esta funcionando
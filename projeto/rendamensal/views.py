from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

from .forms import RendaForm
from .models import Renda
from django.contrib.auth.decorators import login_required

@login_required


# Create your views here.
def cadastroRenda(request):
    mes_param = request.GET.get('mes')          # None, '', ou '01'...'12'
    mes_corrente = date.today().strftime('%m')  # mês atual do sistema

    # decidir que mês usar como filtro
    if mes_param is None:
        # filtra pelo mês atual
        mes_filtro = mes_corrente
    elif mes_param == '':
        # usuário escolheu todos os meses
        mes_filtro = None
    else:
        mes_filtro = mes_param

    rendas_qs = Renda.objects.all()

    # filtro por mês
    if mes_filtro:
        rendas_qs = rendas_qs.filter(mes=mes_filtro)
    
    # ordenando
    if mes_filtro:
        rendas = rendas_qs.order_by('data_recebimento')
    else:
        rendas = rendas_qs.order_by('mes', 'data_recebimento')
    
    # total do mês
    if mes_filtro:
        total_mes = rendas_qs.aggregate(total=Sum('valor'))['total'] or 0
        mostrar_total_mes= True
    else:
        total_mes = None
        mostrar_total_mes = False 

    # botões editar e remover só aparecem no mês atual 
    mostrar_botoes = bool(mes_filtro and mes_filtro == mes_corrente)

    mes_para_template = mes_param if mes_param is not None else mes_corrente
       

    contexto = {
        'rendas': rendas,
        'meses': Renda.MES_CHOICES,
        'mes_atual': mes_para_template,           # valor selecionado no filtro
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
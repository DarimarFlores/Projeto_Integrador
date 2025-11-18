from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

from .models import Financiamento
from .forms import FinanciamentoForm
from django.contrib.auth.decorators import login_required

@login_required

def lista_financiamentos(request):    
    mes_param = request.GET.get('mes')
    status_param = request.GET.get('status')
    mes_corrente = date.today().strftime('%m')

    # iniciar app com mês atual    
    if mes_param is None:
        mes_filtro = mes_corrente
    elif mes_param == '':
        mes_filtro = None
    else:
        # usuário escolhe um mês específico
        mes_filtro = mes_param
    
    financ_qs = Financiamento.objects.all()

    # filtro por mês
    if mes_filtro:
        financ_qs = financ_qs.filter(mes=mes_filtro)
    
    # filtro por status
    if status_param == 'pago':
        financ_qs = financ_qs.filter(pago=True)
    elif status_param == 'pendente':
        financ_qs = financ_qs.filter(pago=False)
    
    # ordenando
    if mes_filtro:
        financiamentos = financ_qs.order_by('data_vencimento', 'credor')
    else:
        financiamentos =financ_qs.order_by('mes', 'data_vencimento', 'credor')

    # total do mês
    total_mes = financ_qs.aggregate(total=Sum('valor_parcela'))['total'] or None
  

    # botões só aparecem no mês atual
    mostrar_botoes = bool(mes_filtro and mes_filtro == mes_corrente)
    
    # valor que o template usa para marcar o select
    mes_para_template = mes_param if mes_param is not None else mes_corrente
    
    contexto = {
        'financiamentos': financiamentos,
        'meses': Financiamento.MES_CHOICES,
        'mes': mes_para_template,
        'status': status_param,
        'total_mes': total_mes,
        'mostrar_botoes': mostrar_botoes,
        'mes_atual': mes_corrente,
    }
    return render(request, 'financiamentos/lista_financiamentos.html', contexto)

def novo_financiamento(request):
    mes_param = request.GET.get('mes', date.today().strftime('%m'))

    if request.method == 'POST':
        form = FinanciamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/financiamentos/?mes={mes_param}')
    else:
        form = FinanciamentoForm()

    return render(request, 'financiamentos/novo_financiamento.html', {'form': form, 'meses': Financiamento.MES_CHOICES})


def editar_financiamento(request, id):
    financiamento = get_object_or_404(Financiamento, id=id)
    mes_param = financiamento.mes or date.today().strftime('%m')

    if request.method == 'POST':
        form = FinanciamentoForm(request.POST, instance=financiamento)
        if form.is_valid():
            form.save()
            return redirect(f'/financiamentos/?mes={mes_param}')
    else:
        form = FinanciamentoForm(instance=financiamento)

    return render(request, 'financiamentos/editar_financiamento.html', {'form': form, 'financiamento': financiamento})


def remover_financiamento(request, id):
    financiamento = get_object_or_404(Financiamento, id=id)
    mes_param = financiamento.mes or date.today().strftime('%m')
    financiamento.delete()
    return redirect(f'/financiamentos/?mes={mes_param}')
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
    
    # financiamentos do usuário logado
    financ_qs = Financiamento.objects.filter(usuario=request.user)

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

@login_required
def novo_financiamento(request):
    mes_param = request.GET.get('mes', date.today().strftime('%m'))

    if request.method == 'POST':
        form = FinanciamentoForm(request.POST)
        if form.is_valid():
            financiamento = form.save(commit=False)
            financiamento.usuario = request.user
            financiamento.save()

            redirect_mes = financiamento.mes or mes_param
            if redirect_mes:
                # volta para o mês do financiamento ou pro filtro da URL
                return redirect(f'/financiamentos/?mes={redirect_mes}')
            return redirect('financiamentos:lista_financiamentos')
    else:
        initial = {'mes': mes_param} if mes_param else None
        form = FinanciamentoForm(initial=initial)

    return render(request, 'financiamentos/novo_financiamento.html', {'form': form, 'meses': Financiamento.MES_CHOICES})

@login_required
def editar_financiamento(request, id):
    financiamento = get_object_or_404(Financiamento, id=id, usuario=request.user)
    mes_param = financiamento.mes or date.today().strftime('%m')

    if request.method == 'POST':
        form = FinanciamentoForm(request.POST, instance=financiamento)
        if form.is_valid():
            financiamento = form.save()
            redirect_mes = financiamento.mes or mes_param
            return redirect(f'/financiamentos/?mes={redirect_mes}')
    else:
        form = FinanciamentoForm(instance=financiamento)

    return render(request, 'financiamentos/editar_financiamento.html', {'form': form, 'financiamento': financiamento})

@login_required
def remover_financiamento(request, id):
    financiamento = get_object_or_404(Financiamento, id=id, usuario=request.user)
    mes_param = financiamento.mes or date.today().strftime('%m')
    financiamento.delete()
    return redirect(f'/financiamentos/?mes={mes_param}')
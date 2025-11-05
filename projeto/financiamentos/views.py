from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Financiamento
from .forms import FinanciamentoForm

def lista_financiamentos(request):    
    mes_param = request.GET.get('mes')
    
    if mes_param:
        financiamentos = Financiamento.objects.filter(mes=mes_param).order_by('data_inicio')
    else:
        financiamentos = Financiamento.objects.all().order_by('mes', 'data_inicio')

    total_mes_atual = financiamentos.aggregate(total_mes=Sum('valor_total'))['total_mes'] or 0

    totais_por_mes = (
        Financiamento.objects
        .values('mes')
        .annotate(total_mes=Sum('valor_total'))
        .order_by('mes')
    )

    contexto = {
        'financiamentos': financiamentos,
        'meses': Financiamento.MES_CHOICES,
        'mes_atual': mes_param,           # pode ser None
        'total_mes_atual': total_mes_atual,
        'totais_por_mes': totais_por_mes,
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
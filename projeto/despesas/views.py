from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

from .models import Despesa
from .forms import DespesaForm

# Create your views here.
def lista_despesas(request):
    mes_param = request.GET.get('mes')

    mes_atual = date.today().strftime('%m')

    if mes_param:
        despesas = Despesa.objects.filter(mes=mes_param).order_by('data_pagamento')
        total_mes = despesas.aggregate(total=Sum('valor'))['total'] or 0
    else:
        # Mostra todas as despesas, mas sem calcular total
        despesas = Despesa.objects.all().order_by('mes', 'data_pagamento')
        total_mes = None  # 👈 importante: sem total

    totais_por_mes = (
        Despesa.objects
        .values('mes')
        .annotate(total_mes=Sum('valor'))
        .order_by('mes')
    )

    context = {
        'despesas': despesas,
        'meses': Despesa.MES_CHOICES,
        'mes': mes_param,
        'total_mes': total_mes,
        'totais_por_mes': totais_por_mes,
        'mes_atual': mes_atual,
    }

    return render(request, 'despesas/lista_despesas.html', context)

def nova_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('despesas:lista_despesas')
    
    else: 
        form = DespesaForm()

    return render(request, 'despesas/nova_despesa.html', {'form': form})

def editar_despesa(request, id):
    despesa = get_object_or_404(Despesa, id=id)
    mes = request.GET.get('mes')  

    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            
            if mes:
                return redirect(f'/despesas/?mes={mes}')
            return redirect('despesas:lista_despesas')
    else:
        form = DespesaForm(instance=despesa)

    contexto = {'form': form, 'mes': mes}
    return render(request, 'despesas/editar_despesa.html', contexto)

def remover_despesa(request, id):
    despesa = get_object_or_404(Despesa, id=id)
    if request.method == 'POST':
        despesa.delete()
        return redirect('despesas:lista_despesas')
    return render(request, 'despesas/remover_despesa.html', {'despesa': despesa})
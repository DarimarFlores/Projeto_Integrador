from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

from .models import Despesa
from .forms import DespesaForm

# Create your views here.
def lista_despesas(request):
    mes_param = request.GET.get('mes')
    status_param = request.GET.get('status')
    mes_corrente = date.today().strftime('%m')        # mes atual

    # começa com todas as despesas
    despesas_qs =Despesa.objects.all()

    #  filtro para o mes escolhido
    if mes_param:
        despesas_qs = despesas_qs.filter(mes=mes_param) 
    
    # filtro por status   
    if status_param == 'pago':
        despesas_qs = despesas_qs.filter(pago=True)
    elif status_param == 'pendente':
        despesas_qs = despesas_qs.filter(pago=False)

    # colocando na orden
    if mes_param:
        despesas = despesas_qs.order_by('data_pagamento')
    else:
        despesas = despesas_qs.order_by('mes', 'data_pagamento')
    
    # total do mês
    if mes_param:
        total_mes = despesas_qs.aggregate(total=Sum('valor'))['total'] or 0
    else:
        total_mes = None
       
    totais_por_mes = (
        Despesa.objects
        .values('mes')
        .annotate(total_mes=Sum('valor'))
        .order_by('mes')
    )

    # Botões só aparecem com mês atual
    mostrar_botoes = bool(mes_param and mes_param == mes_corrente)

    context = {
        'despesas': despesas,
        'meses': Despesa.MES_CHOICES,
        'mes': mes_param,
        'status': status_param,       
        'total_mes': total_mes,      # valor do mês escolhido
        'totais_por_mes': totais_por_mes,
        'mes_atual': mes_corrente,
        'mostrar_botoes': mostrar_botoes,
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
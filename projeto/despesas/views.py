from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

from .models import Despesa
from .forms import DespesaForm
from django.contrib.auth.decorators import login_required

@login_required
def lista_despesas(request):
    mes_param = request.GET.get('mes')
    status_param = request.GET.get('status')
    mes_corrente = date.today().strftime('%m')  # mes atual
        
    # primeira vez que entrou na pagina, não veio ?mes= na URL
    if mes_param is None:
        # filtra pelo mês actual
        mes_filtro = mes_corrente
    elif mes_param == '':
        # usuário escolheu todos os meses no filtro 
        mes_filtro = None
    else:
        mes_filtro = mes_param       

    # começa com todas as despesas do usuário logado
    despesas_qs =Despesa.objects.filter(usuario=request.user)

    #  filtro para o mes escolhido
    if mes_filtro:
        despesas_qs = despesas_qs.filter(mes=mes_filtro) 
    
    # filtro por status   
    if status_param == 'pago':
        despesas_qs = despesas_qs.filter(pago=True)
    elif status_param == 'pendente':
        despesas_qs = despesas_qs.filter(pago=False)

    # colocando na orden
    if mes_filtro:
        despesas = despesas_qs.order_by('data_pagamento')
    else:
        despesas = despesas_qs.order_by('mes', 'data_pagamento')
    
    # total do mês
    if mes_filtro:
        total_mes = despesas_qs.aggregate(total=Sum('valor'))['total'] or 0
    else:
        total_mes = None
       
    totais_por_mes = (
        Despesa.objects
        .filter(usuario=request.user)
        .values('mes')
        .annotate(total_mes=Sum('valor'))
        .order_by('mes')
    )

    # Botões só aparecem com mês atual
    mostrar_botoes = bool(mes_filtro and mes_filtro == mes_corrente)

    mes_para_template = mes_param if mes_param is not None else mes_corrente

    context = {
        'despesas': despesas,
        'meses': Despesa.MES_CHOICES,
        'mes': mes_para_template,
        'status': status_param,       
        'total_mes': total_mes,      # valor do mês escolhido
        'totais_por_mes': totais_por_mes,
        'mes_atual': mes_corrente,
        'mostrar_botoes': mostrar_botoes,
    }

    return render(request, 'despesas/lista_despesas.html', context)

@login_required
def nova_despesa(request):
    mes_param = request.GET.get('mes')

    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.usuario = request.user # despesa do usuário logado
            despesa.save()

            # depois de salvar, volta pra lista filtrada pelo mês da renda
            redirect_mes = despesa.mes or mes_param
            if redirect_mes:
                return redirect(f'/despesas/?mes={redirect_mes}')
            return redirect('despesas:lista_despesas')           
    
    else:
        initial = {'mes': mes_param} if mes_param else None
        form = DespesaForm(initial=initial)

    return render(request, 'despesas/nova_despesa.html', {'form': form})

@login_required
def editar_despesa(request, id):
    despesa = get_object_or_404(Despesa, id=id, usuario=request.user)
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

@login_required
def remover_despesa(request, id):
    despesa = get_object_or_404(Despesa, id=id, usuario=request.user)
    if request.method == 'POST':
        despesa.delete()
        return redirect('despesas:lista_despesas')
    return render(request, 'despesas/remover_despesa.html', {'despesa': despesa})
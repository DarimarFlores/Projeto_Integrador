from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .forms import RendaForm
from .models import Renda


# Create your views here.
def cadastroRenda(request):
    mes_param = request.GET.get('mes')
    if not mes_param:        
        mes_param = date.today().strftime('%m')


    if request.method == 'POST':
        form = RendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/rendamensal/?mes={mes_param}')

    else:
        form = RendaForm()
    
    rendas = Renda.objects.filter(mes=mes_param).order_by('data_recebimento')

    total_mes_atual = (
        rendas.aggregate(total_mes=Sum('valor'))['total_mes'] or 0
    )

    totais_por_mes = (
        Renda.objects
        .values('mes')
        .annotate(total_mes=Sum('valor'))
        .order_by('mes')
    )

    contexto = {
        'form': form,
        'rendas': rendas,
        'totais_por_mes': totais_por_mes,
        'mes_atual': mes_param,
        'meses': Renda.MES_CHOICES,  # para montar o <select> no template
        'total_mes_atual': total_mes_atual,
    }

    return render(request, 'rendamensal/cadastro_renda.html', contexto)


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
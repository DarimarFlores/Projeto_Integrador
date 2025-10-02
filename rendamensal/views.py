from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone
import locale
import calendar

from .forms import RendaForm
from .models import Renda

# Create your views here.
def cadastro_renda(request):
    if request.method == 'POST':
        form = RendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastro_renda')

    else:
        form = RendaForm()
    
    hoje = timezone.now().date()
    mes_padrao = hoje.month
    ano_padrao = hoje.year

    def to_int(v,default):
        try:
            return int(v)
        except (TypeError, ValueError):
                return default

    mes = to_int(request.GET.get('mes'), mes_padrao)
    ano = to_int(request.GET.get ('ano'), ano_padrao)

    if mes < 1 or mes >12:
        mes = mes_padrao       

    if ano < 1900 or ano > 2100:
        ano = ano_padrao    
    
    rendas = (Renda.objects.filter(
        data_recebimento__month=mes,
        data_recebimento__year=ano
    ).order_by('data_recebimento')
    )

    total = rendas.aggregate(total=Sum('valor'))['total']or 0

    try:
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8") #Linux/Mac
    except locale.Error:
        locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252") #Windows

    meses = [(i, calendar.month_name[i].capitalize()) for i in range(1,13)]

    return render(request, 'rendamensal/renda.html', {
        'form': form,
        'rendas': rendas,
        'total': total,
        'mes': mes,
        'ano':ano,
        'meses': meses,
     })

def editar_renda(request, id):
    renda = get_object_or_404(Renda, id=id)
    if request.method == 'POST':
        form =RendaForm(requesr.POST, instance=renda)
        if form.is_valid():
            form.save()
            return redirect('cadastro_renda')

    else:
        form = RendaForm(instance=renda)
    return render(request, 'rendamensal/editar_renda.html', {'form': form})

def remover_renda(request, id):
    renda = get_object_or_404(Renda, id=id)
    if request.method =='POST':
        renda.delete()
        return redirect('cadastro_renda')
    return render(request, 'rendamensal/remover_renda.html', {'renda': renda})


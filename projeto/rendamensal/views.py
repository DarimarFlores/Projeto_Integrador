from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .forms import RendaForm
from .models import Renda


# Create your views here.
def cadastroRenda(request):
    if request.method == 'POST':
        form = RendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rendamensal:cadastro_renda')

    else:
        form = RendaForm()
    
    rendas = Renda.objects.all().order_by('data_recebimento')
    
    totais_por_mes = (
        Renda.objects
        .values('mes')
        .annotate(total_mes=Sum('valor'))
        .order_by('mes')
    )
    
    return render(request, 'rendamensal/cadastro_renda.html', {'form': form, 'rendas': rendas, 'totais_por_mes': totais_por_mes})

def editar_renda(request, id):
    renda = get_object_or_404(Renda, id=id)
    if request.method == 'POST':
        form = RendaForm(request.POST, instance=renda)
        if form.is_valid():
            form.save()
            return redirect('rendamensal:cadastro_renda')

    else: 
        form = RendaForm(instance=renda)
    return render(request, 'rendamensal/editar_renda.html', {'form': form, 'renda': renda})

def remover_renda(request, id):
    renda = get_object_or_404(Renda, id=id)
    renda.delete()
    return redirect('rendamensal:cadastro_renda')
#prova do que gitignore esta funcionando
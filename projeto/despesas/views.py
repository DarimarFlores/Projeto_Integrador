from django.shortcuts import render, redirect, get_object_or_404
from .models import Despesa
from .forms import DespesaForm

# Create your views here.
def lista_despesas(request):
    despesas = Despesa.objects.all()
    return render(request, 'despesas/lista_despesas.html', {'despesas': despesas})

def nova_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_despesas')
    
    else: 
        form = DespesaForm()

    return render(request, 'despesas/nova_despesa.html', {'form': form})

def editar_despesa(request, id):
    despesa = get_object_or_404(Despesa, id=id)
    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            return redirect('lista_despesas')
    else:
        form = DespesaForm(instance=despesa)
    return render(request, 'despesas/editar_despesa.html', {'form': form})

def remover_despesa(request, id):
    despesa = get_object_or_404(Despesa, id=id)
    if request.method == 'POST':
        despesa.delete()
        return redirect('lista_despesas')
    return render(request, 'despesas/remover_despesa.html', {'despesa': despesa})
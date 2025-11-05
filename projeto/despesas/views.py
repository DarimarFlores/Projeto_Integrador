from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Despesa
from .forms import DespesaForm

# Create your views here.
def lista_despesas(request):
    mes = request.GET.get('mes')

    if mes:
        despesas = Despesa.objects.filter(mes=mes)
    else:
        despesas = Despesa.objects.all()
    
    total_mes = despesas.aggregate(total=Sum('valor'))['total'] or 0

    context = {
        'despesas': despesas,
        'mes': mes,
        'meses': Despesa.MES_CHOICES,
        'total_mes': total_mes,
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
    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            return redirect('despesas:lista_despesas')
    else:
        form = DespesaForm(instance=despesa)
    return render(request, 'despesas/editar_despesa.html', {'form': form})

def remover_despesa(request, id):
    despesa = get_object_or_404(Despesa, id=id)
    if request.method == 'POST':
        despesa.delete()
        return redirect('despesas:lista_despesas')
    return render(request, 'despesas/remover_despesa.html', {'despesa': despesa})
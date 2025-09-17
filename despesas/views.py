from django.shortcuts import render, redirect
from .forms import DespesaForm
from .models import Despesa

# Create your views here.
def lista_despesas(request):
    despesas = Despesa.objects.all()
    return render(request, 'despesas/lista_despesas.html', {'despesas': despesas})

def nova_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nova_despesa')
    
    else: 
        form = DespesaForm()
        return render(request, 'despesas/nova_despesa', {'form': form})

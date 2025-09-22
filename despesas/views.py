from django.shortcuts import render, redirect
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

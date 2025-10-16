from django.shortcuts import render, redirect
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
    
    rendas = Renda.objects.all()
    return render(request, 'rendamensal/renda_index.html', {'form': form, 'rendas': rendas})

#prova do que gitignore esta funcionando
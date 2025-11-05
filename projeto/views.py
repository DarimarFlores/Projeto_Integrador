from datetime import date

from django.shortcuts import render
from django.db.models import Sum

from projeto.rendamensal.models import Renda
from projeto.despesas.models import Despesa
from projeto.financiamentos.models import Financiamento


def inicio(request):
    # mês atual em formato '01', '02', ...
    mes_atual = date.today().strftime('%m')

    # nome do mês usando as choices da Renda
    mes_nome = dict(Renda.MES_CHOICES).get(mes_atual, '')

    # totais por app
    total_renda = (
        Renda.objects.filter(mes=mes_atual)
        .aggregate(total=Sum('valor'))['total'] or 0
    )

    total_despesas = (
        Despesa.objects.filter(mes=mes_atual)
        .aggregate(total=Sum('valor'))['total'] or 0
    )

    total_financiamentos = (
        Financiamento.objects.filter(mes=mes_atual)
        .aggregate(total=Sum('valor_total'))['total'] or 0
    )

    # saldo simples: renda - despesas - financiamentos
    saldo = total_renda - total_despesas - total_financiamentos

    contexto = {
        'mes_atual_codigo': mes_atual,
        'mes_atual_nome': mes_nome,
        'total_renda': total_renda,
        'total_despesas': total_despesas,
        'total_financiamentos': total_financiamentos,
        'saldo': saldo,
    }
    return render(request, 'inicio.html', contexto)
from datetime import date
import json

from django.shortcuts import render
from django.db.models import Sum

from projeto.rendamensal.models import Renda
from projeto.despesas.models import Despesa
from projeto.financiamentos.models import Financiamento


def inicio(request):
    mes_atual = date.today().strftime('%m')

    # choices de mês vindas do model Renda
    meses_choices = Renda.MES_CHOICES
    mes_nome = dict(meses_choices).get(mes_atual, '')

    # --------- totais do mês atual ---------
    total_renda = (
        Renda.objects.filter(mes=mes_atual)
        .aggregate(total=Sum('valor'))['total'] or 0
    )

    total_despesas = (
        Despesa.objects.filter(mes=mes_atual)
        .aggregate(total=Sum('valor'))['total'] or 0
    )

    # aqui é valor_total, porque Financiamento não tem campo "valor"
    total_financiamentos = (
        Financiamento.objects.filter(mes=mes_atual)
        .aggregate(total=Sum('valor_total'))['total'] or 0
    )

    # saldo = renda - (despesas + financiamentos)
    saldo = total_renda - (total_despesas + total_financiamentos)

    # --------- dados mês a mês para o gráfico ---------
    labels = []
    renda_por_mes = []
    despesas_por_mes = []
    financiamentos_por_mes = []
    saldo_por_mes = []

    for codigo, nome in meses_choices:
        labels.append(nome)

        renda_mes = (
            Renda.objects.filter(mes=codigo)
            .aggregate(total=Sum('valor'))['total'] or 0
        )

        despesa_mes = (
            Despesa.objects.filter(mes=codigo)
            .aggregate(total=Sum('valor'))['total'] or 0
        )

        financ_mes = (
            Financiamento.objects.filter(mes=codigo)
            .aggregate(total=Sum('valor_total'))['total'] or 0
        )

        renda_por_mes.append(float(renda_mes))
        despesas_por_mes.append(float(despesa_mes))
        financiamentos_por_mes.append(float(financ_mes))
        saldo_por_mes.append(float(renda_mes - (despesa_mes + financ_mes)))

    contexto = {
        'mes_atual_nome': mes_nome,
        'total_renda': total_renda,
        'total_despesas': total_despesas,
        'total_financiamentos': total_financiamentos,
        'saldo': saldo,

        'labels_json': json.dumps(labels),
        'renda_por_mes_json': json.dumps(renda_por_mes),
        'despesas_por_mes_json': json.dumps(despesas_por_mes),
        'financiamentos_por_mes_json': json.dumps(financiamentos_por_mes),
        'saldo_por_mes_json': json.dumps(saldo_por_mes),
    }

    return render(request, 'inicio.html', contexto)
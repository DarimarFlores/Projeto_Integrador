from datetime import date
import json
import math
from decimal import Decimal

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
        .aggregate(total=Sum('valor_parcela'))['total'] or 0
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
            .aggregate(total=Sum('valor_parcela'))['total'] or 0
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

def meta_poupanca(request):
    mes_atual = date.today().strftime('%m')
    meses_choices = Renda.MES_CHOICES
    mes_atual_nome = dict(meses_choices).get(mes_atual,'')

    # cálculo da situação atual do mês
    total_renda_mes = (
        Renda.objects.filter(mes=mes_atual).aggregate(total=Sum('valor'))['total'] or 0
    )

    total_despesas_mes = (
        Despesa.objects.filter(mes=mes_atual).aggregate(total=Sum('valor'))['total'] or 0
    )

    total_financiamentos_mes = (
        Financiamento.objects.filter(mes=mes_atual).aggregate(total=Sum('valor_parcela'))['total'] or 0
    )

    saldo_mes = total_renda_mes - (total_despesas_mes + total_financiamentos_mes)

    # simulação
    valor_meta_raw = request.GET.get('valor_meta')
    prazo_raw = request.GET.get('prazo_meses')

    # valores da simulação iniciais
    valor_meta = None
    prazo_meses = None
    poupanca_mensal = None
    prazo_ideal = None
    erro_validacao = False
    houve_simulacao = False

    if valor_meta_raw or prazo_raw:
        houve_simulacao = True
        try:
            valor_meta = float(valor_meta_raw.replace(',', '.'))
            prazo_meses = int(prazo_raw)

            if valor_meta <= 0 or prazo_meses <= 0:
                erro_validacao = True
            else:
                # quanto guardar por mês para atingir a meta no prazo desejado
                poupanca_mensal = valor_meta / prazo_meses

                # se o saldo mensal for positivo, em quantos meses você atinge essa meta
                if saldo_mes > 0:
                    prazo_ideal = valor_meta / saldo_mes

        except (ValueError, TypeError, AttributeError):
            erro_validacao = True
  
    contexto = {
        'mes_atual_nome': mes_atual_nome,
        'total_renda_mes': total_renda_mes,
        'total_despesas_mes': total_despesas_mes,
        'total_financiamentos_mes': total_financiamentos_mes,
        'saldo_mes': saldo_mes,
        'valor_meta': valor_meta,
        'prazo_meses': prazo_meses,
        'poupanca_mensal': poupanca_mensal,        
        'prazo_ideal': prazo_ideal,
        'erro_validacao': erro_validacao,
        'houve_simulacao': houve_simulacao
    }

    return render(request, 'meta_poupanca.html', contexto)

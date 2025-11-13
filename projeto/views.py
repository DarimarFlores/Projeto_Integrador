from datetime import date, timedelta
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

    # alertas para despesas e financiamentos
def alertas_financiamentos(request):
    hoje = date.today()
    limite = hoje + timedelta(days=5)

   
    financ_vencidas = Financiamento.objects.filter(pago=False, data_vencimento__lt=hoje).order_by('data_vencimento')
    financ_vence_hoje = Financiamento.objects.filter(pago=False, data_vencimento=hoje).order_by('credor')
    financ_proximos = Financiamento.objects.filter(pago=False, data_vencimento__gt=hoje, data_vencimento__lte=limite).order_by('data_vencimento')

    despesas_vencidas = Despesa.objects.filter(pago=False, data_vencimento__lt=hoje).order_by('data_vencimento')
    despesas_vence_hoje = Despesa.objects.filter(pago=False, data_vencimento=hoje).order_by('credor')
    despesas_proximas = Despesa.objects.filter(pago=False, data_vencimento__gt=hoje, data_vencimento__lte=limite).order_by('data_vencimento')
    
    contexto = {
        'financ_vencidos': financ_vencidos,
        'financ_vence_hoje': financ_vence_hoje,
        'financ_proximos': financ_proximos,
        'despesas_vencidas': despesas_vencidas,
        'despesas_vence_hoje': despesas_vence_hoje,
        'despesas_proximas': despesas_proximas,
        'hoje': hoje,
        'limite': limite,

    }
    return render(request, 'financiamentos/inicio.html', contexto)


def meta_poupanca(request):
    mes_atual = date.today().strftime('%m')
    meses_choices = Renda.MES_CHOICES
    mes_atual_nome = dict(meses_choices).get(mes_atual, '')

    # --- Situação do mês atual ---
    total_renda_mes = (
        Renda.objects.filter(mes=mes_atual).aggregate(total=Sum('valor'))['total'] or 0
    )
    total_despesas_mes = (
        Despesa.objects.filter(mes=mes_atual).aggregate(total=Sum('valor'))['total'] or 0
    )
    total_financiamentos_mes = (
        Financiamento.objects.filter(mes=mes_atual).aggregate(total=Sum('valor_parcela'))['total'] or 0
    )

    # saldo_mes pode vir como Decimal; converto pra float pra contas simples
    saldo_mes = float(total_renda_mes) - float(total_despesas_mes + total_financiamentos_mes)

    # --- Lê os valores da simulação ---
    valor_meta_raw = (request.GET.get('valor_meta') or '').strip()
    prazo_raw = (request.GET.get('prazo_meses') or '').strip()

    valor_meta = None
    prazo_meses = None
    poupanca_mensal = None
    prazo_ideal = None

    houve_simulacao = bool(valor_meta_raw or prazo_raw)
    mostrar_erro = False

    if valor_meta_raw and prazo_raw:
        try:
            vm = float(valor_meta_raw.replace(',', '.'))
            pm = int(prazo_raw)

            if vm > 0 and pm > 0:
                valor_meta = vm
                prazo_meses = pm
                poupanca_mensal = vm / pm

                # aqui uso saldo_mes (float) sem erro de tipo
                if saldo_mes > 0:
                    prazo_ideal = vm / saldo_mes
            else:
                mostrar_erro = True

        except (ValueError, TypeError):
            mostrar_erro = True

    elif houve_simulacao:
        # clicou em calcular mas deixou algum campo vazio
        mostrar_erro = True

    contexto = {
        'mes_atual_nome': mes_atual_nome,
        'total_renda_mes': total_renda_mes,
        'total_despesas_mes': total_despesas_mes,
        'total_financiamentos_mes': total_financiamentos_mes,
        'saldo_mes': saldo_mes,  # já como float, mas pra exibir não tem problema

        'valor_meta': valor_meta,
        'prazo_meses': prazo_meses,
        'poupanca_mensal': poupanca_mensal,
        'prazo_ideal': prazo_ideal,

        'houve_simulacao': houve_simulacao,
        'mostrar_erro': mostrar_erro,
    }

    return render(request, 'meta_poupanca.html', contexto)

"""Gaps e plano ordenado por dependências; conhecimento não altera afinidade."""
import math
from .base import validar_base

def planejar(base,trilha_id,conhecimentos,horas_semana=6,objetivo='primeiro'):
    validar_base(base)
    if trilha_id not in base['trilhas']: raise ValueError('Trilha desconhecida.')
    if not isinstance(conhecimentos,dict) or set(conhecimentos)!=set(base['competencias']):
        raise ValueError('Informe o nível atual de todas as competências.')
    if any(type(v) is not int or not 0<=v<=4 for v in conhecimentos.values()):
        raise ValueError('Níveis de conhecimento devem ser inteiros de 0 a 4.')
    if type(horas_semana) is not int or not 1<=horas_semana<=40:
        raise ValueError('Informe de 1 a 40 horas semanais.')
    if objetivo not in base['objetivos']: raise ValueError('Objetivo desconhecido.')
    trilha=base['trilhas'][trilha_id]
    requisitos={s:dict(r) for s,r in trilha['requisitos_junior'].items()}
    def expandir(s):
        for pre in base['competencias'][s]['pre_requisitos']:
            if pre not in requisitos:
                requisitos[pre]=dict(nivel=2,prioridade=3)
            expandir(pre)
    for s in list(requisitos): expandir(s)
    gaps=[];alcancado=necessario=0
    for s,r in requisitos.items():
        atual=conhecimentos[s];alvo=r['nivel'];peso=r['prioridade']
        necessario+=alvo*peso;alcancado+=min(atual,alvo)*peso
        if atual<alvo:
            competencia=base['competencias'][s]
            gaps.append(dict(id=s,nome=competencia['nome'],atual=atual,alvo=alvo,gap=alvo-atual,
                prioridade=peso,horas=math.ceil(competencia['horas']*(alvo-atual)/alvo),
                evidencia=competencia['evidencia'],pre_requisitos=competencia['pre_requisitos']))
    # Ordenação topológica: uma prioridade alta não ultrapassa seus fundamentos.
    pendentes={g['id']:g for g in gaps};ordenados=[]
    acumulado=0
    while pendentes:
        livres=[g for g in pendentes.values() if not any(s in pendentes for s in g['pre_requisitos'])]
        proximo=sorted(livres,key=lambda g:(-g['prioridade'],-g['gap'],g['id']))[0]
        proximo=dict(proximo,ordem=len(ordenados)+1,semana_inicio=acumulado//horas_semana+1)
        acumulado+=proximo['horas']
        proximo['semana_fim']=math.ceil(acumulado/horas_semana)
        ordenados.append(proximo);del pendentes[proximo['id']]
    return dict(trilha_id=trilha_id,trilha=trilha['nome'],referencial='Júnior (modelo educacional)',
        atendimento_referencial=round(100*alcancado/necessario,2),gaps=ordenados,
        horas_estimadas=acumulado,semanas_estimadas=math.ceil(acumulado/horas_semana),horas_semana=horas_semana,
        objetivo=objetivo,orientacao=base['orientacoes_objetivo'][objetivo],projeto=trilha['projeto'],
        certificacoes=[base['certificacoes'][c] for c in trilha['certificacoes']])

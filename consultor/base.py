"""Carregamento e validação do conhecimento externo, sem executar expressões."""
import json
import math
from pathlib import Path

CAMINHO_BASE=Path(__file__).resolve().parents[1]/'base/regras_carreiras.json'

def numero(valor, minimo=0, maximo=float('inf')):
    return type(valor) in (int,float) and math.isfinite(valor) and minimo<=valor<=maximo

def exigir(condicao, mensagem="Campo inválido na base."):
    if not condicao:
        raise ValueError(mensagem)

def validar_base(base):
    try:
        exigir(base['escala']=={'minimo':1,'maximo':5})
        exigir(numero(base['config']['margem_empate'],0,100))
        exigir(numero(base['config']['cobertura_minima'],0,100))
        dims,skills,trilhas=base['dimensoes'],base['competencias'],base['trilhas']
        exigir(dims and skills and len(trilhas)==10)
        exigir(base['objetivos'].keys()==base['orientacoes_objetivo'].keys())
        exigir(set(base['niveis_conhecimento'])=={'0','1','2','3','4'})
        for d in dims.values():
            exigir(d['nome'] and d['descricao'] and d['etapa'] in (1,2))
        for sid,s in skills.items():
            exigir(s['nome'] and s['evidencia'] and numero(s['horas'],1))
            exigir(len(s['pre_requisitos'])==len(set(s['pre_requisitos'])))
            exigir(all(p in skills and p!=sid for p in s['pre_requisitos']))
        visitados,ativos=set(),set()
        def visitar(s):
            exigir(s not in ativos, 'Ciclo de pré-requisitos.')
            if s in visitados: return
            ativos.add(s)
            for p in skills[s]['pre_requisitos']: visitar(p)
            ativos.remove(s);visitados.add(s)
        for s in skills: visitar(s)
        for t in trilhas.values():
            exigir(t['nome'] and t['pesos'] and set(t['pesos'])<=set(dims))
            exigir(all(numero(w) for w in t['pesos'].values()) and sum(t['pesos'].values())>0)
            exigir(t['requisitos_junior'] and set(t['requisitos_junior'])<=set(skills))
            for r in t['requisitos_junior'].values():
                exigir(type(r['nivel']) is int and 1<=r['nivel']<=4)
                exigir(numero(r['prioridade'],1))
            exigir(t['projeto']['titulo'] and t['projeto']['criterios'])
            exigir(t['certificacoes'] and all(c in base['certificacoes'] for c in t['certificacoes']))
        for c in base['certificacoes'].values():
            exigir(c['nome'] and c['quando'] and c['url'].startswith('https://'))
        ids=set()
        for p in base['penalidades']:
            exigir(p['id'] not in ids)
            ids.add(p['id'])
            exigir(p['trilhas'] and set(p['trilhas'])<=set(trilhas))
            exigir(numero(p['pontos'],0,100) and p['motivo'] and p['condicoes'])
            for c in p['condicoes']:
                exigir(c['dimensao'] in dims and c['operador'] in {'le','ge'})
                exigir(type(c['valor']) is int and 1<=c['valor']<=5)
    except (ValueError,KeyError,TypeError,AttributeError) as exc:
        raise ValueError('Base de conhecimento inválida: confira pesos, referências, escalas e pré-requisitos.') from exc
    return base

def carregar_base(caminho=CAMINHO_BASE):
    try:
        base=json.loads(Path(caminho).read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError) as exc:
        raise ValueError('Não foi possível carregar o arquivo JSON de conhecimento.') from exc
    return validar_base(base)

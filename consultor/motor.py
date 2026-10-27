"""Soma ponderada com regras declarativas e rastreabilidade por atributo."""
from .base import validar_base

def validar_afinidades(base,respostas):
    if not isinstance(respostas,dict) or set(respostas)!=set(base['dimensoes']):
        raise ValueError('Informe todas as dimensões; use None para uma afinidade desconhecida.')
    if any(v is not None and (type(v) is not int or not 1<=v<=5) for v in respostas.values()):
        raise ValueError('As afinidades devem ser inteiros de 1 a 5 ou None.')

def avaliar(base,respostas):
    validar_base(base)
    validar_afinidades(base,respostas)
    ranking=[]
    for tid,trilha in base['trilhas'].items():
        total=sum(trilha['pesos'].values())
        evidencias=[]
        soma=conhecido=0.0
        for dim,peso in trilha['pesos'].items():
            resposta=respostas[dim]
            contribuicao=0 if resposta is None else 100*peso*((resposta-1)/4)/total
            soma+=contribuicao
            if resposta is not None: conhecido+=peso
            evidencias.append(dict(dimensao=dim,nome=base['dimensoes'][dim]['nome'],resposta=resposta,
                                   peso=peso,contribuicao=round(contribuicao,4)))
        penalidades=[];desconto_possivel=0
        for regra in base['penalidades']:
            def corresponde(c):
                v=respostas[c['dimensao']]
                if v is None: return False
                return v<=c['valor'] if c['operador']=='le' else v>=c['valor']
            if tid in regra['trilhas'] and all(respostas[c['dimensao']] is None or corresponde(c) for c in regra['condicoes']):
                desconto_possivel+=regra['pontos']
            if tid in regra['trilhas'] and all(corresponde(c) for c in regra['condicoes']):
                penalidades.append(dict(id=regra['id'],pontos=regra['pontos'],motivo=regra['motivo'],
                    condicoes=[dict(c,resposta=respostas[c['dimensao']]) for c in regra['condicoes']]))
        desconto=sum(p['pontos'] for p in penalidades)
        pontuacao=max(0,min(100,soma-desconto))
        ranking.append(dict(id=tid,nome=trilha['nome'],compatibilidade=round(pontuacao,2),
            base_percentual=round(soma,4),desconto=desconto,cobertura=round(100*conhecido/total,2),
            piso_cauteloso=round(max(0,min(100,soma-desconto_possivel)),2),
            teto_otimista=round(max(0,min(100,soma+100*(total-conhecido)/total-desconto)),2),
            evidencias=evidencias,penalidades=penalidades))
    # A igualdade é definida na precisão percentual exibida; ID só estabiliza a ordem.
    ranking.sort(key=lambda r:(-r['compatibilidade'],r['id']))
    anterior=None;posicao=0
    for i,r in enumerate(ranking,1):
        if r['compatibilidade']!=anterior: posicao=i
        r['posicao']=posicao;anterior=r['compatibilidade']
    maior=ranking[0]['compatibilidade']
    proximas=[r['id'] for r in ranking if maior-r['compatibilidade']<=base['config']['margem_empate']]
    sem_dados=all(v is None for v in respostas.values())
    baixa_cobertura=any(r['cobertura']<base['config']['cobertura_minima'] for r in ranking[:3])
    return dict(versao_base=base['versao'],ranking=ranking,top3=ranking[:3],proximas=proximas,
                status='insuficiente' if sem_dados or baixa_cobertura or maior==0 else 'comparavel',
                empate_no_corte=len(ranking)>3 and ranking[2]['compatibilidade']==ranking[3]['compatibilidade'])

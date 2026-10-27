import copy
import itertools
import math
import pytest
from consultor.motor import avaliar
from consultor.base import carregar_base,validar_base

@pytest.mark.parametrize('indice',range(10))
def test_personas(base,personas,indice):
    p=personas[indice];r=avaliar(base,p['afinidades'])
    assert r['ranking'][0]['id']==p['esperado']
    assert len(r['top3'])==3 and len(r['ranking'])==10
    assert len(r['proximas'])==1
    assert r['ranking'][0]['compatibilidade']==100

def test_neutro_empate_explicito(base):
    r=avaliar(base,{d:3 for d in base['dimensoes']})
    assert all(t['compatibilidade']==50 and t['posicao']==1 for t in r['ranking'])
    assert r['empate_no_corte'] and len(r['proximas'])==10

def test_todos_minimos_sem_indicacao(base):
    r=avaliar(base,{d:1 for d in base['dimensoes']})
    assert r['status']=='insuficiente'
    assert all(t['compatibilidade']==0 for t in r['ranking'])

def test_todos_maximos(base):
    r=avaliar(base,{d:5 for d in base['dimensoes']})
    assert all(t['compatibilidade']==100 and not t['penalidades'] for t in r['ranking'])

def test_tudo_desconhecido(base):
    r=avaliar(base,{d:None for d in base['dimensoes']})
    assert r['status']=='insuficiente'
    assert all(t['cobertura']==0 and t['compatibilidade']==0 and t['teto_otimista']==100 for t in r['ranking'])
    assert all(not t['penalidades'] for t in r['ranking'])

def test_calculo_manual(base):
    respostas={d:3 for d in base['dimensoes']};respostas['logica']=5
    t=next(t for t in avaliar(base,respostas)['ranking'] if t['id']=='backend')
    # Pesos: 6*1 + 2*0,5 + 1*0,5 + 1*0,5 = 8; soma dos pesos = 10.
    assert t['compatibilidade']==80
    assert math.isclose(sum(e['contribuicao'] for e in t['evidencias']),80,abs_tol=0.0003)

def test_penalidade_e_condicoes_cruzadas(base):
    respostas={d:3 for d in base['dimensoes']};respostas.update(infraestrutura=2,automacao=5)
    r=avaliar(base,respostas)
    t=next(t for t in r['ranking'] if t['id']=='cloud')
    assert t['desconto']==15
    assert {p['id'] for p in t['penalidades']}=={'P_cloud','P_cloud_operacao'}
    assert t['compatibilidade']==round(max(0,t['base_percentual']-15),2)

def test_json_muda_motor_sem_editar_codigo(base):
    respostas={d:3 for d in base['dimensoes']};respostas['logica']=5
    antes=avaliar(base,respostas)
    base['trilhas']['backend']['pesos']={'visual':1}
    depois=avaliar(base,respostas)
    indice=lambda r:next(t['compatibilidade'] for t in r['ranking'] if t['id']=='backend')
    assert indice(antes)==80 and indice(depois)==50

@pytest.mark.parametrize('valor',[0,6,-1,2.5,True,'5',float('nan'),float('inf')])
def test_rejeita_escala_invalida(base,valor):
    respostas={d:3 for d in base['dimensoes']};respostas['logica']=valor
    with pytest.raises(ValueError): avaliar(base,respostas)

def test_rejeita_campos_ausentes_extras(base):
    with pytest.raises(ValueError): avaliar(base,{})
    with pytest.raises(ValueError): avaliar(base,dict({d:3 for d in base['dimensoes']},extra=2))

def test_sem_mutacao(base,personas):
    copia=copy.deepcopy(base);p=copy.deepcopy(personas[0]['afinidades'])
    r1=avaliar(base,p);avaliar(base,personas[1]['afinidades']);r2=avaliar(base,p)
    assert base==copia and r1==r2 and p==personas[0]['afinidades']

def test_limites_incerteza_envolvem_completamentos(base):
    p={d:3 for d in base['dimensoes']};p.update(infraestrutura=None,automacao=None)
    parcial={r['id']:r for r in avaliar(base,p)['ranking']}
    for a,b in itertools.product(range(1,6),repeat=2):
        for r in avaliar(base,dict(p,infraestrutura=a,automacao=b))['ranking']:
            assert parcial[r['id']]['piso_cauteloso']<=r['compatibilidade']<=parcial[r['id']]['teto_otimista']

@pytest.mark.parametrize('par',[('dados','visual'),('infraestrutura','automacao'),('logica','qualidade')])
def test_perfis_mistos_ranking_consistente(base,par):
    p={d:3 for d in base['dimensoes']};p.update({d:5 for d in par})
    r=avaliar(base,p)
    valores=[t['compatibilidade'] for t in r['ranking']]
    assert valores==sorted(valores,reverse=True) and all(0<=v<=100 for v in valores)

@pytest.mark.parametrize('problema',['peso_negativo','peso_zero','ciclo','referencia','nan','operador','duplicada'])
def test_base_invalida(base,problema):
    if problema=='peso_negativo': base['trilhas']['backend']['pesos']['logica']=-1
    if problema=='peso_zero': base['trilhas']['backend']['pesos']={'logica':0}
    if problema=='ciclo': base['competencias']['programacao']['pre_requisitos']=['python']
    if problema=='referencia': base['competencias']['python']['pre_requisitos']=['inexistente']
    if problema=='nan': base['config']['margem_empate']=float('nan')
    if problema=='operador': base['penalidades'][0]['condicoes'][0]['operador']='eval'
    if problema=='duplicada': base['penalidades'].append(copy.deepcopy(base['penalidades'][0]))
    with pytest.raises(ValueError): validar_base(base)

def test_json_invalido_e_ausente(tmp_path):
    with pytest.raises(ValueError): carregar_base(tmp_path/'ausente.json')
    p=tmp_path/'invalido.json';p.write_text('{')
    with pytest.raises(ValueError): carregar_base(p)

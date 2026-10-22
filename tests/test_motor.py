import json
from pathlib import Path
import pytest
from consultor.dominio import CARREIRAS
from consultor.servico import consultar
from consultor.motor import MotorCarreiras

PERSONAS = json.loads((Path(__file__).resolve().parents[1]/'personas.json').read_text(encoding='utf-8'))

@pytest.mark.parametrize('persona', PERSONAS, ids=lambda p:p['esperado'])
def test_personas(persona):
    r = consultar(persona['respostas'])
    assert r['carreira'] == persona['esperado']
    assert r['pontos'][r['carreira']] == 12
    assert len([e for e in r['evidencias'] if e['carreira']==r['carreira']]) == 2

def test_25_regras():
    assert len(MotorCarreiras().get_rules()) == 25

def test_iniciante_nao_e_excluido():
    p = dict(PERSONAS[0]['respostas'], ferramenta='iniciante', matematica='baixa')
    assert consultar(p)['carreira'] == 'backend'

def test_dados_matematica_baixa_pede_refinamento():
    p = dict(PERSONAS[2]['respostas'], matematica='baixa')
    assert consultar(p)['pendente']
    r = consultar(p,'ciencia')
    assert r['carreira'] == 'ciencia'
    assert 'Reforce matemática' in r['plano']

def test_perfil_exploratorio_nao_inventa_indicacao():
    p = dict(PERSONAS[0]['respostas'], atividade='explorar', entrega='explorar', ferramenta='iniciante')
    r = consultar(p)
    assert r['carreira'] is None and r['pendente']
    assert set(r['candidatas']) == set(CARREIRAS)

@pytest.mark.parametrize('area', list(CARREIRAS))
def test_refinamento_cobre_dez_trilhas(area):
    p = dict(PERSONAS[0]['respostas'], atividade='explorar', entrega='explorar', ferramenta='iniciante')
    r = consultar(p,area)
    assert r['carreira'] == area
    assert len(r['evidencias']) == 1
    assert r['evidencias'][0]['regra'].startswith('R2')

def test_evidencia_fraca_exige_pergunta():
    p = dict(PERSONAS[0]['respostas'], entrega='explorar')
    assert consultar(p)['carreira'] is None
    assert consultar(p, 'backend')['carreira'] == 'backend'

def test_empate_positivo_dados_e_refinamento():
    p=dict(PERSONAS[2]['respostas'],entrega='explorar')
    r=consultar(p)
    assert r['pontos']['ciencia']==r['pontos']['engenharia']==4
    assert r['pendente'] and r['carreira'] is None
    assert consultar(p,'engenharia')['carreira']=='engenharia'

def test_consultas_independentes():
    a,b=PERSONAS[0],PERSONAS[2]
    primeiro=consultar(a['respostas'])
    consultar(b['respostas'])
    assert consultar(a['respostas']) == primeiro

def test_objetivo_adapta_plano():
    p=PERSONAS[0]['respostas']
    assert 'transição' in consultar(dict(p,objetivo='transicao'))['plano']
    assert 'complexidade' in consultar(dict(p,objetivo='aprofundar'))['plano']

@pytest.mark.parametrize('alteracao',[{'matematica':'extrema'},{'objetivo':None},{'entrega':[]}])
def test_rejeita_resposta_invalida(alteracao):
    with pytest.raises(ValueError):
        consultar(dict(PERSONAS[0]['respostas'], **alteracao))

def test_rejeita_campos_ausentes_e_extras():
    with pytest.raises(ValueError): consultar({})
    with pytest.raises(ValueError): consultar(dict(PERSONAS[0]['respostas'],extra='x'))
    with pytest.raises(ValueError): consultar(PERSONAS[0]['respostas'],'inexistente')

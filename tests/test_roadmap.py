import pytest
from consultor.motor import avaliar
from consultor.roadmap import planejar
from consultor.relatorio import gerar_markdown

@pytest.mark.parametrize('indice',range(10))
def test_roadmap_dez_trilhas(base,indice):
    tid=list(base['trilhas'])[indice];niveis={s:0 for s in base['competencias']}
    plano=planejar(base,tid,niveis)
    assert plano['gaps'] and plano['atendimento_referencial']==0
    ordem={g['id']:i for i,g in enumerate(plano['gaps'])}
    for g in plano['gaps']:
        for pre in g['pre_requisitos']:
            if pre in ordem: assert ordem[pre]<ordem[g['id']]
        assert g['horas']>0 and g['semana_inicio']<=g['semana_fim']
    assert plano['certificacoes'] and len(plano['projeto']['criterios'])>=3

def test_sem_gaps_nao_reestuda(base):
    p=planejar(base,'ciencia',{s:4 for s in base['competencias']})
    assert p['gaps']==[] and p['horas_estimadas']==0 and p['semanas_estimadas']==0
    assert p['atendimento_referencial']==100

def test_conhecimento_reduz_gaps_e_tempo(base):
    antes=planejar(base,'backend',{s:0 for s in base['competencias']})
    depois=planejar(base,'backend',{s:2 for s in base['competencias']})
    assert depois['horas_estimadas']<antes['horas_estimadas']
    assert depois['atendimento_referencial']>antes['atendimento_referencial']

def test_disponibilidade_altera_semanas_sem_alterar_horas(base):
    n={s:0 for s in base['competencias']}
    lento=planejar(base,'backend',n,2);rapido=planejar(base,'backend',n,10)
    assert lento['horas_estimadas']==rapido['horas_estimadas']
    assert lento['semanas_estimadas']>rapido['semanas_estimadas']

def test_prerequisito_acrescentado(base):
    p=planejar(base,'qa',{s:0 for s in base['competencias']})
    assert 'javascript' in {g['id'] for g in p['gaps']}

@pytest.mark.parametrize('horas',[0,41,True,2.5])
def test_horas_invalidas(base,horas):
    with pytest.raises(ValueError): planejar(base,'backend',{s:0 for s in base['competencias']},horas)

@pytest.mark.parametrize('valor',[-1,5,True,'2',None])
def test_conhecimentos_invalidos(base,valor):
    n={s:0 for s in base['competencias']};n['git']=valor
    with pytest.raises(ValueError): planejar(base,'backend',n)

def test_referencia_ou_objetivo_invalido(base):
    n={s:0 for s in base['competencias']}
    with pytest.raises(ValueError): planejar(base,'invalida',n)
    with pytest.raises(ValueError): planejar(base,'backend',{})
    with pytest.raises(ValueError): planejar(base,'backend',n,objetivo='invalido')

def test_relatorio_explicavel_com_certificacao_e_penalidade(base):
    analise=avaliar(base,{d:1 for d in base['dimensoes']})
    plano=planejar(base,'backend',{s:0 for s in base['competencias']})
    texto=gerar_markdown(analise,plano)
    assert 'Penalidade' in texto and 'horas' in texto and 'https://' in texto
    assert 'insuficientes' in texto and 'empatadas' in texto

def test_objetivo_adapta_plano(base):
    n={s:4 for s in base['competencias']}
    assert 'transferíveis' in planejar(base,'produto',n,objetivo='transicao')['orientacao']
    assert 'revisão técnica' in planejar(base,'produto',n,objetivo='aprofundar')['orientacao']

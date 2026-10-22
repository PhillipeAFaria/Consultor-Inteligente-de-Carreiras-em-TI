from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1]/'app.py')

def preencher(at, atividade='logica', entrega='servicos', ferramenta='python'):
    for key,value in dict(matematica='media',atividade=atividade,entrega=entrega,ferramenta=ferramenta,objetivo='primeiro').items():
        at.selectbox(key=key).select(value)
    return at.run()

def test_fluxo_backend_e_reinicio():
    at=AppTest.from_file(APP).run()
    assert not at.exception
    assert at.button(key='recomendar').disabled
    preencher(at)
    at.button(key='recomendar').click().run()
    assert not at.exception
    assert 'Back-end' in at.success[0].value
    at.button(key='reiniciar').click().run()
    assert at.selectbox(key='atividade').value is None
    assert not at.success

def test_fluxo_dinamico_sem_evidencias():
    at=AppTest.from_file(APP).run()
    preencher(at,'explorar','explorar','iniciante')
    assert len(at.radio)==1
    assert at.button(key='recomendar').disabled
    at.radio[0].set_value('produto').run()
    at.button(key='recomendar').click().run()
    assert not at.exception
    assert 'Gestão de Produtos' in at.success[0].value

def test_alterar_respostas_remove_refinamento_antigo():
    at=AppTest.from_file(APP).run()
    preencher(at,'explorar','explorar','iniciante')
    at.radio[0].set_value('produto').run()
    at.selectbox(key='objetivo').select('transicao').run()
    assert at.radio[0].value is None
    assert at.button(key='recomendar').disabled

from pathlib import Path
from unittest.mock import patch
import runpy
import pytest
from streamlit.testing.v1 import AppTest
import iniciar

APP=str(Path(__file__).resolve().parents[1]/'app.py')

def clicar(at,chave):
    at.button(key=chave).click().run()
    assert not at.exception

def concluir(at):
    clicar(at,'continuar_1');clicar(at,'continuar_2');clicar(at,'calcular')

def test_wizard_vazio_nao_inventa_plano():
    at=AppTest.from_file(APP,default_timeout=15).run()
    assert not at.exception and at.session_state['passo']==1
    concluir(at)
    assert at.session_state['passo']==4 and at.warning
    assert at.selectbox(key='trilha_plano').value is None
    at.selectbox(key='trilha_plano').select('backend').run()
    assert not at.exception and len(at.metric)>=4

def test_wizard_completo_retorno_e_persistencia():
    at=AppTest.from_file(APP,default_timeout=15).run()
    at.selectbox(key='afinidade_comunicacao').select(4).run()
    clicar(at,'continuar_1')
    at.selectbox(key='afinidade_logica').select(5).run()
    at.multiselect(key='competencias_selecionadas').set_value(['git','python']).run()
    at.slider(key='nivel_python').set_value(3).run()
    clicar(at,'voltar_2')
    assert at.selectbox(key='afinidade_comunicacao').value==4
    clicar(at,'continuar_1')
    assert at.selectbox(key='afinidade_logica').value==5
    assert at.slider(key='nivel_python').value==3
    clicar(at,'continuar_2')
    at.number_input(key='horas_widget').set_value(8).run()
    clicar(at,'calcular')
    at.selectbox(key='trilha_plano').select('qa').run()
    assert not at.exception and at.session_state['conhecimentos']['python']==3
    at.run()
    assert at.session_state['passo']==4
    clicar(at,'editar')
    assert at.session_state['passo']==1 and 'analise' not in at.session_state

def test_reiniciar_limpa_respostas():
    at=AppTest.from_file(APP).run()
    at.selectbox(key='afinidade_negocio').select(5).run()
    clicar(at,'reiniciar')
    assert at.session_state['passo']==1
    assert all(v is None for v in at.session_state['afinidades'].values())

def test_desmarcar_competencia_zera_nivel():
    at=AppTest.from_file(APP).run();clicar(at,'continuar_1')
    at.multiselect(key='competencias_selecionadas').set_value(['git']).run()
    at.slider(key='nivel_git').set_value(4).run()
    at.multiselect(key='competencias_selecionadas').set_value([]).run()
    assert at.session_state['conhecimentos']['git']==0

def test_iniciador_usa_pasta_e_interpretador():
    with patch('iniciar.subprocess.call',return_value=0) as chamada:
        assert iniciar.main()==0
        args=chamada.call_args.args[0]
        assert args[:4]==[iniciar.sys.executable,'-m','streamlit','run']
        assert Path(args[4])==Path(APP)
        assert chamada.call_args.kwargs['cwd']==Path(APP).parent

def test_app_direto_delega():
    with patch('streamlit.runtime.scriptrunner.get_script_run_ctx',return_value=None),patch('iniciar.main',return_value=0) as main:
        with pytest.raises(SystemExit) as saida: runpy.run_path(APP,run_name='__main__')
        assert saida.value.code==0
        main.assert_called_once()

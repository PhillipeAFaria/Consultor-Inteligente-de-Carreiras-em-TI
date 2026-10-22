"""Execute: python -m streamlit run app.py"""
import json
import streamlit as st
from consultor.dominio import CARREIRAS, OPCOES
from consultor.servico import consultar

st.set_page_config(page_title='Consultor de Carreiras em TI', page_icon='🧭', layout='centered')
st.title('🧭 Qual caminho seguir em TI?')
st.write('Conte o que você gosta de fazer. O consultor cruza suas respostas com 25 regras e explica a recomendação.')
st.caption('Orientação educacional baseada em preferências; as pontuações são heurísticas, não probabilidades.')
with st.sidebar:
    st.header('Como funciona')
    st.write('1. Responda às cinco perguntas.\n2. Refine a preferência, se necessário.\n3. Veja a trilha, as regras e um plano inicial.')
    st.write('As respostas não são gravadas em arquivo pelo aplicativo.')
    if st.button('Reiniciar entrevista', key='reiniciar'):
        st.session_state.clear()
        st.rerun()

rotulos = {
 'matematica':'1. Qual é sua afinidade com matemática e estatística?',
 'atividade':'2. Qual atividade você gostaria de fazer no dia a dia?',
 'ferramenta':'3. Qual ferramenta ou linguagem você conhece melhor?',
 'entrega':'4. Que tipo de resultado você prefere entregar?',
 'objetivo':'5. Qual é seu objetivo profissional agora?'
}
respostas = {}
for campo, opcoes in OPCOES.items():
    respostas[campo] = st.selectbox(rotulos[campo], list(opcoes), index=None,
        placeholder='Selecione uma opção', format_func=opcoes.get, key=campo)
completas = all(v is not None for v in respostas.values())
st.progress(sum(v is not None for v in respostas.values())/5)
projeto = None
base = consultar(respostas) if completas else None
if base and base['pendente']:
    st.info('Seu perfil ainda permite mais de uma interpretação. Escolha o projeto que mais gostaria de experimentar.')
    # A chave muda com o perfil: uma escolha antiga não vale para respostas novas.
    assinatura = '|'.join(respostas.values())
    projeto = st.radio('Qual destes projetos desperta mais interesse?', base['candidatas'],
        index=None, format_func=lambda area:CARREIRAS[area]['projeto'], key='projeto_'+assinatura)
pronto = completas and (not base['pendente'] or projeto is not None)
if st.button('Ver minha recomendação', type='primary', disabled=not pronto, key='recomendar'):
    resultado = consultar(respostas, projeto)
    area = resultado['carreira']
    st.success('Trilha recomendada: '+CARREIRAS[area]['titulo'])
    st.subheader('Por que esta trilha?')
    for e in resultado['evidencias']:
        if e['carreira'] == area:
            st.write(f"**{e['regra']} · +{e['pontos']} pontos** — {e['motivo']}")
    st.subheader('Por onde começar')
    st.write(resultado['plano'])
    with st.expander('Auditar todas as regras disparadas e pontuações'):
        st.dataframe([{'Trilha':c['titulo'], 'Pontos':resultado['pontos'][a]} for a,c in CARREIRAS.items()], hide_index=True)
        st.json(resultado['evidencias'])
    st.download_button('Baixar diagnóstico em JSON', json.dumps(resultado,ensure_ascii=False,indent=2),
                       file_name='diagnostico-carreira.json', mime='application/json')

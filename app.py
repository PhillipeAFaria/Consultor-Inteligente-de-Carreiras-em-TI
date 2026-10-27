"""Interface em três etapas; execute iniciar.py no PyCharm."""
import json
import pandas as pd
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

if __name__=='__main__' and get_script_run_ctx(suppress_warning=True) is None:
    from iniciar import main
    raise SystemExit(main())

from consultor.base import carregar_base
from consultor.motor import avaliar
from consultor.roadmap import planejar
from consultor.relatorio import gerar_markdown

st.set_page_config(page_title='Carreiras em TI · Etapa 2',page_icon='🧭',layout='wide')
try:
    base=carregar_base()
except ValueError as exc:
    st.error(str(exc));st.stop()

st.title('🧭 Consultor Avançado de Carreiras em TI')
st.caption('Explore afinidades, compare trilhas e transforme lacunas em próximos passos.')
if 'passo' not in st.session_state:
    st.session_state.update(passo=1,afinidades={d:None for d in base['dimensoes']},
        conhecimentos={s:0 for s in base['competencias']},objetivo='primeiro',horas=6)
with st.sidebar:
    st.header('Seu percurso')
    for i,n in enumerate(['Perfil pessoal','Afinidades e conhecimentos','Objetivos de carreira','Compatibilidade e plano'],1):
        st.write(('→ ' if st.session_state.passo==i else '')+f'{i}. {n}')
    st.caption('Afinidade: 1 = muito baixa; 3 = moderada; 5 = muito alta. “Não sei ainda” registra incerteza.')
    st.caption('Conhecimento: 0 = não conheço; 1 = conceitos; 2 = exercícios com apoio; 3 = tarefas simples com autonomia; 4 = domínio consolidado.')
    if st.button('Reiniciar',key='reiniciar'):
        st.session_state.clear();st.rerun()
    st.caption('As respostas permanecem apenas na sessão até você exportar o relatório. Pontos não são probabilidades.')

passo=st.session_state.passo
st.progress(min(passo,3)/3,text=f'Etapa {min(passo,3)} de 3'+(' · resultado' if passo==4 else ''))

def ir(p):
    st.session_state.passo=p
    st.session_state.pop('analise',None)
    st.rerun()

def perguntas(etapa):
    for dim,d in base['dimensoes'].items():
        if d['etapa']!=etapa: continue
        opcoes=[None,1,2,3,4,5]
        valor=st.selectbox(d['nome'],opcoes,index=opcoes.index(st.session_state.afinidades[dim]),
            format_func=lambda x:'Não sei ainda' if x is None else f'{x} / 5',
            help=d['descricao'],key='afinidade_'+dim)
        st.session_state.afinidades[dim]=valor

if passo==1:
    st.subheader('1. Perfil pessoal e preferências de trabalho')
    st.write('Informe seu interesse por negócio, comunicação e pesquisa. Não há resposta certa ou errada.')
    perguntas(1)
    if st.button('Continuar',key='continuar_1',type='primary'): ir(2)
elif passo==2:
    st.subheader('2. Afinidades técnicas e conhecimentos atuais')
    afinidades,conhecimentos=st.tabs(['O que gosto de fazer','O que já consigo fazer'])
    with afinidades: perguntas(2)
    with conhecimentos:
        st.write('Marque somente as competências que conhece e indique seu nível atual. As demais ficam no nível 0.')
        nomes=base['competencias']
        conhecidas=st.multiselect('Competências que conheço',list(nomes),
            default=[s for s,v in st.session_state.conhecimentos.items() if v>0],
            format_func=lambda s:nomes[s]['nome'],key='competencias_selecionadas')
        atual={s:0 for s in nomes}
        for s in conhecidas:
            valor=st.slider(nomes[s]['nome'],1,4,max(1,st.session_state.conhecimentos[s]),key='nivel_'+s)
            atual[s]=valor
            st.caption(base['niveis_conhecimento'][str(valor)])
        st.session_state.conhecimentos=atual
    a,b=st.columns(2)
    if a.button('Voltar',key='voltar_2'): ir(1)
    if b.button('Continuar',key='continuar_2',type='primary'): ir(3)
elif passo==3:
    st.subheader('3. Objetivos de carreira')
    objetivos=list(base['objetivos'])
    st.session_state.objetivo=st.selectbox('Seu objetivo',objetivos,index=objetivos.index(st.session_state.objetivo),
        format_func=lambda o:base['objetivos'][o],key='objetivo_widget')
    st.session_state.horas=st.number_input('Horas de estudo por semana',min_value=1,max_value=40,value=st.session_state.horas,step=1,key='horas_widget')
    st.info('O plano compara suas competências com um referencial educacional de entrada Júnior. Isso não certifica senioridade profissional.')
    conhecidas=sum(v is not None for v in st.session_state.afinidades.values())
    st.write(f'Resumo: {conhecidas}/{len(base["dimensoes"])} afinidades informadas e {sum(v>0 for v in st.session_state.conhecimentos.values())} competências conhecidas.')
    with st.expander('Revisar afinidades'):
        st.table([{'Dimensão':base['dimensoes'][d]['nome'],'Resposta':v if v is not None else 'Não sei'} for d,v in st.session_state.afinidades.items()])
    a,b=st.columns(2)
    if a.button('Voltar',key='voltar_3'): ir(2)
    if b.button('Calcular compatibilidade',key='calcular',type='primary'):
        st.session_state.analise=avaliar(base,st.session_state.afinidades)
        st.session_state.passo=4;st.rerun()
else:
    analise=st.session_state.get('analise')
    if analise is None: ir(1)
    st.subheader('Seu mapa de compatibilidade')
    if analise['status']=='insuficiente':
        st.warning('Não há informação ou sinal de afinidade suficiente para uma indicação segura. Complete ou revise suas respostas. O ranking é provisório.')
    if len(analise['proximas'])>1:
        st.info('Há trilhas com resultados iguais ou próximos (até 1 ponto percentual). A ordem de exibição entre empatadas não significa preferência.')
    if analise['empate_no_corte']:
        st.caption('Outras trilhas estão empatadas com a terceira exibida; confira a matriz completa.')
    colunas=st.columns(3)
    for col,r in zip(colunas,analise['top3']):
        col.metric(f"Posição {r['posicao']} · {base['trilhas'][r['id']]['nome_curto']}",f"{r['compatibilidade']:.2f}%")
        col.caption(f"Cobertura: {r['cobertura']:.0f}% dos pesos respondidos")
    tabela=pd.DataFrame([{'Posição':r['posicao'],'Trilha':r['nome'],'Compatibilidade (%)':r['compatibilidade'],
        'Cobertura (%)':r['cobertura'],'Piso cauteloso (%)':r['piso_cauteloso'],'Teto otimista (%)':r['teto_otimista']} for r in analise['ranking']])
    grafico=tabela.copy()
    grafico['Trilha']=[base['trilhas'][r['id']]['nome_curto'] for r in analise['ranking']]
    st.bar_chart(grafico,x='Trilha',y='Compatibilidade (%)',horizontal=True,sort='-Compatibilidade (%)')
    st.dataframe(tabela,hide_index=True,use_container_width=True)
    st.caption('Percentuais independentes por trilha, sem obrigação de somar 100%. Respostas desconhecidas não somam contribuição no índice provisório. Piso e teto delimitam cenários possíveis usando os pesos e penalidades; não são intervalos estatísticos de confiança.')
    candidatas=[r['id'] for r in analise['ranking']]
    escolhida=st.selectbox('Escolha a trilha para desenvolver seu plano',candidatas,
        index=0 if analise['status']=='comparavel' else None,
        format_func=lambda t:base['trilhas'][t]['nome'],placeholder='Escolha uma trilha para explorar',key='trilha_plano')
    if escolhida:
        plano=planejar(base,escolhida,st.session_state.conhecimentos,st.session_state.horas,st.session_state.objetivo)
        st.subheader('Lacunas para o referencial Júnior')
        st.metric('Atendimento ao referencial de competências',f"{plano['atendimento_referencial']:.2f}%")
        st.caption('Indicador separado da afinidade. Usa os níveis declarados e não comprova aptidão ou senioridade.')
        if not plano['gaps']:
            st.success('Nenhuma lacuna no referencial declarado. Valide o domínio com o projeto de portfólio.')
        else:
            st.dataframe(pd.DataFrame(plano['gaps'])[['ordem','nome','atual','alvo','gap','horas','semana_inicio','semana_fim']],hide_index=True)
            for g in plano['gaps']:
                with st.expander(f"{g['ordem']}. {g['nome']} · nível {g['atual']} → {g['alvo']}"):
                    st.write(g['evidencia'])
                    st.caption('Pré-requisitos: '+(', '.join(base['competencias'][s]['nome'] for s in g['pre_requisitos']) or 'Nenhum'))
        st.write(f"Carga sugerida: **{plano['horas_estimadas']} horas**, cerca de **{plano['semanas_estimadas']} semanas** a {plano['horas_semana']} h/semana. Estimativa didática, sem garantia de prazo.")
        st.subheader('Projeto para o GitHub')
        st.markdown('**'+plano['projeto']['titulo']+'**')
        for criterio in plano['projeto']['criterios']: st.write('• '+criterio)
        st.write(plano['orientacao'])
        st.subheader('Certificações opcionais')
        for c in plano['certificacoes']:
            st.markdown(f"[{c['nome']}]({c['url']})")
            st.write(c['quando'])
        st.caption('Certificação não é requisito do referencial. Materiais oficiais podem ser gratuitos; exames podem ter custos. Consulte o emissor antes de investir.')
        with st.expander('Auditar cálculo da trilha escolhida'):
            r=next(r for r in analise['ranking'] if r['id']==escolhida)
            st.dataframe(pd.DataFrame(r['evidencias']),hide_index=True)
            st.write(f"Base ponderada: {r['base_percentual']:.4f}%; descontos: {r['desconto']} pontos percentuais.")
            st.json(r['penalidades'])
        pacote=dict(analise=analise,plano=plano,afinidades=st.session_state.afinidades,conhecimentos=st.session_state.conhecimentos)
        st.download_button('Baixar plano e ranking',gerar_markdown(analise,plano),'plano-carreira.md','text/markdown',key='baixar_md')
        st.download_button('Baixar diagnóstico JSON',json.dumps(pacote,ensure_ascii=False,indent=2),'diagnostico.json','application/json',key='baixar_json')
    if st.button('Editar respostas',key='editar'): ir(1)

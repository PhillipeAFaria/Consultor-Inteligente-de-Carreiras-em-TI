# Consultor Inteligente de Carreiras em TI

Sistema especialista para a atividade da Aula 08 de Inteligência Artificial, com motor **Experta**, encadeamento para frente e interface **Streamlit**. Recomenda uma das dez trilhas previstas no enunciado e apresenta os motivos da decisão.

## 1. Instalação e execução

Requer Python 3.10 ou superior. A versão efetivamente validada neste ambiente consta em `docs/validacao.md`. Abra o terminal na pasta que contém este README.

Windows (PowerShell), sem precisar ativar o ambiente:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Acesse o endereço local informado pelo Streamlit, normalmente `http://localhost:8501`. Para encerrar, pressione Ctrl+C no terminal. Também é possível usar `pip install -r requirements.txt` e `streamlit run app.py` com o ambiente virtual ativado.

Executar pelo terminal do PyCharm
python -m streamlit run app.py

## 2. Como utilizar

1. Responda às cinco perguntas sobre matemática, atividade diária, ferramenta conhecida, entrega de valor e objetivo profissional.
2. Se faltarem evidências ou houver proximidade entre trilhas, escolha o projeto que mais gostaria de experimentar. A pergunta aparece dinamicamente.
3. Clique em **Ver minha recomendação**. O resultado contém uma única trilha, justificativas identificadas por regra e um plano inicial de estudos.
4. Abra a seção de auditoria para consultar todas as evidências, inclusive de trilhas concorrentes. O diagnóstico pode ser baixado em JSON.
5. Use **Reiniciar entrevista** para começar novamente.

## 3. Engenharia de conhecimento

A [matriz de decisão](docs/matriz_decisao.md) documenta todas as 25 regras:

- R01–R10: cruzam atividade e entrega de valor; Ciência de Dados também exige afinidade matemática média ou alta. Valem 8 pontos.
- R11–R20: cruzam atividade e ferramenta conhecida; Ciência de Dados também considera matemática. Valem 4 pontos.
- R21–R25: tratam cinco pares de projetos, abrangendo as dez trilhas. A escolha explícita de um projeto produz 20 pontos para a trilha correspondente.

As preferências vêm do enunciado; os pesos, o limiar de decisão e as personas foram definidos neste projeto para demonstrar o raciocínio. A base é educacional e não resulta de entrevistas com especialistas de mercado.

Cada entrevista cria um novo `MotorCarreiras`. O serviço executa `reset()`, declara um `Perfil` e, quando necessário, um `Projeto`, e chama `run()`. Os decoradores `@Rule` são condições reais do Experta; suas ações declaram fatos `Evidencia`. O serviço consolida esses fatos e resolve a decisão após o motor terminar, sem depender da ordem de disparo.

O líder precisa de pelo menos 8 pontos e vantagem superior a 4 para uma recomendação direta. Caso contrário, a interface solicita um projeto entre as trilhas próximas; sem evidências, apresenta as dez. Sem essa resposta, o diagnóstico permanece pendente. Os 20 pontos da preferência explícita superam o máximo inicial de 12 por trilha. Não existe desempate alfabético nem aleatório. A ordenação alfabética interna só estabiliza a apresentação de pontuações iguais.

**Exemplo:** alguém que gosta de analisar dados e conhece Python pode ativar evidências para Ciência de Dados e Engenharia de Dados. A preferência por previsões favorece Ciência; a preferência por pipelines e infraestrutura favorece Engenharia. Se a entrega ainda for desconhecida, o projeto adicional resolve a ambiguidade.

O objetivo profissional adapta o plano de estudos. Conhecer uma ferramenta não é pré-requisito de entrada: as primeiras dez regras permitem recomendar a iniciantes. Pontos não representam probabilidade, diagnóstico psicológico ou garantia de emprego. Se Ciência de Dados for escolhida com matemática baixa, o plano recomenda reforço de fundamentos.

## 4. Organização

```text
app.py                       Interface Streamlit
carreiras.json               Descrições, projetos e estudos das dez trilhas
consultor/dominio.py         Vocabulário e validação de entradas
consultor/motor.py           Classes Fact e 25 regras @Rule
consultor/servico.py         Execução do motor e consolidação da recomendação
personas.json                Dez perfis fictícios com resultados esperados
validar_personas.py          Validação das personas pelo terminal
tests/                      Testes de inferência e interação Streamlit
docs/matriz_decisao.md       Condições, conclusões, pesos e conflitos
docs/validacao.md            Ambiente e resultados efetivamente executados
requirements.txt            Dependências da aplicação
requirements-dev.txt        Dependências adicionais de teste
```

## 5. Validar

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe validar_personas.py
.\.venv\Scripts\python.exe -m pytest -q
```

As personas cobrem as dez trilhas, incluindo os quatro grupos mínimos pedidos: analítico, infraestrutura/segurança, visual e negócios/produto. Os testes verificam também conflitos, matemática baixa, ausência de experiência, isolamento entre consultas, validação das entradas e fluxos da interface. Os testes de interface usam `AppTest`, que simula a interação Streamlit; não substituem uma inspeção visual no navegador.

## 6. Compatibilidade do Experta

`experta==1.9.4` depende de `frozendict==1.2`, que referencia `collections.Mapping`, nome removido do módulo `collections` no Python 3.10. Antes de importar Experta, `consultor/motor.py` disponibiliza esse alias a partir de `collections.abc.Mapping`, somente quando ele estiver ausente. Essa adaptação fica no processo da aplicação e não modifica a biblioteca instalada. Não substituímos Experta por um motor próprio. O projeto deve importar Experta por esse módulo para respeitar a ordem de inicialização.



# Sistema Especialista para Compatibilidade e Trilha de Carreira em TI

## 1. Objetivo

Desenvolver um consultor que reconheça perfis multifacetados e produza um ranking de carreiras, uma análise de competências e um plano individualizado. A Etapa 2 utiliza motor próprio de soma ponderada, opção expressamente permitida pelo enunciado, em vez de limitar a entrevista a uma recomendação binária.

## 2. Engenharia do conhecimento

A base externa JSON descreve 12 dimensões de afinidade, dez trilhas, 32 competências, níveis-alvo Júnior, pré-requisitos, estimativas de estudo, projetos e certificações opcionais. Há 11 regras de penalidade, incluindo uma regra cruzada que identifica interesse alto em automação combinado com baixa afinidade por infraestrutura.

As correlações foram propostas para esta atividade, sem entrevistas com especialistas ou calibração empírica. Dados e matemática ganham mais peso em Ciência de Dados; integração, dados e infraestrutura em Engenharia de Dados. DevOps destaca automação e operação; Cloud prioriza arquitetura de infraestrutura. As demais trilhas diferem por lógica, visual, segurança, mobile, qualidade e negócio.

## 3. Inferência e tratamento da incerteza

As respostas graduais vão de 1 a 5. A normalização `(resposta - 1) / 4` transforma afinidade mínima em 0 e máxima em 1. Cada valor multiplica o peso da dimensão, e a soma é dividida pelo máximo da própria trilha. Penalidades declarativas são descontadas em pontos percentuais, com resultado limitado ao intervalo 0–100.

“Não sei ainda” é armazenado como `None`. O valor desconhecido não soma contribuição nem ativa penalidade. A cobertura considera os pesos respondidos. O piso cauteloso usa contribuição zero para desconhecidos e todos os descontos ainda possíveis; o teto otimista usa a contribuição máxima dos desconhecidos e apenas descontos já observados. São limites heurísticos, possivelmente amplos, e não intervalos de confiança.

O ranking apresenta as dez trilhas e um Top 3. Empates na precisão exibida compartilham posição; diferenças de até 1 ponto percentual são sinalizadas como próximas. Empate no corte do Top 3 é informado. Cobertura menor que 60% em qualquer entrada do Top 3 ou ausência de resultado positivo torna a comparação insuficiente; não há escolha automática de um plano nesse caso. O usuário ainda pode escolher uma trilha para explorar.

## 4. Gaps e plano de ação

O conhecimento utiliza escala própria de 0 a 4. Para cada competência, calcula-se `gap = máximo(0, nível-alvo - nível-atual)`. O indicador de atendimento ao referencial soma os níveis alcançados, limitados ao alvo, ponderados por prioridade, e divide pelo total requerido. Esse indicador é separado da compatibilidade por afinidade.

Pré-requisitos são incluídos no plano. Uma ordenação topológica garante que fundamentos apareçam antes das competências dependentes; entre opções liberadas, priorizam-se maior prioridade, maior gap e ID para estabilizar a apresentação. Competências já atendidas são omitidas do estudo.

As horas de cada módulo são estimadas proporcionalmente à lacuna. A soma, dividida pelas horas semanais, determina o cronograma sugerido. O plano inclui evidência prática por competência, projeto com critérios de aceite e uma orientação adaptada ao objetivo profissional. Certificações são opcionais: os links oficiais permitem verificar conteúdo e condições antes de qualquer investimento. O referencial não declara que alguém já possui senioridade Júnior no mercado.

## 5. Interface e arquitetura

O wizard Streamlit divide a entrevista em perfil pessoal, afinidades/conhecimentos e objetivos. O resultado combina métricas, barras, tabela completa, roadmap e auditoria das contribuições e penalidades. Respostas são preservadas ao voltar às etapas; editar invalida o resultado anterior; reiniciar limpa a sessão. Relatórios podem ser baixados em Markdown e JSON.

O módulo `base.py` carrega e valida o conhecimento, incluindo referências e ciclos. `motor.py` calcula afinidades. `roadmap.py` gera gaps e sequência de estudo. `relatorio.py` exporta os resultados. O código não executa condições arbitrárias: somente os operadores declarativos permitidos, `le` e `ge`, são aceitos. `iniciar.py` facilita o uso no PyCharm.

## 6. Validação e limitações

Foram aprovados 71 testes e dez personas ideais, uma por carreira. A suíte cobre cálculo manual, alteração de pesos no JSON, empates, perfis mistos, valores extremos, desconhecidos, penalidades, intervalos, entradas inválidas, bases malformadas, roadmap e navegação. Um fluxo com perfil de teste de negócios/produto também foi percorrido no navegador, com ranking, gráfico e plano gerados.

Os resultados demonstram consistência com a base proposta, sem validar precisão vocacional em uma população externa. Afinidades e competências são autoavaliações. Os pesos, as penalidades e os prazos são heurísticos. As estimativas não garantem aprendizagem, emprego ou aprovação em certificações. Uma próxima validação pode envolver especialistas de cada trilha e usuários externos.

## 7. Atendimento às fases

| Fase | Arquivos e evidências |
|---|---|
| 1. Conhecimento e JSON | `base/regras_carreiras.json`, `docs/matriz_decisao.md` |
| 2. Motor ponderado | `consultor/motor.py`, contribuições e penalidades auditáveis |
| 3. Gaps e roadmap | `consultor/roadmap.py`, pré-requisitos e projeto por trilha |
| 4. Interface | `app.py`, wizard, Top 3, barras e exportação |
| 5. Robustez | `tests/`, `dados/personas.json`, `docs/validacao.md` |

## 8. Referências

- Material fornecido: *Trabalho Etapa 2.pdf*, Inteligência Artificial, UNIPAC Barbacena, 22/10/2026.
- [Streamlit: testes de aplicação](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest).
- [Microsoft: Azure Fundamentals](https://learn.microsoft.com/credentials/certifications/azure-fundamentals/).
- [Microsoft: Azure Data Fundamentals](https://learn.microsoft.com/certifications/azure-data-fundamentals/).
- [ISC2: Certified in Cybersecurity](https://www.isc2.org/certifications/cc).
- [ISTQB: certificações](https://istqb.org/certifications/).
- [Scrum.org: certificações profissionais](https://www.scrum.org/professional-scrum-certifications).

Os links de certificação foram conferidos em 27/10/2026. A base contém descrições resumidas elaboradas para a atividade; o PDF original não é redistribuído no pacote.

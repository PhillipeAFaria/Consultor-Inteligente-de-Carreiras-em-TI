# Matriz de decisão

Todas as condições de uma linha são conjunções (E). `|` representa OU. As regras R01–R20 cruzam dimensões do perfil. R21–R25 refinam a decisão com a escolha explícita de um projeto. Nenhuma linguagem isolada determina uma carreira.

| Regra | Condições SE | Conclusão ENTÃO | Pontos |
|---|---|---|---|
| R01 | atividade=logica; entrega=servicos | Desenvolvimento Back-end | 8 |
| R02 | atividade=visual; entrega=interface | Desenvolvimento Front-end & UI/UX | 8 |
| R03 | atividade=dados; entrega=previsoes; matemática=média ou alta | Ciência de Dados e Machine Learning | 8 |
| R04 | atividade=pipelines ou dados; entrega=infra_dados | Engenharia de Dados | 8 |
| R05 | atividade=seguranca; entrega=protecao | Cibersegurança (Security / Pentesting) | 8 |
| R06 | atividade=automacao ou arquitetura; entrega=operacao | DevOps & SRE | 8 |
| R07 | atividade=arquitetura; entrega=infraestrutura | Computação em Nuvem (Cloud Architecture) | 8 |
| R08 | atividade=apps ou visual; entrega=aplicativo | Desenvolvimento Mobile | 8 |
| R09 | atividade=testes ou logica; entrega=qualidade | Engenharia de Qualidade e Testes (QA) | 8 |
| R10 | atividade=negocio; entrega=produto | Gestão de Produtos (Product Management) | 8 |
| R11 | atividade=logica; ferramenta=python ou java | Desenvolvimento Back-end | 4 |
| R12 | atividade=visual; ferramenta=javascript ou design | Desenvolvimento Front-end & UI/UX | 4 |
| R13 | atividade=dados; ferramenta=python ou estatistica; matemática=média ou alta | Ciência de Dados e Machine Learning | 4 |
| R14 | atividade=pipelines ou dados; ferramenta=python ou sql | Engenharia de Dados | 4 |
| R15 | atividade=seguranca; ferramenta=linux ou seguranca | Cibersegurança (Security / Pentesting) | 4 |
| R16 | atividade=automacao ou arquitetura; ferramenta=linux ou containers | DevOps & SRE | 4 |
| R17 | atividade=arquitetura; ferramenta=cloud ou linux | Computação em Nuvem (Cloud Architecture) | 4 |
| R18 | atividade=apps ou visual; ferramenta=mobile ou javascript | Desenvolvimento Mobile | 4 |
| R19 | atividade=testes ou logica; ferramenta=testes ou python | Engenharia de Qualidade e Testes (QA) | 4 |
| R20 | atividade=negocio; ferramenta=gestao ou design | Gestão de Produtos (Product Management) | 4 |
| R21 | projeto escolhido=ciencia ou engenharia | Trilha correspondente ao projeto escolhido | 20 |
| R22 | projeto escolhido=devops ou cloud | Trilha correspondente ao projeto escolhido | 20 |
| R23 | projeto escolhido=frontend ou mobile | Trilha correspondente ao projeto escolhido | 20 |
| R24 | projeto escolhido=backend ou qa | Trilha correspondente ao projeto escolhido | 20 |
| R25 | projeto escolhido=seguranca ou produto | Trilha correspondente ao projeto escolhido | 20 |

## Resolução de conflitos

1. Cada regra dispara no máximo uma vez por consulta, com um único Perfil e, opcionalmente, um Projeto.
2. O serviço soma os fatos Evidencia por trilha após `run()`. A ordem da agenda não decide o vencedor.
3. Recomenda diretamente se o líder tem pelo menos 8 pontos e uma vantagem superior a 4 pontos.
4. Caso contrário, pergunta qual projeto o usuário prefere entre as trilhas a até 4 pontos do líder; sem evidências, apresenta as dez.
5. A resposta gera um fato Projeto e uma nova execução do motor. Seus 20 pontos superam o máximo inicial de 12, resolvendo o empate por uma preferência informada.
6. Sem resposta de refinamento, o resultado fica pendente; não há desempate alfabético ou indicação aleatória.

## Interpretação e limites

Os pesos são heurísticos definidos para este trabalho; não foram calibrados com dados de profissionais. Pontos não são probabilidades, aptidão medida nem garantia de emprego. Matemática baixa não é exclusão profissional: para Ciência de Dados, um projeto escolhido pode indicar interesse, acompanhado de uma orientação de estudos. O objetivo profissional adapta o plano inicial; não é uma condição de exclusão de carreiras. Ferramentas são evidências secundárias e iniciantes podem receber indicação pelas preferências de atividade e entrega.

Ciência de Dados prioriza previsões e estatística; Engenharia de Dados prioriza pipelines e infraestrutura. DevOps prioriza entrega contínua e confiabilidade operacional; Cloud prioriza planejamento de arquitetura. Front-end se diferencia de Mobile pelo contexto web versus dispositivos. Back-end se diferencia de QA pela entrega de serviços versus verificação de qualidade. Segurança e Produto possuem atividades e entregas específicas. O agrupamento R25 apenas reúne duas escolhas remanescentes, sem afirmar proximidade conceitual entre elas.

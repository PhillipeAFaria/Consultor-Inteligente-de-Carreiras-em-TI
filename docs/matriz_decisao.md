# Matriz de pesos e regras

Fonte de execução: `base/regras_carreiras.json`. Esta tabela documenta a base entregue; ao alterar o JSON, revise a documentação. Pesos não são percentuais: cada trilha é normalizada pela própria soma.

| Trilha | Dimensões e pesos | Soma |
|---|---|---:|
| Desenvolvimento Back-end | Lógica e programação = 6; Dados e informação = 2; Qualidade e investigação = 1; Automação e operação = 1 | 10 |
| Desenvolvimento Front-end & UI/UX | Design visual e experiência = 6; Comunicação e colaboração = 2; Lógica e programação = 2; Pesquisa e experimentação = 1 | 11 |
| Ciência de Dados e Machine Learning | Matemática e estatística = 4; Dados e informação = 4; Pesquisa e experimentação = 2; Lógica e programação = 1 | 11 |
| Engenharia de Dados | Dados e informação = 4; Infraestrutura e redes = 3; Automação e operação = 3; Lógica e programação = 2 | 12 |
| Cibersegurança | Segurança digital = 7; Infraestrutura e redes = 3; Lógica e programação = 2; Pesquisa e experimentação = 1 | 13 |
| DevOps & SRE | Automação e operação = 5; Infraestrutura e redes = 4; Qualidade e investigação = 2; Lógica e programação = 1 | 12 |
| Computação em Nuvem (Cloud Architecture) | Infraestrutura e redes = 6; Comunicação e colaboração = 2; Automação e operação = 2; Segurança digital = 1 | 11 |
| Desenvolvimento Mobile | Aplicativos móveis = 7; Design visual e experiência = 2; Lógica e programação = 2; Qualidade e investigação = 1 | 12 |
| Engenharia de Qualidade e Testes (QA) | Qualidade e investigação = 7; Lógica e programação = 2; Automação e operação = 2; Comunicação e colaboração = 1 | 12 |
| Gestão de Produtos (Product Management) | Negócio e produto = 7; Comunicação e colaboração = 4; Pesquisa e experimentação = 3; Design visual e experiência = 1 | 15 |

## Penalidades declarativas

Todas as condições de uma regra são ligadas por E. Desconhecido não satisfaz nenhuma condição.

| Regra | Condições | Trilhas | Desconto (p.p.) |
|---|---|---|---:|
| P_backend | Lógica e programação ≤ 2 | backend | 10 |
| P_frontend | Design visual e experiência ≤ 2 | frontend | 10 |
| P_ciencia | Matemática e estatística ≤ 2 | ciencia | 10 |
| P_engenharia | Dados e informação ≤ 2 | engenharia | 10 |
| P_seguranca | Segurança digital ≤ 2 | seguranca | 10 |
| P_devops | Automação e operação ≤ 2 | devops | 10 |
| P_cloud | Infraestrutura e redes ≤ 2 | cloud | 10 |
| P_mobile | Aplicativos móveis ≤ 2 | mobile | 10 |
| P_qa | Qualidade e investigação ≤ 2 | qa | 10 |
| P_produto | Negócio e produto ≤ 2 | produto | 10 |
| P_cloud_operacao | Infraestrutura e redes ≤ 2 E Automação e operação ≥ 4 | cloud, devops | 5 |

## Exemplo auditável

Back-end: lógica = 5; dados, qualidade e automação = 3. Após normalização, as contribuições ponderadas são 6 × 1 + 2 × 0,5 + 1 × 0,5 + 1 × 0,5 = 8. Dividindo por 10 e multiplicando por 100, a base é 80%. A penalidade de lógica baixa não dispara, logo a aderência final é 80%.

Com todas as afinidades em 3, todas as trilhas atingem 50%. Essa é uma resposta neutra e empatada, não uma preferência descoberta pelo sistema.

## Conhecimento e referencial Júnior

Escala: 0 = não conheço; 1 = reconheço conceitos; 2 = exercícios com apoio; 3 = tarefas simples com autonomia; 4 = aplicação consolidada. Cada trilha define níveis-alvo e prioridades no JSON. Os pré-requisitos ausentes do referencial direto são acrescentados com nível-alvo 2 e prioridade 3. Esses dois padrões são parâmetros estruturais do algoritmo, não pesos de compatibilidade.

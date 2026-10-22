# Relatório de validação

Validação executada em 22/10/2026.

## Ambiente efetivamente testado

- Windows, Python 3.12.14.
- Experta 1.9.4, frozendict 1.2, schema 0.6.7.
- Streamlit 1.66.1, pytest 9.1.1.
- Ambiente virtual isolado; nenhuma alteração no Python global do usuário.

O projeto declara Python 3.10 ou superior, mas somente Python 3.12.14 foi executado neste trabalho. O alias `collections.Mapping` permitiu executar o Experta com sua dependência original, sem alterar arquivos instalados.

## Resultados

| Verificação | Resultado observado |
|---|---|
| `python validar_personas.py` | 10/10 personas aprovadas |
| `python -m pytest -q` | 35 testes aprovados em 4,74 segundos |
| Quantidade de regras no motor | 25 regras Experta |
| `pip check` no ambiente de teste | Nenhum requisito incompatível |

Os 35 testes incluem 32 verificações do motor e 3 fluxos da interface Streamlit. As dez personas são fictícias e foram elaboradas junto da matriz: os resultados demonstram consistência com a base definida, sem constituir uma avaliação externa da precisão vocacional.

## Personas

| Persona | Perfil | Trilha esperada e obtida |
|---|---|---|
| Bruno | Lógica, serviços e Python | Back-end |
| Clara | Visual, interface e JavaScript | Front-end & UI/UX |
| Ana | Análise de dados, matemática alta e Python | Ciência de Dados e Machine Learning |
| Diego | Pipelines, infraestrutura de dados e Python | Engenharia de Dados |
| Eva | Segurança, proteção e Linux | Cibersegurança |
| Fábio | Automação, disponibilidade e Linux | DevOps & SRE |
| Gabriela | Arquitetura, infraestrutura e nuvem | Cloud Architecture |
| Hugo | Aplicativos, dispositivos móveis e ferramentas mobile | Desenvolvimento Mobile |
| Iara | Investigação de falhas, qualidade e ferramentas de testes | QA |
| João | Negócio, produto e gestão | Product Management |

Os detalhes das cinco respostas de cada persona estão em `personas.json`.

## Casos adicionais

- Perfil iniciante com preferências claras recebe recomendação sem precisar conhecer uma linguagem.
- Perfil exploratório, sem evidências suficientes, permanece pendente e apresenta a pergunta de projeto.
- Perfil de dados com Python e entrega indefinida ativa evidências de Ciência e Engenharia de Dados; a escolha adicional resolve o empate.
- As cinco regras de refinamento foram exercitadas para as dez trilhas.
- Matemática baixa não ativa as regras iniciais de Ciência de Dados; a escolha explícita de um projeto dessa área produz recomendação e orientação de reforço em fundamentos.
- Objetivos de primeira oportunidade, transição e especialização adaptam o plano inicial.
- Consultas independentes não compartilham evidências.
- Entradas ausentes, desconhecidas ou fora do vocabulário são rejeitadas.
- AppTest confirmou o bloqueio do botão com respostas incompletas, indicação de Back-end, reinício da entrevista, refinamento para Produto e invalidação de uma escolha antiga após mudança nas respostas.

## Limites da verificação

Os testes da interface foram executados pelo `streamlit.testing.v1.AppTest`, sem inspeção visual em navegador. O sandbox bloqueava sockets locais usados pelo asyncio; os testes passaram ao serem executados com essa restrição removida. Isso não exigiu alteração na lógica da aplicação.

Não foram realizados deploy público, teste de carga, publicação no GitHub ou validação com profissionais externos. A documentação contém os comandos para instalação, execução e publicação do repositório.

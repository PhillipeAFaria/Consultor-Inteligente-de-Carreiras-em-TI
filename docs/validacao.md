# Validação da entrega — Etapa 2

Data: **27/10/2026**.

## 1. Ambiente

Windows, Python 3.12.14, Streamlit 1.66.1, Pandas 3.1.0 e pytest 9.1.1. Os testes utilizaram um ambiente virtual de trabalho separado dos arquivos da entrega. Não foram executados testes em Python 3.10 ou 3.11.

## 2. Resultados observados

| Verificação | Resultado |
|---|---|
| `python -m pytest -q` | 71 testes aprovados |
| `python validar_personas.py` | Dez de dez personas com a primeira trilha esperada, sem empate no topo |
| Interface simulada | Wizard, voltar, manter respostas, editar, reiniciar e selecionar plano aprovados com AppTest |
| Navegador local | Fluxo de negócios/produto percorrido; ranking, gráfico e roadmap exibidos |

Os dez perfis ideais em `dados/personas.json` geram 100% para sua trilha correspondente. Isso é esperado pela construção das fixtures e pela normalização, não uma taxa de acerto em usuários reais. Casos mistos, desconhecidos e conflitantes são testados separadamente na suíte.

## 3. Cobertura funcional

- Cálculo manual de 80% para Back-end em um perfil de referência.
- Empate neutro de 50% entre as dez trilhas e empate no corte do Top 3.
- Extremos 1 e 5, ausência total de informação e perfis mistos de dados/web, infraestrutura/automação e lógica/qualidade.
- Penalidades simples e cruzadas, com registro das condições observadas.
- Limites cauteloso/otimista verificados contra todos os 25 preenchimentos de duas respostas desconhecidas.
- Rejeição de números fora da escala, booleanos, NaN, infinito, campos ausentes e extras.
- Rejeição de peso negativo, soma zero, referência inexistente, ciclo de pré-requisitos, regra duplicada, operador desconhecido e JSON inválido.
- Mudança de peso no JSON altera o resultado sem modificar o motor.
- Roadmap das dez trilhas com dependências válidas, redução de gaps pelo conhecimento, adaptação às horas semanais e ausência de estudo desnecessário quando o referencial é atendido.
- Exportação de ranking, auditoria, plano e certificação; inicialização com o interpretador configurado.

## 4. Limites

Não houve validação com especialistas ou usuários externos, teste de carga, deploy público ou publicação automática no GitHub. A inspeção em navegador cobriu um cenário de teste; os demais fluxos foram exercitados por testes automatizados. As chamadas do iniciador e a delegação direta de `app.py` foram verificadas com substituição controlada de subprocessos.

A captura `capturas/compatibilidade.png` registra a inspeção do ranking no navegador. No cenário observado, Produto obteve 93,33%, Front-end/UX 17,27% e Ciência de Dados 8,18%, com empate de Cloud no terceiro lugar devidamente informado.

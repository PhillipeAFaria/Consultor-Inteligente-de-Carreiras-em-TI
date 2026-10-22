"""Vocabulário da entrevista, compartilhado pela interface e validação."""
import json
from pathlib import Path

CARREIRAS = json.loads((Path(__file__).resolve().parents[1] / 'carreiras.json').read_text(encoding='utf-8'))
OPCOES = {
 'matematica': {'baixa':'Baixa', 'media':'Média', 'alta':'Alta'},
 'atividade': {
  'logica':'Escrever algoritmos e regras de negócio', 'visual':'Criar layouts e experiências visuais',
  'dados':'Analisar dados e procurar padrões', 'pipelines':'Integrar e organizar grandes volumes de dados',
  'seguranca':'Investigar ameaças e proteger sistemas', 'automacao':'Automatizar deploys e operar serviços',
  'arquitetura':'Planejar servidores e arquitetura de infraestrutura', 'apps':'Criar aplicativos para celulares',
  'testes':'Investigar falhas e automatizar testes', 'negocio':'Entender necessidades e priorizar soluções',
  'explorar':'Ainda estou explorando'},
 'ferramenta': {
  'python':'Python', 'java':'Java / C#', 'javascript':'JavaScript / TypeScript', 'design':'Figma / design',
  'estatistica':'R / estatística', 'sql':'SQL / bancos de dados', 'linux':'Linux / redes',
  'seguranca':'Ferramentas de segurança', 'containers':'Docker / CI/CD', 'cloud':'AWS / Azure / GCP',
  'mobile':'Flutter / Kotlin / Swift', 'testes':'pytest / Selenium / testes', 'gestao':'Métricas / gestão ágil',
  'iniciante':'Nenhuma / iniciante'},
 'entrega': {
  'servicos':'Serviços, APIs e regras de negócio', 'interface':'Interface e experiência de uso na web',
  'previsoes':'Análises, previsões e modelos de IA', 'infra_dados':'Pipelines e infraestrutura de dados',
  'protecao':'Proteção contra ataques', 'operacao':'Deploys confiáveis e serviços disponíveis',
  'infraestrutura':'Arquitetura de infraestrutura escalável', 'aplicativo':'Aplicativo para dispositivos móveis',
  'qualidade':'Software confiável e defeitos detectados', 'produto':'Valor de negócio e prioridades do produto',
  'explorar':'Ainda não sei'},
 'objetivo': {'primeiro':'Conseguir a primeira oportunidade', 'transicao':'Mudar de área', 'aprofundar':'Aprofundar minha especialização'}
}

def validar(respostas):
    if set(respostas) != set(OPCOES):
        raise ValueError('Informe exatamente as cinco dimensões da entrevista.')
    for campo, valor in respostas.items():
        if not isinstance(valor, str) or valor not in OPCOES[campo]:
            raise ValueError(f'Resposta inválida para {campo}.')
    return dict(respostas)

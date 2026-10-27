"""Exportação de resultado completo e legível."""
def gerar_markdown(analise,plano):
    linhas=['# Consultor Avançado de Carreiras em TI','',
        'Percentuais de aderência heurística; não são probabilidade de contratação.',
        '', '## Ranking de compatibilidade', '| Posição | Trilha | Aderência | Cobertura |', '|---|---|---|---|']
    for r in analise['ranking']:
        linhas.append(f"| {r['posicao']} | {r['nome']} | {r['compatibilidade']:.2f}% | {r['cobertura']:.2f}% |")
    if analise['empate_no_corte']: linhas+=['','Há outras trilhas empatadas com a terceira colocada.']
    if analise['status']=='insuficiente': linhas+=['','Informações insuficientes para uma comparação segura; complete as afinidades.']
    linhas+=['','## Trilha escolhida',plano['trilha'],'',
        f"Atendimento ao referencial Júnior: {plano['atendimento_referencial']:.2f}% (autoavaliação).",'',
        '## Lacunas e roadmap']
    if not plano['gaps']: linhas.append('Nenhuma lacuna no referencial declarado. Valide o domínio por um projeto prático.')
    for g in plano['gaps']:
        linhas.append(f"{g['ordem']}. **{g['nome']}**: nível {g['atual']} → {g['alvo']}; {g['horas']} h estimadas; semanas {g['semana_inicio']}–{g['semana_fim']}. Evidência: {g['evidencia']}")
    linhas+=['',f"Carga estimada: {plano['horas_estimadas']} horas; {plano['semanas_estimadas']} semanas a {plano['horas_semana']} h/semana. Estimativa didática, sem garantia de prazo.",
        '', '## Projeto de portfólio',plano['projeto']['titulo']]
    linhas += ['- '+c for c in plano['projeto']['criterios']]
    linhas += ['',plano['orientacao'],'','## Certificações opcionais']
    for c in plano['certificacoes']: linhas.append(f"- [{c['nome']}]({c['url']}): {c['quando']}")
    linhas+=['','Treinamentos oficiais podem ser gratuitos; exames podem ter custos. Verifique as condições no site oficial.','',
        '## Auditoria das regras']
    for r in analise['ranking']:
        linhas += ['',f"### {r['nome']}",f"Base: {r['base_percentual']:.4f}; descontos: {r['desconto']} pontos percentuais."]
        for e in r['evidencias']:
            linhas.append(f"- {e['nome']}: resposta={e['resposta']}, peso={e['peso']}, contribuição={e['contribuicao']:.4f} p.p.")
        for p in r['penalidades']: linhas.append(f"- Penalidade {p['id']} (-{p['pontos']} p.p.): {p['motivo']}")
    return '\n'.join(linhas)+'\n'

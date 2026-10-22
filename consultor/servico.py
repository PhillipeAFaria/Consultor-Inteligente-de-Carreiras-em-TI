"""Valida entradas, executa Experta e consolida evidências de forma determinística."""
from .dominio import CARREIRAS, validar
from .motor import MotorCarreiras, Perfil, Projeto, Evidencia

def consultar(respostas, projeto=None):
    respostas = validar(respostas)
    if projeto is not None and projeto not in CARREIRAS:
        raise ValueError('Projeto inválido.')
    motor = MotorCarreiras()
    motor.reset()
    motor.declare(Perfil(**respostas))
    if projeto is not None:
        motor.declare(Projeto(area=projeto))
    motor.run()
    evidencias = sorted([
        {k:f[k] for k in ('regra','carreira','pontos','motivo')}
        for f in motor.facts.values() if isinstance(f, Evidencia)
    ], key=lambda e:e['regra'])
    pontos = {area:sum(e['pontos'] for e in evidencias if e['carreira']==area) for area in CARREIRAS}
    ranking = sorted(pontos, key=lambda area:(-pontos[area], area))
    primeiro, segundo = ranking[:2]
    maior = pontos[primeiro]
    pendente = projeto is None and (maior < 8 or maior-pontos[segundo] <= 4)
    candidatas = [area for area in ranking if maior-pontos[area] <= 4] if maior else list(CARREIRAS)
    carreira = None if pendente else primeiro
    plano = None
    if carreira:
        inicio = {
          'primeiro':'Comece por fundamentos e construa um projeto pequeno para seu portfólio.',
          'transicao':'Mapeie suas habilidades transferíveis e construa um projeto de transição.',
          'aprofundar':'Aprofunde os fundamentos e implemente um projeto com maior complexidade.'
        }[respostas['objetivo']]
        plano = inicio + ' Estude: ' + CARREIRAS[carreira]['estudos'] + '.'
        if carreira == 'ciencia' and respostas['matematica'] == 'baixa':
            plano += ' Reforce matemática e estatística antes de avançar em modelagem.'
    return dict(carreira=carreira, pendente=pendente, candidatas=candidatas,
                pontos=pontos, evidencias=evidencias, plano=plano, respostas=respostas,
                projeto=projeto)

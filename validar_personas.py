"""Validação executável das dez personas, sem interface web."""
import json
from pathlib import Path
from consultor.servico import consultar

def main():
    personas = json.loads(Path(__file__).with_name('personas.json').read_text(encoding='utf-8'))
    erros = 0
    for persona in personas:
        r = consultar(persona['respostas'])
        ok = r['carreira'] == persona['esperado']
        erros += not ok
        print(f"{'OK' if ok else 'FALHA'} | {persona['nome']} | esperado={persona['esperado']} | obtido={r['carreira']}")
    print(f'{len(personas)-erros}/{len(personas)} personas aprovadas')
    return int(erros > 0)

if __name__ == '__main__':
    raise SystemExit(main())

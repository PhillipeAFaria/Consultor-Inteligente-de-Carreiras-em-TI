"""Executa as dez personas sem iniciar a interface web."""
import json
from pathlib import Path
from consultor.base import carregar_base
from consultor.motor import avaliar

def main():
    base=carregar_base()
    personas=json.loads((Path(__file__).resolve().parent/'dados/personas.json').read_text(encoding='utf-8'))
    erros=0
    for persona in personas:
        r=avaliar(base,persona['afinidades'])
        esperado=persona['esperado']
        ok=r['ranking'][0]['id']==esperado and len(r['proximas'])==1
        erros+=not ok
        print(f"{'OK' if ok else 'FALHA'} | {esperado} | obtido={r['ranking'][0]['id']} | {r['ranking'][0]['compatibilidade']}%")
    print(f'{len(personas)-erros}/{len(personas)} personas aprovadas')
    return int(erros>0)
if __name__=='__main__': raise SystemExit(main())

"""Execute este arquivo pelo botão Run do PyCharm."""
from pathlib import Path
import subprocess
import sys
def main():
    raiz=Path(__file__).resolve().parent
    try:
        return subprocess.call([sys.executable,'-m','streamlit','run',str(raiz/'app.py')],cwd=raiz)
    except KeyboardInterrupt:
        return 0
if __name__=='__main__':
    raise SystemExit(main())

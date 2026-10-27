import json
from pathlib import Path
import pytest
from consultor.base import carregar_base

@pytest.fixture
def base(): return carregar_base()

@pytest.fixture
def personas():
    return json.loads((Path(__file__).resolve().parents[1]/'dados/personas.json').read_text(encoding='utf-8'))

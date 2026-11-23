"""Roda todos os cadernos de resolvidos/ e mostra quais deram erro.

Uso (na raiz do repositório):  .venv\\Scripts\\python.exe ferramentas\\testar_cadernos.py
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

RAIZ = Path(__file__).resolve().parent.parent
import json
KERNEL = "ir" if json.loads((RAIZ / "ferramentas" / "livro.json").read_text(encoding="utf-8")).get("linguagem") == "r" else "python3"
erros = 0
for nb_path in sorted((RAIZ / "resolvidos").glob("*.ipynb")):
    nb = nbformat.read(nb_path, as_version=4)
    try:
        NotebookClient(nb, timeout=600, kernel_name=KERNEL,
                       resources={"metadata": {"path": str(nb_path.parent)}}).execute()
        print("ok  ", nb_path.name)
    except CellExecutionError as e:
        erros += 1
        print("ERRO", nb_path.name, "->", str(e).strip().splitlines()[-1][:200])
print("Erros:", erros)
sys.exit(1 if erros else 0)

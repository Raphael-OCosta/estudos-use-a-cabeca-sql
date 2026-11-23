"""Gera praticar/capXX_*.ipynb (para você escrever) e resolvidos/capXX_*.ipynb (gabarito).

Uso (na raiz do repositório):  .venv\\Scripts\\python.exe ferramentas\\gerar_cadernos.py
Lê ferramentas/livro.json (capítulos, seções e páginas do PDF) e comum/exercicios.py.
Nunca sobrescreve um caderno de praticar/ que já existe (para não apagar o que você escreveu).
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "comum"))
from exercicios import EXERCICIOS  # noqa: E402

LIVRO = json.loads((RAIZ / "ferramentas" / "livro.json").read_text(encoding="utf-8"))
KERNEL = {"python": {"name": "python3", "display_name": "Python 3 (.venv)", "language": "python"},
          "r": {"name": "ir", "display_name": "R", "language": "R"}}[LIVRO.get("linguagem", "python")]


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")[:40].strip("_")


def md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": s}


def code(s=""):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s}


def caderno(cells):
    for i, c in enumerate(cells):
        c["id"] = f"c{i:03d}"
    return {"cells": cells, "nbformat": 4, "nbformat_minor": 5,
            "metadata": {"kernelspec": KERNEL, "language_info": {"name": KERNEL["language"].lower()}}}


def prep(n, modo, recomecar):
    """Preparação do capítulo: cada caderno usa o esquema do seu capítulo no PostgreSQL."""
    return LIVRO["preparacao"].replace("{CAP}", str(n)).replace("{MODO}", modo).replace("{RECOMECAR}", recomecar)


usados = set()
for chave, info in LIVRO["capitulos"].items():
    n = int(chave)
    titulo = info["titulo"]
    nome = f"cap{n:02d}_{slug(titulo)}.ipynb"
    ex_cap = [(i, e) for i, e in enumerate(EXERCICIOS) if e[0] == n]
    cab = f"# Capítulo {n} — {titulo}\n\n**Livro:** começa na página **{info['pag']}** do PDF.\n\n"

    pratica = [md(cab + "**Como usar:**\n"
                  "1. Rode a célula **Preparação** (`Shift+Enter`).\n"
                  "2. Leia cada seção no livro. Nas seções com **Exercício**, escreva o código na célula vazia "
                  "(quando a 1ª linha já vier preenchida, como `%%sql`, digite o SQL embaixo dela).\n"
                  "3. Nas outras, use a célula **Anotações** para resumir com suas palavras (dois cliques para editar).\n\n"
                  f"**Travou?** O gabarito está em `../resolvidos/{nome}`. Tente antes de olhar."),
               md("## Preparação"), code(prep(n, "praticar", ""))]
    gabarito = [md(cab + "**Gabarito** dos exercícios do caderno de prática. Tente sozinho antes de olhar."),
                md("## Preparação"), code(prep(n, "gabarito", ", recomecar=True"))]

    # cada exercício vai só para a 1ª seção cujo título começa com o texto indicado
    dono = {}
    for i, e in ex_cap:
        dono[i] = next((s[1] for s in info["secoes"] if s[1].startswith(e[1])), None)
    for nivel, sec, pag in info["secoes"]:
        cabecalho = ("## " if nivel == 2 else "### ") + f"{sec} · PDF p. {pag}"
        pratica.append(md(cabecalho))
        exs = [(i, e) for i, e in ex_cap if dono.get(i) == sec]
        if sec.lower().startswith("resumo"):
            pratica.append(md("**Os 3 pontos mais importantes do capítulo, com suas palavras:**\n\n1. \n2. \n3. "))
            continue
        if not exs and sec.lower().startswith(("exercícios", "exercicios", "excercícios", "exercises")):
            pratica += [md("**Exercícios do livro:** resolva aqui (crie mais células com `Esc` + `B`)."), code()]
            continue
        if not exs:
            pratica.append(md("**Anotações:** _(dois cliques para escrever)_"))
            continue
        gabarito.append(md(cabecalho))
        for i, (_, _, nome_ex, enunciado, solucao) in exs:
            usados.add(i)
            # comandos mágicos (%%writefile, %%sql) já vêm na 1ª linha; o resto você digita
            inicio = solucao.split("\n", 1)[0] + "\n" if solucao.startswith("%%") else ""
            pratica += [md(f"#### Exercício: {nome_ex}\n\n{enunciado}"), code(inicio)]
            gabarito += [md(f"#### Exercício: {nome_ex}\n\n{enunciado}"), code(solucao)]

    if not info["secoes"]:
        pratica.append(md("**Anotações do capítulo:** _(dois cliques para escrever)_"))
    pratica.append(md("## Minhas anotações do capítulo\n\n- Aprendi:\n- Dúvidas:\n"))

    for pasta, cells, proteger in (("praticar", pratica, True), ("resolvidos", gabarito, False)):
        destino = RAIZ / pasta / nome
        destino.parent.mkdir(exist_ok=True)
        if proteger and destino.exists():
            print("já existe, mantido:", destino.relative_to(RAIZ))
            continue
        destino.write_text(json.dumps(caderno(cells), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"cap{n:02d}: {len(ex_cap)} exercícios -> {nome}")

sobrando = [EXERCICIOS[i][2] for i in range(len(EXERCICIOS)) if i not in usados]
print("Exercícios sem seção correspondente:", sobrando or "nenhum")

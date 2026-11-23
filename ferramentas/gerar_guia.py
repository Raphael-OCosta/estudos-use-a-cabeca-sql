"""Gera o guia de estudos em PDF (guia_pdf/guia.html -> Guia_de_Estudos.pdf) a partir de livro.json.

Uso (na raiz do repositório):  .venv\\Scripts\\python.exe ferramentas\\gerar_guia.py
Precisa do Microsoft Edge instalado (usa o modo headless para imprimir em PDF).
"""
import html
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "comum"))
from exercicios import EXERCICIOS  # noqa: E402

L = json.loads((RAIZ / "ferramentas" / "livro.json").read_text(encoding="utf-8"))
E = html.escape
R = L.get("linguagem", "python") == "r"
KERNEL = "R" if R else ".venv (Python 3.12)"
PASTA = RAIZ.name


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")[:40].strip("_")


linhas = []
for k, c in L["capitulos"].items():
    n = int(k)
    qtd = sum(1 for e in EXERCICIOS if e[0] == n)
    linhas.append(f"<tr><td>{n}</td><td>{E(c['titulo'])}</td><td>{c['pag']}</td>"
                  f"<td><code>cap{n:02d}_{slug(c['titulo'])}</code></td><td>{qtd or 'leitura'}</td></tr>")
total = len(EXERCICIOS)
paginas = L.get("paginas") or max(c["pag"] for c in L["capitulos"].values())

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:"Segoe UI",Calibri,Arial,sans-serif;color:#1f2933;font-size:11pt;line-height:1.55;margin:0}
.pg{break-after:page}
.capa{height:250mm;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(160deg,#1f4e79,#2f7d6d);color:#fff;border-radius:10px;padding:0 16mm}
.capa .tag{letter-spacing:.2em;text-transform:uppercase;font-size:10pt;opacity:.85}
.capa h1{font-size:30pt;margin:4mm 0 2mm;line-height:1.15}.capa h2{font-weight:400;font-size:15pt;margin:0 0 10mm;opacity:.95;border:0;color:#fff}
.capa .lema{font-size:13pt;border-left:4px solid #9fe0c9;padding-left:5mm;max-width:140mm}
h2{color:#1f4e79;font-size:18pt;margin:0 0 4mm;padding-bottom:2mm;border-bottom:2px solid #e6eef6}
h3{color:#1f4e79;font-size:13pt;margin:6mm 0 2mm}
code{font-family:Consolas,monospace;font-size:9.5pt;background:#f2f5f8;padding:0 4px;border-radius:3px}
kbd{border:1px solid #c9d2db;border-bottom-width:2px;border-radius:4px;padding:0 5px;font-size:9.5pt;background:#fff}
.passo{display:flex;gap:4mm;margin:0 0 3.5mm;break-inside:avoid}
.n{flex:0 0 9mm;height:9mm;border-radius:50%;background:#1f4e79;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700}
.ok{color:#2e7d5b;font-size:10pt}
.box{border-radius:7px;padding:3mm 5mm;margin:3mm 0;break-inside:avoid}
.dica{background:#e8f5ee;border-left:4px solid #2e7d5b}.aviso{background:#fff5df;border-left:4px solid #a86b00}
table{border-collapse:collapse;width:100%;font-size:10pt;margin:2mm 0}
th{background:#1f4e79;color:#fff;text-align:left;padding:2mm}td{padding:1.6mm 2mm;border-bottom:1px solid #e3e8ee}
tr:nth-child(even) td{background:#f7f9fb}
.linha{display:flex;gap:3mm;margin:2mm 0}.min{flex:0 0 22mm;font-weight:700;color:#2f7d6d}
"""

corpo = f"""
<section class="pg capa">
  <div class="tag">Guia de estudos · ler + praticar</div>
  <h1>{E(L['titulo'])}</h1>
  <h2>{E(L.get('subtitulo', ''))} — {E(L['autor'])}</h2>
  <p class="lema">A melhor forma de estudar um livro técnico: <b>ler um trecho e, em seguida, escrever o código com as próprias mãos</b>.
  Este guia mostra o caminho, do primeiro clique à rotina diária.</p>
</section>

<section class="pg">
  <h2>1. O método: ler e praticar</h2>
  <p>Ler sem praticar dá a sensação de que você entendeu. Praticar sem ler vira copiar e colar. Os dois juntos fixam o conteúdo:</p>
  <div class="passo"><div class="n">1</div><div><b>Leia</b> uma seção no PDF (o caderno diz a página).</div></div>
  <div class="passo"><div class="n">2</div><div><b>Escreva</b> a solução do exercício na célula vazia do caderno de <code>praticar/</code>. Errar faz parte.</div></div>
  <div class="passo"><div class="n">3</div><div><b>Confira</b> com o gabarito em <code>resolvidos/</code> só depois de tentar.</div></div>
  <div class="passo"><div class="n">4</div><div><b>Resuma</b> nas células com as suas palavras. Se não conseguir explicar, releia.</div></div>
  <div class="passo"><div class="n">5</div><div><b>Salve no GitHub</b> (commit + push): seu progresso fica registrado e público.</div></div>
  <h3>O que tem na pasta</h3>
  <table><tr><th>Pasta/arquivo</th><th>Para que serve</th></tr>
  <tr><td><code>praticar/</code></td><td>Cadernos com células vazias para <b>você</b> escrever.</td></tr>
  <tr><td><code>resolvidos/</code></td><td>Gabarito de cada exercício.</td></tr>
  <tr><td><code>comum/exercicios.py</code></td><td>Fonte dos {total} exercícios (enunciado + solução).</td></tr>
  <tr><td><code>ferramentas/</code></td><td>Scripts que geram os cadernos, o guia e testam o gabarito.</td></tr>
  <tr><td><code>.venv/</code></td><td>{'(não usado neste livro: o código é em R)' if R else 'O Python deste livro com as bibliotecas. Não mexa.'}</td></tr></table>
  <div class="box aviso">O PDF do livro <b>não</b> fica no repositório (direitos autorais). Use a sua cópia.</div>
</section>

<section class="pg">
  <h2>2. Primeira vez (uma vez só)</h2>
  <div class="passo"><div class="n">1</div><div>Abra o VS Code pelo atalho <b>Projetos e Estudos</b> da Área de Trabalho. A pasta deste livro aparece na barra da esquerda.<div class="ok">Você deve ver as pastas praticar/ e resolvidos/.</div></div></div>
  <div class="passo"><div class="n">2</div><div>Se aparecer “Do you trust the authors…”, clique em <b>Yes, I trust the authors</b>.</div></div>
  <div class="passo"><div class="n">3</div><div>Abra <code>praticar/cap01_…ipynb</code>. No canto superior direito, clique em <b>Select Kernel</b> → <b>Python Environments</b> → <b>{E(KERNEL)}</b> desta pasta.</div></div>
  <div class="passo"><div class="n">4</div><div>Clique na célula <b>Preparação</b> e aperte <kbd>Shift</kbd>+<kbd>Enter</kbd>.<div class="ok">Aparece “Pronto.” com a versão da biblioteca.</div></div></div>
  <div class="passo"><div class="n">5</div><div>Abra o PDF do livro ao lado (ou em outra tela) na página indicada no topo do caderno.</div></div>
  <h3>Problemas comuns</h3>
  <table><tr><th>O que aparece</th><th>O que fazer</th></tr>
  <tr><td>“requires ipykernel” / kernel não inicia</td><td>Escolha o kernel <b>{E(KERNEL)}</b> desta pasta, não outro Python. Se continuar: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → <b>Reload Window</b>.</td></tr>
  <tr><td><code>NameError</code></td><td>Uma célula de cima não foi rodada. Rode a Preparação e as anteriores.</td></tr>
  <tr><td><code>ModuleNotFoundError</code></td><td>Kernel errado (veja a 1ª linha).</td></tr>
  <tr><td>Célula “rodando” para sempre</td><td>Botão <b>Interrupt</b> (■) ou <b>Restart</b> no topo do caderno.</td></tr></table>
</section>

<section class="pg">
  <h2>3. A rotina de 60 minutos</h2>
  <div class="linha"><div class="min">0–5 min</div><div>Abra o caderno do capítulo e rode a Preparação. Releia suas anotações da última vez.</div></div>
  <div class="linha"><div class="min">5–30 min</div><div>Leia a próxima seção no PDF. Teste os exemplos do livro numa célula nova (<kbd>B</kbd> cria uma célula abaixo).</div></div>
  <div class="linha"><div class="min">30–50 min</div><div>Resolva o exercício sem olhar o gabarito. Travou por 10 minutos? Olhe, entenda e reescreva sem copiar.</div></div>
  <div class="linha"><div class="min">50–55 min</div><div>Escreva o resumo da seção.</div></div>
  <div class="linha"><div class="min">55–60 min</div><div>Salve e envie para o GitHub (abaixo).</div></div>
  <h3>Salvar o progresso no GitHub</h3>
  <div class="passo"><div class="n">1</div><div>No VS Code, clique no ícone <b>Source Control</b> (3º da barra esquerda) e escolha o repositório <b>{E(PASTA)}</b>.</div></div>
  <div class="passo"><div class="n">2</div><div>Escreva uma mensagem curta, por ex.: <code>cap03: produto escalar e inversa</code>.</div></div>
  <div class="passo"><div class="n">3</div><div>Clique em <b>Commit</b> (se perguntar sobre “stage”, responda <b>Yes</b>) e depois em <b>Sync Changes</b>.<div class="ok">No site do GitHub, o repositório mostra o seu commit.</div></div></div>
  <div class="box dica">Ritmo sugerido: cerca de {max(5, round(paginas / 30))} sessões por semana até terminar as {paginas} páginas. Constância vale mais que velocidade.</div>
</section>

{L.get("extra_html", "")}
<section class="pg">
  <h2>4. Mapa dos capítulos</h2>
  <table><tr><th>Cap.</th><th>Título</th><th>PDF p.</th><th>Caderno</th><th>Exercícios</th></tr>{''.join(linhas)}</table>
  <p>"leitura" = capítulo só de leitura: use as células de anotações. Total: <b>{total} exercícios</b>.</p>
  <h3>Atalhos que você vai usar</h3>
  <table><tr><th>Atalho</th><th>O que faz</th></tr>
  <tr><td><kbd>Shift</kbd>+<kbd>Enter</kbd></td><td>Roda a célula e vai para a próxima</td></tr>
  <tr><td><kbd>Ctrl</kbd>+<kbd>Enter</kbd></td><td>Roda a célula e fica nela</td></tr>
  <tr><td><kbd>Esc</kbd> e <kbd>B</kbd> / <kbd>A</kbd></td><td>Nova célula abaixo / acima</td></tr>
  <tr><td><kbd>Esc</kbd> e <kbd>M</kbd> / <kbd>Y</kbd></td><td>Transforma em texto (Markdown) / código</td></tr>
  <tr><td><kbd>Ctrl</kbd>+<kbd>S</kbd></td><td>Salva o caderno</td></tr></table>
</section>
"""

saida_html = RAIZ / "guia_pdf" / "guia.html"
saida_html.parent.mkdir(exist_ok=True)
saida_html.write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Guia de Estudos</title>'
                      f"<style>{CSS}</style></head><body>{corpo}</body></html>", encoding="utf-8")
pdf = RAIZ / "Guia_de_Estudos.pdf"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
subprocess.run([edge, "--headless=new", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", saida_html.as_uri()],
               check=True, capture_output=True)
print("Guia gerado:", pdf)

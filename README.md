# Estudos — *Use a Cabeça! SQL* (Lynn Beighley)

> **A melhor forma de estudar um livro técnico é ler e praticar ao mesmo tempo.**
> Leia uma seção, feche o livro e escreva o SQL com as próprias mãos. Só depois confira o gabarito.

Este repositório registra meu estudo de *Use a Cabeça! SQL*. O livro vai do `CREATE TABLE` à segurança com usuários e permissões, passando por normalização, junções, subconsultas, views e transações.
Cada capítulo virou um caderno Jupyter em que se escreve **SQL puro** (células `%%sql`). Cada seção aponta para a página do PDF.

## O método

| Passo | O que fazer | Onde |
|---|---|---|
| 1. Ler | Ler a seção indicada | PDF do livro (página no caderno) |
| 2. Praticar | Escrever o SQL **sem olhar a resposta** | `praticar/capXX_*.ipynb` |
| 3. Conferir | Comparar com o gabarito e entender a diferença | `resolvidos/capXX_*.ipynb` |
| 4. Resumir | Explicar com as próprias palavras nas células | `praticar/` |
| 5. Registrar | Commit + push | GitHub |

## Conteúdo (140 exercícios)

| Cap. | Tema | O que se pratica |
|---|---|---|
| 1 | Dados e tabelas | `CREATE TABLE`, tipos, "DESC", `DROP`, `INSERT` e variações, `NULL`, `NOT NULL`, `DEFAULT` |
| 2 | SELECT | `WHERE`, aspas, `AND`/`OR`, `IS NULL`, `LIKE`, `BETWEEN`, `IN`, `NOT` |
| 3 | DELETE e UPDATE | `DELETE` preciso, `INSERT` + `DELETE` × `UPDATE`, `UPDATE` com expressões, `ROLLBACK` de segurança |
| 4 | Tabelas inteligentes | dados atômicos, chave primária, `SERIAL`, `ALTER TABLE ... PRIMARY KEY` |
| 5 | ALTER | renomear tabela e coluna, mudar tipo, `DROP COLUMN`, funções de texto, `UPDATE` a partir de outra coluna |
| 6 | SELECT avançado | `CASE`, `ORDER BY`, `SUM`/`AVG`/`MIN`/`MAX`/`COUNT`, `GROUP BY`, `DISTINCT`, `LIMIT`/`OFFSET` |
| 7 | Várias tabelas | chave estrangeira, um-a-um, um-para-muitos, muitos-para-muitos, chave composta, 2FN e 3FN |
| 8 | Junções | `CREATE TABLE AS`, `INSERT ... SELECT`, apelidos, `CROSS`/`INNER`/não-equijoin/`NATURAL JOIN` |
| 9 | Subconsultas | `IN`, subconsulta escalar, subconsulta como coluna, correlacionadas, `EXISTS`/`NOT EXISTS` |
| 10 | Junções externas e uniões | `LEFT`/`RIGHT`/`FULL JOIN`, autojunção, `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT` |
| 11 | Restrições, views e transações | `CHECK`, `CREATE VIEW`, `WITH CHECK OPTION`, `BEGIN`/`COMMIT`/`ROLLBACK`, atomicidade |
| 12 | Segurança | `CREATE ROLE`, `GRANT`/`REVOKE`, permissão por coluna, `GRANT OPTION`, papéis, `ADMIN OPTION` |

## Melhorias em relação ao livro

- **PostgreSQL 16 no Docker** (`compose.yml`, porta 5434) no lugar do MySQL. Ele tem tudo o que o livro usa, inclusive `INTERSECT`, `EXCEPT` e `FULL OUTER JOIN`, que o MySQL da época não tinha.
- Cada capítulo tem um **esquema** próprio, com as tabelas iniciais criadas pela Preparação. Prática e gabarito nunca se misturam, e dá para recomeçar um capítulo com `recomecar=True`.
- Os dados são **fictícios e originais** (`comum/banco.py`), com as mesmas tabelas dos temas do livro: contatos, bebidas, palhaços, filmes, vendas de biscoitos, empregos e contas.
- As diferenças entre MySQL e PostgreSQL estão nos enunciados e no guia (`DESC`, `AUTO_INCREMENT`, `CHANGE`/`MODIFY`, `SUBSTRING_INDEX`, `LIMIT x, y`, usuários).
- Os comandos que **devem** falhar (chave duplicada, `CHECK`, permissão negada) são mostrados com `try/except`, para ver a proteção funcionando sem travar o caderno.
- O gabarito inteiro roda em `ferramentas/testar_cadernos.py`, com 0 erros.

## Como usar

```powershell
docker compose up -d                                       # sobe o PostgreSQL (Docker Desktop aberto)
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-estudos.txt
.venv\Scripts\python.exe ferramentas\testar_cadernos.py   # opcional: roda o gabarito
```

Abra `praticar/cap01_*.ipynb` no VS Code, escolha o kernel `.venv` e rode a Preparação. O [Guia de Estudos (PDF)](Guia_de_Estudos.pdf) explica o passo a passo.

A senha `estudos` do `compose.yml` vale só para este banco local de estudo, que escuta apenas em 127.0.0.1.

## Direitos autorais

O livro **não** está neste repositório. Para estudar, use a sua própria cópia.
Os exercícios, os dados, os cadernos, os scripts e o guia são autorais e estão sob licença [MIT](LICENSE).

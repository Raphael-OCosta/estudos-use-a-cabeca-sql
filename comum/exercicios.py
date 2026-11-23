"""Exercícios práticos criados para estudar *Use a Cabeça! SQL*, um ou mais por seção.

Formato: (capítulo, início do título da seção, nome, enunciado em Markdown, solução).
As soluções são células `%%sql` (jupysql) rodando num PostgreSQL local (Docker, porta 5434).
Os dados são fictícios e foram criados para estes estudos (comum/banco.py).

O livro usa MySQL. As diferenças de sintaxe aparecem nos enunciados:
- DESC tabela          -> consulta em information_schema.columns
- AUTO_INCREMENT       -> SERIAL (ou GENERATED ... AS IDENTITY)
- CHANGE / MODIFY      -> RENAME COLUMN e ALTER COLUMN ... TYPE
- SUBSTRING_INDEX      -> split_part
- LIMIT 1, 1           -> LIMIT 1 OFFSET 1
- START TRANSACTION    -> BEGIN
- usuários do MySQL    -> papéis (ROLE) do PostgreSQL
Quando um comando DEVE dar erro (para você ver a proteção funcionando), o exercício usa
`try/except` em Python com a mágica de linha `%sql`, para o caderno não parar.
"""

DESC = '''SELECT column_name AS coluna, data_type AS tipo, character_maximum_length AS tamanho,
       is_nullable AS aceita_nulo, column_default AS padrao
FROM information_schema.columns
WHERE table_schema = current_schema() AND table_name = '{}'
ORDER BY ordinal_position;'''

EXERCICIOS = [
    # ---------------- 1. Dados e tabelas ----------------
    (1, "Tome o comando", "Onde estou?",
     "No MySQL o livro usa `CREATE DATABASE` e `USE`. Aqui cada capítulo tem um **esquema** próprio (cap01, "
     "cap02...), que funciona como um banco separado. Liste os esquemas que existem e mostre em qual você está "
     "(`current_schema()`).",
     '''%%sql
SELECT schema_name, schema_name = current_schema() AS estou_aqui
FROM information_schema.schemata
WHERE schema_name NOT LIKE 'pg_%' AND schema_name <> 'information_schema'
ORDER BY schema_name;'''),
    (1, "Preparando a tabela", "Sua primeira tabela",
     "Crie a tabela `lista_compras` com as colunas `item` (texto de até 30 caracteres) e `quantidade` "
     "(número inteiro).",
     '''%%sql
CREATE TABLE lista_compras (
    item VARCHAR(30),
    quantidade INT
);'''),
    (1, "Criando uma tabela um pouco mais complicada", "Escolhendo os tipos",
     "Crie `receitas` com: `nome` (até 40), `tempo_preparo` (minutos, inteiro), `porcoes` (inteiro), `custo` "
     "(dinheiro, 2 casas: `DECIMAL(6,2)`), `vegetariana` (`CHAR(1)`: S/N), `criada_em` (`DATE`) e "
     "`modo_preparo` (`TEXT`, texto longo).",
     '''%%sql
CREATE TABLE receitas (
    nome VARCHAR(40),
    tempo_preparo INT,
    porcoes INT,
    custo DECIMAL(6,2),
    vegetariana CHAR(1),
    criada_em DATE,
    modo_preparo TEXT
);'''),
    (1, "Finalmente, criando a tabela meus_contatos", "A tabela meus_contatos",
     "Crie `meus_contatos` com: `sobrenome`, `primeiro_nome`, `email`, `sexo` (`CHAR(1)`), `aniversario` "
     "(`DATE`), `profissao`, `local`, `estado_civil`, `interesses` e `procurando`. Escolha tamanhos sensatos.",
     '''%%sql
CREATE TABLE meus_contatos (
    sobrenome VARCHAR(30),
    primeiro_nome VARCHAR(20),
    email VARCHAR(50),
    sexo CHAR(1),
    aniversario DATE,
    profissao VARCHAR(50),
    local VARCHAR(50),
    estado_civil VARCHAR(20),
    interesses VARCHAR(100),
    procurando VARCHAR(100)
);'''),
    (1, "Sua tabela DESCrita", "O DESC do PostgreSQL",
     "O `DESC meus_contatos` do MySQL não existe aqui. Consulte `information_schema.columns` para ver coluna, "
     "tipo, tamanho, se aceita nulo e o valor padrão.",
     "%%sql\n" + DESC.format("meus_contatos")),
    (1, "Você não pode recriar", "Criar de novo dá erro",
     "Tente criar `lista_compras` outra vez (dentro de `try/except` em Python, com `%sql` na frente do comando) e "
     "veja o erro. Depois use `CREATE TABLE IF NOT EXISTS`, que não reclama.",
     '''try:
    %sql CREATE TABLE lista_compras (item VARCHAR(30), quantidade INT)
except Exception as erro:
    print("Erro esperado:", str(erro).splitlines()[-2:])
%sql CREATE TABLE IF NOT EXISTS lista_compras (item VARCHAR(30), quantidade INT)'''),
    (1, "Fora com a tabela antiga", "DROP TABLE e recriar",
     "Apague `lista_compras` com `DROP TABLE` e crie de novo com uma coluna a mais: `unidade` (até 10 "
     "caracteres). Mostre a estrutura nova.",
     '''%%sql
DROP TABLE lista_compras;
CREATE TABLE lista_compras (
    item VARCHAR(30),
    quantidade INT,
    unidade VARCHAR(10)
);
''' + DESC.format("lista_compras")),
    (1, "Criando o comando INSERT", "INSERT com todas as colunas",
     "Insira em `meus_contatos` uma pessoa (invente os dados) listando as 10 colunas e os 10 valores na mesma "
     "ordem. Datas vão como `'AAAA-MM-DD'`.",
     '''%%sql
INSERT INTO meus_contatos
    (sobrenome, primeiro_nome, email, sexo, aniversario, profissao, local, estado_civil, interesses, procurando)
VALUES
    ('Moura', 'Marina', 'marina.m@exemplo.com', 'F', '1989-06-11', 'Analista de Dados', 'Recife, PE',
     'solteira', 'trilhas, fotografia', 'amizade');'''),
    (1, "Variações para o comando INSERT", "Três variações",
     "Faça 3 inserções: (a) com as colunas em outra ordem; (b) só com `primeiro_nome` e `email` (as outras ficam "
     "nulas); (c) duas pessoas num único `INSERT` (várias linhas em `VALUES`).",
     '''%%sql
INSERT INTO meus_contatos (primeiro_nome, sobrenome, local, sexo)
VALUES ('Lucas', 'Lins', 'Maceió, AL', 'M');
INSERT INTO meus_contatos (primeiro_nome, email) VALUES ('Iara', 'iara@exemplo.com');
INSERT INTO meus_contatos (primeiro_nome, sobrenome, profissao) VALUES
    ('Bruno', 'Barbosa', 'Professor'),
    ('Carla', 'Cardoso', 'Designer');'''),
    (1, "Espie sua tabela", "SELECT * e os NULLs",
     "Mostre tudo de `meus_contatos`. Repare nas colunas vazias (`None`/`NULL`) de quem foi inserido sem todos "
     "os valores.",
     '''%%sql
SELECT * FROM meus_contatos;'''),
    (1, "Controlando seu NULL interior", "NOT NULL",
     "Crie `rosquinhas` com `nome` e `tipo`, ambos `NOT NULL`. Insira uma válida e tente (com `try/except`) "
     "inserir uma sem `tipo`.",
     '''%sql CREATE TABLE rosquinhas (nome VARCHAR(20) NOT NULL, tipo VARCHAR(10) NOT NULL)
%sql INSERT INTO rosquinhas VALUES ('Coco', 'assada')
try:
    %sql INSERT INTO rosquinhas (nome) VALUES ('Doce de leite')
except Exception as erro:
    print("Bloqueado pelo NOT NULL:", "not-null" in str(erro) or "null value" in str(erro))
%sql SELECT * FROM rosquinhas'''),
    (1, "NOT NULL aparece em DESC", "Conferindo o NOT NULL",
     "Veja a estrutura de `rosquinhas`: a coluna `aceita_nulo` deve dizer `NO`.",
     "%%sql\n" + DESC.format("rosquinhas")),
    (1, "Preencha os espaços em branco com DEFAULT", "Valor padrão",
     "Crie `doces` com `nome` (NOT NULL) e `preco` `DECIMAL(4,2) NOT NULL DEFAULT 1.00`. Insira um doce sem "
     "preço e outro com preço, e mostre a tabela.",
     '''%%sql
CREATE TABLE doces (nome VARCHAR(20) NOT NULL, preco DECIMAL(4,2) NOT NULL DEFAULT 1.00);
INSERT INTO doces (nome) VALUES ('Paçoca');
INSERT INTO doces (nome, preco) VALUES ('Cocada', 2.50);
SELECT * FROM doces;'''),

    # ---------------- 2. SELECT ----------------
    (2, "Um SELECT melhor", "WHERE com texto",
     "Mostre tudo das pessoas de `meus_contatos` cujo primeiro nome é `Ana`.",
     '''%%sql
SELECT * FROM meus_contatos WHERE primeiro_nome = 'Ana';'''),
    (2, "Que * é esta?", "Todas as colunas de algumas linhas",
     "Mostre todas as colunas das bebidas de `bebidas_faceis` cujo ingrediente principal é `chá mate`.",
     '''%%sql
SELECT * FROM bebidas_faceis WHERE principal = 'chá mate';'''),
    (2, "Como fazer consultas nos seus tipos", "Números, datas e texto",
     "Três consultas na mesma célula não mostram tudo (só a última). Faça uma por vez: (a) bebidas com `qtd2 = "
     "1.0` (número sem aspas); (b) contatos nascidos em `'1990-03-14'`; (c) contatos que trabalham como "
     "`Professora`. Nesta célula, deixe a (b).",
     '''%%sql
SELECT primeiro_nome, aniversario FROM meus_contatos WHERE aniversario = '1990-03-14';'''),
    (2, "INSERT (Insira) dados com aspas simples", "Aspas dentro do texto",
     "Insira em `notas_cafeterias` a visita à `Pão d'Água` (use duas aspas simples: `d''Água`), com data, item, "
     "nota e comentário. Depois consulte por esse local.",
     '''%%sql
INSERT INTO notas_cafeterias VALUES ('Pão d''Água', '2024-03-15', 'café coado', 9, 'cheiro de casa de vó');
SELECT * FROM notas_cafeterias WHERE local = 'Pão d''Água';'''),
    (2, "SELECT (selecionar) colunas específicas para limitar", "Só as colunas que importam",
     "Mostre só `nome_bebida` e `principal` das bebidas cujo segundo ingrediente é `suco de limão`.",
     '''%%sql
SELECT nome_bebida, principal FROM bebidas_faceis WHERE segundo = 'suco de limão';'''),
    (2, "Combinando suas consultas", "AND",
     "Mostre nome, sobrenome e email das **mulheres** que moram em `Recife, PE`.",
     '''%%sql
SELECT primeiro_nome, sobrenome, email
FROM meus_contatos
WHERE sexo = 'F' AND local = 'Recife, PE';'''),
    (2, "Encontrando dados numéricos com operadores", "Comparações com números",
     "Mostre as bebidas que levam **4 ou mais** do ingrediente principal e as notas de cafeterias **menores que "
     "8** (uma consulta por célula; aqui, a das notas).",
     '''%%sql
SELECT local, item, nota FROM notas_cafeterias WHERE nota < 8;'''),
    (2, "Amarrando os dados em texto", "Comparações com texto",
     "Mostre as bebidas cujo nome começa com uma letra de `M` até `O` usando `>=` e `<` (dica: "
     "`nome_bebida >= 'M' AND nome_bebida < 'P'`).",
     '''%%sql
SELECT nome_bebida FROM bebidas_faceis WHERE nome_bebida >= 'M' AND nome_bebida < 'P';'''),
    (2, "Ser OR (ou) não ser", "OR",
     "Mostre os contatos que moram em Natal **ou** são Analista de Dados.",
     '''%%sql
SELECT primeiro_nome, local, profissao
FROM meus_contatos
WHERE local = 'Natal, RN' OR profissao = 'Analista de Dados';'''),
    (2, "A diferença entre AND e OR", "Parênteses mudam o resultado",
     "Compare, contando as linhas com `COUNT(*)`: `sexo = 'F' AND local = 'Recife, PE' OR profissao = 'Chef'` "
     "contra `sexo = 'F' AND (local = 'Recife, PE' OR profissao = 'Chef')`. O `AND` é avaliado antes do `OR`.",
     '''%%sql
SELECT
  (SELECT COUNT(*) FROM meus_contatos WHERE sexo = 'F' AND local = 'Recife, PE' OR profissao = 'Chef') AS sem_parenteses,
  (SELECT COUNT(*) FROM meus_contatos WHERE sexo = 'F' AND (local = 'Recife, PE' OR profissao = 'Chef')) AS com_parenteses;'''),
    (2, "Usando IS NULL", "IS NULL (e não = NULL)",
     "Mostre quem está sem email e quem está sem estado civil. Depois confira que `WHERE email = NULL` não "
     "traz nada.",
     '''%%sql
SELECT primeiro_nome, email, estado_civil
FROM meus_contatos
WHERE email IS NULL OR estado_civil IS NULL;'''),
    (2, "O chamado do Coringa", "LIKE com % e _",
     "Mostre: (a) os contatos com profissão terminada em `Software` (`%`); (b) os contatos cujo primeiro nome "
     "tem `a` como **segunda** letra (`_a%`). Aqui, a (b).",
     '''%%sql
SELECT primeiro_nome FROM meus_contatos WHERE primeiro_nome LIKE '_a%';'''),
    (2, "Bem BETWEEN", "BETWEEN",
     "Mostre as notas de 7 a 9 (inclusive) e as visitas entre `2024-03-05` e `2024-03-10` (aqui, as duas "
     "condições juntas com AND).",
     '''%%sql
SELECT * FROM notas_cafeterias
WHERE nota BETWEEN 7 AND 9 AND visita BETWEEN '2024-03-05' AND '2024-03-10';'''),
    (2, "Depois dos encontros, você está IN", "IN",
     "Mostre os contatos que moram em Recife, Olinda ou Natal usando `IN`.",
     '''%%sql
SELECT primeiro_nome, local FROM meus_contatos
WHERE local IN ('Recife, PE', 'Olinda, PE', 'Natal, RN');'''),
    (2, "...ou você está NOT IN", "NOT IN",
     "Agora os que **não** moram nessas três cidades.",
     '''%%sql
SELECT primeiro_nome, local FROM meus_contatos
WHERE local NOT IN ('Recife, PE', 'Olinda, PE', 'Natal, RN');'''),
    (2, "Mais NOT", "NOT com BETWEEN, LIKE e NULL",
     "Mostre as bebidas cujo `qtd1` **não** está entre 3 e 4, cujo nome **não** começa com `B` e que têm "
     "instruções preenchidas (`IS NOT NULL`).",
     '''%%sql
SELECT nome_bebida, qtd1 FROM bebidas_faceis
WHERE qtd1 NOT BETWEEN 3 AND 4
  AND nome_bebida NOT LIKE 'B%'
  AND instrucoes IS NOT NULL;'''),

    # ---------------- 3. DELETE e UPDATE ----------------
    (3, "Os palhaços estão em movimento", "Onde o palhaço foi visto",
     "Mostre todas as linhas do palhaço `Pipoca` em `palhacos_info`. Por que ele aparece duas vezes?",
     '''%%sql
SELECT * FROM palhacos_info WHERE nome = 'Pipoca';'''),
    (3, "Como os nossos dados de palhaços são inseridos", "Registrando um novo avistamento",
     "A `Zazá` foi vista na `Biblioteca Central`, com a mesma aparência e atividades. Insira a nova linha copiando "
     "os outros dados dela.",
     '''%%sql
INSERT INTO palhacos_info VALUES ('Zazá', 'Biblioteca Central', 'F, óculos gigantes', 'contação de histórias');
SELECT * FROM palhacos_info WHERE nome = 'Zazá';'''),
    (3, "Eliminando um registro com DELETE", "DELETE com WHERE preciso",
     "Apague só o avistamento **antigo** do Pipoca (o da `Festa da Rua Aurora`). Confira o resultado.",
     '''%%sql
DELETE FROM palhacos_info WHERE nome = 'Pipoca' AND ultima_vez_visto = 'Festa da Rua Aurora';
SELECT * FROM palhacos_info WHERE nome = 'Pipoca';'''),
    (3, "Os dois passos do INSERT e DELETE", "Inserir o novo, depois apagar o velho",
     "O `Tico-Tico` mudou de lugar: foi visto no `Parque da Jaqueira`. Faça em dois passos: insira a linha nova "
     "e apague a antiga (`Shopping Boa Vista`). Por que inserir **antes** de apagar?",
     '''%%sql
INSERT INTO palhacos_info VALUES ('Tico-Tico', 'Parque da Jaqueira', 'M, chapéu-coco, gravata enorme', 'monociclo');
DELETE FROM palhacos_info WHERE nome = 'Tico-Tico' AND ultima_vez_visto = 'Shopping Boa Vista';
SELECT * FROM palhacos_info WHERE nome = 'Tico-Tico';'''),
    (3, "Cuidado com o seu DELETE", "Teste antes com SELECT (e com ROLLBACK)",
     "Um `DELETE` sem `WHERE` apaga **tudo**. Veja isso com segurança: `BEGIN;` abre uma transação, o `DELETE` "
     "apaga, `ROLLBACK;` desfaz. Termine contando as linhas para confirmar que nada foi perdido. (Transações são "
     "o assunto do capítulo 11.)",
     '''%%sql
BEGIN;
DELETE FROM palhacos_info;
ROLLBACK;
SELECT COUNT(*) AS linhas_continuam_la FROM palhacos_info;'''),
    (3, "Altere seus dados com UPDATE", "UPDATE em uma coluna",
     "Troque o `UPDATE` pelos dois passos do exercício anterior: a `Lulu` foi vista no `Teatro Santa Isabel`.",
     '''%%sql
UPDATE palhacos_info SET ultima_vez_visto = 'Teatro Santa Isabel' WHERE nome = 'Lulu';
SELECT * FROM palhacos_info WHERE nome = 'Lulu';'''),
    (3, "UPDATE em ação", "UPDATE em várias colunas",
     "O `Fuxico` foi visto na `Feira de Casa Amarela` e agora também faz `mágica`. Atualize as duas colunas num "
     "único `UPDATE`.",
     '''%%sql
UPDATE palhacos_info
SET ultima_vez_visto = 'Feira de Casa Amarela',
    atividades = 'malabarismo, buzina, mágica'
WHERE nome = 'Fuxico';
SELECT * FROM palhacos_info WHERE nome = 'Fuxico';'''),
    (3, "UPDATE (atualize) seus preços", "Preço com expressão",
     "Aumente em R$ 1,00 o preço das bebidas **com gelo** (`gelo = 'S'`) usando `preco = preco + 1`.",
     '''%%sql
UPDATE bebidas_precos SET preco = preco + 1 WHERE gelo = 'S';
SELECT nome_bebida, preco, gelo FROM bebidas_precos ORDER BY nome_bebida;'''),
    (3, "Tudo o que precisamos é um UPDATE", "UPDATE sem WHERE, de propósito",
     "Todas as bebidas ganharam uma versão sem açúcar com 20% menos calorias. Atualize a coluna `calorias` de "
     "**todas** as linhas (`calorias * 0.8`, arredondado com `ROUND`).",
     '''%%sql
UPDATE bebidas_precos SET calorias = ROUND(calorias * 0.8);
SELECT nome_bebida, calorias FROM bebidas_precos;'''),

    # ---------------- 4. Tabelas inteligentes ----------------
    (4, "Duas tabelas de pescadores", "Mesma pergunta, duas tabelas",
     "Encontre os peixes da Bahia nas duas tabelas: em `info_peixes` o estado está misturado em `local` "
     "(`LIKE '%, BA'`); em `recordes_peixes` há a coluna `uf`. Qual consulta é mais confiável?",
     '''%%sql
SELECT 'info_peixes' AS tabela, nome_comum, local FROM info_peixes WHERE local LIKE '%, BA'
UNION ALL
SELECT 'recordes_peixes', nome_comum, local || ' / ' || uf FROM recordes_peixes WHERE uf = 'BA';'''),
    (4, "Dados atômicos", "O preço de não ser atômico",
     "Em `meus_contatos`, a coluna `interesses` guarda vários valores. Encontre quem gosta de `xadrez` e de "
     "`cinema` ao mesmo tempo. Repare como o `LIKE` é frágil (e se alguém escrever `Xadrez`?).",
     '''%%sql
SELECT primeiro_nome, interesses FROM meus_contatos
WHERE interesses LIKE '%xadrez%' AND interesses LIKE '%cinema%';'''),
    (4, "Regras da CHAVE PRIMÁRIA", "Chave primária impede repetidos",
     "Crie `clientes` com `cliente_id INT PRIMARY KEY` e `nome`. Insira o cliente 1 e tente inserir outro "
     "cliente 1 (`try/except`).",
     '''%sql CREATE TABLE clientes (cliente_id INT PRIMARY KEY, nome VARCHAR(30) NOT NULL)
%sql INSERT INTO clientes VALUES (1, 'Ana')
try:
    %sql INSERT INTO clientes VALUES (1, 'Outra Ana')
except Exception as erro:
    print("Chave repetida bloqueada:", "duplicate key" in str(erro) or "duplicada" in str(erro))
%sql SELECT * FROM clientes'''),
    (4, "Mostre-me a tabela", "SHOW CREATE TABLE do PostgreSQL",
     "O MySQL tem `SHOW CREATE TABLE`. Aqui, junte as colunas (`information_schema.columns`) com as restrições "
     "(`information_schema.table_constraints`) de `clientes`. Liste as restrições: tipo e nome.",
     '''%%sql
SELECT constraint_type AS tipo, constraint_name AS nome
FROM information_schema.table_constraints
WHERE table_schema = current_schema() AND table_name = 'clientes'
ORDER BY 1;'''),
    (4, "1, 2, 3... auto incrementando", "Chave que se numera sozinha",
     "Crie `contatos_novos` com `contato_id SERIAL PRIMARY KEY` (o `AUTO_INCREMENT` do MySQL), `primeiro_nome` e "
     "`email`. Insira 3 pessoas **sem** informar o id e mostre a tabela.",
     '''%%sql
CREATE TABLE contatos_novos (
    contato_id SERIAL PRIMARY KEY,
    primeiro_nome VARCHAR(20) NOT NULL,
    email VARCHAR(50)
);
INSERT INTO contatos_novos (primeiro_nome, email) VALUES
    ('Ana', 'ana@exemplo.com'), ('Bruno', 'bruno@exemplo.com'), ('Carla', NULL);
SELECT * FROM contatos_novos;'''),
    (4, "ALTER TABLE e adicionar uma PRIMARY KEY", "Chave primária numa tabela que já existe",
     "Acrescente `contato_id SERIAL PRIMARY KEY` à tabela `meus_contatos` (que já tem dados) com `ALTER TABLE ... "
     "ADD COLUMN`. Os ids são preenchidos sozinhos? (No PostgreSQL a coluna nova vai para o fim; o `FIRST` do "
     "MySQL não existe.)",
     '''%%sql
ALTER TABLE meus_contatos ADD COLUMN contato_id SERIAL PRIMARY KEY;
SELECT contato_id, primeiro_nome, sobrenome FROM meus_contatos ORDER BY contato_id;'''),
    (4, "Consertando a tabela do Greg", "Separando cidade e estado",
     "Sem mudar a tabela, mostre `local` separado em `cidade` e `uf` usando `split_part(local, ', ', 1)` e "
     "`split_part(local, ', ', 2)`. (No capítulo 5 você grava isso em colunas.)",
     '''%%sql
SELECT primeiro_nome, split_part(local, ', ', 1) AS cidade, split_part(local, ', ', 2) AS uf
FROM meus_contatos;'''),

    # ---------------- 5. ALTER ----------------
    (5, "Alterações de tabelas", "ADD COLUMN",
     "Acrescente a coluna `telefone VARCHAR(15)` em `meus_contatos` e mostre a estrutura.",
     "%%sql\nALTER TABLE meus_contatos ADD COLUMN telefone VARCHAR(15);\n" + DESC.format("meus_contatos")),
    (5, "Renomeando a tabela", "RENAME TO",
     "A tabela `projetos` passa a se chamar `lista_projetos`.",
     '''%%sql
ALTER TABLE projetos RENAME TO lista_projetos;
SELECT * FROM lista_projetos;'''),
    (5, "Reinstrumentalizando nossas colunas", "Renomear coluna e criar chave",
     "Renomeie `numero` para `proj_id` e transforme-a em chave primária (`ADD PRIMARY KEY (proj_id)`).",
     '''%%sql
ALTER TABLE lista_projetos RENAME COLUMN numero TO proj_id;
ALTER TABLE lista_projetos ADD PRIMARY KEY (proj_id);
''' + DESC.format("lista_projetos")),
    (5, "ALTER e CHANGE", "O CHANGE do MySQL em dois comandos",
     "O `CHANGE` do MySQL renomeia e muda o tipo de uma vez. Aqui: renomeie `descricaodoprojeto` para `descricao` "
     "e mude o tipo para `VARCHAR(100)` (`ALTER COLUMN ... TYPE`). Faça o mesmo com `empreiteiranaobra` → "
     "`empreiteira`.",
     '''%%sql
ALTER TABLE lista_projetos RENAME COLUMN descricaodoprojeto TO descricao;
ALTER TABLE lista_projetos ALTER COLUMN descricao TYPE VARCHAR(100);
ALTER TABLE lista_projetos RENAME COLUMN empreiteiranaobra TO empreiteira;
''' + DESC.format("lista_projetos")),
    (5, "Altere duas colunas com apenas um comando", "Várias mudanças num ALTER",
     "Num **único** `ALTER TABLE`, acrescente `data_inicio DATE` e `orcamento DECIMAL(9,2)` e mude "
     "`empreiteira` para `VARCHAR(60)` (separe as ações por vírgula).",
     '''%%sql
ALTER TABLE lista_projetos
    ADD COLUMN data_inicio DATE,
    ADD COLUMN orcamento DECIMAL(9,2),
    ALTER COLUMN empreiteira TYPE VARCHAR(60);
''' + DESC.format("lista_projetos")),
    (5, "Rápido! Largue esta coluna", "DROP COLUMN",
     "Remova a coluna `data_inicio`.",
     "%%sql\nALTER TABLE lista_projetos DROP COLUMN data_inicio;\n" + DESC.format("lista_projetos")),
    (5, "Reconstrução total de tabelas", "Reformando o calhambeque",
     "A tabela `calhambeques` está mal feita. Reforme: renomeie para `carros`; acrescente `carro_id SERIAL PRIMARY "
     "KEY`; renomeie `mod` para `modelo`; mude `ano` para `INT` e `preco` para `DECIMAL(9,2)` (texto vira "
     "número com `USING ano::int` e `USING preco::numeric`).",
     '''%%sql
ALTER TABLE calhambeques RENAME TO carros;
ALTER TABLE carros ADD COLUMN carro_id SERIAL PRIMARY KEY;
ALTER TABLE carros RENAME COLUMN mod TO modelo;
ALTER TABLE carros
    ALTER COLUMN ano TYPE INT USING ano::int,
    ALTER COLUMN preco TYPE DECIMAL(9,2) USING preco::numeric;
SELECT * FROM carros;'''),
    (5, "Algumas funções de texto muito úteis", "Funções de texto",
     "Aplique a `'  Recife, PE  '`: `TRIM`, `LENGTH` (antes e depois do TRIM), `UPPER`, `LOWER`, `REVERSE`, "
     "`LEFT(...,6)`, `RIGHT(...,2)` (depois do TRIM), `SUBSTRING(... FROM 1 FOR 3)` e `split_part(..., ',', 1)`.",
     '''%%sql
SELECT TRIM('  Recife, PE  ') AS aparado,
       LENGTH('  Recife, PE  ') AS tam_antes, LENGTH(TRIM('  Recife, PE  ')) AS tam_depois,
       UPPER('Recife, PE') AS maiusc, LOWER('Recife, PE') AS minusc, REVERSE('Recife, PE') AS invertido,
       LEFT('Recife, PE', 6) AS esquerda, RIGHT(TRIM('  Recife, PE  '), 2) AS direita,
       SUBSTRING('Recife, PE' FROM 1 FOR 3) AS pedaco, split_part('Recife, PE', ',', 1) AS antes_da_virgula;'''),
    (5, "Utilize uma coluna atual para preencher", "UPDATE com funções",
     "Acrescente `cidade VARCHAR(40)` e `uf CHAR(2)` em `meus_contatos` e preencha a partir de `local` com "
     "`UPDATE ... SET uf = RIGHT(local, 2), cidade = split_part(local, ',', 1)`.",
     '''%%sql
ALTER TABLE meus_contatos ADD COLUMN cidade VARCHAR(40), ADD COLUMN uf CHAR(2);
UPDATE meus_contatos SET uf = RIGHT(local, 2), cidade = split_part(local, ',', 1);
SELECT primeiro_nome, local, cidade, uf FROM meus_contatos;'''),
    (5, "Como funciona nosso combo", "Removendo a coluna não atômica",
     "Agora que `cidade` e `uf` existem, apague `local`. Conte quantos contatos há por `uf`.",
     '''%%sql
ALTER TABLE meus_contatos DROP COLUMN local;
SELECT uf, COUNT(*) AS contatos FROM meus_contatos GROUP BY uf ORDER BY contatos DESC;'''),

    # ---------------- 6. SELECT avançado ----------------
    (6, "Combinando dados existentes", "Uma coluna de categoria",
     "A tabela `filmes` tem uma coluna T/F para cada gênero. Acrescente `categoria VARCHAR(10)`.",
     '''%%sql
ALTER TABLE filmes ADD COLUMN categoria VARCHAR(15);
SELECT titulo, drama, comedia, acao, terror, ficcao, infantil, desenho, categoria FROM filmes;'''),
    (6, "Povoando sua nova coluna", "Vários UPDATEs",
     "Preencha `categoria` com um `UPDATE` por gênero: `drama`, `comédia`, `ação`, `terror`, `ficção`, "
     "`família` (infantil) e `desenho`. Em que ordem você rodou? Um filme com dois gêneros fica com qual?",
     '''%%sql
UPDATE filmes SET categoria = 'drama' WHERE drama = 'T';
UPDATE filmes SET categoria = 'comédia' WHERE comedia = 'T';
UPDATE filmes SET categoria = 'ação' WHERE acao = 'T';
UPDATE filmes SET categoria = 'terror' WHERE terror = 'T';
UPDATE filmes SET categoria = 'ficção' WHERE ficcao = 'T';
UPDATE filmes SET categoria = 'família' WHERE infantil = 'T';
UPDATE filmes SET categoria = 'desenho' WHERE desenho = 'T';
SELECT titulo, categoria FROM filmes;'''),
    (6, "UPDATE com uma expressão CASE", "Um único UPDATE com CASE",
     "Refaça com **um** `UPDATE` e `CASE`. A primeira condição verdadeira vence. Use `ELSE 'diversos'`. Mude a "
     "ordem: desenho primeiro, depois família.",
     '''%%sql
UPDATE filmes SET categoria =
    CASE
        WHEN desenho = 'T' THEN 'desenho'
        WHEN infantil = 'T' THEN 'família'
        WHEN drama = 'T' THEN 'drama'
        WHEN comedia = 'T' THEN 'comédia'
        WHEN acao = 'T' THEN 'ação'
        WHEN terror = 'T' THEN 'terror'
        WHEN ficcao = 'T' THEN 'ficção'
        ELSE 'diversos'
    END;
SELECT titulo, categoria FROM filmes;'''),
    (6, "Parece que temos um problema", "CASE com mais de uma condição",
     "Filmes de terror com classificação `16` devem virar `terror leve` e os de `18`, `terror`. Faça com `CASE` "
     "dentro de `UPDATE ... WHERE terror = 'T'`.",
     '''%%sql
UPDATE filmes SET categoria =
    CASE WHEN classificacao = '18' THEN 'terror' ELSE 'terror leve' END
WHERE terror = 'T';
SELECT titulo, classificacao, categoria FROM filmes WHERE terror = 'T';'''),
    (6, "Tente um simples ORDER BY", "ORDER BY",
     "Liste título e categoria dos filmes em ordem alfabética de título.",
     '''%%sql
SELECT titulo, categoria FROM filmes ORDER BY titulo;'''),
    (6, "ORDER com duas colunas", "Ordenando por duas colunas",
     "Ordene por categoria e, dentro de cada categoria, por título.",
     '''%%sql
SELECT categoria, titulo FROM filmes ORDER BY categoria, titulo;'''),
    (6, "Inverta o comando ORDER com DESC", "DESC",
     "Liste os filmes da classificação mais alta para a mais baixa e, empatados, em ordem de título.",
     '''%%sql
SELECT classificacao, titulo FROM filmes ORDER BY classificacao DESC, titulo;'''),
    (6, "SUM pode somá-las", "SUM",
     "Quanto a `Nina` vendeu de biscoitos no total?",
     '''%%sql
SELECT SUM(vendas) AS total_nina FROM vendas_biscoitos WHERE primeiro_nome = 'Nina';'''),
    (6, "SUM (some) todas de uma vez com GROUP BY", "GROUP BY",
     "Mostre o total de cada vendedora, da maior para a menor. Quem é a líder?",
     '''%%sql
SELECT primeiro_nome, SUM(vendas) AS total
FROM vendas_biscoitos
GROUP BY primeiro_nome
ORDER BY total DESC;'''),
    (6, "AVG combinada com GROUP BY", "AVG",
     "Mostre a média por vendedora, arredondada em 2 casas.",
     '''%%sql
SELECT primeiro_nome, ROUND(AVG(vendas), 2) AS media
FROM vendas_biscoitos GROUP BY primeiro_nome ORDER BY media DESC;'''),
    (6, "MIN e MAX", "MIN e MAX",
     "Mostre a menor e a maior venda de cada uma.",
     '''%%sql
SELECT primeiro_nome, MIN(vendas) AS menor, MAX(vendas) AS maior
FROM vendas_biscoitos GROUP BY primeiro_nome ORDER BY primeiro_nome;'''),
    (6, "COUNT (conte) os dias", "COUNT",
     "Em quantos dias cada uma vendeu **alguma coisa** (`vendas > 0`)? E em quantos dias diferentes houve venda "
     "no total (`COUNT(DISTINCT data)`)? Aqui, a primeira.",
     '''%%sql
SELECT primeiro_nome, COUNT(data) AS dias_com_venda
FROM vendas_biscoitos WHERE vendas > 0
GROUP BY primeiro_nome ORDER BY dias_com_venda DESC;'''),
    (6, "SELECT DISTINCT", "DISTINCT",
     "Liste as datas distintas em que houve vendas, em ordem.",
     '''%%sql
SELECT DISTINCT data FROM vendas_biscoitos ORDER BY data;'''),
    (6, "LIMIT (limite) o número de resultados", "LIMIT",
     "Mostre só as 2 primeiras do ranking de totais.",
     '''%%sql
SELECT primeiro_nome, SUM(vendas) AS total
FROM vendas_biscoitos GROUP BY primeiro_nome ORDER BY total DESC LIMIT 2;'''),
    (6, "LIMIT (limite) apenas para a segunda", "LIMIT com OFFSET",
     "Mostre **só a segunda colocada**. No MySQL seria `LIMIT 1, 1`; aqui é `LIMIT 1 OFFSET 1`.",
     '''%%sql
SELECT primeiro_nome, SUM(vendas) AS total
FROM vendas_biscoitos GROUP BY primeiro_nome ORDER BY total DESC LIMIT 1 OFFSET 1;'''),

    # ---------------- 7. Várias tabelas ----------------
    (7, "Encontrando uma namorada para Nigel", "Busca difícil numa tabela só",
     "Encontre mulheres solteiras que gostam de `cinema` e de `trilhas`. Com tudo numa tabela só, a busca depende "
     "de `LIKE` em texto livre.",
     '''%%sql
SELECT primeiro_nome, estado_civil, interesses FROM meus_contatos
WHERE sexo = 'F' AND estado_civil = 'solteira'
  AND interesses LIKE '%cinema%' AND interesses LIKE '%trilhas%';'''),
    (7, "Pense além da tabela única", "Preparando a chave",
     "Para ligar outras tabelas a `meus_contatos`, ela precisa de uma chave. Acrescente `contato_id SERIAL "
     "PRIMARY KEY`.",
     '''%%sql
ALTER TABLE meus_contatos ADD COLUMN contato_id SERIAL PRIMARY KEY;
SELECT contato_id, primeiro_nome FROM meus_contatos ORDER BY contato_id;'''),
    (7, "CREATE uma tabela com uma CHAVE ESTRANGEIRA", "FOREIGN KEY",
     "Crie `interesses` (`int_id SERIAL PRIMARY KEY`, `interesse`, `contato_id`) com uma `CONSTRAINT ... "
     "FOREIGN KEY (contato_id) REFERENCES meus_contatos (contato_id)`. Insira os interesses da contato 1 (um "
     "por linha).",
     '''%%sql
CREATE TABLE interesses (
    int_id SERIAL PRIMARY KEY,
    interesse VARCHAR(50) NOT NULL,
    contato_id INT NOT NULL,
    CONSTRAINT meus_contatos_contato_id_fk FOREIGN KEY (contato_id) REFERENCES meus_contatos (contato_id)
);
INSERT INTO interesses (interesse, contato_id) VALUES ('cinema', 1), ('trilhas', 1), ('xadrez', 1);
SELECT * FROM interesses;'''),
    (7, "Restringindo sua chave externa", "A chave estrangeira protege",
     "Tente inserir um interesse para o contato `999` (que não existe) com `try/except`.",
     '''try:
    %sql INSERT INTO interesses (interesse, contato_id) VALUES ('pôquer', 999)
except Exception as erro:
    print("Bloqueado pela chave estrangeira:", "foreign key" in str(erro) or "chave estrangeira" in str(erro))'''),
    (7, "Padrões de dados: um-a-um", "Um-para-um",
     "Dados raramente usados podem ir para uma tabela à parte, com a **mesma** chave. Crie `contatos_extras` "
     "(`contato_id INT PRIMARY KEY REFERENCES meus_contatos`, `apelido`, `cor_favorita`) e insira 2 linhas.",
     '''%%sql
CREATE TABLE contatos_extras (
    contato_id INT PRIMARY KEY REFERENCES meus_contatos (contato_id),
    apelido VARCHAR(20),
    cor_favorita VARCHAR(15)
);
INSERT INTO contatos_extras VALUES (1, 'Aninha', 'verde'), (2, 'Brunão', 'azul');
SELECT * FROM contatos_extras;'''),
    (7, "Padrões de dados: um-para-muitos", "Um-para-muitos: profissões",
     "Crie `profissoes` (`prof_id SERIAL PRIMARY KEY`, `profissao UNIQUE`) e preencha com as profissões distintas "
     "(`INSERT INTO ... SELECT DISTINCT`). Depois acrescente `prof_id` em `meus_contatos` com referência e "
     "preencha com `UPDATE ... FROM profissoes` (sintaxe do PostgreSQL).",
     '''%%sql
CREATE TABLE profissoes (prof_id SERIAL PRIMARY KEY, profissao VARCHAR(50) UNIQUE NOT NULL);
INSERT INTO profissoes (profissao) SELECT DISTINCT profissao FROM meus_contatos ORDER BY profissao;
ALTER TABLE meus_contatos ADD COLUMN prof_id INT REFERENCES profissoes (prof_id);
UPDATE meus_contatos m SET prof_id = p.prof_id FROM profissoes p WHERE p.profissao = m.profissao;
SELECT primeiro_nome, profissao, prof_id FROM meus_contatos ORDER BY prof_id;'''),
    (7, "Padrões de dados: nós precisamos de uma junction table", "Muitos-para-muitos com tabela de ligação",
     "Palhaços fazem várias atividades e cada atividade é feita por vários palhaços. Crie `palhaco` (`palhaco_id "
     "SERIAL`, `nome UNIQUE`), `atividade` (`atividade_id SERIAL`, `atividade UNIQUE`) e a tabela de ligação "
     "`palhaco_atividade` com chave composta. Preencha `palhaco` a partir de `palhacos_info` e ligue alguns.",
     '''%%sql
CREATE TABLE palhaco (palhaco_id SERIAL PRIMARY KEY, nome VARCHAR(30) UNIQUE NOT NULL);
CREATE TABLE atividade (atividade_id SERIAL PRIMARY KEY, atividade VARCHAR(30) UNIQUE NOT NULL);
CREATE TABLE palhaco_atividade (
    palhaco_id INT REFERENCES palhaco (palhaco_id),
    atividade_id INT REFERENCES atividade (atividade_id),
    PRIMARY KEY (palhaco_id, atividade_id)
);
INSERT INTO palhaco (nome) SELECT DISTINCT nome FROM palhacos_info ORDER BY nome;
INSERT INTO atividade (atividade) VALUES ('malabarismo'), ('balões'), ('mágica'), ('monociclo');
INSERT INTO palhaco_atividade
SELECT p.palhaco_id, a.atividade_id FROM palhaco p, atividade a
WHERE (p.nome = 'Pipoca' AND a.atividade IN ('malabarismo', 'balões'))
   OR (p.nome = 'Biribinha' AND a.atividade = 'mágica')
   OR (p.nome = 'Fuxico' AND a.atividade = 'malabarismo');
SELECT * FROM palhaco_atividade;'''),
    (7, "Chaves compostas utilizam múltiplas colunas", "Conferindo a chave composta",
     "Mostre as colunas que formam a chave primária de `palhaco_atividade` "
     "(`information_schema.key_column_usage`).",
     '''%%sql
SELECT k.column_name, k.ordinal_position
FROM information_schema.table_constraints t
JOIN information_schema.key_column_usage k
  ON k.constraint_name = t.constraint_name AND k.table_schema = t.table_schema
WHERE t.table_schema = current_schema() AND t.table_name = 'palhaco_atividade'
  AND t.constraint_type = 'PRIMARY KEY'
ORDER BY k.ordinal_position;'''),
    (7, "Segunda Forma Normal", "Tirando a dependência parcial (2NF)",
     "Na tabela `estoque_lojas(brinquedo_id, loja_id, quantidade, endereco_loja)` a chave é (brinquedo_id, "
     "loja_id), mas `endereco_loja` depende só de `loja_id`. Crie a tabela ruim com 3 linhas e depois a versão "
     "2NF: `lojas(loja_id, endereco)` e `estoque(brinquedo_id, loja_id, quantidade)`, preenchidas a partir dela.",
     '''%%sql
CREATE TABLE estoque_lojas (brinquedo_id INT, loja_id INT, quantidade INT, endereco_loja VARCHAR(40),
                            PRIMARY KEY (brinquedo_id, loja_id));
INSERT INTO estoque_lojas VALUES (1, 10, 5, 'Rua A, 100'), (2, 10, 3, 'Rua A, 100'), (1, 20, 7, 'Av. B, 200');
CREATE TABLE lojas AS SELECT DISTINCT loja_id, endereco_loja AS endereco FROM estoque_lojas;
ALTER TABLE lojas ADD PRIMARY KEY (loja_id);
CREATE TABLE estoque AS SELECT brinquedo_id, loja_id, quantidade FROM estoque_lojas;
ALTER TABLE estoque ADD PRIMARY KEY (brinquedo_id, loja_id),
                    ADD FOREIGN KEY (loja_id) REFERENCES lojas (loja_id);
SELECT * FROM lojas;'''),
    (7, "Terceira Forma Normal", "Tirando a dependência transitiva (3NF)",
     "Em `cursos(curso_id, curso, professor, sala_do_professor)`, a sala depende do professor (que não é chave): "
     "dependência transitiva. Crie a tabela com 3 linhas e separe em `professores(professor, sala)` e "
     "`cursos_3nf(curso_id, curso, professor)`.",
     '''%%sql
CREATE TABLE cursos (curso_id INT PRIMARY KEY, curso VARCHAR(30), professor VARCHAR(30), sala_do_professor VARCHAR(10));
INSERT INTO cursos VALUES (1, 'SQL Básico', 'Marta', 'B-12'), (2, 'SQL Avançado', 'Marta', 'B-12'),
                          (3, 'Python', 'Caio', 'C-03');
CREATE TABLE professores AS SELECT DISTINCT professor, sala_do_professor AS sala FROM cursos;
ALTER TABLE professores ADD PRIMARY KEY (professor);
CREATE TABLE cursos_3nf AS SELECT curso_id, curso, professor FROM cursos;
ALTER TABLE cursos_3nf ADD PRIMARY KEY (curso_id),
                       ADD FOREIGN KEY (professor) REFERENCES professores (professor);
SELECT * FROM professores;'''),

    # ---------------- 8. Junções ----------------
    (8, "Os interesses especiais", "Colunas para os interesses",
     "Em `contatos_antigos`, os interesses estão juntos e separados por vírgula. Acrescente as colunas "
     "`interesse1`, `interesse2` e `interesse3`.",
     '''%%sql
ALTER TABLE contatos_antigos ADD COLUMN interesse1 VARCHAR(30), ADD COLUMN interesse2 VARCHAR(30),
                             ADD COLUMN interesse3 VARCHAR(30);
SELECT * FROM contatos_antigos;'''),
    (8, "UPDATE todos seus interesses", "Separando com split_part",
     "Preencha as três colunas com `split_part(interesses, ',', 1)`, `2` e `3` (no MySQL seria "
     "`SUBSTRING_INDEX`). Use `NULLIF(..., '')` para que a falta de valor vire `NULL`.",
     '''%%sql
UPDATE contatos_antigos SET
    interesse1 = NULLIF(split_part(interesses, ',', 1), ''),
    interesse2 = NULLIF(split_part(interesses, ',', 2), ''),
    interesse3 = NULLIF(split_part(interesses, ',', 3), '');
SELECT contato_id, primeiro_nome, interesse1, interesse2, interesse3 FROM contatos_antigos ORDER BY contato_id;'''),
    (8, "CREATE, SELECT, e INSERT a (quase)", "CREATE e depois INSERT ... SELECT",
     "Crie `lista_interesses (id SERIAL PRIMARY KEY, interesse VARCHAR(30))` e preencha com os valores distintos "
     "de `interesse1` (sem nulos), em ordem.",
     '''%%sql
CREATE TABLE lista_interesses (id SERIAL PRIMARY KEY, interesse VARCHAR(30));
INSERT INTO lista_interesses (interesse)
SELECT DISTINCT interesse1 FROM contatos_antigos WHERE interesse1 IS NOT NULL ORDER BY interesse1;
SELECT * FROM lista_interesses;'''),
    (8, "CREATE, SELECT e INSERT ao mesmo tempo", "CREATE TABLE ... AS SELECT",
     "Crie numa só instrução a tabela `todos_interesses` com **todos** os interesses distintos das três colunas "
     "(junte com `UNION`).",
     '''%%sql
CREATE TABLE todos_interesses AS
SELECT interesse1 AS interesse FROM contatos_antigos WHERE interesse1 IS NOT NULL
UNION SELECT interesse2 FROM contatos_antigos WHERE interesse2 IS NOT NULL
UNION SELECT interesse3 FROM contatos_antigos WHERE interesse3 IS NOT NULL;
SELECT * FROM todos_interesses ORDER BY interesse;'''),
    (8, "Pseudônimos de coluna", "AS em colunas",
     "Mostre primeiro nome, sobrenome e aniversário de `meus_contatos` com os títulos `nome`, `sobrenome` e "
     "`nascimento`.",
     '''%%sql
SELECT primeiro_nome AS nome, sobrenome, aniversario AS nascimento FROM meus_contatos;'''),
    (8, "Pseudônimos de tabelas", "AS em tabelas",
     "Repita usando o apelido `mc` para a tabela (`FROM meus_contatos AS mc`) e `mc.coluna` no SELECT.",
     '''%%sql
SELECT mc.primeiro_nome AS nome, mc.email FROM meus_contatos AS mc WHERE mc.sexo = 'F';'''),
    (8, "Conexão cartesiana", "CROSS JOIN",
     "Combine cada garoto com cada brinquedo (`CROSS JOIN`) e conte as linhas. Quanto deveria dar?",
     '''%%sql
SELECT COUNT(*) AS combinacoes,
       (SELECT COUNT(*) FROM garotos) * (SELECT COUNT(*) FROM brinquedos) AS esperado
FROM garotos CROSS JOIN brinquedos;'''),
    (8, "A conexão interna em ação: a equijoin", "INNER JOIN (equijoin)",
     "Mostre cada garoto com o **seu** brinquedo (`INNER JOIN ... ON g.brinquedo_id = b.brinquedo_id`).",
     '''%%sql
SELECT g.garoto, b.brinquedo
FROM garotos AS g
INNER JOIN brinquedos AS b ON g.brinquedo_id = b.brinquedo_id
ORDER BY g.garoto;'''),
    (8, "A conexão interna em ação: a não-equijoin", "Não-equijoin",
     "Mostre, para cada garoto, os brinquedos que ele **não** tem (`ON g.brinquedo_id <> b.brinquedo_id`).",
     '''%%sql
SELECT g.garoto, b.brinquedo
FROM garotos AS g
INNER JOIN brinquedos AS b ON g.brinquedo_id <> b.brinquedo_id
ORDER BY g.garoto, b.brinquedo;'''),
    (8, "A última conexão interna: a conexão natural", "NATURAL JOIN",
     "As duas tabelas têm a coluna `brinquedo_id`. Use `NATURAL JOIN` e compare com a equijoin.",
     '''%%sql
SELECT garoto, brinquedo FROM garotos NATURAL JOIN brinquedos ORDER BY garoto;'''),
    (8, "Consultas conectadas", "Várias tabelas de uma vez",
     "Mostre nome, profissão, cidade, UF e estado civil de cada contato juntando `meus_contatos`, `profissao`, "
     "`codigos_cep` e `estado_civil`. Depois acrescente os interesses de cada um numa só célula com "
     "`string_agg` (via `contato_interesse` e `interesses`).",
     '''%%sql
SELECT mc.primeiro_nome, p.profissao, c.cidade, c.uf, e.status,
       string_agg(i.interesse, ', ' ORDER BY i.interesse) AS interesses
FROM meus_contatos mc
JOIN profissao p ON p.prof_id = mc.prof_id
JOIN codigos_cep c ON c.cep = mc.cep
JOIN estado_civil e ON e.status_id = mc.status_id
LEFT JOIN contato_interesse ci ON ci.contato_id = mc.contato_id
LEFT JOIN interesses i ON i.interesse_id = ci.interesse_id
GROUP BY mc.contato_id, mc.primeiro_nome, p.profissao, c.cidade, c.uf, e.status
ORDER BY mc.contato_id;'''),

    # ---------------- 9. Subconsultas ----------------
    (9, "Greg utiliza uma conexão interior", "Primeiro, com junção",
     "Mostre nome e cargo desejado de quem quer ser `Desenvolvedora Web` ou `Desenvolvedor Web` (junte "
     "`meus_contatos` e `emprego_desejado`).",
     '''%%sql
SELECT mc.primeiro_nome, ed.cargo
FROM meus_contatos mc
JOIN emprego_desejado ed ON ed.contato_id = mc.contato_id
WHERE ed.cargo IN ('Desenvolvedora Web', 'Desenvolvedor Web');'''),
    (9, "Subconsultas", "IN com subconsulta",
     "Agora sem escrever os cargos à mão: quem deseja um cargo que aparece em `vagas` (`IN (SELECT cargo FROM "
     "vagas)`)?",
     '''%%sql
SELECT mc.primeiro_nome, ed.cargo
FROM meus_contatos mc
JOIN emprego_desejado ed ON ed.contato_id = mc.contato_id
WHERE ed.cargo IN (SELECT cargo FROM vagas);'''),
    (9, "Uma subconsulta em ação", "Subconsulta que devolve um valor",
     "Mostre os contatos que moram em Natal usando `cep = (SELECT cep FROM codigos_cep WHERE cidade = 'Natal')`.",
     '''%%sql
SELECT primeiro_nome, cep FROM meus_contatos
WHERE cep = (SELECT cep FROM codigos_cep WHERE cidade = 'Natal');'''),
    (9, "Um acompanhamento na construção", "Construindo de dentro para fora",
     "Quem ganha **acima da média** em `emprego_atual`? Rode antes só a subconsulta (`SELECT AVG(salario) ...`) "
     "numa célula nova para ver o número; depois use-a no `WHERE`.",
     '''%%sql
SELECT mc.primeiro_nome, ea.cargo, ea.salario
FROM emprego_atual ea JOIN meus_contatos mc ON mc.contato_id = ea.contato_id
WHERE ea.salario > (SELECT AVG(salario) FROM emprego_atual)
ORDER BY ea.salario DESC;'''),
    (9, "Uma subconsulta como uma coluna", "Subconsulta no SELECT",
     "Mostre o nome de cada contato e a cidade dele usando uma subconsulta **como coluna**: "
     "`(SELECT cidade FROM codigos_cep c WHERE c.cep = mc.cep) AS cidade`.",
     '''%%sql
SELECT mc.primeiro_nome,
       (SELECT cidade FROM codigos_cep c WHERE c.cep = mc.cep) AS cidade
FROM meus_contatos mc;'''),
    (9, "Outro exemplo: Subconsulta com uma conexão natural", "Quem ganha mais",
     "Mostre nome e salário de quem tem o **maior** salário atual (`NATURAL JOIN` + `= (SELECT MAX(...))`).",
     '''%%sql
SELECT primeiro_nome, salario
FROM meus_contatos NATURAL JOIN emprego_atual
WHERE salario = (SELECT MAX(salario) FROM emprego_atual);'''),
    (9, "Uma subconsulta não-correlacionada com múltiplos valores", "NOT IN",
     "Quais profissões da tabela `profissao` não têm **nenhum** contato? Use `NOT IN (SELECT prof_id FROM "
     "meus_contatos)`.",
     '''%%sql
SELECT profissao FROM profissao
WHERE prof_id NOT IN (SELECT prof_id FROM meus_contatos WHERE prof_id IS NOT NULL);'''),
    (9, "Subconsultas correlacionadas", "Subconsulta correlacionada",
     "Mostre os contatos com **exatamente 3** interesses. A subconsulta usa o `contato_id` da consulta de fora.",
     '''%%sql
SELECT mc.primeiro_nome
FROM meus_contatos mc
WHERE 3 = (SELECT COUNT(*) FROM contato_interesse ci WHERE ci.contato_id = mc.contato_id);'''),
    (9, "Uma subconsulta correlacionada (útil) com NOT EXISTS", "NOT EXISTS",
     "Quem **não** tem emprego atual?",
     '''%%sql
SELECT mc.primeiro_nome, mc.email
FROM meus_contatos mc
WHERE NOT EXISTS (SELECT 1 FROM emprego_atual ea WHERE ea.contato_id = mc.contato_id);'''),
    (9, "EXISTS e NOT EXISTS", "EXISTS",
     "Quem tem pelo menos um interesse entre `xadrez` e `games`?",
     '''%%sql
SELECT mc.primeiro_nome
FROM meus_contatos mc
WHERE EXISTS (
    SELECT 1 FROM contato_interesse ci JOIN interesses i ON i.interesse_id = ci.interesse_id
    WHERE ci.contato_id = mc.contato_id AND i.interesse IN ('xadrez', 'games'));'''),
    (9, "A empresa de Greg para serviços", "Candidatos para cada vaga",
     "Para cada vaga, liste os contatos que desejam aquele cargo, estão disponíveis (`disponivel = 'S'`) e cujo "
     "`salario_min` cabe no salário da vaga.",
     '''%%sql
SELECT v.cargo, v.salario, mc.primeiro_nome, ed.salario_min
FROM vagas v
JOIN emprego_desejado ed ON ed.cargo = v.cargo
JOIN meus_contatos mc ON mc.contato_id = ed.contato_id
WHERE ed.disponivel = 'S' AND ed.salario_min <= v.salario
ORDER BY v.cargo;'''),

    # ---------------- 10. Junções externas e uniões ----------------
    (10, "Aqui está uma conexão externa esquerda", "LEFT JOIN",
     "Mostre **todos** os garotos com o brinquedo de cada um. O `Noé` não tem brinquedo: o que aparece?",
     '''%%sql
SELECT g.garoto, b.brinquedo
FROM garotos g LEFT JOIN brinquedos b ON g.brinquedo_id = b.brinquedo_id
ORDER BY g.garoto;'''),
    (10, "É uma questão de esquerda e direita", "Trocando o lado",
     "Agora `brinquedos LEFT JOIN garotos`: quais brinquedos ninguém tem? (Filtre com `g.garoto IS NULL`.)",
     '''%%sql
SELECT b.brinquedo
FROM brinquedos b LEFT JOIN garotos g ON g.brinquedo_id = b.brinquedo_id
WHERE g.garoto IS NULL;'''),
    (10, "Conexão externa direita", "RIGHT JOIN",
     "Escreva o mesmo resultado com `garotos RIGHT JOIN brinquedos`.",
     '''%%sql
SELECT b.brinquedo
FROM garotos g RIGHT JOIN brinquedos b ON g.brinquedo_id = b.brinquedo_id
WHERE g.garoto IS NULL;'''),
    (10, "Conexões externas e combinações múltiplas", "LEFT JOIN com várias tabelas",
     "Mostre todos os contatos, o emprego atual (se houver) e o cargo desejado (se houver).",
     '''%%sql
SELECT mc.primeiro_nome, ea.cargo AS cargo_atual, ed.cargo AS cargo_desejado
FROM meus_contatos mc
LEFT JOIN emprego_atual ea ON ea.contato_id = mc.contato_id
LEFT JOIN emprego_desejado ed ON ed.contato_id = mc.contato_id
ORDER BY mc.contato_id;'''),
    (10, "Enquanto você estava conectando externamente", "FULL OUTER JOIN",
     "O MySQL do livro não tem `FULL OUTER JOIN`; o PostgreSQL tem. Mostre garotos e brinquedos, incluindo "
     "garotos sem brinquedo **e** brinquedos sem garoto.",
     '''%%sql
SELECT g.garoto, b.brinquedo
FROM garotos g FULL OUTER JOIN brinquedos b ON g.brinquedo_id = b.brinquedo_id
ORDER BY g.garoto NULLS LAST, b.brinquedo;'''),
    (10, "Uma chave externa auto-referenciada", "Chave que aponta para a própria tabela",
     "Em `palhacos`, `chefe_id` aponta para outro palhaço. Insira o palhaço `Bolinha` (id 7) com chefe `Zazá` "
     "(id 6) e mostre a tabela.",
     '''%%sql
INSERT INTO palhacos VALUES (7, 'Bolinha', 6);
SELECT * FROM palhacos ORDER BY palhaco_id;'''),
    (10, "Nós precisamos de uma autoconexão", "SELF-JOIN",
     "Mostre cada palhaço e o nome do seu chefe juntando `palhacos` com ela mesma (apelidos `p` e `chefe`). Use "
     "`LEFT JOIN` para o Pipoca (sem chefe) aparecer.",
     '''%%sql
SELECT p.nome AS palhaco, chefe.nome AS chefe
FROM palhacos p LEFT JOIN palhacos chefe ON p.chefe_id = chefe.palhaco_id
ORDER BY p.palhaco_id;'''),
    (10, "Você pode utilizar uma UNION", "UNION",
     "Liste todos os cargos que aparecem em `emprego_atual`, `emprego_desejado` e `vagas`, sem repetir, em ordem.",
     '''%%sql
SELECT cargo FROM emprego_atual
UNION SELECT cargo FROM emprego_desejado
UNION SELECT cargo FROM vagas
ORDER BY cargo;'''),
    (10, "UNION ALL", "UNION ALL mantém os repetidos",
     "Conte quantas linhas saem com `UNION` e com `UNION ALL` (use cada união como subconsulta no `FROM`).",
     '''%%sql
SELECT
  (SELECT COUNT(*) FROM (SELECT cargo FROM emprego_atual UNION SELECT cargo FROM emprego_desejado
                         UNION SELECT cargo FROM vagas) AS u) AS com_union,
  (SELECT COUNT(*) FROM (SELECT cargo FROM emprego_atual UNION ALL SELECT cargo FROM emprego_desejado
                         UNION ALL SELECT cargo FROM vagas) AS ua) AS com_union_all;'''),
    (10, "Crie uma tabela a partir da sua UNION", "CREATE TABLE AS com UNION",
     "Crie a tabela `cargos` a partir da `UNION` dos três cargos.",
     '''%%sql
CREATE TABLE cargos AS
SELECT cargo FROM emprego_atual UNION SELECT cargo FROM emprego_desejado UNION SELECT cargo FROM vagas;
SELECT COUNT(*) AS cargos_distintos FROM cargos;'''),
    (10, "INTERSECT e EXCEPT", "INTERSECT e EXCEPT",
     "Quais cargos têm vaga aberta **e** alguém que deseja (`INTERSECT`)? E quais cargos têm vaga mas ninguém "
     "deseja (`EXCEPT`)? (O MySQL antigo do livro não tinha esses dois.) Mostre os dois com uma coluna de "
     "identificação.",
     '''%%sql
(SELECT 'vaga e desejo' AS grupo, cargo FROM vagas INTERSECT SELECT 'vaga e desejo', cargo FROM emprego_desejado)
UNION ALL
(SELECT 'só vaga', cargo FROM vagas EXCEPT SELECT 'só vaga', cargo FROM emprego_desejado)
ORDER BY grupo, cargo;'''),
    (10, "Transformando uma subconsulta em uma conexão", "De subconsulta para junção",
     "Reescreva com `INNER JOIN` a consulta do capítulo 9: quem deseja um cargo que aparece em `vagas`. Use "
     "`DISTINCT` para não repetir.",
     '''%%sql
SELECT DISTINCT mc.primeiro_nome, ed.cargo
FROM meus_contatos mc
JOIN emprego_desejado ed ON ed.contato_id = mc.contato_id
JOIN vagas v ON v.cargo = ed.cargo
ORDER BY mc.primeiro_nome;'''),
    (10, "Um autorrelacionamento como uma subconsulta", "Self-join com subconsulta",
     "Mostre cada palhaço e o nome do chefe usando uma subconsulta no `SELECT` em vez de junção.",
     '''%%sql
SELECT p.nome AS palhaco,
       (SELECT c.nome FROM palhacos c WHERE c.palhaco_id = p.chefe_id) AS chefe
FROM palhacos p ORDER BY p.palhaco_id;'''),

    # ---------------- 11. Restrições, views e transações ----------------
    (11, "CHECK, por favor", "CHECK CONSTRAINT",
     "No `cofrinho` só entram moedas de 0.05, 0.10, 0.25, 0.50 e 1.00. Crie a restrição `moeda_valida` e tente "
     "inserir uma moeda de 0.03 (`try/except`).",
     '''%sql ALTER TABLE cofrinho ADD CONSTRAINT moeda_valida CHECK (moeda IN (0.05, 0.10, 0.25, 0.50, 1.00))
try:
    %sql INSERT INTO cofrinho (moeda) VALUES (0.03)
except Exception as erro:
    print("Bloqueado pelo CHECK:", "moeda_valida" in str(erro))
%sql SELECT * FROM cofrinho ORDER BY id'''),
    (11, "CHECKando o sexo", "CHECK em texto",
     "Garanta que `meus_contatos.sexo` só aceita `M` ou `F` e tente atualizar alguém para `X`.",
     '''%sql ALTER TABLE meus_contatos ADD CONSTRAINT sexo_valido CHECK (sexo IN ('M', 'F'))
try:
    %sql UPDATE meus_contatos SET sexo = 'X' WHERE contato_id = 1
except Exception as erro:
    print("Bloqueado pelo CHECK:", "sexo_valido" in str(erro))'''),
    (11, "Criando uma view", "CREATE VIEW",
     "Crie a view `desenvolvedores_web` com nome, sobrenome, telefone e email de quem deseja um cargo que "
     "começa com `Desenvolvedor`.",
     '''%%sql
CREATE VIEW desenvolvedores_web AS
SELECT mc.primeiro_nome, mc.sobrenome, mc.telefone, mc.email
FROM meus_contatos mc
NATURAL JOIN emprego_desejado ed
WHERE ed.cargo LIKE 'Desenvolvedor%';
SELECT * FROM desenvolvedores_web;'''),
    (11, "Visualizando suas views", "Listando as views",
     "Liste as views do esquema (`information_schema.views`) com a definição de cada uma.",
     '''%%sql
SELECT table_name AS view, view_definition
FROM information_schema.views WHERE table_schema = current_schema();'''),
    (11, "O que sua view está realmente fazendo", "A view é uma consulta guardada",
     "Mostre que `SELECT * FROM desenvolvedores_web` é o mesmo que usar a consulta da view como subconsulta no "
     "`FROM` (dê um apelido para ela).",
     '''%%sql
SELECT * FROM (
    SELECT mc.primeiro_nome, mc.sobrenome, mc.telefone, mc.email
    FROM meus_contatos mc NATURAL JOIN emprego_desejado ed
    WHERE ed.cargo LIKE 'Desenvolvedor%'
) AS dw;'''),
    (11, "Inserindo, atualizando e deletando com views", "Inserindo pela view",
     "Crie a view `moedas_grandes` (moedas >= 0.50 do `cofrinho`) e insira uma moeda de 1.00 **pela view**. "
     "Confira na tabela.",
     '''%%sql
CREATE VIEW moedas_grandes AS SELECT id, moeda, data_moeda FROM cofrinho WHERE moeda >= 0.50;
INSERT INTO moedas_grandes (moeda) VALUES (1.00);
SELECT * FROM cofrinho ORDER BY id;'''),
    (11, "View com CHECK OPTION", "WITH CHECK OPTION",
     "Sem proteção, a view aceitaria uma moeda de 0.10 (que ela nem mostra). Recrie com `WITH CHECK OPTION` e "
     "tente inserir 0.10 por ela (`try/except`).",
     '''%sql CREATE OR REPLACE VIEW moedas_grandes AS SELECT id, moeda, data_moeda FROM cofrinho WHERE moeda >= 0.50 WITH CHECK OPTION
try:
    %sql INSERT INTO moedas_grandes (moeda) VALUES (0.10)
except Exception as erro:
    print("Bloqueado pelo CHECK OPTION:", "check option" in str(erro).lower())'''),
    (11, "Quando você tiver terminado com sua view", "DROP VIEW",
     "Apague a view `moedas_grandes` e confira a lista de views.",
     '''%%sql
DROP VIEW moedas_grandes;
SELECT table_name FROM information_schema.views WHERE table_schema = current_schema();'''),
    (11, "O que aconteceu dentro do caixa eletrônico", "Dinheiro sumindo sem transação",
     "Simule uma transferência de R$ 100 da conta 101 para a 202 que falha no meio: o débito roda, um erro em "
     "Python acontece antes do crédito. Mostre o saldo total antes e depois. Em seguida, devolva os R$ 100 à "
     "conta 101.",
     '''def total():
    resultado = %sql SELECT SUM(saldo) AS total FROM contas
    return resultado
print("antes:", total())
try:
    %sql UPDATE contas SET saldo = saldo - 100 WHERE conta = 101
    raise RuntimeError("queda de energia no caixa eletrônico!")
    %sql UPDATE contas SET saldo = saldo + 100 WHERE conta = 202
except RuntimeError as erro:
    print(erro)
print("depois:", total())
%sql UPDATE contas SET saldo = saldo + 100 WHERE conta = 101'''),
    (11, "SQL ajuda a gerenciar suas transações", "BEGIN e COMMIT",
     "Faça a transferência de R$ 100 dentro de uma transação: `BEGIN;`, os dois `UPDATE`s, `COMMIT;`. Mostre os "
     "saldos. (No MySQL é `START TRANSACTION`.)",
     '''%%sql
BEGIN;
UPDATE contas SET saldo = saldo - 100 WHERE conta = 101;
UPDATE contas SET saldo = saldo + 100 WHERE conta = 202;
COMMIT;
SELECT * FROM contas ORDER BY conta;'''),
    (11, "O teste clássico ACID", "Atomicidade: tudo ou nada",
     "Crie a regra `saldo >= 0` em `contas`. Em Python, com `with motor.begin() as con:` (transação do "
     "SQLAlchemy), tente transferir R$ 10.000 da conta 202 para a 101: o crédito roda primeiro e o débito viola "
     "a regra. Mostre que **nenhum** dos dois ficou gravado.",
     '''from sqlalchemy import text
%sql ALTER TABLE contas ADD CONSTRAINT saldo_nao_negativo CHECK (saldo >= 0)
try:
    with motor.begin() as con:
        con.execute(text("UPDATE contas SET saldo = saldo + 10000 WHERE conta = 101"))
        con.execute(text("UPDATE contas SET saldo = saldo - 10000 WHERE conta = 202"))
except Exception as erro:
    print("Transação desfeita por inteiro:", type(erro).__name__)
%sql SELECT * FROM contas ORDER BY conta'''),
    (11, "Agora tente você mesmo", "ROLLBACK",
     "Abra uma transação, zere o saldo de todo mundo, confira dentro da própria transação e desfaça com "
     "`ROLLBACK`. Termine mostrando os saldos.",
     '''%%sql
BEGIN;
UPDATE contas SET saldo = 0;
ROLLBACK;
SELECT * FROM contas ORDER BY conta;'''),

    # ---------------- 12. Segurança ----------------
    (12, "Proteja a conta de usuários raiz", "Quem é você no banco",
     "Mostre o usuário atual e se ele é superusuário (`pg_roles.rolsuper`). Liste também os papéis que não são do "
     "sistema (nome sem `pg_`). O usuário `estudos` é o \"root\" deste banco.",
     '''%%sql
SELECT rolname, rolsuper, rolcanlogin
FROM pg_roles WHERE rolname NOT LIKE 'pg%' ORDER BY rolname;'''),
    (12, "Adicione um novo usuário", "CREATE ROLE ... LOGIN",
     "Crie o usuário `estagiaria` (`CREATE ROLE estagiaria LOGIN`; num servidor de verdade você daria também uma "
     "senha). Confira que ele ainda não pode ler `palhacos_info` (`has_table_privilege`).",
     '''%%sql
CREATE ROLE estagiaria LOGIN;
SELECT has_table_privilege('estagiaria', 'palhacos_info', 'SELECT') AS pode_ler;'''),
    (12, "Um simples comando GRANT", "GRANT SELECT",
     "Dê à `estagiaria` permissão de leitura em `palhacos_info`. Depois \"vire\" a estagiária com `SET ROLE`, "
     "conte as linhas e volte com `RESET ROLE`.",
     '''%%sql
GRANT SELECT ON palhacos_info TO estagiaria;
SET ROLE estagiaria;
SELECT current_user, COUNT(*) AS palhacos FROM palhacos_info;'''),
    (12, "Um simples comando GRANT", "Testando o que ela não pode",
     "Ainda como `estagiaria`, tente apagar um palhaço (`try/except`). Volte para o seu usuário no `finally`.",
     '''try:
    %sql DELETE FROM palhacos_info WHERE palhaco_id = 1
except Exception as erro:
    print("Sem permissão:", "permission denied" in str(erro) or "permissão negada" in str(erro))
finally:
    %sql RESET ROLE
%sql SELECT current_user'''),
    (12, "Variações do comando GRANT", "Várias permissões e permissão por coluna",
     "Dê à `estagiaria` `SELECT` e `INSERT` em `info_local`, e `UPDATE` **só** na coluna `descricao` de "
     "`palhacos_info`. Confira com `has_table_privilege` e `has_column_privilege`.",
     '''%%sql
GRANT SELECT, INSERT ON info_local TO estagiaria;
GRANT UPDATE (descricao) ON palhacos_info TO estagiaria;
SELECT has_table_privilege('estagiaria', 'info_local', 'INSERT') AS insere_local,
       has_column_privilege('estagiaria', 'palhacos_info', 'descricao', 'UPDATE') AS muda_descricao,
       has_column_privilege('estagiaria', 'palhacos_info', 'nome', 'UPDATE') AS muda_nome;'''),
    (12, "REVOKE (REVOGUE) privilégios", "REVOKE",
     "Retire o `INSERT` em `info_local` da `estagiaria` e confira.",
     '''%%sql
REVOKE INSERT ON info_local FROM estagiaria;
SELECT has_table_privilege('estagiaria', 'info_local', 'SELECT') AS le,
       has_table_privilege('estagiaria', 'info_local', 'INSERT') AS insere;'''),
    (12, "REVOGANDO uma GRANT OPTION usada", "WITH GRANT OPTION e CASCADE",
     "Crie `gerente_palhacos` e `visitante`. Dê ao gerente `SELECT` em `atividades` `WITH GRANT OPTION`. Como "
     "gerente (`SET ROLE`), repasse ao visitante. Volte (`RESET ROLE`), revogue do gerente com `CASCADE` e veja "
     "que o visitante também perdeu.",
     '''%%sql
CREATE ROLE gerente_palhacos;
CREATE ROLE visitante;
GRANT SELECT ON atividades TO gerente_palhacos WITH GRANT OPTION;
SET ROLE gerente_palhacos;
GRANT SELECT ON atividades TO visitante;
RESET ROLE;
REVOKE SELECT ON atividades FROM gerente_palhacos CASCADE;
SELECT has_table_privilege('gerente_palhacos', 'atividades', 'SELECT') AS gerente,
       has_table_privilege('visitante', 'atividades', 'SELECT') AS visitante;'''),
    (12, "REVOGANDO com mais precisão", "RESTRICT",
     "Repita o repasse e agora tente revogar com `RESTRICT` (padrão): como há uma permissão dependente, o banco "
     "recusa (`try/except`). Depois revogue só a opção de repassar: `REVOKE GRANT OPTION FOR ... CASCADE`.",
     '''%sql GRANT SELECT ON atividades TO gerente_palhacos WITH GRANT OPTION
%sql SET ROLE gerente_palhacos
%sql GRANT SELECT ON atividades TO visitante
%sql RESET ROLE
try:
    %sql REVOKE SELECT ON atividades FROM gerente_palhacos RESTRICT
except Exception as erro:
    print("RESTRICT recusou: existem permissões dependentes")
%sql REVOKE GRANT OPTION FOR SELECT ON atividades FROM gerente_palhacos CASCADE
%sql SELECT has_table_privilege('gerente_palhacos', 'atividades', 'SELECT') AS gerente_ainda_le, has_table_privilege('gerente_palhacos', 'atividades', 'SELECT WITH GRANT OPTION') AS pode_repassar'''),
    (12, "Utilizando sua role", "Papéis (roles) de grupo",
     "Crie o papel `equipe_dados` com `SELECT` em `palhacos_info` e `info_local`. Crie o usuário "
     "`leitor_relatorios` (LOGIN) e coloque-o no papel (`GRANT equipe_dados TO leitor_relatorios`). Ele herdou "
     "a leitura?",
     '''%%sql
CREATE ROLE equipe_dados;
GRANT SELECT ON palhacos_info, info_local TO equipe_dados;
CREATE ROLE leitor_relatorios LOGIN;
GRANT equipe_dados TO leitor_relatorios;
SELECT has_table_privilege('leitor_relatorios', 'info_local', 'SELECT') AS le_local,
       has_table_privilege('leitor_relatorios', 'atividades', 'SELECT') AS le_atividades;'''),
    (12, "Eliminando roles", "DROP ROLE",
     "Elimine o papel `visitante`. Antes, tire as permissões dele com `DROP OWNED BY visitante` (o banco não "
     "deixa apagar um papel que ainda tem permissões).",
     '''%%sql
DROP OWNED BY visitante;
DROP ROLE visitante;
SELECT rolname FROM pg_roles WHERE rolname = 'visitante';'''),
    (12, "Utilizando sua role WITH ADMIN OPTION", "WITH ADMIN OPTION",
     "Crie `chefe_equipe` e dê a ele o papel `equipe_dados` `WITH ADMIN OPTION`: ele pode colocar outras pessoas "
     "no papel. Como chefe, coloque a `estagiaria`. Confira em `pg_auth_members`.",
     '''%%sql
CREATE ROLE chefe_equipe;
GRANT equipe_dados TO chefe_equipe WITH ADMIN OPTION;
SET ROLE chefe_equipe;
GRANT equipe_dados TO estagiaria;
RESET ROLE;
SELECT r.rolname AS papel, m.rolname AS membro, a.admin_option
FROM pg_auth_members a
JOIN pg_roles r ON r.oid = a.roleid
JOIN pg_roles m ON m.oid = a.member
WHERE r.rolname = 'equipe_dados'
ORDER BY membro;'''),
    (12, "Combinando CREATE USER com GRANT", "Criar o usuário já no papel",
     "No MySQL dá para criar e dar permissões de uma vez. No PostgreSQL: `CREATE USER novato IN ROLE "
     "equipe_dados` (`CREATE USER` = `CREATE ROLE ... LOGIN`). Confira que ele lê `palhacos_info`.",
     '''%%sql
CREATE USER novato IN ROLE equipe_dados;
SELECT has_table_privilege('novato', 'palhacos_info', 'SELECT') AS novato_le;'''),
    (12, "A lista de Greg agora é global", "Relatório de permissões",
     "Monte o relatório de quem pode o quê nas tabelas deste esquema (`information_schema.role_table_grants`), "
     "sem o seu próprio usuário.",
     '''%%sql
SELECT grantee AS quem, table_name AS tabela, string_agg(privilege_type, ', ' ORDER BY privilege_type) AS pode
FROM information_schema.role_table_grants
WHERE table_schema = current_schema() AND grantee <> current_user
GROUP BY grantee, table_name
ORDER BY grantee, table_name;'''),
]

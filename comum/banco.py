"""Prepara o banco PostgreSQL de cada capítulo do Use a Cabeça! SQL.

Cada capítulo tem um esquema próprio, que funciona como um "banco" separado:
- praticar/ usa cap01, cap02, ...
- resolvidos/ usa gab_cap01, gab_cap02, ... (o gabarito nunca mexe no que você fez)

preparar(n) cria o esquema e as tabelas iniciais do capítulo só na primeira vez.
preparar(n, recomecar=True) apaga o esquema e começa do zero.

Os dados são fictícios e foram criados para estes estudos (não são os do livro).
O banco sobe com `docker compose up -d` na pasta do repositório (porta 5434).
"""
import os

import psycopg
from sqlalchemy import create_engine

URL = os.environ.get("USE_A_CABECA_SQL_URL", "postgresql://estudos:estudos@127.0.0.1:5434/use_a_cabeca")

# ---------------------------------------------------------------- dados iniciais por capítulo
CONTATOS_SIMPLES = """
CREATE TABLE meus_contatos (
    sobrenome VARCHAR(30), primeiro_nome VARCHAR(20), email VARCHAR(50), sexo CHAR(1),
    aniversario DATE, profissao VARCHAR(50), local VARCHAR(50), estado_civil VARCHAR(20),
    interesses VARCHAR(100), procurando VARCHAR(100));
INSERT INTO meus_contatos VALUES
('Albuquerque','Ana','ana.alb@exemplo.com','F','1990-03-14','Engenheira de Software','Recife, PE','solteira','cinema, trilhas, xadrez','amizade'),
('Barbosa','Bruno','bruno.b@exemplo.com','M','1985-07-02','Professor','Olinda, PE','casado','futebol, leitura','networking'),
('Cardoso','Carla','carla.c@exemplo.com','F','1993-11-23','Designer','Natal, RN','solteira','desenho, cinema','relacionamento'),
('Dantas','Davi','davi.d@exemplo.com','M','1979-01-30','Médico','Recife, PE','divorciado','corrida, culinária','relacionamento'),
('Esteves','Elisa','elisa.e@exemplo.com','F','1988-05-09','Advogada','João Pessoa, PB','solteira','xadrez, viagens','amizade'),
('Farias','Fábio','fabio.f@exemplo.com','M','1995-09-17','Engenheiro de Software','Fortaleza, CE','solteiro','games, trilhas','relacionamento'),
('Gomes','Gabi','gabi.g@exemplo.com','F','1991-12-01','Jornalista','Salvador, BA','casada','leitura, viagens','networking'),
('Holanda','Heitor','heitor.h@exemplo.com','M','1983-04-26','Chef','Recife, PE','solteiro','culinária, música','amizade'),
('Ibiapina','Iara',NULL,'F','1997-08-08','Estudante','Teresina, PI','solteira','dança, cinema','amizade'),
('Jucá','Joana','joana.j@exemplo.com','F','1986-02-19','Professora','Natal, RN',NULL,'leitura','relacionamento'),
('Lins','Lucas','lucas.l@exemplo.com','M','1992-10-05','Analista de Dados','Maceió, AL','solteiro','xadrez, games','networking'),
('Moura','Marina','marina.m@exemplo.com','F','1989-06-11','Analista de Dados','Recife, PE','solteira','trilhas, fotografia','amizade');
"""

BEBIDAS = """
CREATE TABLE bebidas_faceis (
    nome_bebida VARCHAR(30), principal VARCHAR(30), qtd1 DECIMAL(4,1), segundo VARCHAR(30),
    qtd2 DECIMAL(4,1), instrucoes VARCHAR(120));
INSERT INTO bebidas_faceis VALUES
('Brisa de Caju','suco de caju',4.0,'água com gás',2.0,'misture com gelo'),
('Pôr do Sol','suco de laranja',3.0,'xarope de groselha',0.5,'coloque a groselha por último'),
('Verde Limão','água de coco',5.0,'suco de limão',1.0,'sirva bem gelado'),
('Mate Gelado','chá mate',6.0,'suco de limão',1.5,'adoce a gosto'),
('Frescor','água com gás',4.0,'hortelã',0.3,'amasse a hortelã antes'),
('Tropical','suco de abacaxi',3.0,'leite de coco',1.0,'bata no liquidificador'),
('Nuvem Rosa','suco de morango',3.5,'iogurte',2.0,'bata e sirva com canudo'),
('Doce Lima','suco de lima',4.0,'mel',0.5,'mexa até dissolver o mel'),
('Caju Mate','chá mate',3.0,'suco de caju',3.0,'misture com gelo');

CREATE TABLE notas_cafeterias (
    local VARCHAR(30), visita DATE, item VARCHAR(30), nota INT, comentario VARCHAR(60));
INSERT INTO notas_cafeterias VALUES
('Café da Praça','2024-03-02','bolo de rolo',9,'massa fininha'),
('Café da Praça','2024-03-09','tapioca',7,'recheio pouco'),
('Padaria Aurora','2024-03-03','pão de queijo',8,'quentinho'),
('Padaria Aurora','2024-03-10','bolo de rolo',6,'muito doce'),
('Grão Fino','2024-03-05','café coado',10,'o melhor da cidade'),
('Grão Fino','2024-03-12','tapioca',8,NULL),
('Casa do Bolo','2024-03-06','bolo de rolo',10,'perfeito');
"""

PALHACOS = """
CREATE TABLE palhacos_info (
    nome VARCHAR(30), ultima_vez_visto VARCHAR(40), aparencia VARCHAR(60), atividades VARCHAR(60));
INSERT INTO palhacos_info VALUES
('Pipoca','Festa da Rua Aurora','M, cabelo azul, sapato gigante','malabarismo, balões'),
('Biribinha','Escola Pequeno Príncipe','F, nariz vermelho, saia de bolinhas','mágica, cantoria'),
('Tico-Tico','Shopping Boa Vista','M, chapéu-coco, gravata enorme','monociclo'),
('Lulu','Aniversário da Júlia','F, peruca rosa','pintura facial, balões'),
('Fuxico','Praça do Arsenal','M, macacão listrado','malabarismo, buzina'),
('Zazá','Hospital Esperança','F, óculos gigantes','contação de histórias'),
('Pirulito','Clube Náutico','M, suspensório amarelo','perna de pau'),
('Pipoca','Shopping Boa Vista','M, cabelo azul, sapato gigante','malabarismo, balões');

CREATE TABLE bebidas_precos (
    nome_bebida VARCHAR(30), preco DECIMAL(5,2), carboidratos DECIMAL(4,1), cor VARCHAR(15),
    gelo CHAR(1), calorias INT);
INSERT INTO bebidas_precos VALUES
('Brisa de Caju',8.00,22.5,'amarelo','S',90),
('Pôr do Sol',9.50,30.0,'laranja','S',120),
('Verde Limão',7.00,15.0,'verde','S',60),
('Mate Gelado',6.50,18.0,'marrom','S',70),
('Frescor',6.00,2.0,'transparente','S',10),
('Tropical',11.00,35.5,'branco','N',180),
('Nuvem Rosa',12.00,40.0,'rosa','N',210),
('Doce Lima',8.50,25.0,'amarelo','S',100);
"""

PESCADORES = """
CREATE TABLE info_peixes (nome_comum VARCHAR(30), especie VARCHAR(40), local VARCHAR(40), peso DECIMAL(5,1));
INSERT INTO info_peixes VALUES
('tucunaré','Cichla ocellaris','Manaus, AM',8.2),
('pirarucu','Arapaima gigas','Santarém, PA',96.0),
('dourado','Salminus brasiliensis','Corumbá, MS',12.5),
('robalo','Centropomus undecimalis','Ilhéus, BA',14.3),
('tambaqui','Colossoma macropomum','Porto Velho, RO',24.0);

CREATE TABLE recordes_peixes (
    primeiro_nome VARCHAR(20), sobrenome VARCHAR(30), nome_comum VARCHAR(30), local VARCHAR(40),
    uf CHAR(2), peso DECIMAL(5,1), data DATE);
INSERT INTO recordes_peixes VALUES
('Raimundo','Nonato','tucunaré','Manaus','AM',8.2,'2019-09-14'),
('Socorro','Lima','pirarucu','Santarém','PA',96.0,'2021-11-02'),
('Edson','Paiva','dourado','Corumbá','MS',12.5,'2018-08-20'),
('Mirela','Castro','robalo','Ilhéus','BA',14.3,'2022-01-07'),
('Jonas','Teixeira','tambaqui','Porto Velho','RO',24.0,'2020-06-30');
"""

ALTER_CAP5 = """
CREATE TABLE projetos (numero INT, descricaodoprojeto VARCHAR(40), empreiteiranaobra VARCHAR(40));
INSERT INTO projetos VALUES
(1,'pintar a fachada','Murillo Pinturas'),
(2,'trocar o telhado','Teto Firme'),
(3,'reformar a cozinha','Casa Nova Reformas'),
(4,'instalar placas solares','Sol Nascente');

CREATE TABLE calhambeques (cor VARCHAR(10), ano VARCHAR(4), marca VARCHAR(15), mod VARCHAR(20), preco VARCHAR(10));
INSERT INTO calhambeques VALUES
('prata','1998','Fiat','Uno Mille','4500.00'),
('vermelho','1986','VW','Fusca','9800.50'),
(NULL,'2001','Chevrolet','Celta','7200.00'),
('azul','1994','Ford','Escort','5300.00');
"""

FILMES_BISCOITOS = """
CREATE TABLE filmes (
    filme_id SERIAL PRIMARY KEY, titulo VARCHAR(50) NOT NULL, classificacao VARCHAR(5),
    drama CHAR(1), comedia CHAR(1), acao CHAR(1), terror CHAR(1), ficcao CHAR(1), infantil CHAR(1),
    desenho CHAR(1), compra CHAR(1));
INSERT INTO filmes (titulo, classificacao, drama, comedia, acao, terror, ficcao, infantil, desenho, compra) VALUES
('O Último Farol','14','T','F','F','F','F','F','F','F'),
('Robôs no Quintal','L','F','T','F','F','T','T','F','T'),
('Perseguição no Sertão','16','F','F','T','F','F','F','F','F'),
('A Casa do Fim da Rua','18','F','F','F','T','F','F','F','F'),
('Planeta Laranja','10','F','F','F','F','T','F','F','T'),
('Tartaruga Valente','L','F','F','F','F','F','T','T','F'),
('Risos na Feira','12','F','T','F','F','F','F','F','F'),
('Corrida das Estrelas','12','F','F','T','F','T','F','F','F'),
('Gato de Botas Azuis','L','F','T','F','F','F','T','T','T'),
('Memórias de Areia','14','T','F','F','F','F','F','F','F'),
('Zumbis de Domingo','16','F','T','F','T','F','F','F','F'),
('Anjos do Asfalto','14','T','F','T','F','F','F','F','F');

CREATE TABLE vendas_biscoitos (primeiro_nome VARCHAR(20), vendas DECIMAL(6,2), data DATE);
INSERT INTO vendas_biscoitos VALUES
('Lia',32.00,'2024-03-06'),('Nina',26.50,'2024-03-06'),('Bia',11.00,'2024-03-06'),('Duda',0.00,'2024-03-06'),
('Lia',15.00,'2024-03-07'),('Nina',43.50,'2024-03-07'),('Bia',30.00,'2024-03-07'),('Duda',19.00,'2024-03-07'),
('Lia',27.50,'2024-03-08'),('Nina',3.50,'2024-03-08'),('Bia',22.00,'2024-03-08'),('Duda',17.50,'2024-03-08'),
('Lia',0.00,'2024-03-09'),('Nina',36.00,'2024-03-09'),('Bia',41.00,'2024-03-09'),('Duda',28.00,'2024-03-09'),
('Lia',12.50,'2024-03-10'),('Nina',8.00,'2024-03-10');
"""

GREGS_LIST = """
CREATE TABLE profissao (prof_id SERIAL PRIMARY KEY, profissao VARCHAR(50) UNIQUE NOT NULL);
INSERT INTO profissao (profissao) VALUES
('Engenheira de Software'),('Professor'),('Designer'),('Médico'),('Advogada'),('Jornalista'),('Chef'),
('Estudante'),('Analista de Dados');

CREATE TABLE codigos_cep (cep CHAR(9) PRIMARY KEY, cidade VARCHAR(40), uf CHAR(2));
INSERT INTO codigos_cep VALUES
('50000-000','Recife','PE'),('53000-000','Olinda','PE'),('59000-000','Natal','RN'),
('58000-000','João Pessoa','PB'),('60000-000','Fortaleza','CE'),('40000-000','Salvador','BA'),
('64000-000','Teresina','PI'),('57000-000','Maceió','AL');

CREATE TABLE estado_civil (status_id SERIAL PRIMARY KEY, status VARCHAR(20) UNIQUE NOT NULL);
INSERT INTO estado_civil (status) VALUES ('solteiro(a)'),('casado(a)'),('divorciado(a)');

CREATE TABLE meus_contatos (
    contato_id SERIAL PRIMARY KEY, sobrenome VARCHAR(30), primeiro_nome VARCHAR(20), telefone VARCHAR(15),
    email VARCHAR(50), sexo CHAR(1), aniversario DATE,
    prof_id INT REFERENCES profissao(prof_id), cep CHAR(9) REFERENCES codigos_cep(cep),
    status_id INT REFERENCES estado_civil(status_id));
INSERT INTO meus_contatos (sobrenome, primeiro_nome, telefone, email, sexo, aniversario, prof_id, cep, status_id) VALUES
('Albuquerque','Ana','81 90000-0001','ana.alb@exemplo.com','F','1990-03-14',1,'50000-000',1),
('Barbosa','Bruno','81 90000-0002','bruno.b@exemplo.com','M','1985-07-02',2,'53000-000',2),
('Cardoso','Carla','84 90000-0003','carla.c@exemplo.com','F','1993-11-23',3,'59000-000',1),
('Dantas','Davi','81 90000-0004','davi.d@exemplo.com','M','1979-01-30',4,'50000-000',3),
('Esteves','Elisa','83 90000-0005','elisa.e@exemplo.com','F','1988-05-09',5,'58000-000',1),
('Farias','Fábio','85 90000-0006','fabio.f@exemplo.com','M','1995-09-17',1,'60000-000',1),
('Gomes','Gabi','71 90000-0007','gabi.g@exemplo.com','F','1991-12-01',6,'40000-000',2),
('Holanda','Heitor','81 90000-0008','heitor.h@exemplo.com','M','1983-04-26',7,'50000-000',1),
('Ibiapina','Iara','86 90000-0009',NULL,'F','1997-08-08',8,'64000-000',1),
('Lins','Lucas','82 90000-0010','lucas.l@exemplo.com','M','1992-10-05',9,'57000-000',1);

CREATE TABLE interesses (interesse_id SERIAL PRIMARY KEY, interesse VARCHAR(30) UNIQUE NOT NULL);
INSERT INTO interesses (interesse) VALUES
('cinema'),('trilhas'),('xadrez'),('futebol'),('leitura'),('desenho'),('corrida'),('culinária'),('viagens'),
('games'),('música'),('dança');

CREATE TABLE contato_interesse (
    contato_id INT REFERENCES meus_contatos(contato_id), interesse_id INT REFERENCES interesses(interesse_id),
    PRIMARY KEY (contato_id, interesse_id));
INSERT INTO contato_interesse VALUES
(1,1),(1,2),(1,3),(2,4),(2,5),(3,6),(3,1),(4,7),(4,8),(5,3),(5,9),(6,10),(6,2),(7,5),(7,9),
(8,8),(8,11),(9,12),(9,1),(10,3),(10,10);

CREATE TABLE procurando (procurando_id SERIAL PRIMARY KEY, procurando VARCHAR(30) UNIQUE NOT NULL);
INSERT INTO procurando (procurando) VALUES ('amizade'),('relacionamento'),('networking');

CREATE TABLE contato_procurando (
    contato_id INT REFERENCES meus_contatos(contato_id), procurando_id INT REFERENCES procurando(procurando_id),
    PRIMARY KEY (contato_id, procurando_id));
INSERT INTO contato_procurando VALUES (1,1),(2,3),(3,2),(4,2),(5,1),(6,2),(7,3),(8,1),(9,1),(10,3),(10,1);
"""

INTERESSES_ANTIGOS = """
CREATE TABLE contatos_antigos (contato_id INT PRIMARY KEY, primeiro_nome VARCHAR(20), interesses VARCHAR(100));
INSERT INTO contatos_antigos VALUES
(1,'Ana','cinema,trilhas,xadrez'),(2,'Bruno','futebol,leitura'),(3,'Carla','desenho,cinema'),
(4,'Davi','corrida,culinária'),(5,'Elisa','xadrez,viagens'),(6,'Fábio','games,trilhas,música');
"""

GAROTOS_BRINQUEDOS = """
CREATE TABLE brinquedos (brinquedo_id INT PRIMARY KEY, brinquedo VARCHAR(30));
INSERT INTO brinquedos VALUES
(1,'pião'),(2,'bola de gude'),(3,'pipa'),(4,'ioiô'),(5,'carrinho de rolimã'),(6,'peteca');
CREATE TABLE garotos (garoto_id INT PRIMARY KEY, garoto VARCHAR(20), brinquedo_id INT REFERENCES brinquedos(brinquedo_id));
INSERT INTO garotos VALUES (1,'Caio',3),(2,'Teo',5),(3,'Rui',2),(4,'Gil',3),(5,'Noé',NULL);
"""

EMPREGOS = """
CREATE TABLE emprego_atual (
    contato_id INT PRIMARY KEY REFERENCES meus_contatos(contato_id), cargo VARCHAR(40), salario DECIMAL(9,2),
    data_inicio DATE);
INSERT INTO emprego_atual VALUES
(1,'Desenvolvedora Web',9500.00,'2021-02-01'),
(2,'Professor',5200.00,'2015-03-01'),
(3,'Designer',6100.00,'2020-07-15'),
(4,'Médico',18000.00,'2010-01-10'),
(6,'Desenvolvedor Web',7800.00,'2022-05-02'),
(7,'Repórter',6400.00,'2019-09-01'),
(8,'Chef',8200.00,'2017-11-20'),
(10,'Analista de Dados',8800.00,'2023-01-09');

CREATE TABLE emprego_desejado (
    contato_id INT PRIMARY KEY REFERENCES meus_contatos(contato_id), cargo VARCHAR(40), salario_min DECIMAL(9,2),
    salario_max DECIMAL(9,2), disponivel CHAR(1), anos_exp INT);
INSERT INTO emprego_desejado VALUES
(1,'Desenvolvedora Web',11000,15000,'S',6),
(3,'Designer',7000,9000,'S',5),
(5,'Advogada',12000,16000,'N',10),
(6,'Desenvolvedor Web',9000,12000,'S',3),
(9,'Estagiária',1500,2500,'S',0),
(10,'Cientista de Dados',11000,14000,'S',4);

CREATE TABLE vagas (vaga_id SERIAL PRIMARY KEY, cargo VARCHAR(40), salario DECIMAL(9,2), cep CHAR(9), descricao VARCHAR(80));
INSERT INTO vagas (cargo, salario, cep, descricao) VALUES
('Desenvolvedora Web',12500,'50000-000','front-end com React'),
('Desenvolvedor Web',10500,'60000-000','back-end com Python'),
('Designer',8000,'59000-000','UX para aplicativos'),
('Cientista de Dados',13000,'50000-000','modelos de churn'),
('Repórter',6000,'40000-000','cobertura de cultura'),
('Professor',5800,'53000-000','matemática no ensino médio');
"""

PALHACOS_CHEFES = """
CREATE TABLE palhacos (palhaco_id INT PRIMARY KEY, nome VARCHAR(30), chefe_id INT REFERENCES palhacos(palhaco_id));
INSERT INTO palhacos VALUES
(1,'Pipoca',NULL),(2,'Biribinha',1),(3,'Tico-Tico',1),(4,'Lulu',2),(5,'Fuxico',2),(6,'Zazá',3);
"""

CAP11 = """
CREATE TABLE cofrinho (id SERIAL PRIMARY KEY, moeda NUMERIC(3,2) NOT NULL, data_moeda DATE DEFAULT CURRENT_DATE);
INSERT INTO cofrinho (moeda, data_moeda) VALUES
(0.25,'2024-04-01'),(0.10,'2024-04-01'),(1.00,'2024-04-02'),(0.05,'2024-04-03'),(0.50,'2024-04-03');

CREATE TABLE contas (conta INT PRIMARY KEY, titular VARCHAR(20) NOT NULL, saldo NUMERIC(10,2) NOT NULL);
INSERT INTO contas VALUES (101,'Ana',500.00),(202,'Bruno',150.00);
"""

CAP12 = """
CREATE TABLE palhacos_info (palhaco_id SERIAL PRIMARY KEY, nome VARCHAR(30), sexo CHAR(1), descricao VARCHAR(60));
INSERT INTO palhacos_info (nome, sexo, descricao) VALUES
('Pipoca','M','cabelo azul, sapato gigante'),('Biribinha','F','nariz vermelho'),('Tico-Tico','M','chapéu-coco'),
('Lulu','F','peruca rosa');
CREATE TABLE atividades (atividade_id SERIAL PRIMARY KEY, atividade VARCHAR(30));
INSERT INTO atividades (atividade) VALUES ('malabarismo'),('balões'),('mágica'),('monociclo');
CREATE TABLE info_local (id SERIAL PRIMARY KEY, palhaco_id INT REFERENCES palhacos_info(palhaco_id),
    local VARCHAR(40), quando DATE);
INSERT INTO info_local (palhaco_id, local, quando) VALUES
(1,'Festa da Rua Aurora','2024-05-04'),(2,'Escola Pequeno Príncipe','2024-05-06'),(1,'Shopping Boa Vista','2024-05-11');
"""

DADOS = {
    1: "",
    2: CONTATOS_SIMPLES + BEBIDAS,
    3: PALHACOS,
    4: PESCADORES + CONTATOS_SIMPLES,
    5: CONTATOS_SIMPLES + ALTER_CAP5,
    6: FILMES_BISCOITOS,
    7: CONTATOS_SIMPLES + PALHACOS,
    8: GREGS_LIST + INTERESSES_ANTIGOS + GAROTOS_BRINQUEDOS,
    9: GREGS_LIST + EMPREGOS,
    10: GREGS_LIST + EMPREGOS + GAROTOS_BRINQUEDOS + PALHACOS_CHEFES,
    11: GREGS_LIST + EMPREGOS + CAP11,
    12: CAP12,
}

# papéis (usuários) criados no capítulo 12: são do servidor inteiro, não do esquema
PAPEIS_CAP12 = ("leitor_relatorios", "estagiaria", "gerente_palhacos", "equipe_dados", "chefe_equipe", "visitante",
                "novato")


def _limpa_papeis(con):
    for papel in PAPEIS_CAP12:
        if con.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (papel,)).fetchone():
            con.execute(f'DROP OWNED BY "{papel}"')
            con.execute(f'DROP ROLE "{papel}"')


def preparar(cap: int, modo: str = "praticar", recomecar: bool = False):
    """Cria (se preciso) o esquema do capítulo e devolve o 'motor' de conexão para o %sql."""
    esquema = f"cap{cap:02d}" if modo == "praticar" else f"gab_cap{cap:02d}"
    try:
        con = psycopg.connect(URL, autocommit=True, connect_timeout=5)
    except psycopg.OperationalError as err:
        raise SystemExit("Não consegui conectar ao PostgreSQL. Abra o Docker Desktop e rode, na pasta do "
                         "repositório: docker compose up -d\n" + str(err)) from None
    with con:
        existe = con.execute("SELECT 1 FROM information_schema.schemata WHERE schema_name = %s",
                             (esquema,)).fetchone()
        if recomecar and existe:
            con.execute(f"DROP SCHEMA {esquema} CASCADE")
            existe = None
        if recomecar and cap == 12:
            _limpa_papeis(con)
        if not existe:
            con.execute(f"CREATE SCHEMA {esquema}")
            con.execute(f"SET search_path TO {esquema}")
            if DADOS.get(cap):
                con.execute(DADOS[cap])
            if cap == 12:  # deixa os papéis criados no capítulo enxergarem o esquema
                con.execute(f"GRANT USAGE ON SCHEMA {esquema} TO PUBLIC")
        tabelas = [r[0] for r in con.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = %s ORDER BY 1", (esquema,))]
    print(f"Pronto. Esquema {esquema} | tabelas: {', '.join(tabelas) or '(nenhuma ainda)'}")
    url_sa = URL.replace("postgresql://", "postgresql+psycopg://")
    return create_engine(url_sa, connect_args={"options": f"-csearch_path={esquema}"})

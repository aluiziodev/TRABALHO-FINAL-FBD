/* SCRIPT de criaçao de todo o banco de dados, junta todos os comandos dos 
7 arquivos desta pagina para criaçao de forma definitiva do BD
*/

/* 01_FILEGROUPS (windows) */

CREATE DATABASE BDSpotPer

ON PRIMARY
(
    NAME = 'BDSpotPer_Primary',
    FILENAME = 'C:\SQLData\BDSpotPer_Primary.mdf',
    SIZE = 50MB,
    FILEGROWTH = 10MB
),
FILEGROUP FG_GENERALDATA
(
    NAME = 'BDSpotPer_Data1',
    FILENAME = 'C:\SQLData\BDSpotPer_Data1.ndf',
    SIZE = 100MB,
    MAXSIZE = 500MB,
    FILEGROWTH = 50MB
),
(
    NAME = 'BDSpotPer_Data2',
    FILENAME = 'C:\SQLData\BDSpotPer_Data2.ndf',
    SIZE = 100MB,
    MAXSIZE = 500MB,
    FILEGROWTH = 50MB
),
FILEGROUP FG_PLAYLISTS
(
    NAME = 'BDSpotPer_Playlists',
    FILENAME = 'C:\SQLData\BDSpotPer_Playlists.ndf',
    SIZE = 100MB,
    MAXSIZE = 300MB,
    FILEGROWTH = 50MB
)
LOG ON
(
    NAME = 'BDSpotPer_Log',
    FILENAME = 'C:\SQLData\BDSpotPer_Log.ldf',
    SIZE = 50MB,
    FILEGROWTH = 25MB
);


/* 02_TABELAS_BDSpotPer */

USE BDSpotPer;

CREATE TABLE gravadora
(
    cod_grvd SMALLINT NOT NULL,
    rua_ender VARCHAR(40) NOT NULL,
    num_ender SMALLINT NOT NULL,
    bairro_ender VARCHAR(30) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    homepage VARCHAR(100) NOT NULL,

    CONSTRAINT PK_cod_grvd PRIMARY KEY (cod_grvd),
    CONSTRAINT U_grav_nome unique (nome),
    CONSTRAINT U_grav_homepage unique (homepage)

) ON FG_GENERALDATA;

CREATE TABLE playlist
(

    cod_play SMALLINT NOT NULL,
    nome VARCHAR(40) NOT NULL,
    dt_criacao DATE NOT NULL,
    temp_exec SMALLINT NOT NULL,

    CONSTRAINT PK_cod_play PRIMARY KEY (cod_play),
    CONSTRAINT U_play_nome unique (nome)

) ON FG_PLAYLISTS;

CREATE TABLE interprete
(
    cod_intp SMALLINT NOT NULL,
    tipo VARCHAR(40) NOT NULL,
    nome VARCHAR(100) NOT NULL,

    CONSTRAINT PK_cod_intp PRIMARY KEY (cod_intp)


) ON FG_GENERALDATA;

CREATE TABLE periodo_musical
(
    cod_per SMALLINT NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    ano_inicio SMALLINT NOT NULL,
    ano_fim SMALLINT CONSTRAINT DF_ano_fim DEFAULT YEAR(GETDATE()),

    CONSTRAINT PK_cod_per PRIMARY KEY (cod_per),
    CONSTRAINT CK_periodo CHECK (ano_fim IS NULL OR ano_inicio<ano_fim)


) ON FG_GENERALDATA;


CREATE TABLE compositor
(
    cod_comp SMALLINT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    dt_nasc DATE NOT NULL,
    dt_morte DATE,
    cidade_nasc VARCHAR(20),
    estado_nasc VARCHAR(20),
    periodo_mus SMALLINT NOT NULL,


    CONSTRAINT PK_cod_comp PRIMARY KEY (cod_comp),
    CONSTRAINT FK_cod_per FOREIGN KEY (periodo_mus) REFERENCES periodo_musical (cod_per),
    CONSTRAINT CK_dt_morte CHECK (dt_morte IS NULL OR dt_nasc<dt_morte)

) ON FG_GENERALDATA;

CREATE TABLE album
(

    cod_alb SMALLINT NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    preco_alb DEC(5,2) NOT NULL,
    dt_compra DATE NOT NULL,
    dt_gravacao DATE NOT NULL,
    grav_alb SMALLINT NOT NULL,
    meio_fis VARCHAR(20) NOT NULL,
    tipo_compra VARCHAR(10) NOT NULL,
    qtd_discos SMALLINT NULL,


    CONSTRAINT PK_cod_alb PRIMARY KEY (cod_alb),
    CONSTRAINT FK_grav_alb FOREIGN KEY (grav_alb) REFERENCES gravadora (cod_grvd),
    CONSTRAINT CK_dt_grav CHECK (dt_gravacao >= '2000-01-01'),
    CONSTRAINT CK_meio_fis CHECK (meio_fis IN ('CD','VINIL','DOWNLOAD')),
    CONSTRAINT CK_album_tipo_compra CHECK (tipo_compra IN ('CREDITO', 'DEBITO', 'PIX', 'ESPECIE', 'BOLETO')),
    CONSTRAINT CK_album_qtd_discos CHECK ((meio_fis = 'DOWNLOAD' AND qtd_discos 
    IS NULL) OR (meio_fis IN ('CD', 'VINIL') AND qtd_discos IS NOT NULL AND qtd_discos > 0))


) ON FG_GENERALDATA;
 
CREATE TABLE tipo_composicao
(
    cod_tipcomp SMALLINT NOT NULL,
    descricao VARCHAR(100) NOT NULL,

    CONSTRAINT PK_cod_tipcomp PRIMARY KEY (cod_tipcomp)

) ON FG_GENERALDATA;


CREATE TABLE faixa
(

    num_faixa_alb SMALLINT NOT NULL,
    num_disc_alb SMALLINT NOT NULL CONSTRAINT DF_num_disc_alb DEFAULT 0,
    descricao VARCHAR(100) NOT NULL,
    temp_exec SMALLINT,
    tipo_grav VARCHAR(3),
    alb_faixa SMALLINT NOT NULL,
    tipo_comp SMALLINT NOT NULL,


    CONSTRAINT PK_faixa PRIMARY KEY (num_faixa_alb, alb_faixa, num_disc_alb),
    CONSTRAINT FK_faixa_alb FOREIGN KEY (alb_faixa) REFERENCES album (cod_alb) ON DELETE CASCADE,
    CONSTRAINT FK_tipo_comp FOREIGN KEY (tipo_comp) REFERENCES tipo_composicao (cod_tipcomp),
    CONSTRAINT CK_exec CHECK (temp_exec > 0),
    CONSTRAINT CK_tipo_grav CHECK (tipo_grav IS NULL OR tipo_grav IN ('ADD','DDD'))

) ON FG_GENERALDATA;


CREATE TABLE fone_gravadora
(

    grvd SMALLINT NOT NULL,
    fone VARCHAR(20) NOT NULL,

    CONSTRAINT PK_fone_grav PRIMARY KEY (grvd, fone),
    CONSTRAINT FK_grvd FOREIGN KEY (grvd) REFERENCES gravadora (cod_grvd)



) ON FG_GENERALDATA;


CREATE TABLE faixa_playlist
(

    cod_play SMALLINT NOT NULL,
    num_faixa_alb SMALLINT NOT NULL,
    alb_faixa SMALLINT NOT NULL,
    num_disc_alb SMALLINT NOT NULL,
    qtd_plays SMALLINT CONSTRAINT DF_qtd_plays DEFAULT 0,
    dt_ult_play DATE,

    CONSTRAINT PK_fp_faixa_play PRIMARY KEY (cod_play, num_faixa_alb, alb_faixa, num_disc_alb),
    CONSTRAINT FK_fp_cod_play FOREIGN KEY (cod_play) REFERENCES playlist (cod_play),
    CONSTRAINT FK_fp_faixa FOREIGN KEY (num_faixa_alb, alb_faixa, num_disc_alb) REFERENCES faixa (num_faixa_alb, alb_faixa, num_disc_alb)

) ON FG_PLAYLISTS;

CREATE TABLE interprete_faixa
(
    num_faixa_alb SMALLINT NOT NULL,
    alb_faixa SMALLINT NOT NULL,
    num_disc_alb SMALLINT NOT NULL,
    cod_intp SMALLINT NOT NULL,

    CONSTRAINT PK_if_intp_faixa PRIMARY KEY (cod_intp, num_faixa_alb, alb_faixa),
    CONSTRAINT FK_if_cod_intp FOREIGN KEY (cod_intp) REFERENCES interprete (cod_intp),
    CONSTRAINT FK_if_faixa FOREIGN KEY (num_faixa_alb, alb_faixa, num_disc_alb) REFERENCES faixa (num_faixa_alb, alb_faixa, num_disc_alb)


) ON FG_GENERALDATA;

CREATE TABLE compositor_faixa
(
    num_faixa_alb SMALLINT NOT NULL,
    alb_faixa SMALLINT NOT NULL,
    num_disc_alb SMALLINT NOT NULL,
    cod_comp SMALLINT NOT NULL,

    CONSTRAINT PK_cf_comp_faixa PRIMARY KEY (cod_comp, num_faixa_alb, alb_faixa, num_disc_alb),
    CONSTRAINT FK_cf_cod_comp FOREIGN KEY (cod_comp) REFERENCES compositor (cod_comp),
    CONSTRAINT FK_cf_faixa FOREIGN KEY (num_faixa_alb, alb_faixa, num_disc_alb) REFERENCES faixa (num_faixa_alb, alb_faixa, num_disc_alb)

) ON FG_GENERALDATA;


/* 03_TRIGGERS */



GO

CREATE TRIGGER trg_check_barroco_DDD
ON faixa
AFTER INSERT, UPDATE
AS
BEGIN
    IF EXISTS (
    SELECT *
    FROM inserted i
        JOIN compositor_faixa cf
        ON i.num_faixa_alb = cf.num_faixa_alb
            AND i.alb_faixa = cf.alb_faixa
        JOIN compositor c
        ON cf.cod_comp = c.cod_comp
        JOIN periodo_musical pm
        ON c.periodo_mus = pm.cod_per
    WHERE pm.descricao = 'Barroco' AND (i.tipo_grav IS NULL OR i.tipo_grav <> 'DDD'))
BEGIN
        RAISERROR('Faixas do período barroco só podem ser inseridas caso gravadas com tipo DDD.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO

CREATE TRIGGER trg_max64_faixas
ON faixa
AFTER INSERT, UPDATE
AS
BEGIN
    IF EXISTS(
    SELECT *
    FROM faixa f
        JOIN inserted i
        ON f.alb_faixa = i.alb_faixa
    GROUP BY i.alb_faixa
    HAVING COUNT(*) > 64
)
BEGIN
        RAISERROR('Um álbum não pode conter mais que 64 faixas no total,', 16, 1)
        ROLLBACK TRANSACTION
    END
END
GO

/*Para a restrição do item c), ON DELETE CASCADE garante a remoção das faixas
decorrente da remoção do álbum. */

CREATE TRIGGER trg_preco_max_alb
ON album
AFTER INSERT, UPDATE
AS
BEGIN
    DECLARE @media_fullddd DECIMAL(10,2);

    SELECT @media_fullddd = AVG(a.preco_alb)
    FROM Album a
    WHERE NOT EXISTS (
    SELECT *
    FROM Faixa f
    WHERE f.alb_faixa = a.cod_alb
        AND (f.tipo_grav IS NULL OR f.tipo_grav <> 'DDD')
    );

    IF @media_fullddd IS NULL
        RETURN;

    IF EXISTS (
    SELECT *
    FROM inserted i
    WHERE i.preco_alb > 3 * @media_fullddd
    )
    BEGIN
        RAISERROR ('O preço de compra de um álbum não pode ser superior a três vezes a média do preço de álbuns com todas as faixas DDD.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO

CREATE TRIGGER trg_valida_tipograv
ON faixa
AFTER INSERT, UPDATE
AS
BEGIN
    IF EXISTS(
    SELECT *
    FROM inserted i
        JOIN album a
        ON i.alb_faixa = a.cod_alb
    WHERE (a.meio_fis in ('DOWNLOAD', 'VINIL') AND (i.tipo_grav IS NOT NULL))
        OR (a.meio_fis = 'CD' AND (i.tipo_grav IS NULL OR i.tipo_grav NOT IN ('ADD', 'DDD')))
)
BEGIN
        RAISERROR('Tipo de gravação inválido conforme o meio físico do álbum.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO

CREATE TRIGGER trg_valida_numdisc_alb
ON faixa
AFTER INSERT, UPDATE
AS
BEGIN
    IF EXISTS (
    SELECT *
    FROM inserted i
        JOIN album a
        ON i.alb_faixa = a.cod_alb
    WHERE (a.meio_fis = 'DOWNLOAD' AND i.num_disc_alb <> 0)
        OR (a.meio_fis IN ('CD', 'VINIL') AND i.num_disc_alb <= 0))
BEGIN
        RAISERROR('Número do disco do álbum inválido conforme o meio físico do álbum.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO

CREATE TRIGGER trg_faixa_playlist_atualiza_tempo
ON faixa_playlist
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE p
    SET p.temp_exec = p.temp_exec + t.soma_tempo
    FROM playlist p
    JOIN (
        SELECT
            i.cod_play,
            SUM(f.temp_exec) AS soma_tempo
        FROM inserted i
        JOIN faixa f
            ON f.num_faixa_alb = i.num_faixa_alb
           AND f.alb_faixa     = i.alb_faixa
           AND (
                (f.num_disc_alb = i.num_disc_alb)
                OR (f.num_disc_alb IS NULL AND i.num_disc_alb IS NULL)
           )
        GROUP BY i.cod_play
    ) t
        ON p.cod_play = t.cod_play;
END;
GO

CREATE TRIGGER trg_faixa_playlist_atualiza_tempo_del
ON faixa_playlist
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE p
    SET p.temp_exec = 
        CASE
            WHEN p.temp_exec - t.soma_tempo < 0 THEN 0
            ELSE p.temp_exec - t.soma_tempo
        END
    FROM playlist p
    JOIN (
        SELECT
            d.cod_play,
            SUM(f.temp_exec) AS soma_tempo
        FROM deleted d
        JOIN faixa f
            ON f.num_faixa_alb = d.num_faixa_alb
           AND f.alb_faixa     = d.alb_faixa
           AND (
                (f.num_disc_alb = d.num_disc_alb)
                OR (f.num_disc_alb IS NULL AND d.num_disc_alb IS NULL)
           )
        GROUP BY d.cod_play
    ) t
        ON p.cod_play = t.cod_play;
END;
GO

/* 04_FUCTION */


USE BDSpotPer;
GO

CREATE FUNCTION function_albuns_compositor 
( @nome_comp VARCHAR(100) )

RETURNS TABLE 
AS RETURN
( SELECT DISTINCT(a.cod_alb), a.descricao FROM compositor c JOIN 
compositor_faixa cf ON c.cod_comp=cf.cod_comp JOIN faixa f ON (f.num_faixa_alb=cf.num_faixa_alb
AND f.alb_faixa=cf.alb_faixa) JOIN album a ON a.cod_alb=f.alb_faixa
WHERE c.nome LIKE '%' + @nome_comp + '%');

GO

/* 05_INDICES */


USE BDSpotPer;
GO

CREATE NONCLUSTERED INDEX idx_faixa_album
ON faixa (alb_faixa)
WITH (FILLFACTOR = 100)
ON FG_PLAYLISTS;


CREATE NONCLUSTERED INDEX idx_faixa_tipo_comp
ON faixa (tipo_comp)
WITH (FILLFACTOR = 100)
ON FG_PLAYLISTS;

GO


/* 06_VIEWS */


CREATE VIEW [dbo].[vw_playlist_album]
WITH SCHEMABINDING
AS
SELECT 
    p.cod_play,
    p.nome AS nome_playlist,
    f.alb_faixa,
    COUNT_BIG(*) AS qtd_albuns
FROM dbo.playlist p
    JOIN dbo.faixa_playlist fp
        ON fp.cod_play = p.cod_play
    JOIN dbo.faixa f
        ON f.num_faixa_alb = fp.num_faixa_alb
    AND f.alb_faixa    = fp.alb_faixa
    AND f.num_disc_alb = fp.num_disc_alb
GROUP BY p.cod_play, p.nome, f.alb_faixa;
GO
CREATE UNIQUE CLUSTERED INDEX idx_vw_playlist_album
ON dbo.vw_playlist_album (cod_play, alb_faixa);
GO


CREATE VIEW [dbo].[vw_playlist_album_count]
WITH SCHEMABINDING
AS
SELECT 
    p.cod_play,
    p.nome_playlist AS nome_playlist,
    COUNT(*) AS qtd_albuns
FROM dbo.vw_playlist_album as p
GROUP BY p.cod_play, p.nome_playlist;
GO


/* 07_POVOAMENTO */



INSERT INTO periodo_musical (cod_per, descricao, ano_inicio, ano_fim) VALUES
(1, 'Barroco', 1600, 1750),
(2, 'Clássico', 1750, 1820),
(3, 'Romântico', 1820, 1910),
(4, 'Moderno', 1910, NULL);



INSERT INTO tipo_composicao (cod_tipcomp, descricao) VALUES
(1, 'Sinfonia'),
(2, 'Concerto'),
(3, 'Sonata'),
(4, 'Ópera');



INSERT INTO compositor
(cod_comp, nome, dt_nasc, dt_morte, cidade_nasc, estado_nasc, periodo_mus)
VALUES
(1, 'Antonio Vivaldi', '1678-03-04', '1741-07-28', 'Veneza', 'Itália', 2),
(2, 'Wolfgang Amadeus Mozart', '1756-01-27', '1791-12-05', 'Salzburgo', 'Áustria', 3),
(3, 'Ludwig van Beethoven', '1770-12-17', '1827-03-26', 'Bonn', 'Alemanha', 4),
(4, 'Compositor Moderno X', '1975-06-12', NULL, 'Berlim', 'Alemanha', 1);


INSERT INTO interprete (cod_intp, nome, tipo) VALUES
(1, 'Orquestra Filarmônica de Berlim', 'Orquestra'),
(2, 'Quarteto Alban Berg', 'Quarteto'),
(3, 'Maria Callas', 'Soprano'),
(4, 'Pianista Romântico', 'SOLISTA');


INSERT INTO gravadora
(cod_grvd, nome, rua_ender, num_ender, bairro_ender, homepage)
VALUES
(1, 'Deutsche Grammophon', 'Berliner Strasse', 12, 'Mitte', 'https://www.dg.com'),
(2, 'EMI Classics', 'Abbey Road', 3, 'Camden', 'https://www.emi.com');


INSERT INTO album
(cod_alb, descricao, preco_alb, dt_compra, dt_gravacao, grav_alb, meio_fis, tipo_compra, qtd_discos)
VALUES
-- Álbuns em CD
(1, 'As Quatro Estações', 59.90, '2023-05-10', '2005-06-01', 1, 'CD', 'CREDITO', 1),
(2, 'Sinfonias de Beethoven', 89.90, '2022-11-20', '2010-03-15', 2, 'CD', 'DEBITO', 3),

-- Álbuns em VINIL
(3, 'Óperas de Mozart', 129.90, '2021-08-12', '2008-09-10', 1, 'VINIL', 'PIX', 4),
(4, 'Concertos Barrocos', 99.90, '2020-02-18', '2001-04-22', 2, 'VINIL', 'BOLETO', 2),

-- Álbuns em DOWNLOAD
(5, 'Sonatas Românticas', 39.90, '2024-01-05', '2018-07-30', 2, 'DOWNLOAD', 'CREDITO', NULL),
(6, 'Música Contemporânea', 29.90, '2023-09-14', '2021-11-02', 1, 'DOWNLOAD', 'PIX', NULL);


INSERT INTO faixa
(num_faixa_alb, num_disc_alb, descricao, temp_exec, tipo_grav, alb_faixa, tipo_comp)
VALUES

(1, 1, 'Symphony No.9 – I', 900, 'DDD', 1, 1),
(2, 1, 'Symphony No.9 – II', 850, 'DDD', 1, 1),


(1, 2, 'Symphony No.9 – IV (Ode to Joy)', 1400, 'DDD', 1, 1),

(1, 1, 'Abertura da Ópera', 420, NULL, 3, 2),
(2, 1, 'Ária Principal', 380, NULL, 3, 2),
(1, 2, 'Dueto Dramático', 450, NULL, 3, 2),
(1, 3, 'Finale', 520, NULL, 3, 2),


(1, 1, 'Concerto em Ré Menor', 600, NULL, 4, 3),
(2, 1, 'Adágio Barroco', 480, NULL, 4, 3),
(1, 2, 'Prelúdio Antigo', 510, NULL, 4, 3),


(1, 0, 'Sonata Romântica nº 1', 540, NULL, 5, 4),
(2, 0, 'Sonata Romântica nº 2', 560, NULL, 5, 4),
(3, 0, 'Intermezzo', 300, NULL, 5, 4),


(1, 0, 'Obra Experimental I', 420, NULL, 6, 4),
(2, 0, 'Obra Experimental II', 460, NULL, 6, 4);

INSERT INTO interprete_faixa
(num_faixa_alb, alb_faixa, num_disc_alb, cod_intp)
VALUES

(1, 3, 1, 1),
(2, 3, 1, 1),
(1, 3, 2, 2),
(1, 3, 3, 1),


(1, 4, 1, 2),
(2, 4, 1, 2),
(1, 4, 2, 1),


(1, 5, 0, 4),
(2, 5, 0, 4),
(3, 5, 0, 4),


(1, 6, 0, 3),
(2, 6, 0, 3);


INSERT INTO compositor_faixa
(num_faixa_alb, alb_faixa, num_disc_alb, cod_comp)
VALUES

(1, 3, 1, 2),
(2, 3, 1, 2),
(1, 3, 2, 2),
(1, 3, 3, 2),


(1, 4, 1, 1),
(2, 4, 1, 1),
(1, 4, 2, 1),

(1, 5, 0, 3),
(2, 5, 0, 3),
(3, 5, 0, 3),


(1, 6, 0, 4),
(2, 6, 0, 4);

INSERT INTO playlist
(cod_play, nome, dt_criacao, temp_exec)
VALUES
(1, 'Clássicos Essenciais', '2024-01-10', 0),
(2, 'Românticas para Piano', '2024-02-05', 0),
(3, 'Música Contemporânea', '2024-03-01', 0);

INSERT INTO faixa_playlist
(cod_play, num_faixa_alb, alb_faixa, num_disc_alb, qtd_plays, dt_ult_play)
VALUES

(1, 1, 3, 1, 15, '2024-05-01'),
(1, 2, 3, 1, 10, '2024-05-02'),
(1, 1, 4, 1, 8,  '2024-05-03'),

(2, 1, 5, 0, 20, '2024-06-01'),
(2, 2, 5, 0, 18, '2024-06-02'),

(3, 1, 6, 0, 12, '2024-06-10'),
(3, 2, 6, 0, 9,  '2024-06-11');


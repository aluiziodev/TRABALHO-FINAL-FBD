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
    CONSTRAINT CK_album_qtd_discos CHECK ((meio_fis = 'DOWNLOAD' AND quantidade_discos 
    IS NULL) OR (meio_fis IN ('CD', 'VINIL') AND quantidade_discos IS NOT NULL AND quantidade_discos > 0))


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
    descriçao VARCHAR(100) NOT NULL,
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
    num_faixa_alb SMALLINT NOT NULL,
    cod_intp SMALLINT NOT NULL,

    CONSTRAINT PK_if_intp_faixa PRIMARY KEY (cod_intp, num_faixa_alb, alb_faixa, num_faixa_alb),
    CONSTRAINT FK_if_cod_intp FOREIGN KEY (cod_intp) REFERENCES interprete (cod_intp),
    CONSTRAINT FK_if_faixa FOREIGN KEY (num_faixa_alb, alb_faixa, num_disc_alb) REFERENCES faixa (num_faixa_alb, alb_faixa, num_disc_alb)


) ON FG_GENERALDATA;

CREATE TABLE compositor_faixa
(
    num_faixa_alb SMALLINT NOT NULL,
    alb_faixa SMALLINT NOT NULL,
    num_faixa_alb SMALLINT NOT NULL,
    cod_comp SMALLINT NOT NULL,

    CONSTRAINT PK_cf_comp_faixa PRIMARY KEY (cod_comp, num_faixa_alb, alb_faixa, num_disc_alb),
    CONSTRAINT FK_cf_cod_comp FOREIGN KEY (cod_comp) REFERENCES compositor (cod_comp),
    CONSTRAINT FK_cf_faixa FOREIGN KEY (num_faixa_alb, alb_faixa, num_disc_alb) REFERENCES faixa (num_faixa_alb, alb_faixa, num_disc_alb)

) ON FG_GENERALDATA;

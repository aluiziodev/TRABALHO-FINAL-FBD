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
(num_faixa_alb, num_disc_alb, descriçao, temp_exec, tipo_grav, alb_faixa, tipo_comp)
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

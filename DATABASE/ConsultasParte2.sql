/* SCRIPT PARA AS CONSULTAS DOS ITENS a), b), c), d) DO TRABALHO PRATICO*/

/* a) */

SELECT cod_alb, descricao, preco_alb
FROM album
WHERE preco_alb > ( SELECT AVG(preco_alb)
                    FROM album)

/* b) */
SELECT g.nome as nome_gravadora,
COUNT(DISTINCT fp.cod_play) as total_playlists
FROM gravadora g JOIN album a ON a.grav_alb = g.cod_grvd
    JOIN faixa f ON f.alb_faixa = a.cod_alb
    JOIN compositor_faixa cf ON cf.num_faixa_alb = f.num_faixa_alb
        AND cf.alb_faixa = f.alb_faixa
        AND cf.num_disc_alb = f.num_disc_alb
    JOIN compositor c ON c.cod_comp = cf.cod_comp
    JOIN faixa_playlist fp ON fp.num_faixa_alb = f.num_faixa_alb
        AND fp.alb_faixa    = f.alb_faixa
        AND fp.num_disc_alb = f.num_disc_alb
WHERE c.nome = 'Antonín Dvořák'
GROUP BY g.nome
HAVING COUNT(DISTINCT fp.cod_play) = (
    SELECT MAX(qtd_playlists)
    FROM (
        SELECT COUNT(DISTINCT fp2.cod_play) as qtd_playlists
        FROM gravadora g2
            JOIN album a2 ON a2.grav_alb = g2.cod_grvd
            JOIN faixa f2 ON f2.alb_faixa = a2.cod_alb
            JOIN compositor_faixa cf2 ON cf2.num_faixa_alb = f2.num_faixa_alb
                AND cf2.alb_faixa    = f2.alb_faixa
                AND cf2.num_disc_alb = f2.num_disc_alb
            JOIN compositor c2 ON c2.cod_comp = cf2.cod_comp
            JOIN faixa_playlist fp2 ON fp2.num_faixa_alb = f2.num_faixa_alb
                AND fp2.alb_faixa    = f2.alb_faixa
                AND fp2.num_disc_alb = f2.num_disc_alb
        WHERE c2.nome = 'Antonín Dvořák'
        GROUP BY g2.cod_grvd
    ) sub)

/* c) */

SELECT c.nome as nome_compositor, COUNT(*) as total_faixas
FROM compositor c
    JOIN compositor_faixa cf ON cf.cod_comp = c.cod_comp
    JOIN faixa_playlist fp ON fp.num_faixa_alb = cf.num_faixa_alb
        AND fp.alb_faixa = cf.alb_faixa
        AND fp.num_disc_alb = cf.num_disc_alb
GROUP BY c.cod_comp, c.nome
HAVING COUNT(*) = (SELECT MAX(qtd_faixas) 
                    FROM (SELECT COUNT(*) as qtd_faixas
                        FROM compositor_faixa cf2
                        JOIN faixa_playlist fp2 ON fp2.num_faixa_alb = cf2.num_faixa_alb
                            AND fp2.alb_faixa    = cf2.alb_faixa
                            AND fp2.num_disc_alb = cf2.num_disc_alb
                        GROUP BY cf2.cod_comp) sub)

/* d) */

SELECT p.cod_play,
    p.nome
FROM playlist p
WHERE NOT EXISTS (
    SELECT *
    FROM faixa_playlist fp
    JOIN faixa f
        ON f.num_faixa_alb = fp.num_faixa_alb
        AND f.alb_faixa    = fp.alb_faixa
        AND f.num_disc_alb = fp.num_disc_alb
    JOIN tipo_composicao tc
        ON tc.cod_tipcomp = f.tipo_comp
    WHERE fp.cod_play = p.cod_play
    AND tc.descricao <> 'Concerto'
)
AND NOT EXISTS (
    SELECT *
    FROM faixa_playlist fp
    JOIN faixa f
        ON f.num_faixa_alb = fp.num_faixa_alb
        AND f.alb_faixa    = fp.alb_faixa
        AND f.num_disc_alb = fp.num_disc_alb
    WHERE fp.cod_play = p.cod_play
    AND NOT EXISTS (
        SELECT *
        FROM compositor_faixa cf
        JOIN compositor c
            ON c.cod_comp = cf.cod_comp
        JOIN periodo_musical pm
            ON pm.cod_per = c.periodo_mus
        WHERE cf.num_faixa_alb = f.num_faixa_alb
            AND cf.alb_faixa    = f.alb_faixa
            AND cf.num_disc_alb = f.num_disc_alb
            AND pm.descricao = 'Barroco'
    )
)

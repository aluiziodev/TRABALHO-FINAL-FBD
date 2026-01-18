USE BDSpotPer;
GO
CREATE VIEW [dbo].[vw_playlist_album_count]
WITH SCHEMABINDING
AS
SELECT 
    p.cod_play,
    p.nome AS nome_playlist,
    COUNT_BIG(DISTINCT f.alb_faixa) AS qtd_albuns
FROM dbo.playlist p
    JOIN dbo.faixa_playlist fp
        ON fp.cod_play = p.cod_play
    JOIN dbo.faixa f
        ON f.num_faixa_alb = fp.num_faixa_alb
    AND f.alb_faixa    = fp.alb_faixa
    AND f.num_disc_alb = fp.num_disc_alb
GROUP BY p.cod_play, p.nome;
GO
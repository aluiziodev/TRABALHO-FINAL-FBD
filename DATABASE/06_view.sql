USE BDSpotPer;
GO
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
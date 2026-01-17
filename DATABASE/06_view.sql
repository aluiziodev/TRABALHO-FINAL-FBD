USE BDSpotPer;
GO

CREATE VIEW dbo.vw_playlist_qtd_albuns
WITH SCHEMABINDING
AS
SELECT
    p.cod_play,
    p.nome AS nome_playlist,
    COUNT_BIG(*) AS qtd_albuns
FROM dbo.playlist AS p
JOIN dbo.faixa_playlist AS fp
    ON p.cod_play = fp.cod_play
GROUP BY
    p.cod_play,
    p.nome;
GO
CREATE UNIQUE CLUSTERED INDEX IX_vw_playlist_qtd_albuns
ON dbo.vw_playlist_qtd_albuns (cod_play, nome_playlist);

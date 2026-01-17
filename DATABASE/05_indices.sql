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
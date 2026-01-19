
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
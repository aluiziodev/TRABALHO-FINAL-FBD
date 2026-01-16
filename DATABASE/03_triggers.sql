USE BDSpotPer
GO

CREATE TRIGGER trg_check_barroco_DDD
ON faixa
AFTER INSERT, UPDATE
AS
BEGIN
    IF EXISTS ( 
        SELECT *
        FROM inserted i JOIN compositor_faixa cf
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
    FROM faixa f JOIN inserted i ON f.alb_faixa = i.alb_faixa
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

    SELECT @media_fullddd = AVG(a.preco_compra)
    FROM Album a
    WHERE NOT EXISTS (
        SELECT *
    FROM Faixa f
    WHERE f.album = a.cod_alb
        AND (f.tipo_grav IS NULL OR f.tipo_grav <> 'DDD')
    );

    IF @media_fullddd IS NULL
        RETURN;

    IF EXISTS (
        SELECT *
    FROM inserted i
    WHERE i.preco_compra > 3 * @media_fullddd
    )
    BEGIN
        RAISERROR ('O preço de compra de um álbum não pode ser superior a três vezes a média do preço de álbuns com todas as faixas DDD.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO

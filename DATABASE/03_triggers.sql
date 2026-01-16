USE BDSpotPer
GO

CREATE TRIGGER trg_check_barroco_DDD
ON faixa
AFTER INSERT, UPDATE
AS
BEGIN
    IF EXISTS ( SELECT 1
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
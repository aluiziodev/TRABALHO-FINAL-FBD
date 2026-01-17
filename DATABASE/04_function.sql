USE BDSpotPer;
GO

CREATE FUNCTION function_albuns_compositor 
( @nome_comp VARCHAR(100) )

RETURNS TABLE 
AS RETURN
( SELECT a.cod_alb, a.descricao FROM compositor c JOIN 
compositor_faixa cf ON c.cod_comp=cf.cod_comp JOIN faixa f ON (f.num_faixa_alb=cf.num_faixa_alb
AND f.alb_faixa=cf.alb_faixa) JOIN album a ON a.cod_alb=f.alb_faixa
WHERE c.nome LIKE '%' + @nome_comp + '%');


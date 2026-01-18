import os  
import pymssql


def listarAlbuns(cursor):
    cursor.execute("""
                     SELECT cod_alb, descricao
                     FROM album
                   """)
    print("\n----- ÁLBUNS -----")
    albuns = cursor.fetchall()
    for row in albuns:
        print("CÓDIGO:", row[0], "| DESCRIÇÃO:", row[1])
    return [cod for cod,_ in albuns]

def listarFaixasAlbum(cursor, cod_alb):
    cursor.execute("""
                     SELECT num_faixa_alb, num_disc_alb, descriçao, temp_exec
                     FROM faixa
                        WHERE alb_faixa = %s           
                   """, (cod_alb,))
    faixas = cursor.fetchall()
    print(f"\n----- FAIXAS DO ÁLBUM {cod_alb} -----")
    for row in faixas:
        print("NÚMERO FAIXA:", row[0], "| NÚMERO DISCO:", row[1], "| DESCRIÇÃO:", row[2], "| TEMPO EXECUÇÃO:", row[3])
    return faixas

def listarPlaylists(cursor):
    cursor.execute("""
                    SELECT cod_play, nome FROM playlist
                """)
    playlists = cursor.fetchall()
    print("\n----- PLAYLISTS -----")
    for row in playlists:
        print("CÓDIGO:", row[0], "| NOME:", row[1])
    return [cod for cod,_ in playlists]


def listarFaixasPlaylist(cursor, cod_play):
    cursor.execute("""
        SELECT f.alb_faixa, f.num_faixa_alb, f.num_disc_alb, f.descriçao, f.temp_exec
        FROM faixa_playlist fp
        JOIN faixa f ON fp.num_faixa_alb = f.num_faixa_alb AND fp.alb_faixa = f.alb_faixa AND fp.num_disc_alb = f.num_disc_alb
        WHERE fp.cod_play = %s
        """, (cod_play,))
    faixas = cursor.fetchall()
    print(f"\n----- FAIXAS DA PLAYLIST {cod_play} -----")
    if not faixas:
        print("\nNenhuma faixa na playlist!!")
    else:
        for row in faixas:
            print("COD ALBUM FAIXA:", row[0], "| NÚMERO FAIXA:", row[1], "| NÚMERO DISCO:", row[2], "| DESCRIÇÃO:", row[3], "| TEMPO EXECUÇÃO:", row[4])
    return faixas
                
def listarFaixasNplaylist(cursor, cod_play): #FAIXAS QUE NAO ESTAO NA PLAYLIST
    cursor.execute("""
            SELECT f.alb_faixa, f.num_faixa_alb, f.num_disc_alb, f.descriçao, f.temp_exec
            FROM faixa f
            WHERE NOT EXISTS (
                SELECT *
                FROM faixa_playlist fp
                WHERE fp.cod_play = %s AND fp.num_faixa_alb = f.num_faixa_alb
                    AND fp.alb_faixa = f.alb_faixa
                    AND fp.num_disc_alb = f.num_disc_alb)
        """, (cod_play,))
    faixas = cursor.fetchall()
    print(f"\n----- FAIXAS DA PLAYLIST {cod_play} -----")
    if not faixas:
        print("\nNenhuma faixa na playlist!!")
    else:
        for row in faixas:
            print("COD ALBUM FAIXA:", row[0], "| NÚMERO FAIXA:", row[1], "| NÚMERO DISCO:", row[2], "| DESCRIÇÃO:", row[3], "| TEMPO EXECUÇÃO:", row[4])
    return faixas


def consultaA(cursor):
    cursor.execute("""
                   SELECT cod_alb, descricao, preco_alb
                   FROM album
                   WHERE preco_alb > ( SELECT AVG(preco_alb)
                                    FROM album)
                   """)
    for row in cursor:
        print("CÓDIGO:", row[0], "| DESCRIÇÃO:", row[1], "| PREÇO:", row[2])
    cursor.close()



def consultaB(cursor):
    cursor.execute("""
                    SELECT g.nome AS nome_gravadora,
                        COUNT(DISTINCT fp.cod_play) AS total_playlists
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
                            SELECT COUNT(DISTINCT fp2.cod_play) AS qtd_playlists
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
                        ) AS sub)
                """)
    
    for row in cursor:
        print("GRAVADORA:", row[0], "| TOTAL DE PLAYLISTS:", row[1])
    cursor.close()

def consultaC(cursor):
    cursor.execute("""
                    SELECT c.nome AS nome_compositor, COUNT(*) AS total_faixas
                    FROM compositor c
                        JOIN compositor_faixa cf ON cf.cod_comp = c.cod_comp
                    JOIN faixa_playlist fp ON fp.num_faixa_alb = cf.num_faixa_alb
                        AND fp.alb_faixa = cf.alb_faixa
                        AND fp.num_disc_alb = cf.num_disc_alb
                    GROUP BY c.cod_comp, c.nome
                    HAVING COUNT(*) = (SELECT MAX(qtd_faixas)
                                        FROM (SELECT COUNT(*) AS qtd_faixas
                                            FROM compositor_faixa cf2
                                            JOIN faixa_playlist fp2 ON fp2.num_faixa_alb = cf2.num_faixa_alb
                                                AND fp2.alb_faixa    = cf2.alb_faixa
                                                AND fp2.num_disc_alb = cf2.num_disc_alb
                                            GROUP BY cf2.cod_comp) AS sub)
                """)
    for row in cursor:
        print("COMPOSITOR:", row[0], "| TOTAL DE FAIXAS:", row[1])
    cursor.close()

def consultaD(cursor):
    cursor.execute("""
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
                   """)
    for row in cursor:
        print("CÓDIGO PLAYLIST:", row[0], "| NOME PLAYLIST:", row[1])
    cursor.close()



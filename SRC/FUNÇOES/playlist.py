import os  
import pymssql
import consultas as cons
from datetime import date


def criarPlaylist(cursor, conn, nomePlaylist):
    cursor.execute("""
                    SELECT ISNULL(MAX(cod_play),0)+1 
                    FROM playlist
            """)
    cod_play = cursor.fetchone()[0]

    dt_criacao = date.today()
    temp_exec = 0

    cursor.execute("""
                    INSERT INTO playlist (cod_play, nome, dt_criacao, temp_exec)
                    VALUES (%s,%s,%s,%s)
                   """, (cod_play, nomePlaylist, dt_criacao, temp_exec))
    
    albuns = cons.listarAlbuns(cursor)
    
    while True:
        cod_alb = int(input("\nEscolha um dos albuns listados(Digite 0 para finalizar): "))
        if cod_alb==0:
            break
        elif cod_alb not in albuns:
            print("\nAlbum Invalido!!")
            continue

        faixas = cons.listarFaixasAlbum(cursor, cod_alb)

        for faixa in faixas:
            resp = input(f"Adicionar a faixa '{faixa[2]}'? (s/n): ").lower()
            if resp == "s":
                cursor.execute("""
                    INSERT INTO faixa_playlist (cod_play, num_faixa_alb, alb_faixa, num_disc_alb, qtd_plays)
                    VALUES (%s, %s, %s, %s, 0)
                """, (cod_play, faixa[0], cod_alb, faixa[1]))

    conn.commit()
    print(f"\n Playlist '{nomePlaylist}' criada!!")


def adicionarFaixa(cursor, conn, cod_play):
    cons.listarFaixasNplaylist(cursor, cod_play)
    num_faixa = int(input("Digite o número da faixa a adicionar: "))
    alb_faixa = int(input("Digite o código do álbum da faixa: "))
    num_disc = int(input("Digite o número do disco (0 se não houver): "))
    try:
        cursor.execute("""
            INSERT INTO faixa_playlist (cod_play, num_faixa_alb, alb_faixa, num_disc_alb)
            VALUES (%s, %s, %s, %s)
            """, (cod_play, num_faixa, alb_faixa, num_disc))
        conn.commit()
        print("Música adicionada com sucesso!")
    except Exception as e:
        print("\n FALHA NA CONEXÃO")
        print(type(e).__name__, "→", e)

def removerFaixa(cursor, conn, cod_play):
    cons.listarFaixasPlaylist(cursor, cod_play)
    num_faixa = int(input("Digite o número da faixa a remover: "))
    alb_faixa = int(input("Digite o código do álbum da faixa: "))
    num_disc = int(input("Digite o número do disco (0 se não houver): "))
    try:
        cursor.execute("""
            DELETE FROM faixa_playlist
            WHERE cod_play = %s AND num_faixa_alb = %s AND alb_faixa = %s AND num_disc_alb = %s
            """, (cod_play, num_faixa, alb_faixa, num_disc))
        conn.commit()
        print("Música removida com sucesso!")
    except Exception as e:
        print("\n FALHA NA CONEXÃO")
        print(type(e).__name__, "→", e)

def manutençaoPlaylist(cursor, conn):
    playlists = cons.listarPlaylists(cursor)
    while True:
        cod_play = int(input("\nEscolha uma dss playlists listadas(Digite 0 para finalizar): "))
        if cod_play==0:
            break
        elif cod_play not in playlists:
            print("\n Playlist invalida!!")
            continue
        while True:
            print("\n1. Adicionar música")
            print("2. Remover música")
            print("0. Sair")
            opc = input("Escolha uma opção: ")
            if opc == "1":
                adicionarFaixa(cursor, conn, cod_play)
            elif opc == "2":
                removerFaixa(cursor, conn, cod_play)
            elif opc == "0":
                break
            else:
                print("Opção inválida!")
        
    







    



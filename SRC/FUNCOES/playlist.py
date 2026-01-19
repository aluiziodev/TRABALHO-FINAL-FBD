import os  
import pymssql
from . import consultas as cons
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox


def criarPlaylist(cursor, conn, nomePlaylist, faixasSelecionadas):

    if not nomePlaylist:
        messagebox.showerror("Erro", "Informe o nome da playlist")
        return False

    if not faixasSelecionadas:
        messagebox.showerror("Erro", "Selecione pelo menos uma faixa")
        return False
    
    try:
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
        
        for num_faixa, num_disc, cod_alb in faixasSelecionadas:
            cursor.execute("""
                INSERT INTO faixa_playlist
                (cod_play, num_faixa_alb, alb_faixa, num_disc_alb, qtd_plays)
                VALUES (%s, %s, %s, %s, 0)
            """, (cod_play, num_faixa, cod_alb, num_disc))
        

        conn.commit()
        messagebox.showinfo(
            "Sucesso",
            f"Playlist '{nomePlaylist}' criada com sucesso!"
        )
        return True

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", str(e))

def excluirFaixa(cursor, conn, cod_play, num_faixa, alb_faixa, num_disc):
    if not cod_play:
        messagebox.showerror("Erro", "Playlist não selecionada")
        return
    try:
        cursor.execute("""
            DELETE FROM faixa_playlist
            WHERE cod_play = %s AND num_faixa_alb = %s AND alb_faixa = %s AND num_disc_alb = %s
            """, (cod_play, num_faixa, alb_faixa, num_disc))
        if cursor.rowcount == 0:
            messagebox.showwarning("Aviso","A faixa não foi encontrada na playlist")
            return

        conn.commit()

        messagebox.showinfo(
            "Sucesso",
            "Faixa removida da playlist com sucesso!"
        )
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", str(e))

        

def adicionarFaixa(cursor, conn, cod_play, num_faixa, alb_faixa, num_disc):
    if not cod_play:
        messagebox.showerror("Erro", "Playlist não selecionada")
        return
    try:
        cursor.execute("""
            INSERT INTO faixa_playlist (cod_play, num_faixa_alb, alb_faixa, num_disc_alb)
            VALUES (%s, %s, %s, %s)
            """, (cod_play, num_faixa, alb_faixa, num_disc))
        conn.commit()
        messagebox.showinfo(
            "Sucesso",
            "Faixa adicionada à playlist com sucesso!"
        )

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", str(e))



        
    







    



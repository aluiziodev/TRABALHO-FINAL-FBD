import tkinter as tk
from tkinter import ttk, messagebox
from FUNCOES import consultas as cons



def carregaAlbuns(tree_albuns, cursor):
    tree_albuns.delete(*tree_albuns.get_children())
    codigos_albuns = cons.listarAlbuns(cursor)  # usa sua função
    for cod, desc in codigos_albuns:
        tree_albuns.insert("", tk.END, values=(cod, desc))

def carregaFaixasAlbum(event, tree_albuns, tree_faixas, cursor):
    tree_faixas.delete(*tree_faixas.get_children())

    item = tree_albuns.focus()
    if not item:
        return

    cod_alb = tree_albuns.item(item, "values")[0]

    faixas = cons.listarFaixasAlbum(cursor, cod_alb)

    for faixa in faixas:
        tree_faixas.insert("", tk.END, values=faixa)

def selecionarFaixas(event, tree_faixas, tree_faixas_selecionadas):
    for item in tree_faixas.selection():
        valores = tree_faixas.item(item, "values")

        # evita duplicação
        ja_existe = False
        for i in tree_faixas_selecionadas.get_children():
            if tree_faixas_selecionadas.item(i, "values") == valores:
                ja_existe = True
                break
        if not ja_existe:
            tree_faixas_selecionadas.insert("", tk.END, values=valores)

def removerFaixaSelecionada(tree_faixas_selecionadas):
    selecionadas = tree_faixas_selecionadas.selection()

    if not selecionadas:
        return

    if not messagebox.askyesno(
        "Remover Faixa",
        "Deseja remover a(s) faixa(s) selecionada(s)?"
    ):
        return

    for item in selecionadas:
        tree_faixas_selecionadas.delete(item)

def carregaPlaylist(cursor, tree_playlists):
    tree_playlists.delete(*tree_playlists.get_children())
    playlists = cons.listarPlaylists(cursor) # usa sua função
    for item in playlists:
        tree_playlists.insert("", tk.END, values=item)

def carregaFaixasPlaylist(event, tree_playlists, tree_faixas_playlist, 
                          tree_faixas_dispon, cursor):
    tree_faixas_playlist.delete(*tree_faixas_playlist.get_children())
    tree_faixas_dispon.delete(*tree_faixas_dispon.get_children())

    item = tree_playlists.focus()
    if not item:
        return

    cod_play = tree_playlists.item(item, "values")[0]

    faixas = cons.listarFaixasPlaylist(cursor, cod_play)
    faixasdisp = cons.listarFaixasNplaylist(cursor, cod_play)

    for faixa in faixas:
        tree_faixas_playlist.insert("", tk.END, values=(cod_play,)+faixa)
    for faixa in faixasdisp:
        tree_faixas_dispon.insert("", tk.END, values=faixa)

def carregaConsultaA(cursor, tree_consulta_a):
    tree_consulta_a.delete(*tree_consulta_a.get_children())
    consulta = cons.consultaA(cursor)
    for item in consulta:
        tree_consulta_a.insert("", tk.END, values=item)

def carregaConsultaB(cursor, tree_consulta_b):
    tree_consulta_b.delete(*tree_consulta_b.get_children())
    consulta = cons.consultaB(cursor)
    for item in consulta:
        tree_consulta_b.insert("", tk.END, values=item)

def carregaConsultaC(cursor, tree_consulta_c):
    tree_consulta_c.delete(*tree_consulta_c.get_children())
    consulta = cons.consultaC(cursor)
    for item in consulta:
        tree_consulta_c.insert("", tk.END, values=item)

def carregaConsultaD(cursor, tree_consulta_d):
    tree_consulta_d.delete(*tree_consulta_d.get_children())
    consulta = cons.consultaD(cursor)
    for item in consulta:
        tree_consulta_d.insert("", tk.END, values=item)





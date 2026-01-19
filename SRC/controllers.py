from FUNCOES import playlist
from tkinter import Tk, messagebox
import treeViews as tv




def limpar_tree(tree):
    tree.delete(*tree.get_children())

def refreshAlbuns(cursor, tree_albuns):
    limpar_tree(tree_albuns)
    tv.carregaAlbuns(tree_albuns, cursor)

def refreshConsultas(tree_consulta_a,
                    tree_consulta_b,
                    tree_consulta_c,
                    tree_consulta_d,
                    tree_consulta_view,
                    tree_consulta_function):
    for tree in (
        tree_consulta_a,
        tree_consulta_b,
        tree_consulta_c,
        tree_consulta_d,
        tree_consulta_view,
        tree_consulta_function
    ):
        limpar_tree(tree)



def refreshPlaylist(tree_playlists,
            tree_faixas_playlist,
            tree_faixas_dispon,
            cursor):

    selected = tree_playlists.focus()
    cod_play = None

    if selected:
        cod_play = tree_playlists.item(selected, "values")[0]


    tree_playlists.delete(*tree_playlists.get_children())
    tv.carregaPlaylist(cursor, tree_playlists)

    if not cod_play:
        return

    #ID RECRIADO APOS DELETE, BUSCAMOS O NOVO ID DO OBJETO
    novo_iid = None
    for iid in tree_playlists.get_children():
        valores = tree_playlists.item(iid, "values")
        if valores and valores[0] == cod_play:
            novo_iid = iid
            break

    if novo_iid:
        tree_playlists.selection_set(novo_iid)
        tree_playlists.focus(novo_iid)

        tv.carregaFaixasPlaylist(
            None,
            tree_playlists,
            tree_faixas_playlist,
            tree_faixas_dispon,
            cursor
        )

def refreshManutencao(
        tree_playlists,
        tree_faixas_playlist,
        tree_faixas_dispon,
        cursor):
    tree_playlists.selection_remove(tree_playlists.selection())
    tree_playlists.focus_set()  

    tree_faixas_playlist.delete(*tree_faixas_playlist.get_children())
    tree_faixas_dispon.delete(*tree_faixas_dispon.get_children())

    tree_playlists.delete(*tree_playlists.get_children())
    tv.carregaPlaylist(cursor, tree_playlists)

    

def refreshFaixasSelecionadas(tree_faixas_selecionadas):
    tree_faixas_selecionadas.delete(*tree_faixas_selecionadas.get_children())

def actionCriarPlaylist(nome, 
                        tree_faixas_selecionadas,
                        tree_albuns,
                        cursor,
                        conn): # Açao criar playlist
    faixas = []
    for item in tree_faixas_selecionadas.get_children():
        valores = tree_faixas_selecionadas.item(item, "values")

        cod_alb   = int(valores[0])
        num_faixa = int(valores[1])
        num_disc  = int(valores[2])

        faixas.append((num_faixa, num_disc, cod_alb))

    if playlist.criarPlaylist(cursor, conn, nome, faixas):
        refreshFaixasSelecionadas(tree_faixas_selecionadas)
    refreshAlbuns(cursor, tree_albuns)


def removerFaixaPlaylist(event=None,
                        tree_playlists=None,
                        tree_faixas_dispon=None,
                        tree_faixas_playlist=None,
                        cursor=None,
                        conn=None): # Açao remover de uma playlist
    selecionadas = tree_faixas_playlist.selection()

    if not selecionadas:
        return

    if not messagebox.askyesno(
        "Remover Faixa",
        "Deseja remover a(s) faixa(s) selecionada(s)?"
    ):
        return

    for item in selecionadas:
        valores = tree_faixas_playlist.item(item, "values")

        cod_play =  int(valores[0])
        cod_alb   = int(valores[1])
        num_faixa = int(valores[2])
        num_disc  = int(valores[3])
        playlist.excluirFaixa(cursor, conn, cod_play, num_faixa, cod_alb, num_disc)
    refreshPlaylist(tree_playlists,
                    tree_faixas_playlist,
                    tree_faixas_dispon,
                    cursor)

def adicionarFaixaPlaylist(event=None,
                           tree_playlists=None,
                           tree_faixas_dispon=None,
                           tree_faixas_playlist=None,
                           cursor=None,
                           conn=None): # Açao de adicionar em uma playlist
    item = tree_playlists.focus()
    if not item:
        return
    cod_play = tree_playlists.item(item, "values")[0]
    

    selecionadas = tree_faixas_dispon.selection()
    if not selecionadas:
        return

    if not messagebox.askyesno(
        "Adicionar Faixa",
        "Deseja adicionar a(s) faixa(s) selecionada(s)?"
    ):
        return

    for item in selecionadas:
        valores = tree_faixas_dispon.item(item, "values")

        cod_alb   = int(valores[0])
        num_faixa = int(valores[1])
        num_disc  = int(valores[2])
        playlist.adicionarFaixa(cursor, conn, cod_play, num_faixa, cod_alb, num_disc)
    refreshPlaylist(tree_playlists,
                    tree_faixas_playlist,
                    tree_faixas_dispon,
                    cursor)

def realizaFunction(nome,
                    tree_consulta_function,
                    cursor,
                    conn):
    tv.carregaFunction(cursor, conn, tree_consulta_function, nome)
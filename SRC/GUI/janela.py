from .ABAS import abaConsultas, abaCriarPlaylist, abaManuntencao
from dbConnection import getConnection
import tkinter as tk
from tkinter import ttk, messagebox


def iniciaApp():


    try:
        conn = getConnection()

        cursor = conn.cursor()

    except Exception as e:
        print("\n FALHA NA CONEXÃO")
        print(type(e).__name__, "→", e)
    
    root = tk.Tk()
    root.title("APLICATIVO BDSpotPer")
    root.geometry("900x600")

    tab_control = ttk.Notebook(root)
    tab_control.add(abaCriarPlaylist.criarTabCriarPLaylists(tab_control, 
                                                            cursor,
                                                            conn), text="Criar Playlist")
    tab_control.add(abaManuntencao.criarTabManutencao(tab_control, 
                                                            cursor,
                                                            conn), text="Editar Playlist")
    tab_control.add(abaConsultas.criarTabConsultas(tab_control, 
                                                            cursor,
                                                            conn), text="Consultas")
    tab_control.pack(expand=1, fill="both")


    root.mainloop()
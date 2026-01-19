import tkinter as tk
from tkinter import ttk
import treeViews as tv
import controllers as ct


def criarTabManutencao(tab_control, cursor, conn):
    tab_manutencao = ttk.Frame(tab_control)
    tk.Label(
        tab_manutencao,
        text="Playlists existentes:",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(5, 0))

    frame_playlists = tk.Frame(tab_manutencao, bd=1, relief=tk.SOLID)
    frame_playlists.pack(fill=tk.X, padx=10, pady=5)

    tree_playlists = ttk.Treeview(
        tab_manutencao,
        columns=("cod_play", "nome", "dt_criacao", "temp_exec"),
        show="headings",
        selectmode="browse"
    )
    tree_playlists.heading("cod_play", text="Código")
    tree_playlists.heading("nome", text="Playlist")
    tree_playlists.heading("dt_criacao", text="Data de Criaçao")
    tree_playlists.heading("temp_exec", text="Tempo de Execuçao(Segundos)")
    tree_playlists.pack(in_=frame_playlists, fill=tk.X, expand=True)

    scroll_y = ttk.Scrollbar(frame_playlists, orient="vertical", command=tree_playlists.yview)
    tree_playlists.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_playlists.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    tk.Label(
        tab_manutencao,
        text="Faixas da Playlist Selecionada",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(10, 0))

    frame_faixas_playlist = tk.Frame(tab_manutencao, bd=1, relief=tk.SOLID)
    frame_faixas_playlist.pack(fill=tk.BOTH, padx=10, pady=5)

    tree_faixas_playlist = ttk.Treeview(
        tab_manutencao,
        columns=("cod_play", "cod_alb", "num_faixa", "num_disc", "descricao", "tempo"),
        show="headings",
        selectmode="extended"
    )
    tree_faixas_playlist.heading("cod_play", text="Playlist")
    tree_faixas_playlist.heading("cod_alb", text="Álbum")
    tree_faixas_playlist.heading("num_faixa", text="Faixa")
    tree_faixas_playlist.heading("num_disc", text="Disco")
    tree_faixas_playlist.heading("descricao", text="Descrição")
    tree_faixas_playlist.heading("tempo", text="Duração(Segundos)")
    tree_faixas_playlist.pack(in_= frame_faixas_playlist,fill=tk.BOTH, expand=True)

    scroll_y = ttk.Scrollbar(frame_faixas_playlist, orient="vertical", command=tree_faixas_playlist.yview)
    tree_faixas_playlist.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_faixas_playlist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    tk.Label(
        tab_manutencao,
        text="Faixas disponíveis para adicionar",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(10, 0))

    frame_faixas_dispon = tk.Frame(tab_manutencao, bd=1, relief=tk.SOLID)
    frame_faixas_dispon.pack(fill=tk.BOTH, padx=10, pady=5)

    tree_faixas_dispon = ttk.Treeview(
        tab_manutencao,
        columns=("cod_alb", "num_faixa", "num_disc", "descricao", "tempo"),
        show="headings",
        selectmode="extended"
    )
    tree_faixas_dispon.heading("cod_alb", text="Álbum")
    tree_faixas_dispon.heading("num_faixa", text="Faixa")
    tree_faixas_dispon.heading("num_disc", text="Disco")
    tree_faixas_dispon.heading("descricao", text="Descrição")
    tree_faixas_dispon.heading("tempo", text="Duração(Segundos)")
    tree_faixas_dispon.pack(in_= frame_faixas_dispon,fill=tk.BOTH, expand=True)

    scroll_y = ttk.Scrollbar(frame_faixas_dispon, orient="vertical", command=tree_faixas_dispon.yview)
    tree_faixas_dispon.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_faixas_dispon.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    tree_playlists.bind(
        "<<TreeviewSelect>>",
        lambda event: tv.carregaFaixasPlaylist(
            event,
            tree_playlists,
            tree_faixas_playlist,
            tree_faixas_dispon,
            cursor)
    )
    tree_faixas_playlist.bind(
        "<Delete>",
        lambda e: ct.removerFaixaPlaylist(e, tree_playlists,
                                          tree_faixas_playlist,
                                          tree_faixas_dispon,
                                          cursor,
                                          conn 
                                       )
    )
    tree_faixas_dispon.bind(
        "<<TreeviewSelect>>",
        lambda event: ct.adicionarFaixaPlaylist(event, tree_playlists,
                                                tree_faixas_dispon,
                                                tree_faixas_playlist,
                                                cursor,
                                                conn)
    )



    frameBotoes2 = tk.Frame(tab_manutencao)
    frameBotoes2.pack(pady=5)
    tk.Button(
        frameBotoes2,
        text="Adicionar Faixa na playlist",
        command=lambda e: ct.adicionarFaixaPlaylist(e, tree_playlists,
                                                tree_faixas_dispon,
                                                tree_faixas_playlist,
                                                cursor,
                                                conn)
    ).pack(side=tk.LEFT, padx=10)
    tk.Button(
        frameBotoes2,
        text="Remover Faixa da Playlist",
        command=lambda: ct.removerFaixaPlaylist(None, tree_playlists,
                                            tree_faixas_dispon,
                                            tree_faixas_playlist,
                                            cursor,
                                            conn)
    ).pack(side=tk.RIGHT, padx=10)
    tk.Button(
        frameBotoes2,
        text="Refresh",
        command=lambda: ct.refreshPlaylist(tree_playlists,
                                   tree_faixas_playlist,
                                   tree_faixas_dispon,
                                   cursor)
    ).pack(side=tk.LEFT, padx=10)

    
    tv.carregaPlaylist(cursor, tree_playlists)

    return tab_manutencao
import tkinter as tk
from tkinter import ttk
import treeViews as tv
import controllers as ct



def criarTabCriarPLaylists(tab_control, cursor, conn):
    tab_criar = ttk.Frame(tab_control)
    tk.Label(tab_criar, text="Nome da Playlist:").pack(pady=5)
    entry_nome = tk.Entry(tab_criar)
    entry_nome.pack(pady=5)



    tk.Label(
        tab_criar,
        text="Álbuns",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(5, 0))

    frame_albuns = tk.Frame(tab_criar, bd=1, relief=tk.SOLID)
    frame_albuns.pack(fill=tk.X, padx=10, pady=5)

    tree_albuns = ttk.Treeview(
        tab_criar,
        columns=("cod_alb", "descricao"),
        show="headings",
        selectmode="browse"
    )
    tree_albuns.heading("cod_alb", text="Código")
    tree_albuns.heading("descricao", text="Álbum")
    tree_albuns.pack(in_=frame_albuns, fill=tk.X, expand=True)

    scroll_y = ttk.Scrollbar(frame_albuns, orient="vertical", command=tree_albuns.yview)
    tree_albuns.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_albuns.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    tk.Label(
        tab_criar,
        text="Faixas do Álbum Selecionado",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(10, 0))

    frame_faixas = tk.Frame(tab_criar, bd=1, relief=tk.SOLID)
    frame_faixas.pack(fill=tk.BOTH, padx=10, pady=5)

    tree_faixas = ttk.Treeview(
        tab_criar,
        columns=("cod_alb", "num_faixa", "num_disc", "descricao", "tempo"),
        show="headings",
        selectmode="extended"
    )
    tree_faixas.heading("cod_alb", text="Álbum")
    tree_faixas.heading("num_faixa", text="Faixa")
    tree_faixas.heading("num_disc", text="Disco")
    tree_faixas.heading("descricao", text="Descrição")
    tree_faixas.heading("tempo", text="Duração(Segundos)")
    tree_faixas.pack(in_= frame_faixas,fill=tk.BOTH, expand=True)

    scroll_y = ttk.Scrollbar(frame_faixas, orient="vertical", command=tree_faixas.yview)
    tree_faixas.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_faixas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    tk.Label(
        tab_criar,
        text="Faixas Selecionadas para a Playlist",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(10, 0))

    frame_faixas_sel = tk.Frame(tab_criar, bd=1, relief=tk.SOLID)
    frame_faixas_sel.pack(fill=tk.BOTH, padx=10, pady=5)

    tree_faixas_selecionadas = ttk.Treeview(
        tab_criar,
        columns=("cod_alb", "num_faixa", "num_disc", "descricao", "tempo"),
        show="headings"
    )
    tree_faixas_selecionadas.heading("cod_alb", text="Álbum")
    tree_faixas_selecionadas.heading("num_faixa", text="Faixa")
    tree_faixas_selecionadas.heading("num_disc", text="Disco")
    tree_faixas_selecionadas.heading("descricao", text="Descrição")
    tree_faixas_selecionadas.heading("tempo", text="Duração(Segundos)")
    tree_faixas_selecionadas.pack(in_= frame_faixas_sel, fill=tk.BOTH, expand=True)

    scroll_y = ttk.Scrollbar(frame_faixas_sel, orient="vertical", command=tree_faixas_selecionadas.yview)
    tree_faixas_selecionadas.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_faixas_selecionadas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    tree_albuns.bind(
        "<<TreeviewSelect>>",
        lambda event: tv.carregaFaixasAlbum(
            event,
            tree_albuns,
            tree_faixas,
            cursor
        )
    )
    tree_faixas.bind(
        "<<TreeviewSelect>>",
        lambda e: tv.selecionarFaixas(
            e, tree_faixas, tree_faixas_selecionadas
        )
    )
    tree_faixas_selecionadas.bind(
        "<Delete>",
        lambda e: tv.removerFaixaSelecionada(tree_faixas_selecionadas)
    )



    frameBotoes = tk.Frame(tab_criar)
    frameBotoes.pack(pady=5)

    tk.Button(
        frameBotoes,
        text="Criar Playlist",
        command=lambda: ct.actionCriarPlaylist(entry_nome.get(),
                                       tree_faixas_selecionadas,
                                       tree_albuns,
                                       cursor,
                                       conn)
    ).pack(side=tk.LEFT, padx=10)
    tk.Button(
        frameBotoes,
        text="Remover Faixa Selecionada",
        command=lambda: tv.removerFaixaSelecionada(tree_faixas_selecionadas)
    ).pack(side=tk.RIGHT, padx=10)
    tk.Button(
        frameBotoes,
        text="Refresh",
        command=lambda: ct.refreshAlbuns(cursor, tree_albuns)
    ).pack(side=tk.LEFT, padx=10)
    tk.Button(
        frameBotoes,
        text="Remover Todas as Faixas",
        command=lambda: ct.refreshFaixasSelecionadas(tree_faixas_selecionadas)
    ).pack(side=tk.LEFT, padx=10)

    tv.carregaAlbuns(tree_albuns, cursor)

    

    return tab_criar

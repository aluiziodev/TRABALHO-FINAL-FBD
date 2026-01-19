import tkinter as tk
from tkinter import ttk
import treeViews as tv
import controllers as ct


def criarTabConsultas(tab_control, cursor, conn):
    tab_consultas = ttk.Frame(tab_control)
    canvas_consultas = tk.Canvas(tab_consultas)
    scroll_consultas = ttk.Scrollbar(
        tab_consultas, orient="vertical",
        command=canvas_consultas.yview
    )
    canvas_consultas.configure(yscrollcommand=scroll_consultas.set)
    scroll_consultas.pack(side=tk.RIGHT, fill=tk.Y)
    canvas_consultas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    frame_consultas = tk.Frame(canvas_consultas)
    window_id = canvas_consultas.create_window(
        (0, 0),
        window=frame_consultas,
        anchor="nw"
    )
    frame_consultas.bind(
        "<Configure>",
        lambda e: canvas_consultas.configure(
            scrollregion=canvas_consultas.bbox("all")
        )
    )
    canvas_consultas.bind(
        "<Configure>",
        lambda e: canvas_consultas.itemconfig(window_id, width=e.width)
    )



    tk.Label(
        frame_consultas,
        text="Consultas sobre o BDSpotPer",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    tk.Label(
        frame_consultas,
        text="A) Álbuns com preço acima da média",
        padx=10, pady=10,
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(5, 0))

    frame_a = tk.Frame(frame_consultas, bd=1, relief=tk.SOLID)
    frame_a.pack(fill=tk.X, padx=10, pady=5)


    tree_consulta_a = ttk.Treeview(
        frame_a,
        columns=("cod_alb", "descricao", "preco"),
        show="headings"
    )
    tree_consulta_a.heading("cod_alb", text="Código")
    tree_consulta_a.heading("descricao", text="Álbum")
    tree_consulta_a.heading("preco", text="Preço de Compra")
    tree_consulta_a.pack(fill=tk.BOTH, expand=True, pady=5)

    scroll_y = ttk.Scrollbar(frame_a, orient="vertical", command=tree_consulta_a.yview)
    tree_consulta_a.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_consulta_a.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    tk.Label(
        frame_consultas,
        text="B) Gravadora com mais playlists (Dvorack)",
        padx=10, pady=10,
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(5, 0))

    frame_b = tk.Frame(frame_consultas, bd=1, relief=tk.SOLID)
    frame_b.pack(fill=tk.X, padx=10, pady=5)

    tree_consulta_b = ttk.Treeview(
        frame_b,
        columns=("gravadora", "qtd_playlists"),
        show="headings"
    )
    tree_consulta_b.heading("gravadora", text="Gravadora")
    tree_consulta_b.heading("qtd_playlists", text="Qtd Playlists")
    tree_consulta_b.pack(fill=tk.BOTH, expand=True, pady=5)

    scroll_y = ttk.Scrollbar(frame_b, orient="vertical", command=tree_consulta_b.yview)
    tree_consulta_b.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_consulta_b.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    tk.Label(
        frame_consultas,
        text="C) Compositor com mais faixas nas playlists",
        padx=10, pady=10,
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(5, 0))

    frame_c = tk.Frame(frame_consultas, bd=1, relief=tk.SOLID)
    frame_c.pack(fill=tk.X, padx=10, pady=5)

    tree_consulta_c = ttk.Treeview(
        frame_c,
        columns=("compositor", "qtd_faixas"),
        show="headings"
    )
    tree_consulta_c.heading("compositor", text="Compositor")
    tree_consulta_c.heading("qtd_faixas", text="Qtd Faixas")
    tree_consulta_c.pack(fill=tk.BOTH, expand=True, pady=5)

    scroll_y = ttk.Scrollbar(frame_c, orient="vertical", command=tree_consulta_c.yview)
    tree_consulta_c.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_consulta_c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    tk.Label(
        frame_consultas,
        text="D) Playlists (Concerto + Barroco)",
        padx=10, pady=10,
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(5, 0))

    frame_d = tk.Frame(frame_consultas, bd=1, relief=tk.SOLID)
    frame_d.pack(fill=tk.X, padx=10, pady=5)

    tree_consulta_d = ttk.Treeview(
        frame_d,
        columns=("cod_play", "nome"),
        show="headings"
    )
    tree_consulta_d.heading("cod_play", text="Código")
    tree_consulta_d.heading("nome", text="Playlist")
    tree_consulta_d.pack(fill=tk.BOTH, expand=True, pady=5)

    scroll_y = ttk.Scrollbar(frame_d, orient="vertical", command=tree_consulta_d.yview)
    tree_consulta_d.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_consulta_d.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    tk.Label(
        frame_consultas,
        text="Function) Álbuns do Compositor",
        padx=10, pady=10,
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(5, 0))

    frame_function = tk.Frame(frame_consultas, bd=1, relief=tk.SOLID)
    frame_function.pack(fill=tk.X, padx=10, pady=5)

    tree_consulta_function = ttk.Treeview(
        frame_function,
        columns=("cod_alb", "desc"),
        show="headings"
    )
    tree_consulta_function.heading("cod_alb", text="Código")
    tree_consulta_function.heading("desc", text="Álbum")
    tree_consulta_function.pack(fill=tk.BOTH, expand=True, pady=5)

    scroll_y = ttk.Scrollbar(frame_function, orient="vertical", command=tree_consulta_function.yview)
    tree_consulta_function.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_consulta_function.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    tk.Label(
        frame_consultas,
        text="View) Playlists e seus Álbuns",
        padx=10, pady=10,
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=10, pady=(5, 0))

    frame_view = tk.Frame(frame_consultas, bd=1, relief=tk.SOLID)
    frame_view.pack(fill=tk.X, padx=10, pady=5)

    tree_consulta_view = ttk.Treeview(
        frame_view,
        columns=("cod_play", "nome", "qtd_albuns"),
        show="headings"
    )
    tree_consulta_view.heading("cod_play", text="Código")
    tree_consulta_view.heading("nome", text="Playlist")
    tree_consulta_view.heading("qtd_albuns", text="Qtd Álbuns")
    tree_consulta_view.pack(fill=tk.BOTH, expand=True, pady=5)

    scroll_y = ttk.Scrollbar(frame_view, orient="vertical", command=tree_consulta_view.yview)
    tree_consulta_view.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_consulta_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    tk.Button(
        frame_a,
        text="Executar Consulta",
        command=lambda: tv.carregaConsultaA(cursor, tree_consulta_a)
    ).pack(anchor="w")
    tk.Button(
        frame_b,
        text="Executar Consulta",
        command=lambda: tv.carregaConsultaB(cursor, tree_consulta_b)
    ).pack(anchor="w")
    tk.Button(
        frame_c,
        text="Executar Consulta",
        command=lambda: tv.carregaConsultaC(cursor, tree_consulta_c)
    ).pack(anchor="w")
    tk.Button(
        frame_d,
        text="Executar Consulta",
        command=lambda: tv.carregaConsultaD(cursor, tree_consulta_d)
    ).pack(anchor="w")
    tk.Label(frame_function, text="Nome do Compositor:").pack(pady=5)
    entry_nome_comp = tk.Entry(frame_function)
    entry_nome_comp.pack(pady=5)
    tk.Button(
        frame_function,
        text="Executar Consulta",
        command=lambda: ct.realizaFunction(entry_nome_comp.get(),
                                           tree_consulta_function,
                                           cursor,
                                           conn)
    ).pack(anchor="w")
    tk.Button(
        frame_view,
        text="Executar Consulta",
        command=lambda: tv.carregaView(cursor, tree_consulta_view)
    ).pack(anchor="w")
    tk.Button(
        tab_consultas,
        text="Refresh",
        command=lambda: ct.refreshConsultas(tree_consulta_a, 
                                            tree_consulta_b,
                                            tree_consulta_c,
                                            tree_consulta_d,
                                            tree_consulta_view,
                                            tree_consulta_function)
    ).pack(side=tk.TOP, padx=10)

    return tab_consultas
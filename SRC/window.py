import tkinter as tk
from tkinter import ttk, messagebox
import treeViews as tv
from FUNCOES import playlist
import os  
import pymssql 

#------------- CONEXAO SQL SERVER -------------

def getConnection():
    return pymssql.connect(
        server=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=1433,
    )

try:
    conn = getConnection()

    cursor = conn.cursor()

except Exception as e:
    print("\n FALHA NA CONEXÃO")
    print(type(e).__name__, "→", e)

#------------- JANELA FRONT-END -------------

def refresh():
    item = tree_playlists.focus()
    tree_playlists.delete(*tree_playlists.get_children())
    tv.carregaPlaylist(cursor, tree_playlists)
    tree_albuns.delete(*tree_albuns.get_children())
    tv.carregaAlbuns(tree_albuns, cursor)
    tree_consulta_a.delete(*tree_consulta_a.get_children())
    tree_consulta_b.delete(*tree_consulta_b.get_children())
    tree_consulta_c.delete(*tree_consulta_c.get_children())
    tree_consulta_d.delete(*tree_consulta_d.get_children())
    tree_consulta_view.delete(*tree_consulta_view.get_children())
    tree_consulta_function.delete(*tree_consulta_function.get_children())


    if not item:
        return

    if item:
        tree_playlists.selection_set(item)
        tree_playlists.focus(item)

        tv.carregaFaixasPlaylist(
            None,
            tree_playlists,
            tree_faixas_playlist,
            tree_faixas_dispon,
            cursor
        )

def refreshFaixasSelecionadas():
    tree_faixas_selecionadas.delete(*tree_faixas_selecionadas.get_children())

def actionCriarPlaylist(): # Açao criar playlist
    nome = entry_nome.get()

    faixas = []
    for item in tree_faixas_selecionadas.get_children():
        valores = tree_faixas_selecionadas.item(item, "values")

        cod_alb   = int(valores[0])
        num_faixa = int(valores[1])
        num_disc  = int(valores[2])

        faixas.append((num_faixa, num_disc, cod_alb))

    if playlist.criarPlaylist(cursor, conn, nome, faixas):
        refresh()
        refreshFaixasSelecionadas()


def removerFaixaPlaylist(): # Açao remover de uma playlist
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
    refresh()

def adicionarFaixaPlaylist(): # Açao de adicionar em uma playlist
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
    refresh()

def realizaFunction():
    nome = entry_nome_comp.get()
    tv.carregaFunction(cursor, conn, tree_consulta_function, nome)




# Janela principal
root = tk.Tk()
root.title("APLICATIVO BDSpotPer")
root.geometry("900x600")

# Abas
tab_control = ttk.Notebook(root)  
tab_criar = ttk.Frame(tab_control)
tab_manutencao = ttk.Frame(tab_control)
tab_consultas = ttk.Frame(tab_control)
tab_control.add(tab_criar, text="Criar Playlist")
tab_control.add(tab_manutencao, text="Editar Playlist")
tab_control.add(tab_consultas, text="Consultas")
tab_control.pack(expand=1, fill="both")



#------------- ABA CRIAÇAO PLAYLIST -------------
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
    command=actionCriarPlaylist
).pack(side=tk.LEFT, padx=10)
tk.Button(
    frameBotoes,
    text="Remover Faixa Selecionada",
    command=lambda: tv.removerFaixaSelecionada(tree_faixas_selecionadas)
).pack(side=tk.RIGHT, padx=10)
tk.Button(
    frameBotoes,
    text="Refresh",
    command=refresh
).pack(side=tk.LEFT, padx=10)
tk.Button(
    frameBotoes,
    text="Remover Todas as Faixas",
    command=refreshFaixasSelecionadas
).pack(side=tk.LEFT, padx=10)





#------------- ABA MANUTENÇAO PLAYLIST -------------

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
    lambda e: removerFaixaPlaylist()
)
tree_faixas_dispon.bind(
    "<<TreeviewSelect>>",
    lambda event: adicionarFaixaPlaylist()
)



frameBotoes2 = tk.Frame(tab_manutencao)
frameBotoes2.pack(pady=5)
tk.Button(
    frameBotoes2,
    text="Adicionar Faixa na playlist",
    command=adicionarFaixaPlaylist
).pack(side=tk.LEFT, padx=10)
tk.Button(
    frameBotoes2,
    text="Remover Faixa da Playlist",
    command=removerFaixaPlaylist
).pack(side=tk.RIGHT, padx=10)
tk.Button(
    frameBotoes2,
    text="Refresh",
    command=refresh
).pack(side=tk.LEFT, padx=10)




#------------- ABA CONSULTAS -------------
# CRIANDO UM CANVAS PARA PODE USAR O SCROLLBAR NA ABA
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
    command=realizaFunction
).pack(anchor="w")
tk.Button(
    frame_view,
    text="Executar Consulta",
    command=lambda: tv.carregaView(cursor, tree_consulta_view)
).pack(anchor="w")
tk.Button(
    tab_consultas,
    text="Refresh",
    command=refresh
).pack(side=tk.TOP, padx=10)





tv.carregaAlbuns(tree_albuns, cursor)
tv.carregaPlaylist(cursor, tree_playlists)


root.mainloop()
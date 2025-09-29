import tkinter as tk
from tkinter import messagebox
import Pokemon as Pokemon  # importa o arquivo com as regras do jogo
from PIL import Image, ImageTk  # Biblioteca para manipulação das imagens
import time  # Biblioteca para manipulação de fps
from random import choice  # Para escolher o oponente
from batalhaPokemon import Batalha  # Importa a classe Batalha
import pygame

# Inicializa o pygame e o mixer
pygame.init()
pygame.mixer.init()

# --- Funções de Música ---

def tocar_musica_menu():
    """Carrega e toca a música do menu em loop."""
    try:
        pygame.mixer.music.load("musicas/menu.mp3")
        pygame.mixer.music.play(-1)
    except pygame.error as e: #tratamento de erro
        print(f"Aviso: Não foi possível carregar a música do menu. {e}")

def tocar_musica_batalha():
    """Carrega e toca a música de batalha em loop."""
    try:
        pygame.mixer.music.load("musicas/batalha.mp3")
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        messagebox.showwarning("Música", f"Não foi possível carregar a música de batalha:\n{e}")


# --- Funções de Navegação ---


def ir_para_batalha():
    frame_menu.pack_forget()
    frame_batalha.pack(expand=True, fill=tk.BOTH)


def ir_para_pokedex(frame_de_origem):
    frame_de_origem.pack_forget()  # Esconde o frame de origem
    frame_pokedex.pack(expand=True)
    # Limpa a seleção e os detalhes ao entrar na pokedex
    label_detalhes_pokemon.config(text="")
    lista_pokemons.selection_clear(0, tk.END)


def voltar_para_menu(frame_atual):
    frame_atual.pack_forget()  # Esconde o frame atual (Batalha ou podekex)
    frame_menu.pack(expand=True)  # Mostra o menu princiapl
    # Se está voltando da batalha, toca a música do menu novamente
    if frame_atual == frame_batalha:
        tocar_musica_menu()


def sair():
    janela.quit()
    janela.destroy()

# --- Variáveis Globais da Batalha ---
batalha_atual = None
pokemon_jogador1 = None   # Para modo PVP
pokemon_jogador2 = None   # Para modo PVP
turno_jogador_atual = 1   # Para controlar turnos no modo PVP
modo_de_jogo = None       # 'PVE' ou 'PVP'

# --- Funções da Batalha ---

def preparar_selecao_pvp():
    """Prepara o jogo para a seleção de Pokémons no modo Jogador vs Jogador."""
    global modo_de_jogo, pokemon_jogador1, pokemon_jogador2
    modo_de_jogo = 'PVP'
    pokemon_jogador1 = None
    pokemon_jogador2 = None
    
    messagebox.showinfo("Seleção de Pokémon", "Jogador 1, escolha seu Pokémon na Pokédex.")
    ir_para_pokedex(frame_batalha)


def iniciar_batalha_vs_maquina():
    """Prepara e inicia a interface da batalha."""
    global batalha_atual, pokemon_escolhido, modo_de_jogo
    modo_de_jogo = 'PVE'

    if not pokemon_escolhido:
        messagebox.showwarning("Aviso", "Selecione um Pokémon na Pokédex primeiro!")
        ir_para_pokedex(frame_batalha)  # Vai para a Pokedex vindo da tela de batalha
        return

    tocar_musica_batalha()  # Toca a música de batalha

    # Escolher um oponente aleatório que não seja o pokémon do jogador
    oponentes_possiveis = [p for p in Pokemon.POKEDEX_DATA if p["nome"] != pokemon_escolhido.nome]
    if not oponentes_possiveis:
        messagebox.showerror("Erro", "Não há oponentes disponíveis para a batalha.")
        return
    
    dados_oponente = choice(oponentes_possiveis)
    oponente = Pokemon.criar_pokemon(dados_oponente["nome"])
    
    # Criar uma nova instância de Batalha (vai resetar o HP)
    pokemon_jogador_batalha = Pokemon.criar_pokemon(pokemon_escolhido.nome)
    batalha_atual = Batalha(pokemon_jogador_batalha, oponente)

    # Esconder o menu de seleção de modo e mostrar a arena
    frame_selecao_modo.pack_forget()
    frame_arena.pack(expand=True, fill=tk.BOTH)
    btn_voltar_batalha.pack_forget()  # Esconde o botão voltar antigo

    # Configurar a UI da batalha
    atualizar_ui_batalha()
    label_log_batalha.config(text=f"A batalha entre {batalha_atual.pokemon_jogador.nome} e {batalha_atual.pokemon_oponente.nome} começou!")


def iniciar_batalha_pvp():
    """Inicia a batalha no modo Jogador vs Jogador."""
    global batalha_atual, turno_jogador_atual

    tocar_musica_batalha()

    # Os pokémons são recriados para garantir que comecem com HP total
    p1 = Pokemon.criar_pokemon(pokemon_jogador1.nome)
    p2 = Pokemon.criar_pokemon(pokemon_jogador2.nome)
    batalha_atual = Batalha(p1, p2)
    
    turno_jogador_atual = 1 # Garante que o Jogador 1 comece

    # Esconde a pokedex/menu e mostra a arena
    frame_pokedex.pack_forget()
    frame_menu.pack_forget()
    frame_batalha.pack(expand=True, fill=tk.BOTH)
    frame_selecao_modo.pack_forget()
    frame_arena.pack(expand=True, fill=tk.BOTH)
    btn_voltar_batalha.pack_forget()

    # Configurar a UI da batalha
    atualizar_ui_batalha()
    label_log_batalha.config(text=f"Começa a batalha!\nTurno do Jogador {turno_jogador_atual} ({batalha_atual.pokemon_jogador.nome})")


def atualizar_ui_batalha():
    """Atualiza as informações dos pokémons (HP, imagem) na tela."""
    if not batalha_atual:
        return

    command_func = None
    atacante_atual = None
    # --- Define os objetos e textos com base no modo de jogo ---
    if modo_de_jogo == 'PVP':
        jogador_obj = batalha_atual.pokemon_jogador
        oponente_obj = batalha_atual.pokemon_oponente
        jogador_label = f"Jogador 1: {jogador_obj.nome}\nHP: {jogador_obj.hp}"
        oponente_label = f"Jogador 2: {oponente_obj.nome}\nHP: {oponente_obj.hp}"
        
        # Define de quem são os ataques a serem exibidos
        atacante_atual = jogador_obj if turno_jogador_atual == 1 else oponente_obj
        command_func = turno_pvp
    
    else: # Modo PVE
        jogador_obj = batalha_atual.pokemon_jogador
        oponente_obj = batalha_atual.pokemon_oponente
        jogador_label = f"{jogador_obj.nome}\nHP: {jogador_obj.hp}"
        oponente_label = f"{oponente_obj.nome}\nHP: {oponente_obj.hp}"
        atacante_atual = jogador_obj
        command_func = turno_jogador

    # --- Atualizar Jogador (Esquerda) ---
    info_jogador_text = jogador_label
    label_info_jogador.config(text=info_jogador_text)
    try:
        img_jogador = Image.open(f"imagens/{jogador_obj.imagem}")
        img_jogador = img_jogador.resize((250, 250), Image.Resampling.LANCZOS)
        foto_jogador = ImageTk.PhotoImage(img_jogador)
        label_img_jogador.config(image=foto_jogador)
        label_img_jogador.image = foto_jogador
    except FileNotFoundError:
        label_img_jogador.config(image="", text=f"{jogador_obj.nome}")

    # --- Atualizar Oponente (Direita) ---
    info_oponente_text = oponente_label
    label_info_oponente.config(text=info_oponente_text)
    try:
        img_oponente = Image.open(f"imagens/{oponente_obj.imagem}")
        img_oponente = img_oponente.resize((250, 250), Image.Resampling.LANCZOS)
        foto_oponente = ImageTk.PhotoImage(img_oponente)
        label_img_oponente.config(image=foto_oponente)
        label_img_oponente.image = foto_oponente
    except FileNotFoundError:
        label_img_oponente.config(image="", text=f"{oponente_obj.nome}")

    # --- Atualizar Botões de Ataque ---
    # Limpar botões antigos para não duplicar
    for widget in frame_acoes_jogador.winfo_children():
        widget.destroy()

    # Criar novos botões para cada ataque do jogador do turno
    for ataque in atacante_atual.ataques:
        btn = tk.Button(
            frame_acoes_jogador,
            text=f"{ataque['nome']}\n(Dano: {ataque['dano']})",
            font=("Courier", 12),
            command=lambda a=ataque, cmd=command_func: cmd(a)
        )
        btn.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)


def turno_jogador(ataque):
    """Executa o ataque do jogador e prepara o turno do oponente."""
    if not batalha_atual:
        return
    
    # Desabilitar botões para prevenir múltiplos cliques
    for widget in frame_acoes_jogador.winfo_children():
        widget.config(state=tk.DISABLED)

    log = batalha_atual.executar_ataque(batalha_atual.pokemon_jogador, batalha_atual.pokemon_oponente, ataque)
    label_log_batalha.config(text=log)
    atualizar_ui_batalha() # Atualiza o HP do oponente na tela

    vencedor = batalha_atual.obter_vencedor()
    if vencedor:
        finalizar_batalha(vencedor)
    else:
        # Turno do oponente após 1.5 segundos para dar tempo de ler
        janela.after(1500, turno_oponente)

def turno_pvp(ataque):
    """Executa o turno de um jogador no modo PVP."""
    global turno_jogador_atual
    if not batalha_atual:
        return

    # Desabilitar botões para prevenir múltiplos cliques
    for widget in frame_acoes_jogador.winfo_children():
        widget.config(state=tk.DISABLED)

    # Determinar atacante e defensor
    if turno_jogador_atual == 1:
        atacante = batalha_atual.pokemon_jogador
        defensor = batalha_atual.pokemon_oponente
    else:
        atacante = batalha_atual.pokemon_oponente
        defensor = batalha_atual.pokemon_jogador

    log = batalha_atual.executar_ataque(atacante, defensor, ataque)
    
    # A atualização da UI mostrará o dano, mas o log é atualizado primeiro
    atualizar_ui_batalha() 
    label_log_batalha.config(text=log)


    vencedor = batalha_atual.obter_vencedor()
    if vencedor:
        finalizar_batalha(vencedor)
    else:
        # Passar o turno para o outro jogador
        turno_jogador_atual = 2 if turno_jogador_atual == 1 else 1
        proximo_atacante_nome = batalha_atual.pokemon_jogador.nome if turno_jogador_atual == 1 else batalha_atual.pokemon_oponente.nome
        
        # Atualiza o log e a UI para o próximo turno após um delay
        def proximo_turno():
            label_log_batalha.config(text=f"Turno do Jogador {turno_jogador_atual} ({proximo_atacante_nome})")
            atualizar_ui_batalha() # Isso vai re-criar e habilitar os botões para o jogador certo

        janela.after(2000, proximo_turno)


def turno_oponente():
    """Executa o ataque do oponente e reabilita os controles do jogador."""
    if not batalha_atual:
        return

    log = batalha_atual.ataque_do_oponente()
    label_log_batalha.config(text=log)
    atualizar_ui_batalha() # Atualiza o HP do jogador na tela

    vencedor = batalha_atual.obter_vencedor()
    if vencedor:
        finalizar_batalha(vencedor)
    else:
        # Reabilita os botões do jogador após um delay para dar tempo de ler
        janela.after(1500, habilitar_controles_jogador)

def habilitar_controles_jogador():
    """Reabilita os botões de ataque do jogador se a batalha não acabou (APENAS MODO PVE)."""
    if modo_de_jogo != 'PVE':
        return
        
    # Garante que os botões não sejam reabilitados se a batalha terminou durante o delay.
    if batalha_atual and not batalha_atual.obter_vencedor():
        for widget in frame_acoes_jogador.winfo_children():
            # Apenas reabilita botões de ataque, e não o de 'voltar' que pode aparecer
            if isinstance(widget, tk.Button) and widget.cget('text') != "Voltar ao Menu":
                 widget.config(state=tk.NORMAL)

def finalizar_batalha(vencedor):
    """Exibe o resultado final da batalha."""
    # Garante que os botões de ataque fiquem desabilitados
    for widget in frame_acoes_jogador.winfo_children():
        widget.config(state=tk.DISABLED)
    
    mensagem_vencedor = ""
    if modo_de_jogo == 'PVP':
        # No Batalha.__init__, pokemon_jogador é o p1 e pokemon_oponente é o p2
        if vencedor is batalha_atual.pokemon_jogador:
            mensagem_vencedor = "O Jogador 1 venceu!"
        else:
            mensagem_vencedor = "O Jogador 2 venceu!"
    else: # PVE
        mensagem_vencedor = f"O vencedor é {vencedor.nome}!"

    messagebox.showinfo("Fim da Batalha", mensagem_vencedor)
    
    # Adicionar um botão para voltar ao menu
    btn_voltar = tk.Button(frame_acoes_jogador, text="Voltar ao Menu", font=("Courier", 14), command=lambda: voltar_para_menu_da_batalha())
    btn_voltar.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

def voltar_para_menu_da_batalha():
    """Limpa a arena e volta para o menu principal."""
    # Esconde a arena e o frame de batalha geral, mostra o menu principal
    frame_arena.pack_forget()
    voltar_para_menu(frame_batalha)
    
    # Remostra os botões de seleção de modo para uma nova partida
    frame_selecao_modo.pack(pady=20)
    btn_voltar_batalha.pack(pady=10)


# --- Funções da Pokédex ---


def mostrar_detalhes(event):
    # Pega o item selecionado na lista
    indices_selecionados = lista_pokemons.curselection()
    if not indices_selecionados:
        return

    nome_pokemon_selecionado = lista_pokemons.get(indices_selecionados[0])

    # Usa a função que já temos para "criar" (buscar os dados) o pokémon
    pokemon = Pokemon.criar_pokemon(nome_pokemon_selecionado)

    if pokemon:
        caminho_imagem = f"imagens/{pokemon.imagem}"
        try:
            img = Image.open(caminho_imagem)
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            foto_pokemon = ImageTk.PhotoImage(img)

            # Atualiza o label da imagem
            label_imagem_pokemon.config(image=foto_pokemon)
            label_imagem_pokemon.image = foto_pokemon
        except FileNotFoundError:
            # Se não encotrar o label, limpa a imagem
            label_imagem_pokemon.config(image="")
            label_imagem_pokemon.image = ""

        # Formata o texto com os detalhes
        detalhes = f"Nome: {pokemon.nome}\n"
        detalhes += f"Tipo: {pokemon.tipo}\n"
        detalhes += f"HP: {pokemon.hp}\n\n"
        detalhes += f"Descrição: {pokemon.descricao}\n\n"
        detalhes += "Ataques:\n"
        for ataque in pokemon.ataques:
            detalhes += f"- {ataque['nome']} (Dano: {ataque['dano']})\n"

        # Atualiza o texto da label de detalhes
        label_detalhes_pokemon.config(text=detalhes)


# --- Configuração da Janela Principal ---
janela = tk.Tk()
janela.title("Pokémon")

# Agora sempre abre em tela cheia
janela.attributes("-fullscreen", True)

# É possivel sair do fullscreen apertando ESC


def sair_fullscreen(event=None):
    janela.attributes("-fullscreen", False)


janela.bind("<Escape>", sair_fullscreen)

janela.config(bg="black")

# --- Frame do Menu Principal ---
frame_menu = tk.Frame(janela, bg="black")

titulo = tk.Label(frame_menu, text="Pokémon", font=(
    "Courier", 20, "bold"), fg="white", bg="black")
titulo.pack(pady=20)

botao_batalhar = tk.Button(frame_menu, text="Battle", font=(
    "Courier", 16), width=15, command=ir_para_batalha)
botao_batalhar.pack(pady=10)

# O comando do botão da Pokédex agora chama a função ir_para_pokedex
botao_pokedex = tk.Button(frame_menu, text="Ver Pokédex", font=(
    "Courier", 16), width=15, command=lambda: ir_para_pokedex(frame_menu))
botao_pokedex.pack(pady=10)

botao_sair = tk.Button(frame_menu, text="Exit", font=(
    "Courier", 16), width=15, command=sair)
botao_sair.pack(pady=10)

# --- Frame da Tela de Batalha ---
frame_batalha = tk.Frame(janela, bg="black")

# -- Sub-frame para SELEÇÃO DE MODO --
frame_selecao_modo = tk.Frame(frame_batalha, bg="black")
frame_selecao_modo.pack(pady=20)

label_batalha = tk.Label(frame_selecao_modo, text="Choose Mode", font=(
    "Courier", 20, "bold"), fg="white", bg="black")
label_batalha.pack(pady=20)

btn_um_jogador = tk.Button(frame_selecao_modo, text="Um jogador", font=(
    "Courier", 16), width=15, command=preparar_selecao_pvp)
btn_um_jogador.pack(pady=10)

btn_vs_maquina = tk.Button(frame_selecao_modo, text="Vs Maquina", font=(
    "Courier", 16), width=15, command=iniciar_batalha_vs_maquina)  # Comando alterado
btn_vs_maquina.pack(pady=10)

# O botão voltar da tela de seleção de modo
btn_voltar_batalha = tk.Button(frame_batalha, text="Voltar", font=(
    "Courier", 16), width=15, command=lambda: voltar_para_menu(frame_batalha))
btn_voltar_batalha.pack(pady=10)


# -- Sub-frame para a ARENA DE BATALHA (inicialmente escondido) --
frame_arena = tk.Frame(frame_batalha, bg="black")

# -- Arena: Topo (Display dos Pokémons) --
frame_pokemons_display = tk.Frame(frame_arena, bg="black")
frame_pokemons_display.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

# Display do Jogador (Esquerda)
frame_jogador = tk.Frame(frame_pokemons_display, bg="black")
frame_jogador.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
label_img_jogador = tk.Label(frame_jogador, bg="black")
label_img_jogador.pack(pady=10)
label_info_jogador = tk.Label(frame_jogador, text="", font=("Courier", 16), fg="white", bg="black")
label_info_jogador.pack(pady=10)

# Display do Oponente (Direita)
frame_oponente = tk.Frame(frame_pokemons_display, bg="black")
frame_oponente.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
label_img_oponente = tk.Label(frame_oponente, bg="black")
label_img_oponente.pack(pady=10)
label_info_oponente = tk.Label(frame_oponente, text="", font=("Courier", 16), fg="white", bg="black")
label_info_oponente.pack(pady=10)

# -- Arena: Meio (Log da Batalha) --
label_log_batalha = tk.Label(frame_arena, text="", font=("Courier", 14), fg="yellow", bg="gray10", height=4, wraplength=800, padx=10)
label_log_batalha.pack(fill=tk.X, padx=20, pady=10)

# -- Arena: Baixo (Ações do Jogador) --
frame_acoes_jogador = tk.Frame(frame_arena, bg="black")
frame_acoes_jogador.pack(fill=tk.X, padx=20, pady=20, side=tk.BOTTOM)


# --- Frame da Pokédex (NOVO) ---
frame_pokedex = tk.Frame(janela, bg="black")

# Frame para a lista à esquerda
frame_lista = tk.Frame(frame_pokedex, bg="black")
frame_lista.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

# Frame para a lista à direita
frame_detalhes = tk.Frame(frame_pokedex, bg="black")
frame_detalhes.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20, pady=20)

# 2. Label para a IMAGEM do Pokémon
label_imagem_pokemon = tk.Label(frame_detalhes, bg="gray20")
label_imagem_pokemon.pack(pady=10)

# Título da Pokédex
label_titulo_pokedex = tk.Label(frame_lista, text="Pokédex", font=(
    "Courier", 20, "bold"), fg="white", bg="black")
label_titulo_pokedex.pack(pady=10)

# Lista para os nomes dos Pokémons
lista_pokemons = tk.Listbox(frame_lista, font=(
    "Courier", 14), width=20, height=15, bg="gray10", fg="white", selectbackground="red")
lista_pokemons.pack(pady=10)

# Adiciona cada nome de Pokémon do seu arquivo de regras na lista
for pokemon_data in Pokemon.POKEDEX_DATA:
    lista_pokemons.insert(tk.END, pokemon_data["nome"])

# "Conecta" a função mostrar_detalhes ao evento de seleção da lista
lista_pokemons.bind("<<ListboxSelect>>", mostrar_detalhes)

# Botão para voltar ao menu
btn_voltar_pokedex = tk.Button(frame_lista, text="Voltar", font=(
    "Courier", 16), width=15, command=lambda: voltar_para_menu(frame_pokedex))
btn_voltar_pokedex.pack(pady=20, side=tk.BOTTOM)

# Label para mostrar os detalhes do Pokémon selecionado
label_detalhes_pokemon = tk.Label(
    frame_detalhes,
    text="Selecione um Pokémon na lista",
    font=("Courier", 14),
    fg="white",
    bg="gray20",
    justify=tk.LEFT,  # Alinha o texto à esquerda
    padx=20,
    pady=20,
    wraplength=400  # Quebra a linha se o texto for muito longo
)
label_detalhes_pokemon.pack(expand=True, fill=tk.BOTH)

# Adicionado botão "Selecionar" na Pokédex
# Ele salva o Pokémon escolhido em uma variável global e leva para a tela de batalha
pokemon_escolhido = None  # variável global para armazenar escolha


def selecionar_pokemon():
    global pokemon_escolhido, pokemon_jogador1, pokemon_jogador2
    indices_selecionados = lista_pokemons.curselection()  # Seleciona o pokémon da lista
    if not indices_selecionados:
        messagebox.showwarning("Aviso", "Selecione um Pokémon primeiro!")
        return

    nome_pokemon_selecionado = lista_pokemons.get(indices_selecionados[0])
    
    if modo_de_jogo == 'PVP':
        if not pokemon_jogador1:
            pokemon_jogador1 = Pokemon.criar_pokemon(nome_pokemon_selecionado)
            messagebox.showinfo("Jogador 1 Selecionou", f"Jogador 1 escolheu {pokemon_jogador1.nome}!\n\nAgora é a vez do Jogador 2.")
            # A tela da Pokédex permanece para o jogador 2
            lista_pokemons.selection_clear(0, tk.END) # Limpa a seleção para o próximo jogador
            label_detalhes_pokemon.config(text="Jogador 2, selecione um Pokémon na lista")
            label_imagem_pokemon.config(image="")
        
        elif not pokemon_jogador2:
            pokemon_jogador2 = Pokemon.criar_pokemon(nome_pokemon_selecionado)
            if pokemon_jogador1.nome == pokemon_jogador2.nome:
                messagebox.showwarning("Aviso", "O Jogador 2 não pode escolher o mesmo pokémon que o Jogador 1!")
                pokemon_jogador2 = None
                return

            messagebox.showinfo("Jogador 2 Selecionou", f"Jogador 2 escolheu {pokemon_jogador2.nome}!\n\nA batalha vai começar!")
            iniciar_batalha_pvp()

    else: # Modo PVE (comportamento original)
        pokemon_escolhido = Pokemon.criar_pokemon(nome_pokemon_selecionado)

        if pokemon_escolhido:
            messagebox.showinfo("Pokémon Selecionado",
                                f"Você escolheu {pokemon_escolhido.nome}!")
            # Para conseguir ir batalha, tive que esconder a tela da Pokédex para ele levar a tela de batalha
            frame_pokedex.pack_forget()  # Aqui ele esconde a tela da Pokédex
            frame_batalha.pack(expand=True, fill=tk.BOTH)


btn_selecionar = tk.Button(
    frame_detalhes,
    text="Selecionar",
    font=("Courier", 16),
    width=15,
    command=selecionar_pokemon
)
btn_selecionar.pack(pady=10)

# Esse codigo mostra o FPS do jogo
fps_label = tk.Label(janela, text="", font=(
    "Courier", 12), fg="green", bg="black")
fps_label.place(x=10, y=10)

# Defini um limite de 60fps, acho que ta bom
ultimo_tempo = time.time()
frames = 0


def game_loop():
    global ultimo_tempo, frames

    frames += 1
    agora = time.time()
    if agora - ultimo_tempo >= 1:  # a cada 1 segundo
        fps_label.config(text=f"FPS: {frames}")
        frames = 0
        ultimo_tempo = agora

    janela.after(16, game_loop)  # 16ms = ~60 FPS


# --- Início do Programa ---
frame_menu.pack(expand=True)  # Sempre abre em tela cheia
tocar_musica_menu()  # Toca a música do menu ao iniciar
game_loop()
janela.mainloop()

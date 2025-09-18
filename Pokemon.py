import tkinter as tk
from tkinter import messagebox
import regrasDoJogo  # Importa o arquivo com as regras do jogo
from PIL import Image, ImageTk # Biblioteca para manipulação de imagens
# --- Funções de Navegação ---

def ir_para_batalha():
    frame_menu.pack_forget()  # Esconde o menu principal
    frame_batalha.pack(expand=True)

def ir_para_pokedex():
    frame_menu.pack_forget()  # Esconde o menu principal
    frame_pokedex.pack(expand=True)
    # Limpa a seleção e os detalhes ao entrar na pokedex
    label_detalhes_pokemon.config(text="")
    lista_pokemons.selection_clear(0, tk.END)

def voltar_para_menu(frame_atual):
    frame_atual.pack_forget()  # Esconde o frame atual (batalha ou pokedex)
    frame_menu.pack(expand=True)  # Mostra o menu principal

def sair():
    janela.quit()
    janela.destroy()

# --- Funções da Pokédex ---

def mostrar_detalhes(event):
    # Pega o item selecionado na lista
    indices_selecionados = lista_pokemons.curselection()
    if not indices_selecionados:
        return

    nome_pokemon_selecionado = lista_pokemons.get(indices_selecionados[0])

    # Usa a função que já temos para "criar" (buscar os dados) o pokémon
    pokemon = regrasDoJogo.criar_pokemon(nome_pokemon_selecionado)

    if pokemon:
        caminho_imagem = f"imagens/{pokemon.imagem}" 
        try:
            img = Image.open(caminho_imagem)
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            foto_pokemon = ImageTk.PhotoImage(img)

            # Atualiza o label da imagem
            label_imagem_pokemon.config(image=foto_pokemon)
            label_imagem_pokemon.image = foto_pokemon # Guarda uma referência para a imagem
        except FileNotFoundError:
            # Se não encontrar a imagem, limpa o label
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
janela.geometry("1920x1080")
janela.config(bg="black")

# --- Frame do Menu Principal ---
frame_menu = tk.Frame(janela, bg="black")

titulo = tk.Label(frame_menu, text="Pokémon", font=("Courier", 20, "bold"), fg="white", bg="black")
titulo.pack(pady=20)

botao_batalhar = tk.Button(frame_menu, text="Battle", font=("Courier", 16), width=15, command=ir_para_batalha)
botao_batalhar.pack(pady=10)

# O comando do botão da Pokédex agora chama a função ir_para_pokedex
botao_pokedex = tk.Button(frame_menu, text="Ver Pokédex", font=("Courier", 16), width=15, command=ir_para_pokedex)
botao_pokedex.pack(pady=10)

botao_sair = tk.Button(frame_menu, text="Exit", font=("Courier", 16), width=15, command=sair)
botao_sair.pack(pady=10)

# --- Frame da Tela de Batalha ---
frame_batalha = tk.Frame(janela, bg="black")

label_batalha = tk.Label(frame_batalha, text="Choose Mode", font=("Courier", 20, "bold"), fg="white", bg="black")
label_batalha.pack(pady=20)

btn_um_jogador = tk.Button(frame_batalha, text="Um jogador", font=("Courier", 16), width=15, command=lambda: messagebox.showinfo("Modo", "Um jogador selecionado!"))
btn_um_jogador.pack(pady=10)

btn_vs_maquina = tk.Button(frame_batalha, text="Vs Maquina", font=("Courier", 16), width=15, command=lambda: messagebox.showinfo("Modo", "Vs Máquina selecionado!"))
btn_vs_maquina.pack(pady=10)

# O botão voltar agora é mais genérico
btn_voltar_batalha = tk.Button(frame_batalha, text="Voltar", font=("Courier", 16), width=15, command=lambda: voltar_para_menu(frame_batalha))
btn_voltar_batalha.pack(pady=10)

# --- Frame da Pokédex (NOVO) ---
frame_pokedex = tk.Frame(janela, bg="black")

# Frame para a lista à esquerda
frame_lista = tk.Frame(frame_pokedex, bg="black")
frame_lista.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

# Frame para os detalhes à direita
frame_detalhes = tk.Frame(frame_pokedex, bg="black")
frame_detalhes.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20, pady=20)

# 2. Label para a IMAGEM do Pokémon
label_imagem_pokemon = tk.Label(frame_detalhes, bg="gray20")
label_imagem_pokemon.pack(pady=10)

# Título da Pokédex
label_titulo_pokedex = tk.Label(frame_lista, text="Pokédex", font=("Courier", 20, "bold"), fg="white", bg="black")
label_titulo_pokedex.pack(pady=10)

# Lista para os nomes dos Pokémon
lista_pokemons = tk.Listbox(frame_lista, font=("Courier", 14), width=20, height=15, bg="gray10", fg="white", selectbackground="red")
lista_pokemons.pack(pady=10)

# Adiciona cada nome de Pokémon do seu arquivo de regras na lista
for pokemon_data in regrasDoJogo.POKEDEX_DATA:
    lista_pokemons.insert(tk.END, pokemon_data["nome"])

# "Conecta" a função mostrar_detalhes ao evento de seleção da lista
lista_pokemons.bind("<<ListboxSelect>>", mostrar_detalhes)

# Botão para voltar ao menu
btn_voltar_pokedex = tk.Button(frame_lista, text="Voltar", font=("Courier", 16), width=15, command=lambda: voltar_para_menu(frame_pokedex))
btn_voltar_pokedex.pack(pady=20, side=tk.BOTTOM)

# Label para mostrar os detalhes do Pokémon selecionado
label_detalhes_pokemon = tk.Label(
    frame_detalhes,
    text="Selecione um Pokémon na lista",
    font=("Courier", 14),
    fg="white",
    bg="gray20",
    justify=tk.LEFT, # Alinha o texto à esquerda
    padx=20,
    pady=20,
    wraplength=400 # Quebra a linha se o texto for muito longo
)
label_detalhes_pokemon.pack(expand=True, fill=tk.BOTH)


# --- Início do Programa ---
frame_menu.pack(expand=True)  # Começa mostrando o menu principal
janela.mainloop()
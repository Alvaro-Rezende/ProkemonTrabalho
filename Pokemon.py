import tkinter as tk
from tkinter import messagebox


def batalhar():
    # Devemos montar a logica de batalha nesse ponto
    frame_menu.pack_forget()  # Esconde o menu principal
    frame_batalha.pack(expand=True)


# Logica para sair da janela
# Não ta dando certo por causa do looping
def sair():
    janela.quit()
    janela.destroy()


def voltar_menu():
    frame_batalha.pack_forget()  # Esconde a tela de batalha
    frame_menu.pack(expand=True)  # Mostra o menu principal


# Criação da janela
janela = tk.Tk()
janela.title("Pokémon")
janela.geometry("1920x1080")
janela.config(bg="black")

# Fundo do programa (menu principal)
frame_menu = tk.Frame(janela, bg="black")

# Titulo da janela
titulo = tk.Label(frame_menu, text="Pokémon", font=(
    "Courier", 20, "bold"), fg="white", bg="black")
titulo.pack(pady=20)

# titulo do botão de batalha
botao_batalhar = tk.Button(frame_menu, text="Battle", font=(
    "Courier", 16), width=15, command=batalhar)
botao_batalhar.pack(pady=10)

# titulo do botão de sair
botao_sair = tk.Button(frame_menu, text="Exit", font=(
    "Courier", 16), width=15, command=sair)
botao_sair.pack(pady=10)

frame_menu.pack(expand=True)

# Tela de batalha
frame_batalha = tk.Frame(janela, bg="black")

label_batalha = tk.Label(frame_batalha, text="Choose Mode", font=(
    "Courier", 20, "bold"), fg="white", bg="black")
label_batalha.pack(pady=20)

btn_um_jogador = tk.Button(frame_batalha, text="Um jogador", font=(
    "Courier", 16), width=15, command=lambda: messagebox.showinfo("Modo", "Um jogador selecionado!"))
btn_um_jogador.pack(pady=10)

btn_vs_maquina = tk.Button(frame_batalha, text="Vs Maquina", font=(
    "Courier", 16), width=15, command=lambda: messagebox.showinfo("Modo", "Vs Máquina selecionado!"))
btn_vs_maquina.pack(pady=10)

btn_voltar = tk.Button(frame_batalha, text="Voltar", font=(
    "Courier", 16), width=15, command=voltar_menu)
btn_voltar.pack(pady=10)

# looping pro programa rodar sem parar
janela.mainloop()

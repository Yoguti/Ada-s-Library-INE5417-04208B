from tkinter import *
import random

class AdasLibraryInterface:
    """
    Interface gráfica simplificada para o jogo Ada's Library.
    """
    def __init__(self):
        # Configuração da janela principal
        self.main_window = Tk()
        self.main_window.title("Ada's Library")
        self.main_window.geometry("800x650")
        self.main_window.resizable(False, False)
        self.main_window.configure(bg="#315931")

        # Frame para mensagens
        self.message_frame = Frame(self.main_window, bg="#315931", pady=5)
        self.message_label = Label(self.message_frame, text="", bg="#F0FFF0", relief="groove", padx=10, pady=5)
        self.message_label.pack()
        self.message_frame.pack(pady=5)

        # Frames principais
        self.opponent_frame = Frame(self.main_window, bg="#315931", pady=10)
        self.objective_frame = Frame(self.main_window, bg="#315931", pady=10)
        self.your_books_frame = Frame(self.main_window, bg="#315931", pady=10)
        self.cards_frame = Frame(self.main_window, bg="#315931", pady=10)
        self.buttons_frame = Frame(self.main_window, bg="#315931", pady=10)

        # Posicionamento dos frames
        Label(self.main_window, text="Vez do Jogador 1", font="Arial 18 bold", bg="#315931").pack(pady=10)

        Label(self.opponent_frame, text="Livros do Oponente", font="Arial 14", bg="#315931").pack()
        self.opponent_frame.pack()

        Label(self.objective_frame, text="Objetivo", font="Arial 14", bg="#315931").pack()
        self.objective_frame.pack()

        Label(self.your_books_frame, text="Seus Livros", font="Arial 14", bg="#315931").pack()
        self.your_books_frame.pack()

        Label(self.cards_frame, text="Cartas", font="Arial 14", bg="#315931").pack()
        self.cards_frame.pack()

        self.buttons_frame.pack(pady=20)

        # Cores dos livros
        self.colors = {
            "vermelho": "#E63946",
            "azul_claro": "#A8DADC",
            "cinza": "#6D6875",
            "marrom": "#8B4513",
            "amarelo": "#F1C40F",
            "azul_escuro": "#1D3557"
        }

        # Criação dos livros do oponente
        self.opponent_books = []
        for i in range(10):
            color = random.choice(list(self.colors.keys()))
            book = Frame(self.opponent_frame, width=50, height=75, bg=self.colors[color],
                         highlightbackground="black", highlightthickness=2)
            book.pack_propagate(False)
            book.pack(side=LEFT, padx=5)
            self.opponent_books.append(book)

        # Criação dos livros do objetivo
        self.objective_books = []
        objective_colors = random.sample(list(self.colors.keys()), 6)
        for color in objective_colors:
            book = Frame(self.objective_frame, width=60, height=90, bg=self.colors[color],
                         highlightbackground="black", highlightthickness=2)
            book.pack_propagate(False)
            book.pack(side=LEFT, padx=5)
            self.objective_books.append(book)

        # Criação dos seus livros
        self.your_books = []
        for i in range(10):
            color = random.choice(list(self.colors.keys()))
            book = Frame(self.your_books_frame, width=50, height=75, bg=self.colors[color],
                         highlightbackground="black", highlightthickness=2)
            book.pack_propagate(False)
            book.pack(side=LEFT, padx=5)
            # Adiciona um evento de clique para cada livro chamando a função clicar_livro_wrapper
            book.bind("<Button-1>", self.criar_funcao_clique_livro(i))
            self.your_books.append(book)

        # Criação das cartas
        self.cards = ["Trocar 2 livros", "Mover esquerda", "Mover direita", "Trocar extremos", "Trocar com oponente"]
        self.card_widgets = []

        for i, text in enumerate(self.cards):
            card = Frame(self.cards_frame, width=70, height=100, bg="white",
                         highlightbackground="black", highlightthickness=2)
            card.pack_propagate(False)
            card.pack(side=LEFT, padx=5)

            label_carta = Label(card, text=text, bg="white", wraplength=60, font="Arial 8")
            label_carta.pack(pady=(40, 0))
            # Adiciona um evento de clique para cada carta chamando a função clicar_carta_wrapper
            card.bind("<Button-1>", self.criar_funcao_clique_carta(i))
            self.card_widgets.append(card)

        # Botões
        Button(self.buttons_frame, text="Descartar", bg="#FF6B6B", fg="white",
              font="Arial 12", padx=10, pady=5, command=self.descartar).pack(side=LEFT, padx=10)

        Button(self.buttons_frame, text="Cancelar", bg="#4ECDC4", fg="white",
              font="Arial 12", padx=10, pady=5, command=self.cancelar).pack(side=LEFT, padx=10)

        Button(self.buttons_frame, text="Conceder", bg="#6D6875", fg="white",
              font="Arial 12", padx=10, pady=5, command=self.conceder).pack(side=LEFT, padx=10)

        # Iniciar o loop principal
        self.main_window.mainloop()

    def mostrar_mensagem(self, mensagem):
        """
        Exibe uma mensagem na label de mensagem.
        """
        self.message_label.config(text=mensagem)
        print(mensagem)

    # Função auxiliar para criar a função de clique do livro com o índice correto
    def criar_funcao_clique_livro(self, indice):
        def clique(event):
            self.clicar_livro(event, indice)
        return clique

    def clicar_livro(self, event, indice):
        """
        Método chamado quando um livro é clicado.
        """
        self.mostrar_mensagem(f"Livro {indice} clicado")
        # Lógica para lidar com o clique no livro

    # Função auxiliar para criar a função de clique da carta com o índice correto
    def criar_funcao_clique_carta(self, indice):
        def clique(event):
            self.clicar_carta(event, indice)
        return clique

    def clicar_carta(self, event, indice):
        """
        Método chamado quando uma carta é clicada.
        """
        self.mostrar_mensagem(f"Carta {indice} clicada: {self.cards[indice]}")
        # Lógica para lidar com o clique na carta

    def descartar(self):
        """
        Método chamado quando o botão Descartar é clicado.
        """
        self.mostrar_mensagem("Botão Descartar clicado")
        # Lógica para descartar

    def cancelar(self):
        """
        Método chamado quando o botão Cancelar é clicado.
        """
        self.mostrar_mensagem("Botão Cancelar clicado")
        # Lógica para cancelar

    def conceder(self):
        """
        Método chamado quando o botão Conceder é clicado.
        """
        self.mostrar_mensagem("Botão Conceder clicado")
        # Lógica para conceder

# Iniciar a aplicação
if __name__ == "__main__":
    app = AdasLibraryInterface()

print("Executando a interface do Ada's Library...")
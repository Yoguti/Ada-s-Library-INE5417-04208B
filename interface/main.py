from tkinter import *
import random

class AdasLibraryInterface:
    """
    Interface gráfica.
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
        self.selected_cards = []
        self.selected_books = []
        self.selected_objetctive = [] 
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
        for i, color in enumerate(objective_colors):
            book = Frame(self.objective_frame, width=60, height=90, bg=self.colors[color],
                        highlightbackground="black", highlightthickness=2)
            book.pack_propagate(False)
            book.pack(side=LEFT, padx=5)
            # Adiciona o bind que estava faltando aqui:
            book.bind("<Button-1>", self.criar_funcao_clique_objetivo(i))
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

        livro = self.your_books[indice]

        if indice in self.selected_books:
            # Desselecionar
            livro.config(highlightbackground="black", highlightthickness=2)
            self.selected_books.remove(indice)
            self.mostrar_mensagem(f"Livro {indice} desmarcado")
        else:
            if len(self.selected_books) >= 2:
                # Remove o mais novo (índice 1)
                antigo_indice = self.selected_books.pop(1)
                self.your_books[antigo_indice].config(highlightbackground="black", highlightthickness=2)
                self.mostrar_mensagem(f"Livro {antigo_indice} desmarcado automaticamente")

            # Selecionar o novo
            livro.config(highlightbackground="white", highlightthickness=3)
            self.selected_books.append(indice)
            self.mostrar_mensagem(f"Livro {indice} selecionado")


    # Função auxiliar para criar a função de clique do objetivo com o índice correto
    def criar_funcao_clique_objetivo(self, indice):
        def clique(event):
            self.clicar_objetivo(event, indice)
        return clique
 
    def clicar_objetivo(self, event, indice):
        """
        Método chamado quando um livro de objetivo é clicado.
        """
        self.mostrar_mensagem(f"Livro objetivo {indice} clicado")

        if indice in self.selected_objetctive:
            # Se já está selecionado, desmarca
            self.objective_books[indice].config(highlightbackground="black", highlightthickness=2)
            self.selected_objetctive.remove(indice)
            self.mostrar_mensagem(f"Livro objetivo {indice} desmarcado")
        else:
            if len(self.selected_objetctive) >= 2:
                # Se já tem dois, remove o mais novo
                antigo = self.selected_objetctive.pop(1)
                self.objective_books[antigo].config(highlightbackground="black", highlightthickness=2)

            # Marca o novo
            self.objective_books[indice].config(highlightbackground="white", highlightthickness=3)
            self.selected_objetctive.append(indice)
            self.mostrar_mensagem(f"Livro objetivo {indice} selecionado")

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

        carta = self.card_widgets[indice]

        if indice in self.selected_cards:
            # Desselecionar
            carta.config(highlightbackground="black", highlightthickness=2)
            self.selected_cards.remove(indice)
            self.mostrar_mensagem(f"Carta {indice} desmarcada")
        else:
            # Desmarca outras se quiser permitir só uma selecionada
            for i in self.selected_cards:
                self.card_widgets[i].config(highlightbackground="black", highlightthickness=2)
            self.selected_cards.clear()

            # Selecionar nova
            carta.config(highlightbackground="yellow", highlightthickness=3)
            self.selected_cards.append(indice)
            self.mostrar_mensagem(f"Carta {indice} selecionada")


    def descartar(self):
        """
        Método chamado quando o botão Descartar é clicado.
        """
        self.mostrar_mensagem("Botão Descartar clicado")
        # Lógica para descartar

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
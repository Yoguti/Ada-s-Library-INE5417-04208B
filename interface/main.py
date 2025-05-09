from tkinter import *
import random

class AdasLibraryInterface:
    """
    Interface gráfica para o jogo Ada's Library com telas separadas.
    """
    def __init__(self):
        # Configuração da janela principal
        self.main_window = Tk()
        self.main_window.title("Ada's Library")
        self.main_window.geometry("800x650")
        self.main_window.resizable(False, False)
        self.main_window.configure(bg="#315931")
        
        # Variáveis de estado do jogo
        self.game_state = "welcome"  # welcome, name_input, playing, game_over
        self.current_player = "Jogador 1"
        self.player_name = None
        self.opponent_name = "Oponente"
        
        # Criar containers para cada tela
        self.welcome_screen = Frame(self.main_window, bg="#315931")
        self.name_input_screen = Frame(self.main_window, bg="#315931")
        self.game_screen = Frame(self.main_window, bg="#315931")
        self.game_over_screen = Frame(self.main_window, bg="#315931")
        
        # Inicializar todas as telas
        self.setup_welcome_screen()
        self.setup_name_input_screen()
        self.setup_game_screen()
        self.setup_game_over_screen()
        
        # Mostrar a tela inicial
        self.show_screen("welcome")
        
        # Iniciar o loop principal
        self.main_window.mainloop()
    
    def show_screen(self, screen_name):
        """
        Mostra a tela especificada e esconde as outras.
        """
        self.welcome_screen.pack_forget()
        self.name_input_screen.pack_forget()
        self.game_screen.pack_forget()
        self.game_over_screen.pack_forget()
        
        self.game_state = screen_name
        
        if screen_name == "welcome":
            self.welcome_screen.pack(fill=BOTH, expand=True)
        elif screen_name == "name_input":
            self.name_input_screen.pack(fill=BOTH, expand=True)
        elif screen_name == "playing":
            self.game_screen.pack(fill=BOTH, expand=True)
        elif screen_name == "game_over":
            self.game_over_screen.pack(fill=BOTH, expand=True)
    
    def setup_welcome_screen(self):
        """
        Configura a tela de boas-vindas.
        """
        # Título grande
        title_label = Label(self.welcome_screen, text="Ada's Library", 
                           font=("Arial", 48, "bold"), bg="#315931", fg="white")
        title_label.pack(pady=(150, 20))
        
        # Subtítulo
        subtitle_label = Label(self.welcome_screen, 
                              text="Um jogo de estratégia com livros e cartas", 
                              font=("Arial", 16), bg="#315931", fg="white")
        subtitle_label.pack(pady=(0, 50))
        
        # Botão para iniciar
        start_button = Button(self.welcome_screen, text="Iniciar Jogo", 
                             font=("Arial", 14, "bold"), bg="#A8DADC", fg="#1D3557",
                             padx=20, pady=10, relief=RAISED, bd=3,
                             command=lambda: self.show_screen("name_input"))
        start_button.pack(pady=20)
    
    def setup_name_input_screen(self):
        """
        Configura a tela de entrada do nome do jogador.
        """
        # Título
        title_label = Label(self.name_input_screen, text="Qual é o seu nome?", 
                           font=("Arial", 24, "bold"), bg="#315931", fg="white")
        title_label.pack(pady=(150, 50))
        
        # Campo de entrada
        self.name_entry = Entry(self.name_input_screen, font=("Arial", 16), width=30)
        self.name_entry.pack(pady=20)
        self.name_entry.focus_set()  # Coloca o cursor no campo de entrada
        
        # Frame para botões
        buttons_frame = Frame(self.name_input_screen, bg="#315931")
        buttons_frame.pack(pady=30)
        
        # Botão para confirmar
        confirm_button = Button(buttons_frame, text="Confirmar", 
                               font=("Arial", 14, "bold"), bg="#A8DADC", fg="#1D3557",
                               padx=15, pady=8, relief=RAISED, bd=3,
                               command=self.confirm_name)
        confirm_button.pack(side=LEFT, padx=10)
        
        # Botão para voltar
        back_button = Button(buttons_frame, text="Voltar", 
                            font=("Arial", 14), bg="#6D6875", fg="white",
                            padx=15, pady=8, relief=RAISED, bd=3,
                            command=lambda: self.show_screen("welcome"))
        back_button.pack(side=LEFT, padx=10)
        
        # Vincular a tecla Enter ao botão confirmar
        self.name_entry.bind("<Return>", lambda event: self.confirm_name())
    
    def confirm_name(self):
        """
        Confirma o nome do jogador e avança para a tela do jogo.
        """
        name = self.name_entry.get().strip()
        if name:
            self.player_name = name
            self.current_player = name
        else:
            self.player_name = "Jogador 1"
            self.current_player = "Jogador 1"
        
        # Limpar o campo para próxima vez
        self.name_entry.delete(0, END)
        
        # Inicializar o jogo e mostrar a tela do jogo
        self.initialize_game()
        self.show_screen("playing")
    
    def setup_game_screen(self):
        """
        Configura a estrutura da tela do jogo.
        """
        # Frame para mensagens
        self.message_frame = Frame(self.game_screen, bg="#315931", pady=5)
        self.message_label = Label(self.message_frame, text="", bg="#F0FFF0", relief="groove", padx=10, pady=5)
        self.message_label.pack()
        self.message_frame.pack(pady=5)

        # Frames principais
        self.selected_cards = []
        self.selected_books = []
        self.selected_objetctive = [] 
        self.opponent_frame = Frame(self.game_screen, bg="#315931", pady=10)
        self.objective_frame = Frame(self.game_screen, bg="#315931", pady=10)
        self.your_books_frame = Frame(self.game_screen, bg="#315931", pady=10)
        self.cards_frame = Frame(self.game_screen, bg="#315931", pady=10)
        self.buttons_frame = Frame(self.game_screen, bg="#315931", pady=10)

        # Posicionamento dos frames
        self.turn_label = Label(self.game_screen, text="Vez do Jogador 1", font="Arial 18 bold", bg="#315931")
        self.turn_label.pack(pady=10)

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

        # Botões
        self.discard_button = Button(self.buttons_frame, text="Descartar", bg="#FF6B6B", fg="white",
                                    font="Arial 12", padx=10, pady=5, command=self.descartar)
        self.discard_button.pack(side=LEFT, padx=10)

        self.concede_button = Button(self.buttons_frame, text="Conceder", bg="#6D6875", fg="white",
                                    font="Arial 12", padx=10, pady=5, command=self.conceder)
        self.concede_button.pack(side=LEFT, padx=10)
        
        # Botão para menu
        self.menu_button = Button(self.buttons_frame, text="Menu", bg="#1D3557", fg="white",
                                 font="Arial 12", padx=10, pady=5, 
                                 command=lambda: self.show_screen("welcome"))
        self.menu_button.pack(side=LEFT, padx=10)
        
        # Variáveis para armazenar os widgets
        self.opponent_books = []
        self.objective_books = []
        self.your_books = []
        self.card_widgets = []
        self.cards = []
    
    def setup_game_over_screen(self):
        """
        Configura a tela de fim de jogo.
        """
        # Título
        self.game_over_title = Label(self.game_over_screen, text="Fim de Jogo", 
                                    font=("Arial", 36, "bold"), bg="#315931", fg="white")
        self.game_over_title.pack(pady=(150, 20))
        
        # Resultado
        self.result_label = Label(self.game_over_screen, text="", 
                                 font=("Arial", 24), bg="#315931", fg="white")
        self.result_label.pack(pady=(0, 50))
        
        # Frame para botões
        buttons_frame = Frame(self.game_over_screen, bg="#315931")
        buttons_frame.pack(pady=30)
        
        # Botão para jogar novamente
        play_again_button = Button(buttons_frame, text="Jogar Novamente", 
                                  font=("Arial", 14, "bold"), bg="#A8DADC", fg="#1D3557",
                                  padx=15, pady=8, relief=RAISED, bd=3,
                                  command=self.reset_game)
        play_again_button.pack(side=LEFT, padx=10)
        
        # Botão para voltar ao menu
        menu_button = Button(buttons_frame, text="Menu Principal", 
                            font=("Arial", 14), bg="#6D6875", fg="white",
                            padx=15, pady=8, relief=RAISED, bd=3,
                            command=lambda: self.show_screen("welcome"))
        menu_button.pack(side=LEFT, padx=10)
        
        # Botão para sair
        exit_button = Button(buttons_frame, text="Sair", 
                            font=("Arial", 14), bg="#E63946", fg="white",
                            padx=15, pady=8, relief=RAISED, bd=3,
                            command=self.main_window.quit)
        exit_button.pack(side=LEFT, padx=10)
    
    def initialize_game(self):
        """
        Inicializa o jogo com os elementos do tabuleiro.
        """
        # Limpar tabuleiro existente
        self.clear_board()
        
        # Atualizar o rótulo de turno
        self.turn_label.config(text=f"Vez de {self.player_name}")
        
        # Criação dos livros do oponente
        for i in range(10):
            color = random.choice(list(self.colors.keys()))
            book = Frame(self.opponent_frame, width=50, height=75, bg=self.colors[color],
                         highlightbackground="black", highlightthickness=2)
            book.pack_propagate(False)
            book.pack(side=LEFT, padx=5)
            self.opponent_books.append(book)

        # Criação dos livros do objetivo
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
        
        # Mostrar mensagem inicial
        self.mostrar_mensagem("Partida iniciada! Selecione uma carta e depois um livro para jogar.")
    
    def clear_board(self):
        """
        Limpa o tabuleiro, removendo todos os livros e cartas.
        """
        # Limpar livros do oponente
        for book in self.opponent_books:
            book.destroy()
        self.opponent_books = []
        
        # Limpar livros objetivo
        for book in self.objective_books:
            book.destroy()
        self.objective_books = []
        
        # Limpar seus livros
        for book in self.your_books:
            book.destroy()
        self.your_books = []
        
        # Limpar cartas
        for card in self.card_widgets:
            card.destroy()
        self.card_widgets = []
        
        # Limpar seleções
        self.selected_cards = []
        self.selected_books = []
        self.selected_objetctive = []
    
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
        if not self.selected_cards:
            self.mostrar_mensagem("Selecione uma carta para descartar.")
            return
            
        card_index = self.selected_cards[0]
        self.mostrar_mensagem(f"Descartando carta: {self.cards[card_index]}")
        
        # Substituir a carta descartada com uma nova aleatória
        new_card_texts = ["Inverter ordem", "Trocar adjacentes", "Mover 2 posições", "Trocar com mestre", "Reorganizar"]
        self.cards[card_index] = random.choice(new_card_texts)
        
        # Atualizar o texto da carta
        card = self.card_widgets[card_index]
        label = card.winfo_children()[0]
        label.config(text=self.cards[card_index])
        
        # Limpar seleção
        card.config(highlightbackground="black", highlightthickness=2)
        self.selected_cards.clear()
        
        # Simular passagem de turno
        self.simulate_opponent_turn()

    def conceder(self):
        """
        Método chamado quando o botão Conceder é clicado.
        """
        self.mostrar_mensagem("Partida concedida!")
        self.end_game(self.opponent_name, conceded=True)
    
    def simulate_opponent_turn(self):
        """
        Simula uma jogada do oponente.
        """
        self.turn_label.config(text=f"Vez do {self.opponent_name}")
        self.mostrar_mensagem(f"{self.opponent_name} está jogando...")
        
        # Simular uma troca visual de livros do oponente após 1.5 segundos
        self.main_window.after(1500, self.perform_opponent_move)
    
    def perform_opponent_move(self):
        """
        Executa a jogada simulada do oponente.
        """
        # Simular uma troca visual de livros do oponente
        if len(self.opponent_books) >= 2:
            idx1, idx2 = random.sample(range(len(self.opponent_books)), 2)
            book1 = self.opponent_books[idx1]
            book2 = self.opponent_books[idx2]
            color1 = book1["bg"]
            color2 = book2["bg"]
            book1.config(bg=color2)
            book2.config(bg=color1)
        
        self.mostrar_mensagem(f"{self.opponent_name} jogou uma carta.")
        
        # Verificar fim de jogo (10% de chance)
        if random.random() < 0.1:
            self.main_window.after(1000, lambda: self.end_game(self.opponent_name))
        else:
            # Devolver o turno para o jogador após 1 segundo
            self.main_window.after(1000, self.return_turn_to_player)
    
    def return_turn_to_player(self):
        """
        Devolve o turno para o jogador.
        """
        self.turn_label.config(text=f"Vez de {self.player_name}")
        self.mostrar_mensagem("Sua vez! Selecione uma carta e depois um livro para jogar.")
    
    def end_game(self, winner, conceded=False):
        """
        Finaliza o jogo com um vencedor.
        """
        # Atualizar a tela de fim de jogo
        if conceded:
            self.game_over_title.config(text="Partida Concedida")
            self.result_label.config(text=f"Vencedor: {winner}")
        else:
            self.game_over_title.config(text="Fim de Jogo")
            self.result_label.config(text=f"Vencedor: {winner}")
        
        # Mostrar a tela de fim de jogo
        self.show_screen("game_over")
    
    def reset_game(self):
        """
        Reseta o jogo para a tela de entrada de nome.
        """
        self.clear_board()
        self.show_screen("name_input")

# Iniciar a aplicação
if __name__ == "__main__":
    app = AdasLibraryInterface()

print("Executando a interface do Ada's Library...")

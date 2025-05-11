from tkinter import *
import random
from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface
from dog.start_status import StartStatus

class ADASLibraryInterface(DogPlayerInterface):
    """
    Interface gráfica para o jogo Ada's Library com telas separadas e integração com o servidor DOG.
    """
    def __init__(self):
        # Inicializa a classe pai DogPlayerInterface
        super().__init__()
        
        # Configuração da conexão DOG
        self.dog_actor = DogActor()
        self.connected = False
        self.in_game = False
        self.players = []
        self.local_player_id = ""
        
        # Configuração da janela principal
        self.main_window = Tk()
        self.main_window.title("Ada's Library")
        self.main_window.geometry("1200x1000")  # AUMENTADO: tamanho da janela
        self.main_window.resizable(False, False)
        self.main_window.configure(bg="#315931")
        
        # Variáveis de estado do jogo
        self.game_state = "welcome"  # welcome, playing, game_over
        self.current_player = "Jogador 1"
        self.player_name = None
        self.opponent_name = "Oponente"
        
        # Criar containers para cada tela
        self.welcome_screen = Frame(self.main_window, bg="#315931")
        self.game_screen = Frame(self.main_window, bg="#315931")
        self.game_over_screen = Frame(self.main_window, bg="#315931")
        
        # Inicializar todas as telas
        self.setup_welcome_screen()
        self.setup_game_screen()
        self.setup_game_over_screen()
        
        # Mostrar a tela inicial
        self.show_screen("welcome")
        
        # Iniciar o loop principal
        self.main_window.mainloop()
    
    # Métodos para integração com o servidor DOG
    
    def conectar_ao_servidor(self, nome_jogador):
        """
        Estabelece uma conexão com o servidor DOG.
        
        Args:
            nome_jogador (str): O nome do jogador a ser registrado no servidor
            
        Returns:
            str: Mensagem indicando o resultado da tentativa de conexão
        """
        self.player_name = nome_jogador
        resultado_conexao = self.dog_actor.initialize(nome_jogador, self)
        
        if resultado_conexao == "Conectado a Dog Server":
            self.connected = True
            print(f"Conectado com sucesso ao servidor DOG como {nome_jogador}")
        else:
            print(f"Falha na conexão: {resultado_conexao}")
            
        return resultado_conexao
    
    def solicitar_sessao_jogo(self, numero_jogadores):
        """
        Envia uma solicitação para iniciar uma sessão de jogo.
        
        Args:
            numero_jogadores (int): O número de jogadores necessários para o jogo
            
        Returns:
            bool: True se a sessão de jogo foi iniciada com sucesso, False caso contrário
        """
        if not self.connected:
            print("Não é possível solicitar sessão de jogo: Não conectado ao servidor")
            return False
        
        # Solicitar início de partida
        start_status = self.dog_actor.start_match(str(numero_jogadores))
        
        # Processar o resultado
        codigo = start_status.get_code()
        mensagem = start_status.get_message()
        
        if codigo == "2":  # Partida iniciada
            self.in_game = True
            self.local_player_id = start_status.get_local_id()
            self.players = start_status.get_players()
            print(f"Sessão de jogo iniciada com sucesso: {mensagem}")
            print(f"Jogadores na partida: {len(self.players)}")
            self._processar_info_jogadores()
            return True
        else:
            print(f"Falha ao iniciar sessão de jogo: {mensagem} (código: {codigo})")
            return False
    
    def _processar_info_jogadores(self):
        """Processa e exibe informações sobre os jogadores na sessão atual."""
        print("\nJogadores nesta sessão de jogo:")
        for i, jogador in enumerate(self.players):
            nome_jogador, id_jogador, ordem_jogador = jogador
            is_local = "(Você)" if id_jogador == self.local_player_id else ""
            print(f"Jogador {i+1}: {nome_jogador} {is_local} - Ordem: {ordem_jogador}")
    
    def enviar_jogada(self, dados_jogada, status_partida="next"):
        """
        Envia uma jogada para o servidor durante uma partida.
        
        Args:
            dados_jogada (dict): Dicionário contendo os dados da jogada
            status_partida (str): Status da partida após esta jogada 
                               ("next", "progress", ou "finished")
        """
        if not self.in_game:
            print("Não é possível enviar jogada: Não está em uma partida ativa")
            return
        
        # Adicionar status da partida aos dados da jogada
        dados_jogada["match_status"] = status_partida
        
        # Enviar a jogada
        resultado = self.dog_actor.send_move(dados_jogada)
        print(f"Jogada enviada ao servidor: {dados_jogada}")
        return resultado
    
    def mostrar_erro(self, mensagem):
        """
        Exibe uma mensagem de erro na tela de boas-vindas.
        
        Args:
            mensagem (str): A mensagem de erro a ser exibida
        """
        if not hasattr(self, 'error_label'):
            self.error_label = Label(self.welcome_screen, text="", 
                                    font=("Arial", 18), bg="#315931", fg="#FF6B6B")
            self.error_label.pack(pady=10)
        
        self.error_label.config(text=mensagem)
    
    # Sobrescrever métodos de DogPlayerInterface
    
    def receive_start(self, start_status):
        """
        Trata o recebimento de um comando de início de jogo do servidor DOG.
        
        Args:
            start_status (StartStatus): Objeto contendo informações sobre o jogo iniciado
        """
        print("\n--- SINAL DE INÍCIO DE JOGO RECEBIDO DO SERVIDOR ---")
        
        self.in_game = True
        self.local_player_id = start_status.get_local_id()
        self.players = start_status.get_players()
        
        print(f"Sessão de jogo iniciada por jogador remoto")
        print(f"Mensagem: {start_status.get_message()}")
        self._processar_info_jogadores()
        
        # Aqui normalmente inicializaria o estado do jogo
        print("Jogo inicializado e pronto para jogar")
        
        # Inicializar o jogo e mostrar a tela do jogo
        self.initialize_game()
        self.show_screen("playing")
    
    def receive_move(self, move_dict):
        """
        Trata o recebimento de uma jogada de outro jogador.
        
        Args:
            move_dict (dict): Dicionário contendo os dados da jogada
        """
        player_id = move_dict.get("player", "desconhecido")
        match_status = move_dict.get("match_status", "desconhecido")
        
        # Encontrar nome do jogador a partir do ID
        player_name = "Jogador Desconhecido"
        for player in self.players:
            if player[1] == player_id:
                player_name = player[0]
                break
        
        print(f"\nRecebida jogada de {player_name} (ID: {player_id}):")
        print(f"Dados da jogada: {move_dict}")
        print(f"Status da partida após jogada: {match_status}")
        
        # Aqui normalmente atualizaria o estado do jogo com base na jogada recebida
        self.mostrar_mensagem(f"Jogada recebida de {player_name}")
        
        # Simular turno do oponente
        self.current_player = self.opponent_name
        self.turn_label.config(text=f"Vez do {self.opponent_name}")
        
        # Devolver o turno para o jogador após 1 segundo
        self.main_window.after(1000, self.return_turn_to_player)
        
        if match_status == "finished":
            print("Jogo foi marcado como finalizado pelo oponente")
            self.in_game = False
            self.end_game(player_name)
    
    def receive_withdrawal_notification(self):
        """Trata notificação de que um oponente abandonou o jogo."""
        print("\n--- NOTIFICAÇÃO DE DESISTÊNCIA DO OPONENTE ---")
        print("Um oponente abandonou a partida. O jogo acabou.")
        self.in_game = False
        
        # Mostrar mensagem na interface
        self.mostrar_mensagem("Um oponente abandonou a partida!")
        self.end_game(self.player_name, conceded=True)
    
    # Métodos da interface gráfica original
    
    def show_screen(self, screen_name):
        """
        Mostra a tela especificada e esconde as outras.
        """
        self.welcome_screen.pack_forget()
        self.game_screen.pack_forget()
        self.game_over_screen.pack_forget()
        
        self.game_state = screen_name
        
        if screen_name == "welcome":
            self.welcome_screen.pack(fill=BOTH, expand=True)
        elif screen_name == "playing":
            self.game_screen.pack(fill=BOTH, expand=True)
        elif screen_name == "game_over":
            self.game_over_screen.pack(fill=BOTH, expand=True)
    
    def setup_welcome_screen(self):
        """
        Configura a tela de boas-vindas com entrada de nome.
        """
        # Título grande
        title_label = Label(self.welcome_screen, text="Ada's Library", 
                           font=("Serif", 180, "bold"), bg="#315931", fg="white")  # AUMENTADO: tamanho da fonte
        title_label.pack(pady=(180, 10))  # AUMENTADO: espaçamento
        
        # Subtítulo
        subtitle_label = Label(self.welcome_screen, 
                              text="Sua estante é seu campo de batalha.", 
                              font=("Serif", 50), bg="#315931", fg="white")  # AUMENTADO: tamanho da fonte
        subtitle_label.pack(pady=(0, 100))  # AUMENTADO: espaçamento
        
        # Pergunta do nome
        name_label = Label(self.welcome_screen, text="Qual é o seu nome?", 
                          font=("Arial", 34, "bold"), bg="#315931", fg="white")
        name_label.pack(pady=(0, 0))
        
        # Campo de entrada
        self.name_entry = Entry(self.welcome_screen, font=("Arial", 22), width=30)  # AUMENTADO: tamanho da fonte
        self.name_entry.pack(pady=20)  # AUMENTADO: espaçamento
        self.name_entry.focus_set()  # Coloca o cursor no campo de entrada
        
        # Botão para iniciar
        start_button = Button(self.welcome_screen, text="Iniciar Partida", 
                             font=("Arial", 33, "bold"), bg="#A8DADC", fg="#1D3557",  # AUMENTADO: tamanho da fonte
                             padx=30, pady=15, relief=RAISED, bd=5,  # AUMENTADO: padding e borda
                             command=self.confirm_name)
        start_button.pack(pady=30)  # AUMENTADO: espaçamento
        
        # Vincular a tecla Enter ao botão iniciar
        self.name_entry.bind("<Return>", lambda event: self.confirm_name())
    
    def confirm_name(self):
        """
        Confirma o nome do jogador e tenta iniciar uma partida.
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
        
        # Conectar ao servidor DOG
        resultado_conexao = self.conectar_ao_servidor(self.player_name)
        
        if not self.connected:
            self.mostrar_erro(f"Falha na conexão: {resultado_conexao}")
            return
            
        # Solicitar sessão de jogo se conectado
        if self.solicitar_sessao_jogo(2):  # Solicitar jogo com 2 jogadores
            # Só inicializa o jogo e mostra a tela se a sessão foi iniciada com sucesso
            self.initialize_game()
            self.show_screen("playing")
        else:
            # Se não conseguiu iniciar a sessão, mostra mensagem de erro
            self.mostrar_erro("Não foi possível iniciar: jogadores insuficientes")
    
    def setup_game_screen(self):
        """
        Configura a estrutura da tela do jogo.
        """
        # Frame para mensagens
        self.message_frame = Frame(self.game_screen, bg="#315931", pady=10)  # AUMENTADO: padding
        self.message_label = Label(self.message_frame, text="", font=("Arial", 30),  # AUMENTADO: tamanho da fonte
                                 bg="#F0FFF0", relief="groove", padx=15, pady=10)  # AUMENTADO: padding
        self.message_label.pack(fill=X)
        self.message_frame.pack(pady=10, fill=X, padx=30)  # AUMENTADO: padding

        # Frames principais
        self.selected_cards = []
        self.selected_books = []
        self.selected_objective = []  # Corrigido o nome da variável
        self.opponent_frame = Frame(self.game_screen, bg="#315931", pady=15)  # AUMENTADO: padding
        self.objective_frame = Frame(self.game_screen, bg="#315931", pady=15)  # AUMENTADO: padding
        self.your_books_frame = Frame(self.game_screen, bg="#315931", pady=15)  # AUMENTADO: padding
        self.cards_frame = Frame(self.game_screen, bg="#315931", pady=15)  # AUMENTADO: padding
        self.buttons_frame = Frame(self.game_screen, bg="#315931", pady=15)  # AUMENTADO: padding

        # Posicionamento dos frames
        self.turn_label = Label(self.game_screen, text="Vez do Jogador 1", font="Arial 24 bold", bg="#315931", fg="white")  # AUMENTADO: tamanho da fonte
        self.turn_label.pack(pady=15)  # AUMENTADO: padding

        Label(self.opponent_frame, text="Livros do Oponente", font="Arial 30", bg="#315931", fg="white").pack()  # AUMENTADO: tamanho da fonte
        self.opponent_frame.pack(pady=(0, 10))  # AUMENTADO: espaçamento

        Label(self.objective_frame, text="Objetivo", font="Arial 30", bg="#315931", fg="white").pack()  # AUMENTADO: tamanho da fonte
        self.objective_frame.pack(pady=(0, 10))  # AUMENTADO: espaçamento

        Label(self.your_books_frame, text="Seus Livros", font="Arial 30", bg="#315931", fg="white").pack()  # AUMENTADO: tamanho da fonte
        self.your_books_frame.pack(pady=(0, 10))  # AUMENTADO: espaçamento

        Label(self.cards_frame, text="Cartas", font="Arial 30", bg="#315931", fg="white").pack()  # AUMENTADO: tamanho da fonte
        self.cards_frame.pack(pady=(0, 10))  # AUMENTADO: espaçamento

        self.buttons_frame.pack(pady=30)  # AUMENTADO: espaçamento

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
                                    font="Arial 30", padx=20, pady=10,  # AUMENTADO: tamanho da fonte e padding
                                    command=self.descartar)
        self.discard_button.pack(side=LEFT, padx=20)  # AUMENTADO: espaçamento

        self.concede_button = Button(self.buttons_frame, text="Conceder", bg="#6D6875", fg="white",
                                    font="Arial 30", padx=20, pady=10,  # AUMENTADO: tamanho da fonte e padding
                                    command=self.conceder)
        self.concede_button.pack(side=LEFT, padx=20)  # AUMENTADO: espaçamento
        
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
                                    font=("Arial", 48, "bold"), bg="#315931", fg="white")  # AUMENTADO: tamanho da fonte
        self.game_over_title.pack(pady=(180, 30))  # AUMENTADO: espaçamento
        
        # Resultado
        self.result_label = Label(self.game_over_screen, text="", 
                                 font=("Arial", 34), bg="#315931", fg="white")  # AUMENTADO: tamanho da fonte
        self.result_label.pack(pady=(0, 70))  # AUMENTADO: espaçamento
        
        # Frame para botões
        buttons_frame = Frame(self.game_over_screen, bg="#315931")
        buttons_frame.pack(pady=40)  # AUMENTADO: espaçamento
        
        # Botão para jogar novamente
        play_again_button = Button(buttons_frame, text="Jogar Novamente", 
                                  font=("Arial", 30, "bold"), bg="#A8DADC", fg="#1D3557",  # AUMENTADO: tamanho da fonte
                                  padx=25, pady=12, relief=RAISED, bd=5,  # AUMENTADO: padding e borda
                                  command=self.reset_game)
        play_again_button.pack(side=LEFT, padx=15)  # AUMENTADO: espaçamento
    
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
            book = Frame(self.opponent_frame, width=70, height=100, bg=self.colors[color],  # AUMENTADO: tamanho dos livros
                         highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
            book.pack_propagate(False)
            book.pack(side=LEFT, padx=8)  # AUMENTADO: espaçamento
            self.opponent_books.append(book)

        # Criação dos livros do objetivo
        objective_colors = random.sample(list(self.colors.keys()), 6)
        for i, color in enumerate(objective_colors):
            book = Frame(self.objective_frame, width=85, height=120, bg=self.colors[color],  # AUMENTADO: tamanho dos livros
                        highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
            book.pack_propagate(False)
            book.pack(side=LEFT, padx=8)  # AUMENTADO: espaçamento
            # Adiciona o bind para clique no objetivo
            book.bind("<Button-1>", self.criar_funcao_clique_objetivo(i))
            self.objective_books.append(book)

        # Criação dos seus livros
        for i in range(10):
            color = random.choice(list(self.colors.keys()))
            book = Frame(self.your_books_frame, width=70, height=100, bg=self.colors[color],  # AUMENTADO: tamanho dos livros
                         highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
            book.pack_propagate(False)
            book.pack(side=LEFT, padx=8)  # AUMENTADO: espaçamento
            # Adiciona um evento de clique para cada livro
            book.bind("<Button-1>", self.criar_funcao_clique_livro(i))
            self.your_books.append(book)

        # Criação das cartas
        self.cards = ["Trocar 2 livros", "Mover esquerda", "Mover direita", "Trocar extremos", "Trocar com oponente"]
        
        for i, text in enumerate(self.cards):
            card = Frame(self.cards_frame, width=100, height=140, bg="white",  # AUMENTADO: tamanho das cartas
                         highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
            card.pack_propagate(False)
            card.pack(side=LEFT, padx=10)  # AUMENTADO: espaçamento

            label_carta = Label(card, text=text, bg="white", wraplength=90, font="Arial 30")  # AUMENTADO: tamanho da fonte e wraplength
            label_carta.pack(pady=(55, 0))  # AUMENTADO: posicionamento vertical
            # Adiciona um evento de clique para cada carta
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
        self.selected_objective = []  # Corrigido o nome da variável
    
    def mostrar_mensagem(self, mensagem):
        """
        Exibe uma mensagem na label de mensagem.
        """
        if hasattr(self, 'message_label'):
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
        # Verificar se é a vez do jogador
        if self.current_player != self.player_name:
            self.mostrar_mensagem("Não é sua vez de jogar.")
            return
            
        # Verificar se já tem uma carta selecionada (RF05)
        if not self.selected_cards:
            self.mostrar_mensagem("Selecione uma carta primeiro.")
            return
            
        self.mostrar_mensagem(f"Livro {indice} clicado")

        livro = self.your_books[indice]

        if indice in self.selected_books:
            # Desselecionar
            livro.config(highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
            self.selected_books.remove(indice)
            self.mostrar_mensagem(f"Livro {indice} desmarcado")
        else:
            # Se já tem 2 livros selecionados, remove o segundo
            if len(self.selected_books) >= 2:
                antigo_indice = self.selected_books.pop(1)
                self.your_books[antigo_indice].config(highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
                self.mostrar_mensagem(f"Livro {antigo_indice} desmarcado automaticamente")

            # Selecionar o novo
            livro.config(highlightbackground="white", highlightthickness=4)  # AUMENTADO: borda destacada
            self.selected_books.append(indice)
            self.mostrar_mensagem(f"Livro {indice} selecionado")
            
            # Se tiver 2 livros selecionados, aplicar o efeito da carta
            if len(self.selected_books) == 2 and self.selected_cards:
                self.aplicar_efeito_carta()

    # Função auxiliar para criar a função de clique do objetivo com o índice correto
    def criar_funcao_clique_objetivo(self, indice):
        def clique(event):
            self.clicar_objetivo(event, indice)
        return clique
 
    def clicar_objetivo(self, event, indice):
        """
        Método chamado quando um livro de objetivo é clicado.
        """
        # Verificar se é a vez do jogador
        if self.current_player != self.player_name:
            self.mostrar_mensagem("Não é sua vez de jogar.")
            return
            
        self.mostrar_mensagem(f"Livro objetivo {indice} clicado")

        if indice in self.selected_objective:  # Corrigido o nome da variável
            # Se já está selecionado, desmarca
            self.objective_books[indice].config(highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
            self.selected_objective.remove(indice)  # Corrigido o nome da variável
            self.mostrar_mensagem(f"Livro objetivo {indice} desmarcado")
        else:
            if len(self.selected_objective) >= 2:  # Corrigido o nome da variável
                # Se já tem dois, remove o mais novo
                antigo = self.selected_objective.pop(1)  # Corrigido o nome da variável
                self.objective_books[antigo].config(highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda

            # Marca o novo
            self.objective_books[indice].config(highlightbackground="white", highlightthickness=4)  # AUMENTADO: borda destacada
            self.selected_objective.append(indice)  # Corrigido o nome da variável
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
        # Verificar se é a vez do jogador
        if self.current_player != self.player_name:
            self.mostrar_mensagem("Não é sua vez de jogar.")
            return
            
        self.mostrar_mensagem(f"Carta {indice} clicada: {self.cards[indice]}")

        carta = self.card_widgets[indice]

        if indice in self.selected_cards:
            # Desselecionar
            carta.config(highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
            self.selected_cards.remove(indice)
            self.mostrar_mensagem(f"Carta {indice} desmarcada")
            
            # Limpar seleções de livros também
            for i in self.selected_books:
                self.your_books[i].config(highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
            self.selected_books.clear()
        else:
            # Desmarca outras cartas se quiser permitir só uma selecionada
            for i in self.selected_cards:
                self.card_widgets[i].config(highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
            self.selected_cards.clear()

            # Selecionar nova
            carta.config(highlightbackground="yellow", highlightthickness=4)  # AUMENTADO: borda destacada
            self.selected_cards.append(indice)
            self.mostrar_mensagem(f"Carta {indice} selecionada: {self.cards[indice]}")

    def aplicar_efeito_carta(self):
        """
        Aplica o efeito da carta selecionada nos livros selecionados.
        """
        if not self.selected_cards or len(self.selected_books) != 2:
            self.mostrar_mensagem("Selecione uma carta e dois livros para jogar.")
            return
            
        card_index = self.selected_cards[0]
        card_type = self.cards[card_index]
        book1_index = self.selected_books[0]
        book2_index = self.selected_books[1]
        
        self.mostrar_mensagem(f"Aplicando efeito da carta: {card_type} nos livros {book1_index} e {book2_index}")
        
        # Aplicar o efeito da carta (trocar os livros)
        book1 = self.your_books[book1_index]
        book2 = self.your_books[book2_index]
        color1 = book1["bg"]
        color2 = book2["bg"]
        
        # Trocar as cores dos livros
        book1.config(bg=color2)
        book2.config(bg=color1)
        
        # Substituir a carta usada com uma nova aleatória
        new_card_texts = ["Inverter ordem", "Trocar adjacentes", "Mover 2 posições", "Trocar com mestre", "Reorganizar"]
        self.cards[card_index] = random.choice(new_card_texts)
        
        # Atualizar o texto da carta
        card = self.card_widgets[card_index]
        label = card.winfo_children()[0]
        label.config(text=self.cards[card_index])
        
        # Limpar seleções
        card.config(highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
        self.selected_cards.clear()
        
        for i in self.selected_books:
            self.your_books[i].config(highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
        self.selected_books.clear()
        
        # Enviar a jogada para o servidor DOG se estiver conectado
        if self.connected and self.in_game:
            jogada = {
                "action": "swap_books",
                "book1": book1_index,
                "book2": book2_index,
                "card": card_type
            }
            self.enviar_jogada(jogada)
        
        # Verificar se o jogador venceu
        if self.verificar_vitoria():
            # Enviar notificação de fim de jogo se estiver conectado
            if self.connected and self.in_game:
                jogada_final = {
                    "action": "game_won",
                    "winner": self.player_name
                }
                self.enviar_jogada(jogada_final, "finished")
            
            self.end_game(self.player_name)
        else:
            # Simular passagem de turno
            self.simulate_opponent_turn()
    
    def verificar_vitoria(self):
        """
        Verifica se o jogador venceu comparando a ordem dos livros com o objetivo.
        """
        # Simplificação: 10% de chance de vitória após cada jogada
        return random.random() < 0.1

    def descartar(self):
        """
        Método chamado quando o botão Descartar é clicado.
        """
        # Verificar se é a vez do jogador
        if self.current_player != self.player_name:
            self.mostrar_mensagem("Não é sua vez de jogar.")
            return
            
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
        card.config(highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
        self.selected_cards.clear()
        
        # Limpar seleções de livros também
        for i in self.selected_books:
            self.your_books[i].config(highlightbackground="black", highlightthickness=3)  # AUMENTADO: borda
        self.selected_books.clear()
        
        # Enviar a jogada de descarte para o servidor DOG se estiver conectado
        if self.connected and self.in_game:
            jogada = {
                "action": "discard",
                "card_index": card_index
            }
            self.enviar_jogada(jogada)
        
        # Simular passagem de turno
        self.simulate_opponent_turn()

    def conceder(self):
        """
        Método chamado quando o botão Conceder é clicado.
        """
        self.mostrar_mensagem("Partida concedida!")
        
        # Enviar notificação de concessão para o servidor DOG se estiver conectado
        if self.connected and self.in_game:
            jogada = {
                "action": "concede",
                "player": self.player_name
            }
            self.enviar_jogada(jogada, "finished")
            self.in_game = False
        
        self.end_game(self.opponent_name, conceded=True)
    
    def simulate_opponent_turn(self):
        """
        Simula uma jogada do oponente.
        """
        self.current_player = self.opponent_name
        self.turn_label.config(text=f"Vez do {self.opponent_name}")
        self.mostrar_mensagem(f"{self.opponent_name} está jogando...")
        
        # Simular turno do oponente após 1.5 segundos
        #self.main_window.after(1500, self.perform_opponent_move)
        # Devolver o turno para o jogador após 1 segundo
        self.main_window.after(1000, self.return_turn_to_player)
    
    def perform_opponent_move(self):
        """
        Executa a jogada simulada do oponente.
        """
    
    def return_turn_to_player(self):
        """
        Devolve o turno para o jogador.
        """
        self.current_player = self.player_name
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
        Reseta o jogo para a tela inicial.
        """
        self.clear_board()
        self.show_screen("welcome")

# Iniciar a aplicação
if __name__ == "__main__":
    app = ADASLibraryInterface()

print("Executando a interface do Ada's Library com integração DOG...")
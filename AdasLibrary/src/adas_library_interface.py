import tkinter as tk
from tkinter import messagebox, simpledialog
from game import Game
from action_card import *
from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface
from dog.start_status import StartStatus

class AdasLibraryInterface(DogPlayerInterface):
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.selected_card_index = None
        self.selected_books = []
        self.selected_target_type = None
        self.awaiting_input = False
        
        # DOG Framework attributes
        self.dog_actor = None
        self.player_name = ""
        self.is_connected = False
        self.match_in_progress = False
        
        self.setup_ui()
    
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Ada's Library")
        
        # Get screen dimensions for responsive sizing
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate window size based on screen size (80% of screen, minimum 1200x900)
        window_width = max(1200, int(screen_width * 0.8))
        window_height = max(900, int(screen_height * 0.8))
        
        # Center window on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)
        self.root.configure(bg="#315931")
        
        # Store dimensions for scaling
        self.window_width = window_width
        self.window_height = window_height
        
        # Create screens
        self.welcome_screen = tk.Frame(self.root, bg="#315931")
        self.game_screen = tk.Frame(self.root, bg="#315931")
        self.game_over_screen = tk.Frame(self.root, bg="#315931")
        
        self.setup_welcome_screen()
        self.setup_game_screen()
        self.setup_game_over_screen()
        
        self.show_screen("welcome")
    
    def setup_welcome_screen(self):
        # Scale font sizes based on window size
        title_font_size = max(120, int(self.window_width * 0.1))
        subtitle_font_size = max(30, int(self.window_width * 0.025))
        button_font_size = max(20, int(self.window_width * 0.017))
        
        # Title
        title_label = tk.Label(self.welcome_screen, text="Ada's Library", 
                              font=("Serif", title_font_size, "bold"), bg="#315931", fg="white")
        title_label.pack(pady=(int(self.window_height * 0.15), 10))
        
        # Subtitle
        subtitle_label = tk.Label(self.welcome_screen, 
                                 text="Sua estante é seu campo de batalha.", 
                                 font=("Serif", subtitle_font_size), bg="#315931", fg="white")
        subtitle_label.pack(pady=(0, int(self.window_height * 0.08)))
        
        # Name input
        name_label = tk.Label(self.welcome_screen, text="Qual é o seu nome?", 
                             font=("Helvetica", button_font_size + 8, "bold"), bg="#315931", fg="white")
        name_label.pack(pady=(0, 0))
        
        self.name_entry = tk.Entry(self.welcome_screen, font=("Helvetica", button_font_size), width=30)
        self.name_entry.pack(pady=20)
        self.name_entry.focus_set()
        
        # Connect button
        connect_button = tk.Button(self.welcome_screen, text="Conectar ao Servidor", 
                                  font=("Helvetica", button_font_size, "bold"), bg="#457b9d", fg="white",
                                  padx=20, pady=10, relief=tk.RAISED, bd=5,
                                  command=self.connect_to_server)
        connect_button.pack(pady=10)
        
        # Start button
        self.start_button = tk.Button(self.welcome_screen, text="Iniciar Partida", 
                                    font=("Helvetica", button_font_size + 5, "bold"), bg="#A8DADC", fg="#1D3557",
                                    padx=30, pady=15, relief=tk.RAISED, bd=5,
                                    command=self.start_game, state=tk.DISABLED)
        self.start_button.pack(pady=30)
        
        # Add reset button to welcome screen
        self.reset_button = tk.Button(self.welcome_screen, text="Resetar Jogo", 
                                    font=("Helvetica", button_font_size, "bold"), bg="#E63946", fg="white",
                                    padx=20, pady=10, relief=tk.RAISED, bd=5,
                                    command=self.reset_game, state=tk.DISABLED)
        self.reset_button.pack(pady=10)
        
        self.name_entry.bind("<Return>", lambda event: self.connect_to_server())
    
    def setup_game_screen(self):
        # Scale font sizes
        message_font_size = max(18, int(self.window_width * 0.015))
        label_font_size = max(20, int(self.window_width * 0.017))
        button_font_size = max(18, int(self.window_width * 0.015))
        
        # Message frame
        self.message_frame = tk.Frame(self.game_screen, bg="#315931", pady=10)
        self.message_label = tk.Label(self.message_frame, text="", font=("Helvetica", message_font_size),
                                     bg="#F0FFF0", relief="groove", padx=15, pady=10)
        self.message_label.pack(fill=tk.X)
        self.message_frame.pack(pady=10, fill=tk.X, padx=30)
        
        # Turn label
        self.turn_label = tk.Label(self.game_screen, text="", font=f"Helvetica {label_font_size} bold", 
                                  bg="#315931", fg="white")
        self.turn_label.pack(pady=15)
        
        # Game frames
        self.opponent_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        self.objective_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        self.your_books_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        self.cards_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        self.buttons_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        
        # Labels with scaled fonts
        tk.Label(self.opponent_frame, text="Livros do Oponente", font=f"Helvetica {label_font_size}", 
                bg="#315931", fg="white").pack()
        self.opponent_frame.pack(pady=(0, 10))
        
        tk.Label(self.objective_frame, text="Objetivo", font=f"Helvetica {label_font_size}", 
                bg="#315931", fg="white").pack()
        self.objective_frame.pack(pady=(0, 10))
        
        tk.Label(self.your_books_frame, text="Seus Livros", font=f"Helvetica {label_font_size}", 
                bg="#315931", fg="white").pack()
        self.your_books_frame.pack(pady=(0, 10))
        
        tk.Label(self.cards_frame, text="Cartas", font=f"Helvetica {label_font_size}", 
                bg="#315931", fg="white").pack()
        self.cards_frame.pack(pady=(0, 10))
        
        self.buttons_frame.pack(pady=30)
        
        # Buttons with scaled fonts
        self.discard_button = tk.Button(self.buttons_frame, text="Descartar Carta", bg="#FF6B6B", fg="white",
                                       font=f"Helvetica {button_font_size}", padx=20, pady=10,
                                       command=self.discard_card)
        self.discard_button.pack(side=tk.LEFT, padx=20)
        
        # Color mapping
        self.colors = {
            "vermelho": "#E63946",
            "azul_claro": "#A8DADC",
            "cinza": "#6D6875",
            "marrom": "#8B4513",
            "amarelo": "#F1C40F",
            "azul_escuro": "#1D3557"
        }
        
        # Widget lists
        self.opponent_books = []
        self.objective_books = []
        self.your_books = []
        self.card_widgets = []
        
        # Calculate book and card sizes based on window size
        self.book_width = max(50, int(self.window_width * 0.04))
        self.book_height = max(70, int(self.window_height * 0.08))
        self.objective_book_width = max(60, int(self.window_width * 0.05))
        self.objective_book_height = max(85, int(self.window_height * 0.09))
        self.card_width = max(80, int(self.window_width * 0.067))
        self.card_height = max(100, int(self.window_height * 0.11))
    
    def setup_game_over_screen(self):
        # Scale font sizes
        title_font_size = max(36, int(self.window_width * 0.03))
        result_font_size = max(24, int(self.window_width * 0.02))
        button_font_size = max(20, int(self.window_width * 0.017))
        
        self.game_over_title = tk.Label(self.game_over_screen, text="Fim de Jogo", 
                                       font=("Helvetica", title_font_size, "bold"), bg="#315931", fg="white")
        self.game_over_title.pack(pady=(int(self.window_height * 0.2), 30))
        
        self.result_label = tk.Label(self.game_over_screen, text="", 
                                    font=("Helvetica", result_font_size), bg="#315931", fg="white")
        self.result_label.pack(pady=(0, 70))
        
        buttons_frame = tk.Frame(self.game_over_screen, bg="#315931")
        buttons_frame.pack(pady=40)
        
        play_again_button = tk.Button(buttons_frame, text="Jogar Novamente", 
                                     font=("Helvetica", button_font_size, "bold"), bg="#A8DADC", fg="#1D3557",
                                     padx=25, pady=12, relief=tk.RAISED, bd=5,
                                     command=self.reset_game)
        play_again_button.pack(side=tk.LEFT, padx=15)
    
    def show_screen(self, screen_name):
        self.welcome_screen.pack_forget()
        self.game_screen.pack_forget()
        self.game_over_screen.pack_forget()
        
        if screen_name == "welcome":
            self.welcome_screen.pack(fill=tk.BOTH, expand=True)
        elif screen_name == "playing":
            self.game_screen.pack(fill=tk.BOTH, expand=True)
        elif screen_name == "game_over":
            self.game_over_screen.pack(fill=tk.BOTH, expand=True)
    
    def start_game(self):
        if not self.is_connected:
            self.show_message("Você precisa estar conectado para iniciar uma partida!")
            return
        
        if self.match_in_progress:
            self.show_message("Já existe uma partida em andamento!")
            return
        
        # Request match start through DOG
        start_status = self.dog_actor.start_match(2)  # Ada's Library is for 2 players
        
        if start_status.code == '0':
            self.show_message("Você está offline")
        elif start_status.code == '1':
            self.show_message("Jogadores insuficientes")
        elif start_status.code == '2':
            self.show_message("Partida iniciada!")
            self.handle_match_start(start_status)
        else:
            self.show_message(f"Erro ao iniciar partida: {start_status.message}")
    
    def initialize_game_display(self):
        self.clear_board()
        
        # Create opponent books
        if self.game.remote_player:
            opponent_books = self.game.remote_player.get_display().get_display()
            for i, book in enumerate(opponent_books):
                color = book.get_color()
                book_widget = tk.Frame(self.opponent_frame, width=self.book_width, height=self.book_height, 
                                      bg=self.colors.get(color, "#BDC3C7"),
                                      highlightbackground="black", highlightthickness=2)
                book_widget.pack_propagate(False)
                book_widget.pack(side=tk.LEFT, padx=5)
                book_widget.bind("<Button-1>", self.create_opponent_book_click(i))
                self.opponent_books.append(book_widget)
        
        # Create objective books
        master_books = self.game.main_display.main_display
        for i, book in enumerate(master_books):
            color = book.get_color()
            book_widget = tk.Frame(self.objective_frame, width=self.objective_book_width, height=self.objective_book_height, 
                                  bg=self.colors.get(color, "#BDC3C7"),
                                  highlightbackground="black", highlightthickness=3)
            book_widget.pack_propagate(False)
            book_widget.pack(side=tk.LEFT, padx=8)
            book_widget.bind("<Button-1>", self.create_objective_book_click(i))
            self.objective_books.append(book_widget)
        
        # Create your books
        if self.game.local_player:
            your_books = self.game.local_player.get_display().get_display()
            for i, book in enumerate(your_books):
                color = book.get_color()
                book_widget = tk.Frame(self.your_books_frame, width=self.book_width, height=self.book_height, 
                                      bg=self.colors.get(color, "#BDC3C7"),
                                      highlightbackground="black", highlightthickness=2)
                book_widget.pack_propagate(False)
                book_widget.pack(side=tk.LEFT, padx=5)
                book_widget.bind("<Button-1>", self.create_your_book_click(i))
                self.your_books.append(book_widget)
        
        # Create cards
        if self.game.local_player:
            cards = self.game.local_player.get_hand().get_cartas()
            card_font_size = max(10, int(self.window_width * 0.008))
            for i, card in enumerate(cards):
                card_widget = tk.Frame(self.cards_frame, width=self.card_width, height=self.card_height, bg="white",
                                      highlightbackground="black", highlightthickness=2)
                card_widget.pack_propagate(False)
                card_widget.pack(side=tk.LEFT, padx=8)
                
                label = tk.Label(card_widget, text=card.description, bg="white", 
                                wraplength=self.card_width-10, font=f"Helvetica {card_font_size}")
                label.pack(pady=(10, 0))
                
                card_widget.bind("<Button-1>", self.create_card_click(i))
                self.card_widgets.append(card_widget)
    
    def clear_board(self):
        for book in self.opponent_books:
            book.destroy()
        self.opponent_books = []
        
        for book in self.objective_books:
            book.destroy()
        self.objective_books = []
        
        for book in self.your_books:
            book.destroy()
        self.your_books = []
        
        for card in self.card_widgets:
            card.destroy()
        self.card_widgets = []
        
        self.selected_books = []
        self.selected_card_index = None
        self.selected_target_type = None
        self.awaiting_input = False
    
    def create_card_click(self, index):
        def click(event):
            self.click_card(index)
        return click
    
    def create_your_book_click(self, index):
        def click(event):
            self.click_your_book(index)
        return click
    
    def create_opponent_book_click(self, index):
        def click(event):
            self.click_opponent_book(index)
        return click
    
    def create_objective_book_click(self, index):
        def click(event):
            self.click_objective_book(index)
        return click
    
    def click_card(self, index):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        # Clear previous card selection
        if self.selected_card_index is not None:
            self.card_widgets[self.selected_card_index].config(
                highlightbackground="black", highlightthickness=2)
        
        # Clear book selections
        self.clear_book_selections()
        
        # Select new card
        self.selected_card_index = index
        self.card_widgets[index].config(highlightbackground="yellow", highlightthickness=4)
        
        # Get card type to determine valid targets
        card = self.game.local_player.get_hand().get_card(index)
        if card:
            self.selected_target_type = card.get_tipo_alvo()
            self.show_message(f"Carta selecionada: {card.description}")
    
    def click_your_book(self, index):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta primeiro!")
            return
        
        if self.selected_target_type not in ["personal", "opponent"]:
            self.show_message("Esta carta não pode ser usada em seus livros!")
            return
        
        self.handle_book_selection(index, "your")
    
    def click_opponent_book(self, index):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta primeiro!")
            return
        
        if self.selected_target_type != "opponent":
            self.show_message("Esta carta não pode ser usada nos livros do oponente!")
            return
        
        self.handle_book_selection(index, "opponent")
    
    def click_objective_book(self, index):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta primeiro!")
            return
        
        if self.selected_target_type != "master":
            self.show_message("Esta carta não pode ser usada nos livros mestres!")
            return
        
        self.handle_book_selection(index, "master")
    
    def handle_book_selection(self, index, book_type):
        card = self.game.local_player.get_hand().get_card(self.selected_card_index)
        if not card:
            return
        
        # Handle different card types
        if isinstance(card, SwapWithSpaces):
            self.handle_swap_with_spaces(index, book_type)
        elif isinstance(card, MoveBookSpaces):
            self.handle_move_book_spaces(index, book_type)
        elif isinstance(card, MoveToEdge):
            self.handle_move_to_edge(index, book_type)
        elif isinstance(card, SwapEdges):
            self.handle_swap_edges()
        elif isinstance(card, SwapWithOpponent):
            self.handle_swap_with_opponent(index, book_type)
        elif isinstance(card, MoveMasterBook):
            self.handle_move_master_book(index, book_type)
    
    def handle_swap_with_spaces(self, index, book_type):
        if len(self.selected_books) == 0:
            self.selected_books.append((index, book_type))
            self.update_book_highlight(index, book_type, True)
            self.show_message("Selecione o segundo livro para trocar.")
        elif len(self.selected_books) == 1:
            self.selected_books.append((index, book_type))
            self.update_book_highlight(index, book_type, True)
            # Apply the card
            target_data = [self.selected_books[0][0], self.selected_books[1][0]]
            self.apply_card_with_data(target_data)
    
    def handle_move_book_spaces(self, index, book_type):
        # Ask for number of spaces to move
        spaces = simpledialog.askinteger("Mover Livro", 
                                        "Quantos espaços mover?\n(negativo = esquerda, positivo = direita)",
                                        minvalue=-9, maxvalue=9)
        if spaces is not None:
            target_data = [index, spaces]
            self.apply_card_with_data(target_data)
    
    def handle_move_to_edge(self, index, book_type):
        # Ask which edge
        edge = messagebox.askyesno("Mover para Extremidade", 
                                  "Mover para a direita?\n(Não = esquerda)")
        edge_value = 1 if edge else 0
        target_data = [index, edge_value]
        self.apply_card_with_data(target_data)
    
    def handle_swap_edges(self):
        # No additional input needed
        target_data = []
        self.apply_card_with_data(target_data)
    
    def handle_swap_with_opponent(self, index, book_type):
        if book_type == "your":
            # Ask for opponent book index (visual position)
            opponent_index = simpledialog.askinteger("Trocar com Oponente", 
                                                    "Posição visual do livro do oponente (1-10):",
                                                    minvalue=1, maxvalue=10)
            if opponent_index is not None:
                # Convert to 0-based index
                visual_index = opponent_index - 1
                target_data = [index, visual_index]
                self.apply_card_with_data(target_data)
    
    def handle_move_master_book(self, index, book_type):
        # Ask for direction and spaces
        direction = messagebox.askyesno("Mover Livro Mestre", 
                                       "Mover para a direita?\n(Não = esquerda)")
        direction_value = 1 if direction else 0
        
        spaces = simpledialog.askinteger("Mover Livro Mestre", 
                                        "Quantos espaços mover? (1 ou 2)",
                                        minvalue=1, maxvalue=2)
        if spaces is not None:
            target_data = [index, direction_value, spaces]
            self.apply_card_with_data(target_data)
    
    def connect_to_server(self):
        player_name = self.name_entry.get().strip()
        if not player_name:
            self.show_message("Por favor, digite seu nome!")
            return
        
        self.player_name = player_name
        
        # Initialize DOG Actor
        self.dog_actor = DogActor()
        connection_result = self.dog_actor.initialize(player_name, self)
        
        self.show_message(connection_result)
        
        if "Conectado" in connection_result:
            self.is_connected = True
            self.start_button.config(state=tk.NORMAL)
            self.name_entry.config(state=tk.DISABLED)
        else:
            self.is_connected = False
            self.start_button.config(state=tk.DISABLED)
    
    def handle_match_start(self, start_status):
        self.match_in_progress = True
        
        # Initialize game with DOG start status
        success = self.game.initialize_players_with_dog(start_status)
        
        if success:
            self.initialize_game_display()
            self.show_screen("playing")
            self.update_display()
            
            # If local player starts, send initial game state
            if self.game.local_player.get_is_turn():
                self.send_initial_game_state()
                self.show_message("Sua vez! Selecione uma carta e depois um livro para jogar.")
            else:
                self.show_message("Aguardando o oponente...")
        else:
            self.show_message("Erro ao inicializar o jogo!")
            self.match_in_progress = False
    
    def send_initial_game_state(self):
        if self.dog_actor and self.game.local_player:
            initial_state = {
                'action': 'initial_state',
                'master_books': [book.get_color() for book in self.game.main_display.main_display],
                'local_books': [book.get_color() for book in self.game.local_player.get_display().get_display()],
                'remote_books': [book.get_color() for book in self.game.remote_player.get_display().get_display()],
                'match_status': 'progress'
            }
            self.dog_actor.send_move(initial_state)
    
    def apply_card_with_data(self, target_data):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        card = self.game.local_player.get_hand().get_card(self.selected_card_index)
        if not card:
            return
        
        success = self.game.apply_card_effect(self.selected_card_index, target_data)
        
        if success:
            self.show_message("Carta aplicada com sucesso!")
            
            # Check for victory
            game_over = self.game.avaliar_fim_da_partida()
            
            # Send move through DOG
            move_data = {
                'action': 'play_card',
                'card_type': card.description,
                'target_data': target_data,
                'match_status': 'finished' if game_over else 'next'
            }
            
            if self.dog_actor:
                self.dog_actor.send_move(move_data)
            
            if game_over:
                self.end_game(self.game.local_player.get_name())
                return
            
            # Switch turns
            self.game.trocar_turno_jogador()
            
            # Clear selections and update display
            self.clear_selections()
            self.update_display()
            
            self.show_message("Aguardando jogada do oponente...")
        else:
            self.show_message("Não foi possível aplicar a carta!")
            self.clear_selections()
    
    def update_book_highlight(self, index, book_type, selected):
        color = "white" if selected else "black"
        thickness = 4 if selected else 2
        
        if book_type == "your" and index < len(self.your_books):
            self.your_books[index].config(highlightbackground=color, highlightthickness=thickness)
        elif book_type == "opponent" and index < len(self.opponent_books):
            self.opponent_books[index].config(highlightbackground=color, highlightthickness=thickness)
        elif book_type == "master" and index < len(self.objective_books):
            self.objective_books[index].config(highlightbackground=color, highlightthickness=thickness)
    
    def discard_card(self):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta para descartar!")
            return
        
        # Remove card and draw new one
        removed_card = self.game.remover_carta_selecionada_da_mao(self.selected_card_index)
        
        if removed_card:
            self.show_message("Carta descartada!")
            
            # Send discard through DOG
            discard_data = {
                'action': 'discard_card',
                'card_index': self.selected_card_index,
                'match_status': 'next'
            }
            
            if self.dog_actor:
                self.dog_actor.send_move(discard_data)
            
            # Switch turns
            self.game.trocar_turno_jogador()
            
            # Clear selections and update display
            self.clear_selections()
            self.update_display()
            
            self.show_message("Aguardando jogada do oponente...")
    
    def receive_start(self, start_status):
        """DOG Framework method - called when match starts remotely"""
        self.show_message("Partida iniciada por outro jogador!")
        self.handle_match_start(start_status)

    def receive_move(self, move):
        """DOG Framework method - called when receiving opponent's move"""
        action = move.get('action', '')
        
        if action == 'initial_state':
            # Receive initial game state from the starting player
            self.game.receive_initial_state(move)
            self.initialize_game_display()
            self.show_screen("playing")
            self.update_display()
            
            if self.game.local_player.get_is_turn():
                self.show_message("Sua vez! Selecione uma carta e depois um livro para jogar.")
            else:
                self.show_message("Aguardando o oponente...")
                
        elif action == 'play_card':
            card_type = move.get('card_type', '')
            target_data = []
            
            # Convert string values back to integers
            raw_target_data = move.get('target_data', [])
            for item in raw_target_data:
                try:
                    target_data.append(int(item))
                except (ValueError, TypeError):
                    target_data.append(item)
            
            # Apply the card effect
            success = self.game.apply_remote_card_effect(card_type, target_data)
            
            if success:
                self.update_display()
                
                # Check match status
                match_status = move.get('match_status', '')
                if match_status == 'finished':
                    # Game ended
                    winner_id = move.get('player', '')
                    winner_name = self.get_player_name_by_id(winner_id)
                    self.end_game(winner_name)
                else:
                    # Continue game
                    self.game.trocar_turno_jogador()
                    self.update_display()
                    
                    if self.game.local_player.get_is_turn():
                        self.show_message("Sua vez! Selecione uma carta e depois um livro para jogar.")
                    else:
                        self.show_message("Aguardando o oponente...")
            else:
                self.show_message("Erro ao processar jogada do oponente!")
                
        elif action == 'discard_card':
            # Opponent discarded a card
            self.game.trocar_turno_jogador()
            self.update_display()
            
            if self.game.local_player.get_is_turn():
                self.show_message("Sua vez! Selecione uma carta e depois um livro para jogar.")

    def receive_withdrawal_notification(self):
        """DOG Framework method - called when opponent withdraws"""
        self.show_message("O oponente abandonou a partida!")
        self.match_in_progress = False
        self.reset_button.config(state=tk.NORMAL)
        
        # Show game over screen with withdrawal message
        self.result_label.config(text="Partida encerrada - Oponente desistiu")
        self.show_screen("game_over")
    
    def get_player_name_by_id(self, player_id):
        """Get player name by their ID"""
        if self.game.local_player_id == player_id:
            return self.game.local_player.get_name()
        elif self.game.remote_player_id == player_id:
            return self.game.remote_player.get_name()
        else:
            return "Jogador Desconhecido"
    
    def reset_to_initial_state(self):
        """Reset game to initial state"""
        self.game = Game()
        self.selected_card_index = None
        self.selected_books = []
        self.selected_target_type = None
        self.awaiting_input = False
        self.match_in_progress = False
        
        self.clear_board()
        self.show_screen("welcome")
        self.name_entry.delete(0, tk.END)
        self.name_entry.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        
        self.show_message("Jogo resetado para o estado inicial.")
    
    def clear_selections(self):
        # Clear card selection
        if self.selected_card_index is not None:
            self.card_widgets[self.selected_card_index].config(
                highlightbackground="black", highlightthickness=2)
        self.selected_card_index = None
        
        # Clear book selections
        self.clear_book_selections()
    
    def clear_book_selections(self):
        for index, book_type in self.selected_books:
            self.update_book_highlight(index, book_type, False)
        self.selected_books = []
    
    def update_display(self):
        # Update turn label
        if self.game.local_player:
            if self.game.local_player.get_is_turn():
                self.turn_label.config(text=f"Vez de {self.game.local_player.get_name()}")
            else:
                self.turn_label.config(text=f"Vez do {self.game.remote_player.get_name()}")
        
        # Update book colors (in case they changed)
        self.update_book_colors()
    
    def update_book_colors(self):
        # Update your books
        if self.game.local_player:
            your_books = self.game.local_player.get_display().get_display()
            for i, book in enumerate(your_books):
                if i < len(self.your_books):
                    color = book.get_color()
                    self.your_books[i].config(bg=self.colors.get(color, "#BDC3C7"))
        
        # Update opponent books
        if self.game.remote_player:
            opponent_books = self.game.remote_player.get_display().get_display()
            for i, book in enumerate(opponent_books):
                if i < len(self.opponent_books):
                    color = book.get_color()
                    self.opponent_books[i].config(bg=self.colors.get(color, "#BDC3C7"))
        
        # Update master books
        master_books = self.game.main_display.main_display
        for i, book in enumerate(master_books):
            if i < len(self.objective_books):
                color = book.get_color()
                self.objective_books[i].config(bg=self.colors.get(color, "#BDC3C7"))
    
    def show_message(self, message):
        self.message_label.config(text=message)
        print(message)
    
    def end_game(self, winner):
        self.result_label.config(text=f"Vencedor: {winner}")
        self.match_in_progress = False
        self.reset_button.config(state=tk.NORMAL)
        self.show_screen("game_over")
    
    def reset_game(self):
        self.reset_to_initial_state()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    interface = AdasLibraryInterface()
    interface.run()

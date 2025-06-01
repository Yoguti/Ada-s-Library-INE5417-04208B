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
        
        # Enhanced interface attributes
        self.current_card = None
        self.selections = []
        self.selection_mode = None
        self.help_label = None
        self.edge_buttons = []
        self.edge_frame = None
        self.clear_btn = None
        self.apply_btn = None
        
        # DOG Framework attributes
        self.dog_actor = None
        self.player_name = ""
        self.is_connected = False
        self.match_in_progress = False
        
        self.setup_ui()
    
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Ada's Library")
        self.root.geometry("1200x1000")
        self.root.resizable(False, False)
        self.root.configure(bg="#315931")
        
        # Create screens
        self.welcome_screen = tk.Frame(self.root, bg="#315931")
        self.game_screen = tk.Frame(self.root, bg="#315931")
        self.game_over_screen = tk.Frame(self.root, bg="#315931")
        
        self.setup_welcome_screen()
        self.setup_game_screen()
        self.setup_game_over_screen()
        
        self.show_screen("welcome")
    
    def setup_welcome_screen(self):
        # Title
        title_label = tk.Label(self.welcome_screen, text="Ada's Library", 
                              font=("Serif", 180, "bold"), bg="#315931", fg="white")
        title_label.pack(pady=(180, 10))
        
        # Subtitle
        subtitle_label = tk.Label(self.welcome_screen, 
                                 text="Sua estante é seu campo de batalha.", 
                                 font=("Serif", 50), bg="#315931", fg="white")
        subtitle_label.pack(pady=(0, 100))
        
        # Name input
        name_label = tk.Label(self.welcome_screen, text="Qual é o seu nome?", 
                             font=("Helvetica", 34, "bold"), bg="#315931", fg="white")
        name_label.pack(pady=(0, 0))
        
        self.name_entry = tk.Entry(self.welcome_screen, font=("Helvetica", 22), width=30)
        self.name_entry.pack(pady=20)
        self.name_entry.focus_set()
        
        # Connect button
        connect_button = tk.Button(self.welcome_screen, text="Conectar ao Servidor", 
                                  font=("Helvetica", 25, "bold"), bg="#457b9d", fg="white",
                                  padx=20, pady=10, relief=tk.RAISED, bd=5,
                                  command=self.connect_to_server)
        connect_button.pack(pady=10)
        
        # Start button
        self.start_button = tk.Button(self.welcome_screen, text="Iniciar Partida", 
                                    font=("Helvetica", 33, "bold"), bg="#A8DADC", fg="#1D3557",
                                    padx=30, pady=15, relief=tk.RAISED, bd=5,
                                    command=self.start_game, state=tk.DISABLED)
        self.start_button.pack(pady=30)

        self.name_entry.bind("<Return>", lambda event: self.connect_to_server())
    
    def setup_game_screen(self):
        # Message frame
        self.message_frame = tk.Frame(self.game_screen, bg="#315931", pady=10)
        self.message_label = tk.Label(self.message_frame, text="", font=("Helvetica", 30),
                                     bg="#F0FFF0", relief="groove", padx=15, pady=10)
        self.message_label.pack(fill=tk.X)
        self.message_frame.pack(pady=10, fill=tk.X, padx=30)
        
        # Enhanced help text area
        self.help_frame = tk.Frame(self.game_screen, bg="#315931", pady=5)
        self.help_label = tk.Label(self.help_frame, text="Selecione uma carta para começar", 
                                  font=("Helvetica", 16), bg="#E8F4FD", fg="#1D3557", 
                                  relief="groove", padx=10, pady=5, wraplength=800)
        self.help_label.pack(fill=tk.X)
        self.help_frame.pack(pady=5, fill=tk.X, padx=30)
        
        # Turn label
        self.turn_label = tk.Label(self.game_screen, text="", font="Helvetica 24 bold", 
                                  bg="#315931", fg="white")
        self.turn_label.pack(pady=15)
        
        # Game frames
        self.opponent_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        self.objective_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        self.your_books_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        self.cards_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        self.buttons_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        
        # Labels
        tk.Label(self.opponent_frame, text="Livros do Oponente", font="Helvetica 30", 
                bg="#315931", fg="white").pack()
        self.opponent_frame.pack(pady=(0, 10))
        
        tk.Label(self.objective_frame, text="Objetivo", font="Helvetica 30", 
                bg="#315931", fg="white").pack()
        self.objective_frame.pack(pady=(0, 10))
        
        tk.Label(self.your_books_frame, text="Seus Livros", font="Helvetica 30", 
                bg="#315931", fg="white").pack()
        self.your_books_frame.pack(pady=(0, 10))
        
        # Edge selection buttons (hidden by default)
        self.edge_frame = tk.Frame(self.your_books_frame, bg="#315931")
        
        left_edge_btn = tk.Button(self.edge_frame, text="◀ BORDA\nESQUERDA", 
                                 font=("Helvetica", 12, "bold"), bg="#FF6B6B", fg="white",
                                 padx=10, pady=20, command=lambda: self.select_edge(0))
        left_edge_btn.pack(side=tk.LEFT, padx=5)
        
        right_edge_btn = tk.Button(self.edge_frame, text="BORDA ▶\nDIREITA", 
                                  font=("Helvetica", 12, "bold"), bg="#FF6B6B", fg="white",
                                  padx=10, pady=20, command=lambda: self.select_edge(1))
        right_edge_btn.pack(side=tk.RIGHT, padx=5)
        
        self.edge_buttons = [left_edge_btn, right_edge_btn]
        
        tk.Label(self.cards_frame, text="Cartas", font="Helvetica 30", 
                bg="#315931", fg="white").pack()
        self.cards_frame.pack(pady=(0, 10))
        
        self.buttons_frame.pack(pady=30)
        
        # Enhanced buttons
        self.clear_btn = tk.Button(self.buttons_frame, text="Limpar Seleção", 
                                  bg="#FFA500", fg="white", font="Helvetica 20",
                                  padx=15, pady=8, command=self.clear_enhanced_selections)
        self.clear_btn.pack(side=tk.LEFT, padx=10)
        
        self.apply_btn = tk.Button(self.buttons_frame, text="Aplicar Carta", 
                                  bg="#28A745", fg="white", font="Helvetica 20",
                                  padx=15, pady=8, command=self.apply_current_card,
                                  state=tk.DISABLED)
        self.apply_btn.pack(side=tk.LEFT, padx=10)
        
        self.discard_button = tk.Button(self.buttons_frame, text="Descartar", bg="#FF6B6B", fg="white",
                                       font="Helvetica 30", padx=20, pady=10,
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
    
    def setup_game_over_screen(self):
        self.game_over_title = tk.Label(self.game_over_screen, text="Fim de Jogo", 
                                       font=("Helvetica", 48, "bold"), bg="#315931", fg="white")
        self.game_over_title.pack(pady=(180, 30))
        
        self.result_label = tk.Label(self.game_over_screen, text="", 
                                    font=("Helvetica", 34), bg="#315931", fg="white")
        self.result_label.pack(pady=(0, 70))
        
        buttons_frame = tk.Frame(self.game_over_screen, bg="#315931")
        buttons_frame.pack(pady=40)
        
        play_again_button = tk.Button(buttons_frame, text="Jogar Novamente", 
                                     font=("Helvetica", 30, "bold"), bg="#A8DADC", fg="#1D3557",
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
                book_widget = tk.Frame(self.opponent_frame, width=70, height=100, 
                                      bg=self.colors.get(color, "#BDC3C7"),
                                      highlightbackground="black", highlightthickness=3)
                book_widget.pack_propagate(False)
                book_widget.pack(side=tk.LEFT, padx=8)
                book_widget.bind("<Button-1>", self.create_opponent_book_click(i))
                self.opponent_books.append(book_widget)
        
        # Create objective books
        master_books = self.game.main_display.main_display
        for i, book in enumerate(master_books):
            color = book.get_color()
            book_widget = tk.Frame(self.objective_frame, width=85, height=120, 
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
                book_widget = tk.Frame(self.your_books_frame, width=70, height=100, 
                                      bg=self.colors.get(color, "#BDC3C7"),
                                      highlightbackground="black", highlightthickness=3)
                book_widget.pack_propagate(False)
                book_widget.pack(side=tk.LEFT, padx=8)
                book_widget.bind("<Button-1>", self.create_your_book_click(i))
                self.your_books.append(book_widget)
        
        # Create cards
        if self.game.local_player:
            cards = self.game.local_player.get_hand().get_cartas()
            for i, card in enumerate(cards):
                card_widget = tk.Frame(self.cards_frame, width=100, height=140, bg="white",
                                      highlightbackground="black", highlightthickness=3)
                card_widget.pack_propagate(False)
                card_widget.pack(side=tk.LEFT, padx=10)
                
                # Use user-friendly name if available
                display_name = getattr(card, 'user_friendly_name', card.description)
                label = tk.Label(card_widget, text=display_name, bg="white", 
                                wraplength=90, font="Helvetica 20")
                label.pack(pady=(20, 0))
                
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
        
        # Clear enhanced selections
        self.clear_enhanced_selections()
    
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
        """Enhanced card selection with better feedback"""
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        # Clear previous selections
        self.clear_enhanced_selections()
        
        # Get the card
        card = self.game.local_player.get_hand().get_card(index)
        if not card:
            return
        
        # Update UI
        self.current_card = card
        self.selected_card_index = index
        
        # Highlight selected card
        for i, widget in enumerate(self.card_widgets):
            if i == index:
                widget.config(highlightbackground="#FFD700", highlightthickness=4)
            else:
                widget.config(highlightbackground="black", highlightthickness=3)
        
        # Show help text
        help_text = getattr(card, 'get_help_text', lambda: "Carta selecionada")()
        user_name = getattr(card, 'user_friendly_name', card.description)
        self.help_label.config(text=f"🎯 {user_name}: {help_text}")
        
        # Set up selection mode
        required = getattr(card, 'get_required_selections', lambda: {"count": 1, "type": "books"})()
        self.selection_mode = required["type"]
        
        # Show edge buttons if needed
        if "edge" in self.selection_mode:
            self.edge_frame.pack(pady=10)
        else:
            self.edge_frame.pack_forget()
        
        # Special handling for cards that need no selections
        if required["count"] == 0:
            self.apply_btn.config(state=tk.NORMAL)
            self.help_label.config(text=f"✅ {user_name}: Pronto para aplicar!")
    
    def click_your_book(self, index):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta primeiro!")
            return
        
        self.handle_enhanced_book_selection(index, "your")
    
    def click_opponent_book(self, index):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta primeiro!")
            return
        
        self.handle_enhanced_book_selection(index, "opponent")
    
    def click_objective_book(self, index):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta primeiro!")
            return
        
        self.handle_enhanced_book_selection(index, "master")
    
    def handle_enhanced_book_selection(self, index, book_type):
        """Enhanced book selection with validation"""
        if not self.current_card:
            self.show_message("Selecione uma carta primeiro!")
            return
        
        # Check if this selection is valid for current card
        target_type = getattr(self.current_card, 'get_tipo_alvo', lambda: "personal")()
        
        if target_type == "personal" and book_type != "your":
            self.show_message("Esta carta só funciona nos seus livros!")
            return
        elif target_type == "opponent" and book_type not in ["your", "opponent"]:
            self.show_message("Esta carta precisa de livros seus e do oponente!")
            return
        elif target_type == "master" and book_type != "master":
            self.show_message("Esta carta só funciona nos livros mestres!")
            return
        
        # Add selection
        self.selections.append((index, book_type))
        
        # Update visual feedback
        self.update_enhanced_book_highlight(index, book_type, True)
        
        # Check if we have enough selections
        required = getattr(self.current_card, 'get_required_selections', lambda: {"count": 1})()
        
        if len(self.selections) >= required["count"]:
            self.validate_and_enable_apply()
        else:
            remaining = required["count"] - len(self.selections)
            self.help_label.config(text=f"📍 Selecione mais {remaining} item(s)")
    
    def select_edge(self, edge_value):
        """Handle edge selection for MoveToEdge card"""
        if not self.current_card or not isinstance(self.current_card, MoveToEdge):
            return
        
        self.selections.append((edge_value, "edge"))
        
        # Highlight selected edge button
        for i, btn in enumerate(self.edge_buttons):
            if i == edge_value:
                btn.config(bg="#28A745")
            else:
                btn.config(bg="#FF6B6B")
        
        self.validate_and_enable_apply()
    
    def validate_and_enable_apply(self):
        """Validate current selections and enable apply button if valid"""
        if not self.current_card:
            return
        
        # Extract just the indices for validation
        if self.selection_mode == "book_and_edge":
            if len(self.selections) >= 2:
                book_selections = [s for s in self.selections if s[1] != "edge"]
                edge_selections = [s for s in self.selections if s[1] == "edge"]
                
                if book_selections and edge_selections:
                    indices = [book_selections[0][0], edge_selections[0][0]]
                else:
                    return
            else:
                return
        else:
            indices = [s[0] for s in self.selections]
        
        # Get display length for validation
        target_type = getattr(self.current_card, 'get_tipo_alvo', lambda: "personal")()
        if target_type == "personal":
            display_length = len(self.game.local_player.get_display().get_display())
        elif target_type == "master":
            display_length = len(self.game.main_display.main_display)
        else:
            display_length = 10  # Default
        
        # Validate if card has validation method
        if hasattr(self.current_card, 'validate_selection'):
            is_valid, message = self.current_card.validate_selection(indices, display_length)
            
            if is_valid:
                self.help_label.config(text=f"✅ {message}")
                self.apply_btn.config(state=tk.NORMAL)
            else:
                self.help_label.config(text=f"❌ {message}")
                self.apply_btn.config(state=tk.DISABLED)
        else:
            # Fallback for cards without validation
            self.apply_btn.config(state=tk.NORMAL)
    
    def apply_current_card(self):
        """Apply the currently selected card with current selections"""
        if not self.current_card or not self.game.verificar_turno_do_jogador():
            return
        
        # Prepare target data based on card type
        target_data = []
        
        if isinstance(self.current_card, SwapWithSpaces):
            target_data = [self.selections[0][0], self.selections[1][0]]
        
        elif isinstance(self.current_card, MoveBookSpaces):
            target_data = [self.selections[0][0], self.selections[1][0]]
        
        elif isinstance(self.current_card, MoveToEdge):
            book_selection = next((s for s in self.selections if s[1] != "edge"), None)
            edge_selection = next((s for s in self.selections if s[1] == "edge"), None)
            if book_selection and edge_selection:
                target_data = [book_selection[0], edge_selection[0]]
        
        elif isinstance(self.current_card, SwapEdges):
            target_data = []
        
        elif isinstance(self.current_card, SwapWithOpponent):
            your_book = next((s for s in self.selections if s[1] == "your"), None)
            opponent_book = next((s for s in self.selections if s[1] == "opponent"), None)
            if your_book and opponent_book:
                target_data = [your_book[0], opponent_book[0]]
        
        elif isinstance(self.current_card, MoveMasterBook):
            target_data = [self.selections[0][0], self.selections[1][0]]
        
        # Apply the card
        success = self.game.apply_card_effect(self.selected_card_index, target_data)
        
        if success:
            self.show_message("✅ Carta aplicada com sucesso!")
            
            # Check for victory
            game_over = self.game.avaliar_fim_da_partida()
            
            if game_over:
                self.end_game(self.game.local_player.get_name())
                return
            
            # Send move through DOG if available
            if hasattr(self, 'dog_actor') and self.dog_actor:
                move_data = {
                    'action': 'play_card',
                    'card_type': self.current_card.description,
                    'target_data': target_data,
                    'match_status': 'finished' if game_over else 'next'
                }
                self.dog_actor.send_move(move_data)
            
            # Switch turns and update display
            self.game.trocar_turno_jogador()
            self.clear_enhanced_selections()
            self.update_display()
            self.show_message("Aguardando jogada do oponente...")
            
        else:
            self.show_message("❌ Não foi possível aplicar a carta!")
    
    def clear_enhanced_selections(self):
        """Clear all current selections and reset UI"""
        # Clear book highlights
        for index, book_type in self.selections:
            if book_type != "edge":
                self.update_enhanced_book_highlight(index, book_type, False)
        
        # Reset edge buttons
        for btn in self.edge_buttons:
            btn.config(bg="#FF6B6B")
        
        # Clear selections
        self.selections = []
        self.current_card = None
        
        # Reset UI elements
        self.apply_btn.config(state=tk.DISABLED)
        self.edge_frame.pack_forget()
        
        # Clear card highlights
        for widget in self.card_widgets:
            widget.config(highlightbackground="black", highlightthickness=3)
        
        self.selected_card_index = None
        self.help_label.config(text="Selecione uma carta para começar")
    
    def update_enhanced_book_highlight(self, index, book_type, selected):
        """Update book highlighting with better visual feedback"""
        if selected:
            color = "#00FF00"  # Bright green for selected
            thickness = 5
        else:
            color = "black"
            thickness = 3
        
        try:
            if book_type == "your" and index < len(self.your_books):
                self.your_books[index].config(highlightbackground=color, highlightthickness=thickness)
            elif book_type == "opponent" and index < len(self.opponent_books):
                self.opponent_books[index].config(highlightbackground=color, highlightthickness=thickness)
            elif book_type == "master" and index < len(self.objective_books):
                self.objective_books[index].config(highlightbackground=color, highlightthickness=thickness)
        except (IndexError, AttributeError):
            pass  # Ignore errors if widgets don't exist yet
    
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
            self.clear_enhanced_selections()
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
        
        self.show_message("Jogo resetado para o estado inicial.")
    
    def clear_selections(self):
        # Clear card selection
        if self.selected_card_index is not None:
            self.card_widgets[self.selected_card_index].config(
                highlightbackground="black", highlightthickness=3)
        self.selected_card_index = None
        
        # Clear book selections
        self.clear_book_selections()
    
    def clear_book_selections(self):
        for index, book_type in self.selected_books:
            self.update_book_highlight(index, book_type, False)
        self.selected_books = []
    
    def update_book_highlight(self, index, book_type, selected):
        color = "white" if selected else "black"
        thickness = 4 if selected else 3
        
        if book_type == "your" and index < len(self.your_books):
            self.your_books[index].config(highlightbackground=color, highlightthickness=thickness)
        elif book_type == "opponent" and index < len(self.opponent_books):
            self.opponent_books[index].config(highlightbackground=color, highlightthickness=thickness)
        elif book_type == "master" and index < len(self.objective_books):
            self.objective_books[index].config(highlightbackground=color, highlightthickness=thickness)
    
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
        self.show_screen("game_over")
    
    def reset_game(self):
        self.reset_to_initial_state()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    interface = AdasLibraryInterface()
    interface.run()

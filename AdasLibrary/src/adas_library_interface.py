import tkinter as tk
from tkinter import messagebox, simpledialog
from game import Game
from action_card import *
from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface
from dog.start_status import StartStatus
import threading
import time

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
        self.searching_for_players = False
        self.connection_retry_count = 0
        self.max_connection_retries = 5
        
        # Threading control
        self.search_thread = None
        self.stop_search = False
        
        self.setup_ui()
    
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Ada's Library")
        self.root.geometry("1200x1000")
        self.root.resizable(False, False)
        self.root.configure(bg="#315931")
        
        # Create screens (remove waiting_screen)
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
        
        # Single "Iniciar Partida" button
        self.start_game_button = tk.Button(self.welcome_screen, text="Iniciar Partida", 
                                          font=("Helvetica", 33, "bold"), bg="#A8DADC", fg="#1D3557",
                                          padx=30, pady=15, relief=tk.RAISED, bd=5,
                                          command=self.iniciar_partida)
        self.start_game_button.pack(pady=20)
        
        # Status messages
        self.connection_status = tk.Label(self.welcome_screen, text="", 
                                         font=("Helvetica", 18), bg="#315931", fg="yellow")
        self.connection_status.pack(pady=10)
        
        self.search_status = tk.Label(self.welcome_screen, text="", 
                                     font=("Helvetica", 18), bg="#315931", fg="cyan")
        self.search_status.pack(pady=5)
        
        # Cancel button (initially hidden)
        self.cancel_button = tk.Button(self.welcome_screen, text="Cancelar", 
                                      font=("Helvetica", 20, "bold"), bg="#E63946", fg="white",
                                      padx=20, pady=10, relief=tk.RAISED, bd=5,
                                      command=self.cancel_game_initiation)
        
        self.name_entry.bind("<Return>", lambda event: self.iniciar_partida())
    
    def setup_game_screen(self):
        # Message frame
        self.message_frame = tk.Frame(self.game_screen, bg="#315931", pady=10)
        self.message_label = tk.Label(self.message_frame, text="", font=("Helvetica", 30),
                                     bg="#F0FFF0", relief="groove", padx=15, pady=10)
        self.message_label.pack(fill=tk.X)
        self.message_frame.pack(pady=10, fill=tk.X, padx=30)
        
        # Turn label
        self.turn_label = tk.Label(self.game_screen, text="", font="Helvetica 24 bold", 
                                  bg="#315931", fg="white")
        self.turn_label.pack(pady=15)
        
        # Game frames
        self.opponent_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        self.objective_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        self.your_books_frame = tk.Frame(self.game_screen, bg="#315931", pady=15)
        self.cards_container = tk.Frame(self.game_screen, bg="#315931", pady=15)
        
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
        
        # Cards section with discard button on the right
        cards_label = tk.Label(self.cards_container, text="Cartas", font="Helvetica 30", 
                              bg="#315931", fg="white")
        cards_label.pack()
        
        # Horizontal container for cards and discard button
        self.cards_and_discard_frame = tk.Frame(self.cards_container, bg="#315931")
        self.cards_and_discard_frame.pack(pady=(0, 10))
        
        # Cards frame (left side)
        self.cards_frame = tk.Frame(self.cards_and_discard_frame, bg="#315931")
        self.cards_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        # Discard button (right side)
        self.discard_button = tk.Button(self.cards_and_discard_frame, text="Descartar", 
                                       bg="#FF6B6B", fg="white", font="Helvetica 30", 
                                       padx=20, pady=10, command=self.discard_card)
        self.discard_button.pack(side=tk.RIGHT, padx=20)
        
        self.cards_container.pack(pady=(0, 10))
        
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
    
    def iniciar_partida(self):
        """Streamlined game initiation: connect and search for players"""
        player_name = self.name_entry.get().strip()
        if not player_name:
            self.connection_status.config(text="Por favor, digite seu nome!", fg="red")
            return
        
        if self.searching_for_players:
            self.connection_status.config(text="Já procurando por partida!", fg="yellow")
            return
        
        self.player_name = player_name
        self.connection_retry_count = 0
        self.searching_for_players = True
        self.stop_search = False
        
        # Disable start button and show cancel button
        self.start_game_button.config(state=tk.DISABLED)
        self.name_entry.config(state=tk.DISABLED)
        
        # Start connection attempt with retry loop
        self.attempt_connection()
    
    def attempt_connection(self):
        """Attempt to connect to server with retry logic"""
        self.connection_status.config(text="Tentando conectar ao servidor...", fg="yellow")
        
        # Initialize DOG Actor
        self.dog_actor = DogActor()
        connection_result = self.dog_actor.initialize(self.player_name, self)
        
        if "Conectado" in connection_result:
            self.is_connected = True
            self.connection_status.config(text="✓ Conectado ao servidor com sucesso!", fg="green")
            self.game.set_dog_interface(self.dog_actor)
            
            # Start player search after successful connection
            self.root.after(1000, self.start_player_search)
        else:
            self.connection_retry_count += 1
            if self.connection_retry_count < self.max_connection_retries and not self.stop_search:
                self.connection_status.config(
                    text=f"Falha na conexão. Tentativa {self.connection_retry_count}/{self.max_connection_retries}. Tentando novamente...", 
                    fg="orange"
                )
                # Retry after 2 seconds
                self.root.after(2000, self.attempt_connection)
            else:
                self.connection_status.config(text="Falha ao conectar após várias tentativas.", fg="red")
                self.cancel_game_initiation()
    
    def start_player_search(self):
        """Start searching for other players"""
        if not self.is_connected or self.stop_search:
            return
        
        self.search_status.config(text="Procurando por outros jogadores...", fg="cyan")
        
        # Start the search thread
        self.search_thread = threading.Thread(target=self.player_search_loop, daemon=True)
        self.search_thread.start()
    
    def player_search_loop(self):
        """Continuous loop to search for players every 5 seconds"""
        while not self.stop_search and self.is_connected:
            try:
                # Request match using DOG's matchmaking
                start_status = self.dog_actor.start_match(2)  # 2 players
                
                if start_status.code == '2':  # Match started immediately
                    self.root.after(0, lambda: self.handle_match_found(start_status))
                    break
                elif start_status.code == '1':  # Waiting for more players
                    # Continue searching - the polling will call receive_start() when found
                    pass
                else:  # Error
                    self.root.after(0, lambda: self.search_status.config(
                        text="Erro na busca por jogadores. Tentando novamente...", fg="orange"))
                
                # Wait 5 seconds before next attempt
                for i in range(50):  # 50 * 0.1 = 5 seconds, but check stop_search frequently
                    if self.stop_search:
                        break
                    time.sleep(0.1)
                    
            except Exception as e:
                print(f"Erro na busca por jogadores: {e}")
                if not self.stop_search:
                    self.root.after(0, lambda: self.search_status.config(
                        text="Erro na busca. Tentando novamente...", fg="orange"))
                    time.sleep(5)
    
    def handle_match_found(self, start_status):
        """Handle when a match is found"""
        self.search_status.config(text="✓ Partida encontrada! Iniciando jogo...", fg="green")
        self.searching_for_players = False
        self.stop_search = True
        
        self.handle_match_start(start_status)
    
    def cancel_game_initiation(self):
        """Cancel the game initiation process"""
        self.stop_search = True
        self.searching_for_players = False
        self.is_connected = False
        
        # Reset UI
        self.start_game_button.config(state=tk.NORMAL)
        self.name_entry.config(state=tk.NORMAL)
        
        # Clear status messages
        self.connection_status.config(text="")
        self.search_status.config(text="")
        
        # Close DOG connection if exists
        if self.dog_actor:
            try:
                # DOG framework cleanup if needed
                pass
            except:
                pass
            self.dog_actor = None
    
    def handle_match_start(self, start_status):
        """Handle when a match actually starts"""
        print(f"handle_match_start called with {len(start_status.players)} players")
        
        if self.match_in_progress:
            print("Já existe uma partida em andamento!")
            return
        
        if len(start_status.players) < 2:
            print("Número insuficiente de jogadores para iniciar partida!")
            self.search_status.config(text="Número insuficiente de jogadores!")
            self.cancel_game_initiation()
            return
        
        self.match_in_progress = True
        self.searching_for_players = False
        
        success = self.game.initialize_players_with_dog(start_status)
        
        if success:
            print("Jogo inicializado com sucesso")
            self.initialize_game_display()
            self.show_screen("playing")
            self.update_display()
            
            if self.game.local_player.get_is_turn():
                self.send_initial_game_state()
                self.show_message("Sua vez! Selecione uma carta e depois um livro para jogar.")
            else:
                self.show_message("Aguardando o oponente...")
        else:
            print("Erro ao inicializar o jogo!")
            self.show_message("Erro ao inicializar o jogo!")
            self.match_in_progress = False
            self.cancel_game_initiation()
    
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
    
    def handle_swap_with_spaces(self, index, book_type):
        """Handle swap with spaces card - allows minimum spaces between books"""
        if len(self.selected_books) == 0:
            self.selected_books.append((index, book_type))
            self.update_book_highlight(index, book_type, True)
            self.show_message("Selecione o segundo livro para trocar.")
        elif len(self.selected_books) == 1:
            self.selected_books.append((index, book_type))
            self.update_book_highlight(index, book_type, True)
            
            # Ask for minimum spaces required
            min_spaces = simpledialog.askinteger("Espaços Mínimos", 
                                                "Quantos espaços mínimos devem haver entre os livros?",
                                                minvalue=0, maxvalue=8)
            if min_spaces is not None:
                target_data = [self.selected_books[0][0], self.selected_books[1][0], min_spaces]
                self.apply_card_with_data(target_data)
            else:
                self.clear_selections()
    
    def handle_swap_with_opponent(self, index, book_type):
        """Handle opponent swap - only allows directly opposite positions"""
        if book_type == "your":
            # The opponent book must be at the same index (directly opposite)
            opponent_index = index  # Same position = directly opposite
            target_data = [index, opponent_index]
            self.apply_card_with_data(target_data)
    
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
                
                label = tk.Label(card_widget, text=card.description, bg="white", 
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
                highlightbackground="black", highlightthickness=3)
        
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
        
        # All new cards have simple, hardcoded effects - just apply with the book index
        if isinstance(card, (ChangeBookColorRandom, MoveBookOneRight, ChangeBookColorRandomly, ChangeParityBooksColor)):
            target_data = [index]
            self.apply_card_with_data(target_data)
        elif isinstance(card, SwapWithOpponent):
            # Opponent swap still works the same way
            if book_type == "your":
                opponent_index = index  # Same position = directly opposite
                target_data = [index, opponent_index]
                self.apply_card_with_data(target_data)
        elif isinstance(card, MoveMasterBookToSequenceSide):
            # Master book movement is now automatic
            target_data = [index]
            self.apply_card_with_data(target_data)
    
    def apply_card_with_data(self, target_data):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        card = self.game.local_player.get_hand().get_card(self.selected_card_index)
        if not card:
            return
        
        success = self.game.apply_card_effect(self.selected_card_index, target_data)
        
        if success:
            # Visual feedback: highlight the used card
            used_widget = self.card_widgets[self.selected_card_index]
            used_widget.config(bg="lightgreen", highlightbackground="green")
            self.root.update()
            
            self.show_message("Carta aplicada com sucesso! Aguarde...")
            
            # Wait a moment to show the card was used
            self.root.after(800, lambda: self._complete_card_play(card, target_data))
        else:
            self.show_message("Não foi possível aplicar a carta!")
            self.clear_selections()

    def _complete_card_play(self, card, target_data):
        """Complete the card play action after visual delay"""
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
        
        # Update card display to show new card
        self._update_card_display()
        
        self.show_message("Nova carta recebida! Aguardando jogada do oponente...")
    
    def update_book_highlight(self, index, book_type, selected):
        color = "white" if selected else "black"
        thickness = 4 if selected else 3
        
        if book_type == "your" and index < len(self.your_books):
            self.your_books[index].config(highlightbackground=color, highlightthickness=thickness)
        elif book_type == "opponent" and index < len(self.opponent_books):
            self.opponent_books[index].config(highlightbackground=color, highlightthickness=thickness)
        elif book_type == "master" and index < len(self.objective_books):
            self.objective_books[index].config(highlightbackground=color, highlightthickness=thickness)
    
    def discard_card(self):
        """Discard selected card with visual feedback"""
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta para descartar!")
            return
        
        # Visual feedback: show card being discarded
        discarded_widget = self.card_widgets[self.selected_card_index]
        discarded_widget.config(bg="#FF6B6B", highlightbackground="red", highlightthickness=4)
        self.root.update()
        
        self.show_message("Carta descartada! Aguarde...")
        
        # Wait a moment to show the discard
        self.root.after(1000, self._complete_discard)

    def _complete_discard(self):
        """Complete the discard action after visual delay"""
        # Add card to discard pile before removing from hand
        card = self.game.local_player.get_hand().get_card(self.selected_card_index)
        if card:
            self.game.action_card_deck.add_to_discard(card)
        
        # Remove card and draw new one
        removed_card = self.game.remover_carta_selecionada_da_mao(self.selected_card_index)
        
        if removed_card:
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
        
            # Recreate the card widgets to show the new card
            self._update_card_display()
        
            self.show_message("Nova carta recebida! Aguardando jogada do oponente...")

    def _update_card_display(self):
        """Update only the card display area"""
        # Clear existing card widgets
        for card in self.card_widgets:
            card.destroy()
        self.card_widgets = []
        
        # Recreate cards
        if self.game.local_player:
            cards = self.game.local_player.get_hand().get_cartas()
            for i, card in enumerate(cards):
                card_widget = tk.Frame(self.cards_frame, width=100, height=140, bg="white",
                                      highlightbackground="black", highlightthickness=3)
                card_widget.pack_propagate(False)
                card_widget.pack(side=tk.LEFT, padx=10)
            
                label = tk.Label(card_widget, text=card.description, bg="white", 
                                wraplength=90, font="Helvetica 20")
                label.pack(pady=(20, 0))
            
                card_widget.bind("<Button-1>", self.create_card_click(i))
                self.card_widgets.append(card_widget)
    
    def receive_start(self, start_status):
        """DOG Framework method - called when match starts remotely"""
        print(f"receive_start called with code: {start_status.code}")
        
        # Only accept match if we're actively searching for one
        if start_status.code == '2':  # Match started
            if self.searching_for_players:
                # We were actively searching for a match
                self.root.after(0, lambda: self.handle_match_found(start_status))
            else:
                # We weren't looking for a match, so decline
                print("Outro jogador iniciou uma partida, mas você não está procurando.")
                return
        else:
            print(f"receive_start chamado com código inesperado: {start_status.code}")

    def receive_move(self, move):
        """DOG Framework method - called when receiving opponent's move"""
        if not self.match_in_progress:
            print("Recebido movimento, mas não há partida em andamento.")
            return
            
        result = self.game.receive_move(move)
    
        if result == 'game_started':
            self.initialize_game_display()
            self.show_screen("playing")
            self.update_display()
        
            if self.game.local_player.get_is_turn():
                self.show_message("Sua vez! Selecione uma carta e depois um livro para jogar.")
            else:
                self.show_message("Aguardando o oponente...")
        elif result == 'game_over':
            winner_id = move.get('player', '')
            winner_name = self.get_player_name_by_id(winner_id)
            self.end_game(winner_name)
        elif result == 'continue':
            self.update_display()
        
            if self.game.local_player.get_is_turn():
                self.show_message("Sua vez! Selecione uma carta e depois um livro para jogar.")
            else:
                self.show_message("Aguardando o oponente...")

    def receive_withdrawal_notification(self):
        """DOG Framework method - called when opponent withdraws"""
        if self.match_in_progress:
            self.show_message("O oponente abandonou a partida!")
            self.match_in_progress = False
            self.searching_for_players = False
            self.stop_search = True
            self.game.waiting_for_match = False
        
            # Show game over screen with withdrawal message
            self.result_label.config(text="Partida encerrada - Oponente desistiu")
            self.show_screen("game_over")
        elif self.searching_for_players:
            # If we were searching for a match and the other player disconnected
            self.search_status.config(text="Um jogador desconectou. Continuando busca...")
        else:
            print("Notificação de abandono recebida, mas não há partida em andamento")
    
    def get_player_name_by_id(self, player_id):
        """Get player name by their ID"""
        if self.game.local_player_id == player_id:
            return self.game.local_player.get_name()
        elif self.game.remote_player_id == player_id:
            return self.game.remote_player.get_name()
        else:
            return "Jogador Desconhecido"
    
    def clear_selections(self):
        # Clear card selection
        if self.selected_card_index is not None and self.selected_card_index < len(self.card_widgets):
            self.card_widgets[self.selected_card_index].config(
                highlightbackground="black", highlightthickness=3)
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
        self.searching_for_players = False
        self.stop_search = True
        self.game.waiting_for_match = False
        self.show_screen("game_over")
    
    def reset_game(self):
        # Stop any ongoing searches
        self.stop_search = True
        self.searching_for_players = False
        
        # Reset game state
        self.game = Game()
        self.selected_card_index = None
        self.selected_books = []
        self.selected_target_type = None
        self.awaiting_input = False
        self.match_in_progress = False
        self.is_connected = False
        self.connection_retry_count = 0
        
        # Reset UI
        self.clear_board()
        self.show_screen("welcome")
        self.name_entry.delete(0, tk.END)
        self.name_entry.config(state=tk.NORMAL)
        self.start_game_button.config(state=tk.NORMAL)

        
        # Clear status messages
        self.connection_status.config(text="")
        self.search_status.config(text="")
        
        # Close DOG connection
        if self.dog_actor:
            self.dog_actor = None
        
        self.show_message("Jogo resetado para o estado inicial.")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    interface = AdasLibraryInterface()
    interface.run()

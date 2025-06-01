import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from game import Game
from action_card import * # Assuming all necessary card classes are imported
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
        
        self.dog_actor = None
        self.player_name = ""
        self.is_connected = False
        self.match_in_progress = False
        
        self.setup_ui()
    
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Ada's Library")
        self.root.minsize(800, 700) 
        self.root.resizable(True, True) 
        self.root.configure(bg="#315931")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.welcome_screen = tk.Frame(self.root, bg="#315931")
        self.game_screen = tk.Frame(self.root, bg="#315931")
        self.game_over_screen = tk.Frame(self.root, bg="#315931")

        for screen in [self.welcome_screen, self.game_screen, self.game_over_screen]:
            screen.grid(row=0, column=0, sticky="nsew")

        self.setup_welcome_screen()
        self.setup_game_screen()
        self.setup_game_over_screen()
        
        self.show_screen("welcome")
    
    def _create_horizontal_scrollable_content_frame(self, parent_container, canvas_height=100):
        scroll_area_container = tk.Frame(parent_container, bg=parent_container.cget('bg'), height=canvas_height)
        scroll_area_container.pack(fill="x", expand=True, pady=5)

        canvas = tk.Canvas(scroll_area_container, bg=parent_container.cget('bg'), highlightthickness=0, height=canvas_height)
        scrollbar = ttk.Scrollbar(scroll_area_container, orient="horizontal", command=canvas.xview)
        
        content_frame = tk.Frame(canvas, bg=parent_container.cget('bg'))
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        
        canvas.pack(side="top", fill="x", expand=True)
        scrollbar.pack(side="bottom", fill="x")
        
        return content_frame

    def setup_welcome_screen(self):
        self.welcome_screen.grid_rowconfigure(0, weight=1) 
        self.welcome_screen.grid_rowconfigure(6, weight=1) 
        self.welcome_screen.grid_columnconfigure(0, weight=1)

        title_label = tk.Label(self.welcome_screen, text="Ada's Library", 
                              font=("Serif", 72, "bold"), bg="#315931", fg="white")
        title_label.grid(row=1, column=0, pady=(30, 5))
        
        subtitle_label = tk.Label(self.welcome_screen, 
                                 text="Sua estante é seu campo de batalha.", 
                                 font=("Serif", 28), bg="#315931", fg="white")
        subtitle_label.grid(row=2, column=0, pady=(0, 50))
        
        name_label = tk.Label(self.welcome_screen, text="Qual é o seu nome?", 
                             font=("Helvetica", 20, "bold"), bg="#315931", fg="white")
        name_label.grid(row=3, column=0, pady=(0, 5))
        
        self.name_entry = tk.Entry(self.welcome_screen, font=("Helvetica", 16), width=30)
        self.name_entry.grid(row=4, column=0, pady=10)
        self.name_entry.focus_set()
        
        button_frame_welcome = tk.Frame(self.welcome_screen, bg="#315931")
        button_frame_welcome.grid(row=5, column=0, pady=20)

        connect_button = tk.Button(button_frame_welcome, text="Conectar ao Servidor", 
                                  font=("Helvetica", 16, "bold"), bg="#457b9d", fg="white",
                                  padx=15, pady=8, relief=tk.RAISED, bd=3,
                                  command=self.connect_to_server)
        connect_button.pack(pady=10)
        
        self.start_button = tk.Button(button_frame_welcome, text="Iniciar Partida", 
                                    font=("Helvetica", 18, "bold"), bg="#A8DADC", fg="#1D3557",
                                    padx=20, pady=10, relief=tk.RAISED, bd=3,
                                    command=self.start_game, state=tk.DISABLED)
        self.start_button.pack(pady=10)
        
        self.name_entry.bind("<Return>", lambda event: self.connect_to_server())
    
    def setup_game_screen(self):
        self.game_screen.grid_rowconfigure(0, weight=0)
        self.game_screen.grid_rowconfigure(1, weight=0)
        self.game_screen.grid_rowconfigure(2, weight=0)
        self.game_screen.grid_rowconfigure(3, weight=1)
        self.game_screen.grid_rowconfigure(4, weight=0)
        self.game_screen.grid_rowconfigure(5, weight=1)
        self.game_screen.grid_rowconfigure(6, weight=0)
        self.game_screen.grid_rowconfigure(7, weight=1)
        self.game_screen.grid_rowconfigure(8, weight=0)
        self.game_screen.grid_rowconfigure(9, weight=1)
        self.game_screen.grid_rowconfigure(10, weight=0)
        self.game_screen.grid_columnconfigure(0, weight=1)

        self.message_frame = tk.Frame(self.game_screen, bg="#315931")
        self.message_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,5))
        self.message_label = tk.Label(self.message_frame, text="", font=("Helvetica", 16),
                                     bg="#F0FFF0", relief="groove", padx=10, pady=5)
        self.message_label.pack(fill=tk.X, expand=True)
        
        self.turn_label = tk.Label(self.game_screen, text="", font="Helvetica 16 bold", 
                                  bg="#315931", fg="white")
        self.turn_label.grid(row=1, column=0, pady=5)
        
        font_section_label = "Helvetica 18"
        book_height_px = 90 
        book_canvas_height = book_height_px + 25 
        card_height_px = 130 
        card_canvas_height = card_height_px + 25

        tk.Label(self.game_screen, text="Livros do Oponente", font=font_section_label, 
                bg="#315931", fg="white").grid(row=2, column=0, sticky="w", padx=10)
        self.opponent_frame_container = tk.Frame(self.game_screen, bg="#315931")
        self.opponent_frame_container.grid(row=3, column=0, sticky="nsew", padx=10)
        self.opponent_frame = self._create_horizontal_scrollable_content_frame(self.opponent_frame_container, book_canvas_height)

        tk.Label(self.game_screen, text="Objetivo", font=font_section_label, 
                bg="#315931", fg="white").grid(row=4, column=0, sticky="w", padx=10)
        self.objective_frame_container = tk.Frame(self.game_screen, bg="#315931")
        self.objective_frame_container.grid(row=5, column=0, sticky="nsew", padx=10)
        self.objective_frame = self._create_horizontal_scrollable_content_frame(self.objective_frame_container, book_canvas_height + 20)

        tk.Label(self.game_screen, text="Seus Livros", font=font_section_label, 
                bg="#315931", fg="white").grid(row=6, column=0, sticky="w", padx=10)
        self.your_books_frame_container = tk.Frame(self.game_screen, bg="#315931")
        self.your_books_frame_container.grid(row=7, column=0, sticky="nsew", padx=10)
        self.your_books_frame = self._create_horizontal_scrollable_content_frame(self.your_books_frame_container, book_canvas_height)
        
        tk.Label(self.game_screen, text="Cartas", font=font_section_label, 
                bg="#315931", fg="white").grid(row=8, column=0, sticky="w", padx=10)
        self.cards_frame_container = tk.Frame(self.game_screen, bg="#315931")
        self.cards_frame_container.grid(row=9, column=0, sticky="nsew", padx=10)
        self.cards_frame = self._create_horizontal_scrollable_content_frame(self.cards_frame_container, card_canvas_height)
        
        self.buttons_frame = tk.Frame(self.game_screen, bg="#315931")
        self.buttons_frame.grid(row=10, column=0, pady=10)
        
        self.discard_button = tk.Button(self.buttons_frame, text="Descartar", bg="#FF6B6B", fg="white",
                                       font="Helvetica 16 bold", padx=15, pady=8,
                                       command=self.discard_card)
        self.discard_button.pack(side=tk.LEFT, padx=10)
        
        self.colors = {
            "vermelho": "#E63946", "azul_claro": "#A8DADC", "cinza": "#6D6875",
            "marrom": "#8B4513", "amarelo": "#F1C40F", "azul_escuro": "#1D3557"
        }
        
        self.opponent_books = []
        self.objective_books = []
        self.your_books = []
        self.card_widgets = []

    def setup_game_over_screen(self):
        self.game_over_screen.grid_rowconfigure(0, weight=1)
        self.game_over_screen.grid_rowconfigure(4, weight=1) # Adjusted row index for spacer
        self.game_over_screen.grid_columnconfigure(0, weight=1)

        self.game_over_title = tk.Label(self.game_over_screen, text="Fim de Jogo", 
                                       font=("Helvetica", 40, "bold"), bg="#315931", fg="white")
        self.game_over_title.grid(row=1, column=0, pady=(50, 20))
        
        self.result_label = tk.Label(self.game_over_screen, text="", 
                                    font=("Helvetica", 22), bg="#315931", fg="white")
        self.result_label.grid(row=2, column=0, pady=(0, 40))
        
        buttons_frame_game_over = tk.Frame(self.game_over_screen, bg="#315931")
        buttons_frame_game_over.grid(row=3, column=0, pady=20) # Removed sticky, let grid center it

        self.play_again_button = tk.Button(buttons_frame_game_over, text="Jogar Novamente", 
                                     font=("Helvetica", 18, "bold"), bg="#A8DADC", fg="#1D3557",
                                     padx=20, pady=10, relief=tk.RAISED, bd=3,
                                     command=self.reset_game)
        self.play_again_button.pack(pady=20)
        self.play_again_button.config(state=tk.DISABLED)

    def show_screen(self, screen_name):
        self.welcome_screen.grid_remove()
        self.game_screen.grid_remove()
        self.game_over_screen.grid_remove()
        
        if screen_name == "welcome":
            self.welcome_screen.grid()
        elif screen_name == "playing":
            self.game_screen.grid()
        elif screen_name == "game_over":
            self.game_over_screen.grid()
    
    def start_game(self):
        if not self.is_connected:
            self.show_message("Você precisa estar conectado para iniciar uma partida!")
            return
        
        if self.match_in_progress:
            self.show_message("Já existe uma partida em andamento!")
            return
        
        # Assuming Ada's Library is for 2 players as per original code
        start_status = self.dog_actor.start_match(2) 
        
        # Interpreting StartStatus codes based on typical DOG framework patterns
        if start_status.get_code() == StartStatus.CODE_OK: # Or specific success code from your DOG version
             self.show_message("Pedido de partida enviado. Aguardando início...")
             # The actual match start and UI transition to game screen is typically
             # handled by the receive_start callback from the server.
        elif start_status.get_code() == StartStatus.CODE_PLAYER_ALREADY_IN_MATCH:
            self.show_message("Você já está em uma partida ou aguardando uma.")
        elif start_status.get_code() == StartStatus.CODE_NOT_ENOUGH_PLAYERS_TO_START: # Example code
            self.show_message("Aguardando jogadores suficientes...")
        elif start_status.get_message(): # Fallback to display any message from server
            self.show_message(f"{start_status.get_message()}")
        else: # Fallback for unknown status
            self.show_message(f"Status de início desconhecido: {start_status.get_code()}")

    def initialize_game_display(self):
        self.clear_board()
        
        book_width, book_height = 60, 90
        master_book_width, master_book_height = 75, 110 
        card_width, card_height = 90, 130
        card_font = "Helvetica 11" 
        card_wraplength = card_width - 10

        if self.game.remote_player and hasattr(self.game.remote_player, 'get_display'):
            opponent_books_data = self.game.remote_player.get_display().get_display()
            for i, book in enumerate(opponent_books_data):
                color = book.get_color()
                book_widget = tk.Frame(self.opponent_frame, width=book_width, height=book_height, 
                                      bg=self.colors.get(color, "#BDC3C7"),
                                      highlightbackground="black", highlightthickness=2)
                book_widget.pack_propagate(False)
                book_widget.pack(side=tk.LEFT, padx=5, pady=5)
                book_widget.bind("<Button-1>", self.create_opponent_book_click(i))
                self.opponent_books.append(book_widget)
        
        if hasattr(self.game, 'main_display'):
            master_books_data = self.game.main_display.main_display
            for i, book in enumerate(master_books_data):
                color = book.get_color()
                book_widget = tk.Frame(self.objective_frame, width=master_book_width, height=master_book_height, 
                                      bg=self.colors.get(color, "#BDC3C7"),
                                      highlightbackground="black", highlightthickness=2)
                book_widget.pack_propagate(False)
                book_widget.pack(side=tk.LEFT, padx=5, pady=5)
                book_widget.bind("<Button-1>", self.create_objective_book_click(i))
                self.objective_books.append(book_widget)
        
        if self.game.local_player and hasattr(self.game.local_player, 'get_display'):
            your_books_data = self.game.local_player.get_display().get_display()
            for i, book in enumerate(your_books_data):
                color = book.get_color()
                book_widget = tk.Frame(self.your_books_frame, width=book_width, height=book_height, 
                                      bg=self.colors.get(color, "#BDC3C7"),
                                      highlightbackground="black", highlightthickness=2)
                book_widget.pack_propagate(False)
                book_widget.pack(side=tk.LEFT, padx=5, pady=5)
                book_widget.bind("<Button-1>", self.create_your_book_click(i))
                self.your_books.append(book_widget)
        
        if self.game.local_player and hasattr(self.game.local_player, 'get_hand'):
            cards_data = self.game.local_player.get_hand().get_cartas()
            for i, card in enumerate(cards_data):
                card_widget = tk.Frame(self.cards_frame, width=card_width, height=card_height, bg="white",
                                      highlightbackground="black", highlightthickness=2)
                card_widget.pack_propagate(False)
                card_widget.pack(side=tk.LEFT, padx=5, pady=5)
                
                # Ensure card.description is available and is a string
                desc_text = getattr(card, 'description', 'N/A') if card else 'N/A' 
                
                label = tk.Label(card_widget, text=str(desc_text), bg="white", 
                                wraplength=card_wraplength, font=card_font, justify="center")
                label.pack(pady=(10,0), padx=5, expand=True, fill="both")
                
                card_widget.bind("<Button-1>", self.create_card_click(i))
                self.card_widgets.append(card_widget)
        
        for frame_container in [self.opponent_frame_container, self.objective_frame_container, 
                                self.your_books_frame_container, self.cards_frame_container]:
            for child in frame_container.winfo_children():
                if isinstance(child, tk.Canvas):
                    child.update_idletasks() 
                    child.config(scrollregion=child.bbox("all"))
                    break

    def clear_board(self):
        for book_list in [self.opponent_books, self.objective_books, self.your_books, self.card_widgets]:
            for widget in book_list:
                widget.destroy()
        
        self.opponent_books.clear()
        self.objective_books.clear()
        self.your_books.clear()
        self.card_widgets.clear()
        
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
        
        if self.selected_card_index is not None and 0 <= self.selected_card_index < len(self.card_widgets):
            self.card_widgets[self.selected_card_index].config(
                highlightbackground="black", highlightthickness=2)
        
        self.clear_book_selections()
        
        self.selected_card_index = index
        if 0 <= index < len(self.card_widgets):
            self.card_widgets[index].config(highlightbackground="yellow", highlightthickness=3)
        
        card = self.game.local_player.get_hand().get_card(index)
        if card:
            self.selected_target_type = card.get_tipo_alvo() # Assuming method exists
            self.show_message(f"Carta selecionada: {getattr(card, 'description', 'N/A')}")
    
    def click_your_book(self, index):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta primeiro!")
            return
        
        card = self.game.local_player.get_hand().get_card(self.selected_card_index)
        # Assuming card.get_tipo_alvo() returns a string or enum for target type
        # And these types are defined in your action_card module.
        if not card or card.get_tipo_alvo() not in ["personal", "all_personal", "any_book_on_table", "your_book"]: # Example types
            self.show_message("Esta carta não pode ser usada em seus livros ou requer um alvo diferente!")
            return
        self.handle_book_selection(index, "your")

    def click_opponent_book(self, index):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta primeiro!")
            return
        card = self.game.local_player.get_hand().get_card(self.selected_card_index)
        if not card or card.get_tipo_alvo() not in ["opponent", "all_opponent", "any_book_on_table", "opponent_book"]: # Example types
            self.show_message("Esta carta não pode ser usada nos livros do oponente ou requer um alvo diferente!")
            return
        self.handle_book_selection(index, "opponent")

    def click_objective_book(self, index):
        if not self.game.verificar_turno_do_jogador():
            self.show_message("Não é seu turno!")
            return
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta primeiro!")
            return
        card = self.game.local_player.get_hand().get_card(self.selected_card_index)
        if not card or card.get_tipo_alvo() not in ["master", "any_book_on_table", "objective_book"]: # Example types
            self.show_message("Esta carta não pode ser usada nos livros mestres ou requer um alvo diferente!")
            return
        self.handle_book_selection(index, "master")

    def handle_book_selection(self, index, book_type):
        card = self.game.local_player.get_hand().get_card(self.selected_card_index)
        if not card:
            self.show_message("Nenhuma carta selecionada.")
            return

        # This logic depends heavily on how your cards are defined (e.g., if they need 1 or 2 targets)
        # Assuming a card might have a method like 'requires_two_targets()'
        requires_two = hasattr(card, 'requires_two_targets') and card.requires_two_targets()

        if requires_two:
            if len(self.selected_books) == 0:
                self.selected_books.append((index, book_type))
                self.update_book_highlight(index, book_type, True)
                self.show_message(f"Primeiro alvo selecionado. Selecione o segundo para '{getattr(card,'description','N/A')}'.")
                return # Wait for second selection
            elif len(self.selected_books) == 1:
                # Check if the second selection is valid with the first (e.g., not the same book, correct type)
                # This is game-specific logic.
                self.selected_books.append((index, book_type))
                self.update_book_highlight(index, book_type, True)
                # Now, call the specific handler or apply_card_with_data for two-target cards
        else: # Single target card
            self.selected_books = [(index, book_type)] # Store the single selection
            # No need to highlight and wait if it's a single target, proceed to handler/apply

        # Call appropriate handler based on card type
        # This part remains highly dependent on your ActionCard subclasses and their specific needs
        if isinstance(card, SwapWithSpaces):
            self.handle_swap_with_spaces(index, book_type) # This handler might need to manage its own state for 2 selections
        elif isinstance(card, MoveBookSpaces):
            self.handle_move_book_spaces(index, book_type)
        elif isinstance(card, MoveToEdge):
            self.handle_move_to_edge(index, book_type)
        elif isinstance(card, SwapEdges):
            self.handle_swap_edges() # May not need index/book_type from click
        elif isinstance(card, SwapWithOpponent):
            self.handle_swap_with_opponent(index, book_type) # Needs careful state for 2 selections of different types
        elif isinstance(card, MoveMasterBook):
            self.handle_move_master_book(index, book_type)
        else:
            # Generic fallback or if the card itself handles its application directly
            # For single target cards, this might be the place to directly call apply_card_with_data
            if not requires_two and self.selected_books:
                # Ensure target_data is structured as your game.apply_card_effect expects
                # For a single book, it might be [index_of_book, book_type_string] or just [index_of_book]
                # if the card's effect is unambiguous about which display it acts upon.
                apply_data = [self.selected_books[0][0]] # Simplest form: just the index
                # If type is needed: apply_data = [self.selected_books[0][0], self.selected_books[0][1]]
                self.apply_card_with_data(apply_data)
            elif requires_two and len(self.selected_books) == 2:
                # Example for two targets, structure as needed by game logic
                apply_data = [self.selected_books[0][0], self.selected_books[1][0]]
                # Or: apply_data = [(self.selected_books[0][0], self.selected_books[0][1]),
                #                   (self.selected_books[1][0], self.selected_books[1][1])]
                self.apply_card_with_data(apply_data)


    def handle_swap_with_spaces(self, index, book_type):
        # This handler is for cards that swap two books, likely on the same shelf.
        # It assumes it's called after each relevant book click.
        # This logic is simplified from original; assumes two books are now in self.selected_books
        if len(self.selected_books) == 2:
            # Ensure books are of compatible types for swapping (e.g., both 'your' or both 'master')
            # This depends on the card's specific rules.
            book1_idx, book1_type = self.selected_books[0]
            book2_idx, book2_type = self.selected_books[1]

            if book1_type != book2_type: # Example validation
                self.show_message("Os livros devem ser do mesmo tipo para esta troca.")
                self.clear_selections()
                return

            target_data = [book1_idx, book2_idx] 
            # If game logic needs type: target_data = [book1_idx, book2_idx, book1_type]
            self.apply_card_with_data(target_data)
        elif len(self.selected_books) == 1:
             self.show_message("Primeiro livro selecionado. Selecione o segundo para trocar.")
        # If called with one selection, it implies the UI is waiting for the second click.
        # The main click_book methods and handle_book_selection should manage this state.

    def handle_move_book_spaces(self, index, book_type):
        spaces = simpledialog.askinteger("Mover Livro", 
                                        "Quantos espaços mover? (negativo = esquerda, positivo = direita)",
                                        parent=self.root, minvalue=-9, maxvalue=9)
        if spaces is not None:
            # Target data might be [book_index, spaces_to_move, book_type_string]
            # if game.apply_card_effect needs to know which display the index refers to.
            target_data = [index, spaces, book_type] 
            self.apply_card_with_data(target_data)
    
    def handle_move_to_edge(self, index, book_type):
        edge = messagebox.askyesno("Mover para Extremidade", 
                                  "Mover para a direita? (Não = esquerda)", parent=self.root)
        edge_value = 1 if edge else 0 # 1 for right, 0 for left (example convention)
        target_data = [index, edge_value, book_type]
        self.apply_card_with_data(target_data)

    def handle_swap_edges(self):
        # This card usually targets a specific display (e.g., player's own, opponent's, master).
        # The card itself (from self.selected_card_index) should know its target type.
        card = self.game.local_player.get_hand().get_card(self.selected_card_index)
        if not card: return

        target_display_type = card.get_tipo_alvo() # e.g., "personal", "opponent", "master"
        
        # Example: If the card is "Swap Edges of YOUR Bookshelf"
        if target_display_type == "personal":
            target_data = ["your"] # Or however your game logic identifies the target display
            self.apply_card_with_data(target_data)
        elif target_display_type == "opponent":
            target_data = ["opponent"]
            self.apply_card_with_data(target_data)
        elif target_display_type == "master":
            target_data = ["master"]
            self.apply_card_with_data(target_data)
        else:
            self.show_message("Tipo de alvo inválido para 'Trocar Extremidades'.")
            self.clear_selections()

    def handle_swap_with_opponent(self, index, book_type):
        # This is for a card that swaps one of YOUR books with one of OPPONENT's books.
        # Requires two selections: first your book, then opponent's book.
        if len(self.selected_books) == 0 and book_type == "your":
            # First selection: a 'your' book
            self.selected_books.append((index, "your"))
            self.update_book_highlight(index, "your", True)
            self.show_message("Seu livro selecionado. Agora clique no livro do oponente para trocar.")
        elif len(self.selected_books) == 1 and self.selected_books[0][1] == "your" and book_type == "opponent":
            # Second selection: an 'opponent' book, after a 'your' book was selected
            your_book_index = self.selected_books[0][0]
            opponent_book_index = index
            
            self.selected_books.append((index, "opponent")) # Store for completeness, though not strictly needed for apply
            self.update_book_highlight(index, "opponent", True) # Highlight briefly

            target_data = [your_book_index, opponent_book_index]
            self.apply_card_with_data(target_data)
        else:
            # Invalid sequence or types
            self.show_message("Para 'Trocar com Oponente': Primeiro selecione SEU livro, depois o do OPONENTE.")
            self.clear_selections()


    def handle_move_master_book(self, index, book_type): # book_type here should be "master"
        if book_type != "master":
            self.show_message("Esta ação só pode ser usada em livros do objetivo (mestres).")
            self.clear_selections() # Clear card selection if target is wrong
            return

        direction = messagebox.askyesno("Mover Livro Mestre", 
                                       "Mover para a direita? (Não = esquerda)", parent=self.root)
        direction_value = 1 if direction else 0
        
        spaces = simpledialog.askinteger("Mover Livro Mestre", 
                                        "Quantos espaços mover? (1 ou 2)",
                                        parent=self.root, minvalue=1, maxvalue=2)
        if spaces is not None:
            target_data = [index, direction_value, spaces] # index is the master book index
            self.apply_card_with_data(target_data)
        else: # User cancelled dialog
            self.clear_selections() # Clear card selection

    def connect_to_server(self):
        player_name = self.name_entry.get().strip()
        if not player_name:
            self.show_message("Por favor, digite seu nome!")
            return
        
        self.player_name = player_name
        self.dog_actor = DogActor() # Assuming DogActor doesn't need server details here
        # The actual connection might happen within initialize or a separate connect method of DogActor
        connection_result_msg = self.dog_actor.initialize(player_name, self) # Initialize returns a message
        self.show_message(str(connection_result_msg))
        
        # Connection success check should be robust. Dog server messages can vary.
        # Using a property of dog_actor or a specific success code is better if available.
        if self.dog_actor.is_connected(): # Assuming DogActor has an is_connected() method
            self.is_connected = True
            self.start_button.config(state=tk.NORMAL)
            self.name_entry.config(state=tk.DISABLED)
        else:
            self.is_connected = False
            self.start_button.config(state=tk.DISABLED)
            # Optionally, you might want to show a more specific error from connection_result_msg
            # if it indicates a failure.

    def handle_match_start(self, start_status: StartStatus):
        self.match_in_progress = True
        
        # Game logic should set up players, decks, hands based on start_status
        # This includes determining player order, IDs, and initial game state.
        success = self.game.initialize_game_from_dog_status(start_status, self.player_name)
        
        if success:
            self.initialize_game_display() 
            self.show_screen("playing")
            self.update_display_for_turn() # Updates turn label and messages
            
            # If this player makes the first move (determined by game logic after init)
            if self.game.is_local_player_turn():
                # Some games require the starting player to send an initial state or first move
                # This depends on your game's protocol with DOG.
                # For instance, if the game involves hidden info setup by the first player:
                # self.send_initial_game_state_if_needed() 
                pass # Or the game might just begin with their turn.
        else:
            self.show_message("Erro ao inicializar o jogo com dados do servidor!")
            self.match_in_progress = False
            self.show_screen("welcome") # Revert to welcome screen
            if hasattr(self, 'start_button'):
                self.start_button.config(state=tk.NORMAL if self.is_connected else tk.DISABLED)


    def send_initial_game_state_if_needed(self):
        # This is a placeholder for games where the starting player needs to send
        # some initial setup information not covered by the standard DOG start_match flow.
        # Most simple turn-based games might not need this if start_status is comprehensive.
        if self.dog_actor and self.game.is_local_player_turn() and self.game.requires_initial_state_broadcast():
            initial_state_data = self.game.get_initial_broadcast_data()
            if initial_state_data:
                 self.dog_actor.send_move(initial_state_data)


    def apply_card_with_data(self, target_data):
        if not self.game.is_local_player_turn(): # Using game's method
            self.show_message("Não é seu turno!")
            return
        
        card = self.game.local_player.get_hand().get_card(self.selected_card_index)
        if not card:
            self.show_message("Nenhuma carta selecionada para aplicar.")
            return
        
        # Game's apply_card_effect should return a status or handle all side effects
        # (drawing new card, checking win, changing turn internally)
        effect_result = self.game.apply_local_player_card(self.selected_card_index, target_data)
        
        if effect_result.is_success(): # Assuming effect_result is an object with status
            self.show_message(effect_result.get_message() or "Carta aplicada com sucesso!")
            
            # Prepare move data for DOG server
            # The structure of this data depends on what the remote client needs to reconstruct the move
            move_payload = {
                'action': 'play_card',
                'card_played_description': getattr(card, 'description', 'N/A'), # For opponent's info
                'card_identifier': getattr(card, 'id', self.selected_card_index), # Or a unique card ID
                'target_data': target_data, # Raw target data
                'game_state_after_move': self.game.get_public_facing_state_for_dog() # Send current public state
            }
            
            if self.dog_actor:
                self.dog_actor.send_move(move_payload)
            
            if self.game.is_game_over():
                winner_name = self.get_player_name_by_id(self.game.get_winner_id()) \
                              if self.game.get_winner_id() else "Ninguém (Empate?)"
                self.end_game(winner_name)
                # Do not proceed to switch turn or update display further if game ended.
            else:
                # Game logic should have handled turn switching internally if the card effect implies it.
                # Or, if apply_local_player_card doesn't switch turns, do it here:
                # if not effect_result.grants_extra_turn(): self.game.end_local_player_turn()
                self.clear_selections()
                self.update_display() # Redraws board, hand, updates turn messages
                self.show_message("Aguardando jogada do oponente...") # Or "Sua vez novamente!"
        else:
            self.show_message(effect_result.get_message() or "Não foi possível aplicar a carta! Verifique as regras.")
            self.clear_selections() # Allow player to try a different action


    def update_book_highlight(self, index, book_type, selected):
        color = "yellow" if selected else "black"
        thickness = 3 if selected else 2
        
        active_list = None
        if book_type == "your": active_list = self.your_books
        elif book_type == "opponent": active_list = self.opponent_books
        elif book_type == "master": active_list = self.objective_books

        if active_list and 0 <= index < len(active_list):
            active_list[index].config(highlightbackground=color, highlightthickness=thickness)


    def discard_card(self):
        if not self.game.is_local_player_turn():
            self.show_message("Não é seu turno!")
            return
        
        if self.selected_card_index is None:
            self.show_message("Selecione uma carta para descartar!")
            return
        
        # Game logic handles removing card, drawing new one.
        discard_result = self.game.local_player_discards_card(self.selected_card_index)
        
        if discard_result.is_success():
            self.show_message(discard_result.get_message() or "Carta descartada. Nova carta comprada.")
            
            discard_payload = {
                'action': 'discard_card',
                'card_index_discarded': self.selected_card_index, # Original index in hand
                 # Could also send description of discarded card for opponent's log
                'card_discarded_description': getattr(discard_result, 'discarded_card_description', 'N/A'),
                'game_state_after_discard': self.game.get_public_facing_state_for_dog()
            }
            
            if self.dog_actor:
                self.dog_actor.send_move(discard_payload)
            
            # Game logic should handle turn change if discarding ends the turn.
            # if not discard_result.grants_extra_turn(): self.game.end_local_player_turn()

            self.clear_selections() 
            self.update_display() # Re-renders hand, board, updates turn messages
            self.show_message("Aguardando jogada do oponente...")
        else:
            self.show_message(discard_result.get_message() or "Não foi possível descartar a carta.")


    def receive_start(self, start_status: StartStatus):
        self.show_message("Partida iniciada pelo servidor!")
        self.handle_match_start(start_status)

    def receive_move(self, move: dict):
        action = move.get('action', '')
        
        # The game instance should be responsible for parsing the move
        # and updating its internal state.
        update_result = self.game.update_state_from_remote_move(move)

        if update_result.is_success():
            self.update_display() # Redraw board, update card counts, etc.
            
            if self.game.is_game_over():
                winner_id = self.game.get_winner_id()
                winner_name = self.get_player_name_by_id(winner_id) if winner_id else "Ninguém"
                self.end_game(winner_name)
            else:
                # Update turn messages based on new game state
                self.update_display_for_turn()
        else:
            self.show_message(f"Erro ao processar jogada do oponente: {update_result.get_message()}")
            # Potentially request resync or show error state if desync is suspected


    def update_display_for_turn(self):
        """Updates messages and UI elements related to whose turn it is."""
        if self.game.is_local_player_turn():
            self.show_message("Sua vez! Selecione uma carta e depois um alvo para jogar.")
        else:
            opponent_name = self.game.get_remote_player_name() if hasattr(self.game, 'get_remote_player_name') else "Oponente"
            self.show_message(f"Aguardando jogada de {opponent_name}...")
        
        # Update turn label specifically
        if hasattr(self.game, 'get_current_turn_player_name'):
            turn_player_name = self.game.get_current_turn_player_name()
            self.turn_label.config(text=f"Vez de: {turn_player_name}")
        else:
            self.turn_label.config(text="Aguardando informações do turno...")


    def receive_withdrawal_notification(self):
        self.show_message("O oponente abandonou a partida!")
        self.match_in_progress = False # Game logic should also reflect this
        if hasattr(self.game, 'handle_opponent_withdrawal'):
            self.game.handle_opponent_withdrawal()
        
        self.result_label.config(text="Partida encerrada - Oponente desistiu")
        if hasattr(self, 'play_again_button'):
            self.play_again_button.config(state=tk.NORMAL)
        self.show_screen("game_over")
    
    def get_player_name_by_id(self, player_id: str) -> str:
        # Game instance should be the source of truth for player names and IDs
        if hasattr(self.game, 'get_player_name_from_id'):
            name = self.game.get_player_name_from_id(player_id)
            return name if name else f"Jogador ({player_id})"
        
        # Fallback if game object doesn't have the method or ID is not found
        if self.game.local_player and str(self.game.local_player.get_id()) == str(player_id):
            return self.game.local_player.get_name()
        elif self.game.remote_player and str(self.game.remote_player.get_id()) == str(player_id):
            return self.game.remote_player.get_name()
        return f"Jogador ({player_id})" if player_id else "Jogador Desconhecido"


    def reset_to_initial_state(self):
        self.game = Game() 
        self.selected_card_index = None
        self.selected_books = []
        self.selected_target_type = None
        self.awaiting_input = False
        self.match_in_progress = False
        
        self.clear_board()
        self.show_screen("welcome")
        
        if hasattr(self, 'name_entry'):
            self.name_entry.config(state=tk.NORMAL)
            self.name_entry.delete(0, tk.END)
        if hasattr(self, 'start_button'):
             # Enable start button only if still connected to DOG server
            self.start_button.config(state=tk.NORMAL if self.is_connected else tk.DISABLED)
        if hasattr(self, 'play_again_button'):
            self.play_again_button.config(state=tk.DISABLED) 
        
        self.show_message("Jogo resetado. Conecte-se para jogar novamente.")


    def clear_selections(self):
        if self.selected_card_index is not None and \
           self.card_widgets and 0 <= self.selected_card_index < len(self.card_widgets):
            self.card_widgets[self.selected_card_index].config(
                highlightbackground="black", highlightthickness=2)
        self.selected_card_index = None
        self.clear_book_selections()
        self.selected_target_type = None
    
    def clear_book_selections(self):
        for index, book_type in self.selected_books:
            self.update_book_highlight(index, book_type, False)
        self.selected_books = []
    
    def update_display(self):
        # This is the main UI refresh point. It should redraw based on current game state.
        self.initialize_game_display() # Clears and recreates book/card widgets
        self.update_display_for_turn()  # Updates turn-specific labels and messages
        
        # If there are other static UI elements that need updating based on game state,
        # do that here. E.g., score displays, opponent's public card count, etc.
        # self.update_score_labels()
        # self.update_opponent_info()

    # update_book_colors might be redundant if initialize_game_display handles it.
    # If initialize_game_display is too slow, more targeted updates like this can be used.
    # def update_book_colors(self): ... 

    def show_message(self, message):
        if hasattr(self, 'message_label') and self.message_label:
            self.message_label.config(text=str(message)) # Ensure message is string
        print(message)
    
    def end_game(self, winner_name):
        self.result_label.config(text=f"Vencedor: {winner_name}!")
        self.match_in_progress = False # Game logic might also set its own internal flag
        if hasattr(self.game, 'finalize_match_locally'):
            self.game.finalize_match_locally()

        if hasattr(self, 'play_again_button'):
            self.play_again_button.config(state=tk.NORMAL)
        self.show_screen("game_over")
    
    def reset_game(self):
        # If connected and in a match, might need to inform server/opponent of resignation
        # This depends on DOG protocol for your game.
        if self.match_in_progress and self.dog_actor and self.dog_actor.is_connected():
            # Example: self.dog_actor.send_move({'action': 'resign_match'})
            pass # For now, local reset. Game logic should handle cleaning up match state.

        self.reset_to_initial_state()
    
    def run(self):
        self.root.mainloop()

# if __name__ == "__main__":
#   interface = AdasLibraryInterface()
#   interface.run()
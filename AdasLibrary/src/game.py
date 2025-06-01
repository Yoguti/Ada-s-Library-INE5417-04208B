import random
from book import Book
from player import Player
from deck import Deck
from master_display import MasterDisplay

class Game:
    def __init__(self):
        self.main_display = MasterDisplay()
        self.local_player = None
        self.remote_player = None
        self.action_card_deck = Deck()
        self.game_state = 0  # 0=initial, 1=waiting_for_opponent, 2=playing, 3=finished
        self.dog_interface = None
        self.local_player_id = None
        self.remote_player_id = None
        self.waiting_for_match = False
    
    def set_dog_interface(self, dog_interface):
        """Set reference to DOG interface for network communication"""
        self.dog_interface = dog_interface
    
    def start_match_request(self, num_players=2):
        """Request to start a match using DOG's proper matchmaking"""
        if not self.dog_interface:
            return False
    
        if self.waiting_for_match:
            return False  # Already waiting
    
        self.waiting_for_match = True
        self.game_state = 1  # waiting_for_opponent
    
        # Use DOG's start_match method instead of send_move
        if hasattr(self.dog_interface, 'start_match'):
            start_status = self.dog_interface.start_match(num_players)
            return start_status
    
        return False
    
    def initialize_players_with_dog(self, start_status):
        """Initialize players using DOG StartStatus"""
        players = start_status.players
        local_id = start_status.local_id
        
        local_info = None
        remote_info = None
        
        for player_info in players:
            name, player_id, order = player_info[0], player_info[1], int(player_info[2])
            if player_id == local_id:
                local_info = (name, player_id, order)
            else:
                remote_info = (name, player_id, order)
        
        if local_info and remote_info:
            self.local_player = Player(local_info[0])
            self.local_player_id = local_info[1]
            self.remote_player = Player(remote_info[0])
            self.remote_player_id = remote_info[1]
            
            # Set turn order
            local_starts = local_info[2] == 1
            self.local_player.set_is_turn(local_starts)
            self.remote_player.set_is_turn(not local_starts)
            
            if local_starts:
                self.initialize_game_state()
                self.send_initial_state()
            
            self.game_state = 2  # Playing
            self.waiting_for_match = False
            return True
        
        return False
    
    def initialize_game_state(self):
        """Initialize books and cards for both players"""
        self.main_display.posicionar_master_books()
        self.reorganizar_livros_aleatorios()
        
        if self.local_player:
            local_cards = self.action_card_deck.distribuir_cartas(5)
            self.local_player.get_hand().set_cartas(local_cards)
        
        if self.remote_player:
            remote_cards = self.action_card_deck.distribuir_cartas(5)
            self.remote_player.get_hand().set_cartas(remote_cards)
    
    def send_initial_state(self):
        """Send initial game state to remote player"""
        if self.dog_interface:
            game_state = {
                'action': 'initial_state',
                'master_books': [book.get_color() for book in self.main_display.main_display],
                'local_books': [book.get_color() for book in self.local_player.get_display().get_display()],
                'remote_books': [book.get_color() for book in self.remote_player.get_display().get_display()],
                'match_status': 'progress'
            }
            self.dog_interface.send_move(game_state)
    
    def receive_initial_state(self, state_data):
        """Receive and process initial game state from remote player"""
        master_colors = state_data.get('master_books', [])
        self.main_display.main_display = [Book(color) for color in master_colors]
        
        local_colors = state_data.get('remote_books', [])
        self.local_player.get_display().set_display([Book(color) for color in local_colors])
        
        remote_colors = state_data.get('local_books', [])
        self.remote_player.get_display().set_display([Book(color) for color in remote_colors])
        
        local_cards = self.action_card_deck.distribuir_cartas(5)
        self.local_player.get_hand().set_cartas(local_cards)
    
    def is_valid_turno_atual(self):
        return self.local_player and self.local_player.get_is_turn()
    
    def is_valid_tipo_alvo(self, card):
        return card.get_tipo_alvo() in ["personal", "opponent", "master"]
    
    def is_valid_posicao_alvo(self, position, target_type="personal"):
        if target_type == "personal" and self.local_player:
            return 0 <= position < len(self.local_player.get_display().get_display())
        elif target_type == "opponent" and self.remote_player:
            return 0 <= position < len(self.remote_player.get_display().get_display())
        elif target_type == "master":
            return 0 <= position < len(self.main_display.main_display)
        return False
    
    def avaliar_fim_da_partida(self):
        """Check if any player has won"""
        if self.local_player and self.check_victory_condition(self.local_player):
            return True
        if self.remote_player and self.check_victory_condition(self.remote_player):
            return True
        return False
    
    def check_victory_condition(self, player):
        """Check if player's books match the master display order"""
        player_books = player.get_display().get_display()
        master_books = self.main_display.main_display
        
        if len(player_books) == 0 or len(master_books) == 0:
            return False
        
        player_colors = [book.get_color() for book in player_books]
        master_colors = [book.get_color() for book in master_books]
        
        master_index = 0
        for player_color in player_colors:
            if master_index < len(master_colors) and player_color == master_colors[master_index]:
                master_index += 1
                if master_index == len(master_colors):
                    return True
        
        return False
    
    def reorganizar_livros_aleatorios(self):
        """Create random books for both players"""
        colors = ["vermelho", "azul_claro", "cinza", "marrom", "amarelo", "azul_escuro"]
        
        local_books = [Book(random.choice(colors)) for _ in range(10)]
        remote_books = [Book(random.choice(colors)) for _ in range(10)]
        
        if self.local_player:
            self.local_player.get_display().set_display(local_books)
        if self.remote_player:
            self.remote_player.get_display().set_display(remote_books)
    
    def registrar_jogada_irregular(self):
        print("Jogada irregular detectada!")
        return False
    
    def trocar_turno_jogador(self):
        if self.local_player and self.remote_player:
            self.local_player.set_is_turn(not self.local_player.get_is_turn())
            self.remote_player.set_is_turn(not self.remote_player.get_is_turn())
    
    def marcar_jogada_finalizada(self):
        self.game_state = 3
    
    def encerrar_partida_com_vitoria_local(self):
        self.marcar_jogada_finalizada()
        return f"Vitória de {self.local_player.get_name()}!"
    
    def verificar_turno_do_jogador(self):
        return self.local_player and self.local_player.get_is_turn()
    
    def identificar_tipo_mensagem(self, message):
        if isinstance(message, dict) and 'action' in message:
            return message['action']
        return 'unknown'
    
    def set_status(self, status):
        self.game_state = status
    
    def remover_carta_selecionada_da_mao(self, card_index):
        if self.local_player:
            removed_card = self.local_player.get_hand().remove_card(card_index)
            if removed_card:
                new_card = self.action_card_deck.draw_card()
                if new_card:
                    self.local_player.get_hand().add_card(new_card)
            return removed_card
        return None
    
    def apply_card_effect(self, card_index, target_data):
        """Apply the effect of a selected card with improved validation"""
        if not self.local_player:
            return False
        
        hand = self.local_player.get_hand()
        card = hand.get_card(card_index)
        
        if not card:
            return False
        
        success = False
        card_type = card.get_tipo_alvo()
        
        try:
            if card_type == "personal":
                success = card.apply(self.local_player, target_data)
            elif card_type == "opponent" and self.remote_player:
                target_with_opponent = target_data + [self.remote_player]
                success = card.apply(self.local_player, target_with_opponent)
            elif card_type == "master":
                target_with_master = target_data + [self.main_display]
                success = card.apply(self.local_player, target_with_master)
        except Exception as e:
            print(f"Error applying card effect: {e}")
            success = False
        
        if success:
            self.remover_carta_selecionada_da_mao(card_index)
        
        return success
    
    def apply_remote_card_effect(self, card_description, target_data):
        """Apply card effect received from remote player"""
        temp_card = None
        for card in self.action_card_deck.action_cards:
            if card.description == card_description:
                temp_card = card
                break
        
        if not temp_card:
            return False
        
        card_type = temp_card.get_tipo_alvo()
        
        try:
            if card_type == "personal":
                return temp_card.apply(self.remote_player, target_data)
            elif card_type == "opponent" and self.local_player:
                target_with_opponent = target_data + [self.local_player]
                return temp_card.apply(self.remote_player, target_with_opponent)
            elif card_type == "master":
                target_with_master = target_data + [self.main_display]
                return temp_card.apply(self.remote_player, target_with_master)
        except Exception as e:
            print(f"Error applying remote card effect: {e}")
            return False
        
        return False
    
    def send_move(self, card_index, target_data):
        """Send a move through DOG interface"""
        if not self.dog_interface or not self.verificar_turno_do_jogador():
            return False
        
        card = self.local_player.get_hand().get_card(card_index)
        if not card:
            return False
        
        success = self.apply_card_effect(card_index, target_data)
        
        if success:
            game_over = self.avaliar_fim_da_partida()
            
            move_data = {
                'action': 'play_card',
                'card_type': card.description,
                'target_data': target_data,
                'match_status': 'finished' if game_over else 'next'
            }
            
            self.dog_interface.send_move(move_data)
            
            if game_over:
                self.marcar_jogada_finalizada()
            else:
                self.trocar_turno_jogador()
            
            return True
        
        return False
    
    def send_discard(self, card_index):
        """Send a discard action through DOG interface"""
        if not self.dog_interface or not self.verificar_turno_do_jogador():
            return False
        
        removed_card = self.remover_carta_selecionada_da_mao(card_index)
        
        if removed_card:
            discard_data = {
                'action': 'discard_card',
                'card_index': card_index,
                'match_status': 'next'
            }
            
            self.dog_interface.send_move(discard_data)
            self.trocar_turno_jogador()
            return True
        
        return False
    
    def receive_move(self, move_data):
        """Process a move received from remote player"""
        action = move_data.get('action', '')
    
        if action == 'initial_state':
            self.receive_initial_state(move_data)
            return 'game_started'
        elif action == 'play_card':
            card_type = move_data.get('card_type', '')
            target_data = move_data.get('target_data', [])
        
            self.apply_remote_card_effect(card_type, target_data)
        
            match_status = move_data.get('match_status', '')
            if match_status == 'finished':
                self.marcar_jogada_finalizada()
                return 'game_over'
            else:
                self.trocar_turno_jogador()
                return 'continue'
        elif action == 'discard_card':
            self.trocar_turno_jogador()
            return 'continue'
    
        return 'continue'

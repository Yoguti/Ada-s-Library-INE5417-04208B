from hand import Hand
from player_display import PlayerDisplay

class Player:
    def __init__(self, name):
        self.is_turn = False
        self.name = name
        self.hand = Hand()
        self.display = PlayerDisplay()
        self.active = False
        self.direction = 0
        self.move = 0
    
    def get_is_turn(self):
        return self.is_turn
    
    def set_is_turn(self, turn):
        self.is_turn = turn
    
    def set_is_turn_turn(self, turn):
        self.is_turn = turn
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    def get_hand(self):
        return self.hand
    
    def get_display(self):
        return self.display
    
    def use_card(self, hand, card, target):
        # Remove card from hand and apply effect
        if card in hand.get_cartas():
            result = card.apply(self, target)
            if result:
                hand.remove_card(hand.get_cartas().index(card))
            return result
        return False
    
    def assume_victory(self, player):
        # Check if this player has won
        return self.check_victory_condition()
    
    def check_victory_condition(self):
        # This will be implemented in the game logic
        return False
    
    def get_active(self):
        return self.active
    
    def set_active(self, active):
        self.active = active
    
    def set_direction(self, direction):
        self.direction = direction
    
    def set_move(self, move):
        self.move = move
    
    def get_direction(self):
        return self.direction
    
    def get_move(self):
        return self.move

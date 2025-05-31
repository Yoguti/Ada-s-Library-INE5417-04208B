class Hand:
    def __init__(self):
        self.cards = []
        self.is_full = False
        self.owner = None
    
    def get_cartas(self):
        return self.cards
    
    def set_cartas(self, cards):
        self.cards = cards
        self.is_full = len(cards) >= 5
    
    def is_full_hand(self):
        return self.is_full
    
    def add_card(self, card):
        if len(self.cards) < 5:
            self.cards.append(card)
            self.is_full = len(self.cards) >= 5
            return True
        return False
    
    def remove_card(self, index):
        if 0 <= index < len(self.cards):
            card = self.cards.pop(index)
            self.is_full = False
            return card
        return None
    
    def get_card(self, index):
        if 0 <= index < len(self.cards):
            return self.cards[index]
        return None
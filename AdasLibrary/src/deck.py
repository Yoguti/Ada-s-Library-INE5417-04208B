import random
from action_card import *

class Deck:
    def __init__(self):
        self.is_empty = False
        self.action_cards = []
        self.criar_deck()
    
    def criar_deck(self):
        cards = []
        
        # Add multiple instances of each card type
        for _ in range(8):
            cards.append(SwapWithSpaces())
        for _ in range(8):
            cards.append(MoveBookSpaces())
        for _ in range(6):
            cards.append(MoveToEdge())
        for _ in range(4):
            cards.append(SwapEdges())
        for _ in range(6):
            cards.append(SwapWithOpponent())
        for _ in range(4):
            cards.append(MoveMasterBook())
        
        random.shuffle(cards)
        self.action_cards = cards
    
    def distribuir_cartas(self, qtd=5):
        cards = []
        for _ in range(qtd):
            if self.action_cards:
                cards.append(self.action_cards.pop())
            else:
                self.is_empty = True
                break
        return cards
    
    def colocar_carta_no_topo(self, card):
        self.action_cards.insert(0, card)
    
    def draw_card(self):
        if self.action_cards:
            return self.action_cards.pop()
        else:
            self.is_empty = True
            return None

import random
from action_card import *

class Deck:
    def __init__(self):
        self.action_cards = []
        self.is_empty = False
        self.discard_pile = []
        self.criar_deck()

    def criar_deck(self):
        """Create the action card deck"""
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
        self.is_empty = False
    
    def distribuir_cartas(self, qtd=5):
        """Distribute cards to players"""
        cards = []
        for _ in range(qtd):
            card = self.draw_card()
            if card:
                cards.append(card)
            else:
                break
        return cards
    
    def colocar_carta_no_topo(self, card):
        """Place a card on top of the deck"""
        self.action_cards.insert(0, card)
        self.is_empty = False
    
    def draw_card(self):
        """Draw a card from the deck"""
        if self.action_cards:
            return self.action_cards.pop()
        else:
            # Try to reshuffle if deck is empty
            if self.reshuffle_deck():
                return self.action_cards.pop() if self.action_cards else None
            else:
                self.is_empty = True
                return None
    
    def reshuffle_deck(self):
        """Reshuffle the discard pile to create a new deck"""
        if len(self.discard_pile) > 0:
            print(f"Reembaralhando {len(self.discard_pile)} cartas do descarte...")
            self.action_cards = self.discard_pile.copy()
            self.discard_pile = []
            random.shuffle(self.action_cards)
            self.is_empty = False
            print(f"Deck reembaralhado com {len(self.action_cards)} cartas")
            return True
        else:
            # If no discard pile, create a new deck
            print("Criando novo deck...")
            self.criar_deck()
            return True
    
    def add_to_discard(self, card):
        """Add a card to the discard pile"""
        self.discard_pile.append(card)
    
    def __len__(self):
        return len(self.action_cards)

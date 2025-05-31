from book import Book
import random

class MasterDisplay:
    def __init__(self):
        self.main_display = []
        self.posicionar_master_books()
    
    def posicionar_master_books(self, qtd=6):
        # Ensure exactly one book of each color
        colors = ["vermelho", "azul_claro", "cinza", "marrom", "amarelo", "azul_escuro"]
        random.shuffle(colors)
        self.main_display = [Book(color) for color in colors]
    
    def remover_master_book(self, index):
        if 0 <= index < len(self.main_display):
            return self.main_display.pop(index)
        return None
    
    def organizar_livros_iniciais(self):
        random.shuffle(self.main_display)
    
    def move_book(self, from_index, direction, spaces):
        """Move a master book left or right by specified spaces"""
        if 0 <= from_index < len(self.main_display):
            book = self.main_display.pop(from_index)
            if direction == "left":
                new_index = max(0, from_index - spaces)
            else:  # right
                new_index = min(len(self.main_display), from_index + spaces)
            self.main_display.insert(new_index, book)
            return True
        return False

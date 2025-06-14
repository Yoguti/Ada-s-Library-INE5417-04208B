from abc import ABC, abstractmethod
import random

class ActionCard(ABC):
    def __init__(self, description):
        self.description = description
    
    def get_tipo_alvo(self):
        return "personal"  # Default: personal books
    
    @abstractmethod
    def apply(self, owner, target=None):
        pass

class SwapWithSpaces(ActionCard):
    def __init__(self):
        super().__init__("Trocar dois livros com espaços específicos")
    
    def apply(self, owner, target=None):
        """Swap two books with a specified number of spaces between them"""
        if target and len(target) >= 3:
            index1, index2, min_spaces = target[0], target[1], target[2]
            display = owner.get_display().get_display()
            
            # Validate indices
            if not (0 <= index1 < len(display) and 0 <= index2 < len(display)):
                return False
            
            if index1 == index2:
                return False
            
            # Calculate actual spaces between books
            actual_spaces = abs(index2 - index1) - 1
            
            # Check if there are at least the specified spaces between the books
            if actual_spaces >= min_spaces:
                display[index1], display[index2] = display[index2], display[index1]
                return True
        return False

class MoveBookSpaces(ActionCard):
    def __init__(self):
        super().__init__("Mover livro por espaços")
    
    def apply(self, owner, target=None):
        """Move a book a specified number of spaces left or right, never past the end"""
        if target and len(target) >= 2:
            book_index, spaces = target[0], target[1]
            display = owner.get_display().get_display()
            
            if not (0 <= book_index < len(display)):
                return False
            
            # Calculate new position
            new_index = book_index + spaces
            
            # Ensure we don't go past the ends (rule: never past the end of display)
            if not (0 <= new_index < len(display)):
                return False
            
            # Only move if the position actually changes
            if new_index != book_index:
                book = display.pop(book_index)
                display.insert(new_index, book)
                return True
        return False

class MoveToEdge(ActionCard):
    def __init__(self):
        super().__init__("Mover livro para extremidade")
    
    def apply(self, owner, target=None):
        """Move a book to either end of the display"""
        if target and len(target) >= 2:
            book_index, edge = target[0], target[1]  # edge: 0=left, 1=right
            display = owner.get_display().get_display()
            
            if not (0 <= book_index < len(display)):
                return False
            
            # Don't move if already at the target edge
            if (edge == 0 and book_index == 0) or (edge == 1 and book_index == len(display) - 1):
                return False
            
            book = display.pop(book_index)
            if edge == 0:  # Move to left edge
                display.insert(0, book)
            else:  # Move to right edge
                display.append(book)
            return True
        return False

class SwapEdges(ActionCard):
    def __init__(self):
        super().__init__("Trocar livros das extremidades")
    
    def apply(self, owner, target=None):
        """Swap the books on the ends of the display"""
        display = owner.get_display().get_display()
        if len(display) >= 2:
            display[0], display[-1] = display[-1], display[0]
            return True
        return False

class SwapWithOpponent(ActionCard):
    def __init__(self):
        super().__init__("Trocar livro com oponente")
    
    def get_tipo_alvo(self):
        return "opponent"
    
    def apply(self, owner, target=None):
        """Swap a book with the book in opponent's display directly opposite"""
        if target and len(target) >= 3:
            owner_index, opponent_index, opponent = target[0], target[1], target[2]
            owner_display = owner.get_display().get_display()
            opponent_display = opponent.get_display().get_display()
            
            # Validate indices
            if not (0 <= owner_index < len(owner_display) and 
                    0 <= opponent_index < len(opponent_display)):
                return False
            
            # Check if books are "directly opposite" (same relative position)
            if owner_index == opponent_index:
                owner_display[owner_index], opponent_display[opponent_index] = \
                    opponent_display[opponent_index], owner_display[owner_index]
                return True
        return False

class MoveMasterBook(ActionCard):
    def __init__(self):
        super().__init__("Mover livro mestre")
    
    def get_tipo_alvo(self):
        return "master"
    
    def apply(self, owner, target=None):
        """Move a book in the master display 1 or 2 spaces to the left or right"""
        if target and len(target) >= 4:
            book_index, direction, spaces, master_display = target[0], target[1], target[2], target[3]
            
            # Validate spaces (only 1 or 2 allowed)
            if spaces not in [1, 2]:
                return False
            
            if hasattr(master_display, 'move_book'):
                direction_str = "left" if direction == 0 else "right"
                return master_display.move_book(book_index, direction_str, spaces)
        return False

class ChangeBookColorRandom(ActionCard):
    def __init__(self):
        super().__init__("Trocar cor do livro por cor aleatória")
    
    def apply(self, owner, target=None):
        """Change the color of selected book to a random color (excluding current color)"""
        if target and len(target) >= 1:
            book_index = target[0]
            display = owner.get_display().get_display()
            
            if not (0 <= book_index < len(display)):
                return False
            
            book = display[book_index]
            current_color = book.get_color()
            
            # All available colors except the current one
            colors = ["vermelho", "azul_claro", "cinza", "marrom", "amarelo", "azul_escuro"]
            available_colors = [color for color in colors if color != current_color]
            
            if available_colors:
                new_color = random.choice(available_colors)
                book.set_color(new_color)
                return True
        return False

class MoveBookOneRight(ActionCard):
    def __init__(self):
        super().__init__("Mover livro 1 espaço à direita")
    
    def apply(self, owner, target=None):
        """Move a book 1 space to the right with circular wrapping"""
        if target and len(target) >= 1:
            book_index = target[0]
            display = owner.get_display().get_display()
            
            if not (0 <= book_index < len(display)):
                return False
            
            # Remove the book from current position
            book = display.pop(book_index)
            
            # Calculate new position with circular wrapping
            if book_index >= len(display):  # Now len(display) is one less after pop
                # Wrap around to the beginning
                new_index = 0
            else:
                # Move one position to the right
                new_index = book_index + 1
                # If this would exceed the length, wrap to beginning
                if new_index > len(display):
                    new_index = 0
            
            # Insert book at new position
            display.insert(new_index, book)
            return True
        return False

class ChangeBookColorRandomly(ActionCard):
    def __init__(self):
        super().__init__("Trocar cor do livro aleatoriamente")
    
    def apply(self, owner, target=None):
        """Randomly change the color of selected book"""
        if target and len(target) >= 1:
            book_index = target[0]
            display = owner.get_display().get_display()
            
            if not (0 <= book_index < len(display)):
                return False
            
            book = display[book_index]
            colors = ["vermelho", "azul_claro", "cinza", "marrom", "amarelo", "azul_escuro"]
            new_color = random.choice(colors)
            book.set_color(new_color)
            return True
        return False

class ChangeParityBooksColor(ActionCard):
    def __init__(self):
        super().__init__("Trocar cor de livros com mesma paridade")
    
    def apply(self, owner, target=None):
        """Change color of all books with same parity index as selected book"""
        if target and len(target) >= 1:
            book_index = target[0]
            display = owner.get_display().get_display()
            
            if not (0 <= book_index < len(display)):
                return False
            
            # Determine parity (even or odd)
            parity = book_index % 2
            colors = ["vermelho", "azul_claro", "cinza", "marrom", "amarelo", "azul_escuro"]
            
            # Change color of all books with same parity
            changed = False
            for i, book in enumerate(display):
                if i % 2 == parity:
                    new_color = random.choice(colors)
                    book.set_color(new_color)
                    changed = True
            
            return changed
        return False

class MoveMasterBookToSequenceSide(ActionCard):
    def __init__(self):
        super().__init__("Mover livro mestre baseado em sequências")
    
    def get_tipo_alvo(self):
        return "master"
    
    def apply(self, owner, target=None):
        """Move master book based on consecutive color patterns in player's display"""
        if target and len(target) >= 2:
            book_index, master_display = target[0], target[1]
            
            if not (0 <= book_index < len(master_display.main_display)):
                return False
            
            # Get owner's display to analyze sequences
            owner_display = owner.get_display().get_display()
            
            if len(owner_display) == 0:
                return False
            
            # Split display into first half and second half
            mid_point = len(owner_display) // 2
            first_half = owner_display[:mid_point] if mid_point > 0 else []
            second_half = owner_display[mid_point:]
            
            # Count consecutive sequences in each half
            first_half_consecutive = self._count_max_consecutive_sequence(first_half)
            second_half_consecutive = self._count_max_consecutive_sequence(second_half)
            
            # Determine movement direction based on which half has more consecutive books
            if second_half_consecutive > first_half_consecutive:
                # Second half has more consecutive books - move to opposite side (right)
                direction = "right"
            elif first_half_consecutive > second_half_consecutive:
                # First half has more consecutive books - move to same side (left)
                direction = "left"
            else:
                # Equal consecutive counts - choose randomly or default to right
                direction = "right"
            
            # Move the master book 1 space in the determined direction
            return master_display.move_book(book_index, direction, 1)
        return False
    
    def _count_max_consecutive_sequence(self, books):
        """Count the maximum consecutive sequence of same-color books in a list"""
        if not books:
            return 0
        
        max_consecutive = 1
        current_consecutive = 1
        
        for i in range(1, len(books)):
            if books[i].get_color() == books[i-1].get_color():
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 1
        
        return max_consecutive

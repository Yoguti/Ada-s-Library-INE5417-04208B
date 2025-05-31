from abc import ABC, abstractmethod

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
        if target and len(target) >= 2:
            index1, index2 = target[0], target[1]
            display = owner.get_display().get_display()
            if (0 <= index1 < len(display) and 0 <= index2 < len(display) and 
                index1 != index2):
                display[index1], display[index2] = display[index2], display[index1]
                return True
        return False

class MoveBookSpaces(ActionCard):
    def __init__(self):
        super().__init__("Mover livro por espaços")
    
    def apply(self, owner, target=None):
        if target and len(target) >= 2:
            book_index, spaces = target[0], target[1]
            display = owner.get_display().get_display()
            if 0 <= book_index < len(display):
                # Determine direction based on sign of spaces
                direction = 1 if spaces > 0 else -1
                abs_spaces = abs(spaces)
                
                new_index = book_index + (direction * abs_spaces)
                new_index = max(0, min(len(display) - 1, new_index))
                
                if new_index != book_index:
                    book = display.pop(book_index)
                    display.insert(new_index, book)
                    return True
        return False

class MoveToEdge(ActionCard):
    def __init__(self):
        super().__init__("Mover livro para extremidade")
    
    def apply(self, owner, target=None):
        if target and len(target) >= 2:
            book_index, edge = target[0], target[1]  # edge: 0=left, 1=right
            display = owner.get_display().get_display()
            if 0 <= book_index < len(display):
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
        # target should be [owner_index, opponent_index, opponent]
        if target and len(target) >= 3:
            owner_index, opponent_index, opponent = target[0], target[1], target[2]
            owner_display = owner.get_display().get_display()
            opponent_display = opponent.get_display().get_display()
            
            if (0 <= owner_index < len(owner_display) and 
                0 <= opponent_index < len(opponent_display)):
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
        # target should be [book_index, direction, spaces, master_display]
        if target and len(target) >= 4:
            book_index, direction, spaces, master_display = target[0], target[1], target[2], target[3]
            if hasattr(master_display, 'move_book'):
                direction_str = "left" if direction == 0 else "right"
                return master_display.move_book(book_index, direction_str, spaces)
        return False

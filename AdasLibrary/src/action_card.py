from abc import ABC, abstractmethod

class ActionCard(ABC):
    def __init__(self, description, user_friendly_name):
        self.description = description
        self.user_friendly_name = user_friendly_name
        self.interaction_mode = "select"  # "select", "drag", "click_sequence"
        self.help_text = ""
    
    def get_tipo_alvo(self):
        return "personal"  # Default: personal books
    
    def get_interaction_mode(self):
        return self.interaction_mode
    
    def get_help_text(self):
        return self.help_text
    
    @abstractmethod
    def apply(self, owner, target=None):
        pass
    
    @abstractmethod
    def get_required_selections(self):
        """Return number and type of selections needed"""
        pass
    
    @abstractmethod
    def validate_selection(self, selections, display_length):
        """Validate if current selections are valid"""
        pass

class SwapWithSpaces(ActionCard):
    def __init__(self):
        super().__init__("Trocar dois livros com espaços específicos", "Trocar Dois Livros")
        self.help_text = "Clique em dois livros para trocá-los de posição"
    
    def get_required_selections(self):
        return {"count": 2, "type": "books", "same_display": True}
    
    def validate_selection(self, selections, display_length):
        if len(selections) != 2:
            return False, "Selecione exatamente 2 livros"
        if selections[0] == selections[1]:
            return False, "Selecione livros diferentes"
        return True, "Pronto para trocar!"
    
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
        super().__init__("Mover livro por espaços", "Mover Livro")
        self.interaction_mode = "drag"
        self.help_text = "Clique e arraste um livro para uma nova posição"
    
    def get_required_selections(self):
        return {"count": 2, "type": "positions", "same_display": True}
    
    def validate_selection(self, selections, display_length):
        if len(selections) != 2:
            return False, "Selecione a posição inicial e final"
        from_pos, to_pos = selections[0], selections[1]
        if from_pos == to_pos:
            return False, "Selecione uma posição diferente"
        if not (0 <= from_pos < display_length and 0 <= to_pos < display_length):
            return False, "Posições inválidas"
        return True, f"Mover livro da posição {from_pos + 1} para {to_pos + 1}"
    
    def apply(self, owner, target=None):
        if target and len(target) >= 2:
            from_index, to_index = target[0], target[1]
            display = owner.get_display().get_display()
            if (0 <= from_index < len(display) and 0 <= to_index < len(display) and 
                from_index != to_index):
                book = display.pop(from_index)
                display.insert(to_index, book)
                return True
        return False

class MoveToEdge(ActionCard):
    def __init__(self):
        super().__init__("Mover livro para extremidade", "Mover para Borda")
        self.help_text = "Clique em um livro, depois clique na borda esquerda ou direita"
    
    def get_required_selections(self):
        return {"count": 2, "type": "book_and_edge", "same_display": True}
    
    def validate_selection(self, selections, display_length):
        if len(selections) != 2:
            return False, "Selecione um livro e depois uma borda"
        book_index, edge = selections[0], selections[1]
        if not (0 <= book_index < display_length):
            return False, "Livro inválido"
        if edge not in [0, 1]:
            return False, "Borda inválida"
        edge_name = "esquerda" if edge == 0 else "direita"
        return True, f"Mover livro {book_index + 1} para a borda {edge_name}"
    
    def apply(self, owner, target=None):
        if target and len(target) >= 2:
            book_index, edge = target[0], target[1]
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
        super().__init__("Trocar livros das extremidades", "Trocar Bordas")
        self.help_text = "Troca automaticamente os livros das bordas esquerda e direita"
    
    def get_required_selections(self):
        return {"count": 0, "type": "none", "same_display": True}
    
    def validate_selection(self, selections, display_length):
        if display_length < 2:
            return False, "Precisa de pelo menos 2 livros"
        return True, "Trocar livros das bordas"
    
    def apply(self, owner, target=None):
        display = owner.get_display().get_display()
        if len(display) >= 2:
            display[0], display[-1] = display[-1], display[0]
            return True
        return False

class SwapWithOpponent(ActionCard):
    def __init__(self):
        super().__init__("Trocar livro com oponente", "Trocar com Oponente")
        self.help_text = "Clique em um dos seus livros, depois em um livro do oponente"
    
    def get_tipo_alvo(self):
        return "opponent"
    
    def get_required_selections(self):
        return {"count": 2, "type": "cross_display", "same_display": False}
    
    def validate_selection(self, selections, display_length):
        if len(selections) != 2:
            return False, "Selecione um livro seu e um do oponente"
        return True, "Pronto para trocar com o oponente!"
    
    def apply(self, owner, target=None):
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
        super().__init__("Mover livro mestre", "Mover Livro Mestre")
        self.help_text = "Clique em um livro mestre e arraste para uma nova posição (máximo 2 espaços)"
    
    def get_tipo_alvo(self):
        return "master"
    
    def get_required_selections(self):
        return {"count": 2, "type": "positions", "same_display": True}
    
    def validate_selection(self, selections, display_length):
        if len(selections) != 2:
            return False, "Selecione posição inicial e final"
        from_pos, to_pos = selections[0], selections[1]
        if from_pos == to_pos:
            return False, "Selecione uma posição diferente"
        distance = abs(to_pos - from_pos)
        if distance > 2:
            return False, "Máximo 2 espaços de movimento"
        return True, f"Mover livro mestre {distance} espaço(s)"
    
    def apply(self, owner, target=None):
        if target and len(target) >= 3:
            from_index, to_index, master_display = target[0], target[1], target[2]
            if hasattr(master_display, 'move_book_to_position'):
                return master_display.move_book_to_position(from_index, to_index)
        return False

class Book:
    def __init__(self, color):
        self.color = color
    
    def get_color(self):
        return self.color
    
    def set_color(self, color):
        """Set the book's color"""
        self.color = color
    
    def __str__(self):
        return f"Book({self.color})"
    
    def __repr__(self):
        return self.__str__()

class PlayerDisplay:
    def __init__(self):
        self.display = []
        self.owner = None
    
    def get_display(self):
        return self.display
    
    def set_display(self, books):
        self.display = books
    
    def get_owner(self):
        return self.owner
    
    def set_owner(self, owner):
        self.owner = owner

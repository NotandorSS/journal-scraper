class Comments:
    def __init__(self, searchString):
        self.id = searchString
        self.posted = []
        self.mentioned = []
        self.used = []
    def __str__(self):
        return self.id + ": \nPOSTED" + str(self.posted) + "\nMENTIONED" + str(self.mentioned) + "\nUSED" + str(self.used)
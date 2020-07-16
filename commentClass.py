class Tokota:
    def __init__(self, nameId_in, tokotna, deviation, favMe):
        self.nameId = nameId_in
        self.tokotnaId = SearchResults(tokotna)
        self.deviationId = SearchResults(deviation)
        self.favMeLink = SearchResults(favMe)

class SearchResults:
    def __init__(self, search):
        self.searchString = search
        self.commented = []
        self.mentionedIn = []
        self.used = []

class User:
    def __init__(self, id_in, searches):
        self.id = id_in
        self.searches = searches #SearchResults | Tokota []

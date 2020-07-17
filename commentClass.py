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

class Link:
    def __init__(self, linkList):
        self.html = linkList[0]
        self.origin = linkList[1]
    def __eq__(self, other):
        return self.html==other.html
    def __hash__(self):
        return hash(('html', self.html))

class User:
    def __init__(self, id_in, searches):
        self.id = id_in
        self.searches = searches #SearchResults | Tokota []

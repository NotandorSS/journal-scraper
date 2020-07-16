from hardCodedInfo import links, userList
from ScraperService import scrapeThread
from FileWriter import writeToXlsx
from commentClass import User, Tokota, SearchResults

#NOTE TO SELF: Python list ARE pass by reference
usersToSearch = userList

scrapeThread(links, usersToSearch)

for user in usersToSearch:
    for search in user.searches:
        if isinstance(search, SearchResults):
            search.commented = list(dict.fromkeys(search.commented))
            search.mentionedIn = list(dict.fromkeys(search.mentionedIn))
            search.used = list(dict.fromkeys(search.used))
        elif isinstance(search, Tokota):
            search.tokotnaId.commented = list(dict.fromkeys(search.tokotnaId.commented))
            search.tokotnaId.mentionedIn = list(dict.fromkeys(search.tokotnaId.mentionedIn))
            search.tokotnaId.used = list(dict.fromkeys(search.tokotnaId.used))
            search.deviationId.commented = list(dict.fromkeys(search.deviationId.commented))
            search.deviationId.mentionedIn = list(dict.fromkeys(search.deviationId.mentionedIn))
            search.deviationId.used = list(dict.fromkeys(search.deviationId.used))
            search.favMeLink.commented = list(dict.fromkeys(search.favMeLink.commented))
            search.favMeLink.mentionedIn = list(dict.fromkeys(search.favMeLink.mentionedIn))
            search.favMeLink.used = list(dict.fromkeys(search.favMeLink.used))

writeToXlsx(usersToSearch)
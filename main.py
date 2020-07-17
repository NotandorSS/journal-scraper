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
            search.commented = list(set(search.commented))
            search.mentionedIn = list(set(search.mentionedIn))
            search.used = list(set(search.used))
        elif isinstance(search, Tokota):
            search.tokotnaId.commented = list(set(search.tokotnaId.commented))
            search.tokotnaId.mentionedIn = list(set(search.tokotnaId.mentionedIn))
            search.tokotnaId.used = list(set(search.tokotnaId.used))
            search.deviationId.commented = list(set(search.deviationId.commented))
            search.deviationId.mentionedIn = list(set(search.deviationId.mentionedIn))
            search.deviationId.used = list(set(search.deviationId.used))
            search.favMeLink.commented = list(set(search.favMeLink.commented))
            search.favMeLink.mentionedIn = list(set(search.favMeLink.mentionedIn))
            search.favMeLink.used = list(set(search.favMeLink.used))

writeToXlsx(usersToSearch)
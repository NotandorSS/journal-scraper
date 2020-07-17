import requests
import asyncio
import copy
import xlsxwriter
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
from hardCodedInfo import links, userList
from commentClass import Link, SearchResults, Tokota, User
from enum import IntEnum
from FileWriter import writeToXlsx

class ThreadType(IntEnum):
    breeding = 0
    ownership = 3
    corrections = 6
    abandoned = 9
    tokotines = 12
    misc = 15

START_TIME = default_timer()
base_url = "https://www.deviantart.com/_napi/shared_api/comments/thread"

def fetch(session, link):
    searchRequests = copy.deepcopy(userList)
    #NOTE the idea here is to grab pointers to the search result objects 
    # directly for easier sifting through when going through comments
    searchResults = []
    for user in searchRequests:
        for search in user.searches:
            if isinstance(search, SearchResults):
                searchResults.append(search)
            elif isinstance(search, Tokota):
                searchResults.append(search.tokotnaId)
                searchResults.append(search.deviationId)
                searchResults.append(search.favMeLink)
    thread = link[0][38:].split('/')
    threadId = thread[0]
    cursor = thread[1]+"+"
    while True:
        with session.get(base_url, params={'itemid': threadId, 'cursor': cursor}) as response:
            threadSegment = response.json()
            for comment in threadSegment['thread']:
                for item in searchResults:
                    if item.searchString == comment['user']['username'].lower(): 
                        item.commented.append(Link([('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId'])), link[1]]))
                    elif item.searchString in comment['textContent']['html']['markup']:
                        item.mentionedIn.append(Link([('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId'])), link[1]]))
            cursor = threadSegment['cursor']
            if not threadSegment['hasMore']:
                break
    elapsed = default_timer() - START_TIME
    time_completed_at = "{:5.2f}s".format(elapsed)
    print("{0:<60} {1:>20}".format(link[0], time_completed_at))
    return searchRequests

async def get_data_asynchronous():
    print("{0:<60} {1:>20}".format("File", "Completed at"))
    with ThreadPoolExecutor() as executor:
        with requests.Session() as session:
            # Set any session parameters here before calling `fetch`
            session.params.update({
                'typeid': '1',
                'maxdepth': '6',
                'order': 'newest',
                'limit': '50'
            })
            loop = asyncio.get_event_loop()
            START_TIME = default_timer()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, link) # Allows us to pass in multiple arguments to `fetch`
                )
                for link in links
            ]
            
            for response in await asyncio.gather(*tasks):
                for userIndex in range(len(userList)):
                    currentUser = userList[userIndex]
                    responseUser = response[userIndex]
                    for searchIndex in range(len(currentUser.searches)):
                        currentSearch = currentUser.searches[searchIndex]
                        responseSearch = responseUser.searches[searchIndex]
                        if isinstance(currentSearch, SearchResults):
                            currentSearch.commented += responseSearch.commented
                            currentSearch.mentionedIn += responseSearch.mentionedIn
                            currentSearch.used += responseSearch.used
                        elif isinstance(currentSearch, Tokota):
                            currentSearch.tokotnaId.commented += responseSearch.tokotnaId.commented
                            currentSearch.tokotnaId.mentionedIn += responseSearch.tokotnaId.mentionedIn
                            currentSearch.tokotnaId.used += responseSearch.tokotnaId.used
                            currentSearch.deviationId.commented += responseSearch.deviationId.commented
                            currentSearch.deviationId.mentionedIn += responseSearch.deviationId.mentionedIn
                            currentSearch.deviationId.used += responseSearch.deviationId.used
                            currentSearch.favMeLink.commented += responseSearch.favMeLink.commented
                            currentSearch.favMeLink.mentionedIn += responseSearch.favMeLink.mentionedIn
                            currentSearch.favMeLink.used += responseSearch.favMeLink.used
                            


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)

    for user in userList:
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
    writeToXlsx(userList)

main()

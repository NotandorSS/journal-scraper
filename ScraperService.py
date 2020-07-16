import requests
import xlsxwriter
from commentClass import Tokota, SearchResults

def scrapeThread(links, searchRequests):
    s = requests.Session()
    s.params.update({
        'typeid': '1',
        'maxdepth': '6',
        'order': 'newest',
        'limit': '50'
    })
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
    
    for link in links:
        thread = link[38:].split('/')
        threadId = thread[0]
        cursor = thread[1]+"+"

        while True:
            threadSegment = s.get("https://www.deviantart.com/_napi/shared_api/comments/thread", params={'itemid': threadId, 'cursor': cursor}).json()
            for comment in threadSegment['thread']:
                for item in searchResults:
                    if item.searchString == comment['user']['username']: 
                        item.commented.append('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId']))
                    elif item.searchString in comment['textContent']['html']['markup']:
                        item.mentionedIn.append('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId']))
                # if username in userSearchResults:
                    
                # if username in searchRequests:
                #     #write to file we got a link
                #     print(username+" posted: ")
                #     print('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId']))
                #     userComment = username + ' https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId'])
                # else:
                #     for searchTerm in searchRequests:
                #         if searchTerm in comment['textContent']['html']['markup']:
                #             #write to file we got a link
                #             print(searchTerm+" mentioned in: ")
                #             print('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId']))
                #             userComment = searchTerm + ' https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId'])
            cursor = threadSegment['cursor']
            if not threadSegment['hasMore']:
                break
    return []


        


    
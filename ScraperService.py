import requests

#startingLinks = list of links
#searchRequests = {'searchTerm': ['requestedBy/tab']}
def scrapeThread(startingLinks, searchRequests):

    s = requests.Session()
    s.params.update({
        'typeid': '1',
        'maxdepth': '6',
        'order': 'newest',
        'limit': '50'
    })
    for link in startingLinks:
        thread = link[38:].split('/')
        threadId = thread[0]
        cursor = thread[1]+"+"
        
        count = 0

        while True:
            threadSegment = s.get("https://www.deviantart.com/_napi/shared_api/comments/thread", params={'itemid': threadId, 'cursor': cursor}).json()
            for comment in threadSegment['thread']:
                username = comment['user']['username']
                if username in searchRequests:
                    #write to file we got a link
                    # print(username+" posted: ")
                    # print('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId']))
                    count = count + 1
                    print (count)
                else:
                    for searchTerm in searchRequests:
                        if searchTerm in comment['textContent']['html']['markup']:
                            #write to file we got a link
                            # print(searchTerm+" mentioned in: ")
                            # print('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId']))
                            count = count + 1
                            print (count)
            cursor = threadSegment['cursor']
            if not threadSegment['hasMore']:
                break
    
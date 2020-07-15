import requests
from commentClass import Comments
from hardCodedInfo import threads, users

url = "https://www.deviantart.com/_napi/shared_api/comments/thread"

s = requests.Session()
s.params.update({
    'typeid': '1',
    'maxdepth': '6',
    'order': 'newest',
    'limit': '50'
})


results = {}
for user in users:
    results[user] = Comments(user)


for thread in threads:
    threadId = thread[0]
    cursor = thread[1]+"+"
    print(threadId)
    while True:
        threadSegment = s.get(url, params={'itemid': threadId, 'cursor': cursor}).json()
        for comment in threadSegment['thread']:
            username = comment['user']['username']
            if username in users:
                 results[username].posted.append('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId']))
            else:
                for user in users:
                    if user in comment['textContent']['html']['markup']:
                        results[user].mentioned.append('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId']))
        cursor = threadSegment['cursor']
        if not threadSegment['hasMore']:
            break

for key in results:
	print(results[key])
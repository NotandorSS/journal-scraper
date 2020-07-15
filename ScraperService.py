import requests
import xlsxwriter

#startingLinks = list of links
#searchRequests = {'searchTerm': ['requestedBy/tab']}
def createWorkSheet(sheetName, workbook, rowCounter):
    print("creating Worksheet for " + sheetName)
    worksheet = workbook.add_worksheet(sheetName)
    worksheet.write(0,0,"Commented")
    worksheet.write(0,1,"Mentioned")
    rowCounter[sheetName] = {"rowCommentCount": 1, "rowMentionedCount": 1}

def addToWorkSheet(workbook, username, comment, searchRequests, rowCounter, isUserComment):
    for sheetName in searchRequests[username]:
        worksheet = workbook.get_worksheet_by_name(sheetName)
        if worksheet == None:
            createWorkSheet(sheetName, workbook, rowCounter)
            worksheet = workbook.get_worksheet_by_name(sheetName)
        if isUserComment:
            worksheet.write(rowCounter[sheetName]["rowCommentCount"], 0, comment)
            rowCounter[sheetName]["rowCommentCount"] += 1
        else:
            worksheet.write(rowCounter[sheetName]["rowMentionedCount"], 1, comment)
            rowCounter[sheetName]["rowMentionedCount"] += 1


def scrapeThread(startingLinks, searchRequests):
    workbook = xlsxwriter.Workbook('TokoTime.xlsx')

    rowCounter = {}
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
                    print(username+" posted: ")
                    print('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId']))
                    userComment = 'https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId'])
                    addToWorkSheet(workbook, username, userComment, searchRequests, rowCounter, True)
                else:
                    for searchTerm in searchRequests:
                        if searchTerm in comment['textContent']['html']['markup']:
                            #write to file we got a link
                            print(searchTerm+" mentioned in: ")
                            print('https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId']))
                            userComment = 'https://www.deviantart.com/comments/1/'+ str(threadId) + '/' + str(comment['commentId'])
                            addToWorkSheet(workbook, searchTerm, userComment, searchRequests, rowCounter, False)
            cursor = threadSegment['cursor']
            if not threadSegment['hasMore']:
                break
    workbook.close()


        


    
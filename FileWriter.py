import xlsxwriter
from commentClass import User, Tokota, SearchResults

def writeToXlsx(userList):
    workbook = xlsxwriter.Workbook('TokoTime.xlsx')
    for user in userList:
        currentWorksheet = workbook.add_worksheet(user.id)

        colCommentedCounter = 0
        colMentionedCounter = 0
        colUsedCounter = 0
        
        colCommentedCounter = __writeToWorkbook(currentWorksheet, colCommentedCounter, 0, "Commented")
        colMentionedCounter = __writeToWorkbook(currentWorksheet, colMentionedCounter, 1, "Mentioned")
        colUsedCounter = __writeToWorkbook(currentWorksheet, colUsedCounter, 2, "Used")

        for search in user.searches:
            maxCounter = max([colCommentedCounter, colMentionedCounter, colUsedCounter])
            if isinstance(search, SearchResults):
                colCommentedCounter = __writeToWorkbook(currentWorksheet, maxCounter, 0, search.searchString)
                colMentionedCounter = colCommentedCounter
                colUsedCounter = colCommentedCounter
                for link in search.commented:
                    colCommentedCounter = __writeToWorkbook(currentWorksheet, colCommentedCounter, 0, link)
                for link in search.mentionedIn:
                    colMentionedCounter = __writeToWorkbook(currentWorksheet, colMentionedCounter, 1, link)
                for link in search.used:
                    colUsedCounter = __writeToWorkbook(currentWorksheet, colUsedCounter, 2, link)
            elif isinstance(search, Tokota):
                colCommentedCounter = __writeToWorkbook(currentWorksheet, maxCounter, 0 , search.nameId)
                colMentionedCounter = colCommentedCounter
                colUsedCounter = colCommentedCounter
                for link in search.tokotnaId.mentionedIn:
                    colMentionedCounter = __writeToWorkbook(currentWorksheet, colMentionedCounter, 1, link)
                for link in search.tokotnaId.used:
                    colUsedCounter = __writeToWorkbook(currentWorksheet, colUsedCounter, 2, link)
                for link in search.deviationId.mentionedIn:
                    colMentionedCounter = __writeToWorkbook(currentWorksheet, colMentionedCounter, 1, link)
                for link in search.deviationId.used:
                    colUsedCounter = __writeToWorkbook(currentWorksheet, colUsedCounter, 2, link)
                for link in search.favMeLink.mentionedIn:
                    colMentionedCounter = __writeToWorkbook(currentWorksheet, colMentionedCounter, 1, link)
                for link in search.favMeLink.used:
                    colUsedCounter = __writeToWorkbook(currentWorksheet, colUsedCounter, 2, link)
    workbook.close()

def __writeToWorkbook(worksheet, row, column, value):
    worksheet.write(row, column, value)
    row += 1
    return row

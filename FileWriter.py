import xlsxwriter
from commentClass import User, Tokota, SearchResults, Link
from enum import IntEnum

def writeToXlsx(userList):
    workbook = xlsxwriter.Workbook('TokoTime.xlsx')
    for user in userList:
        currentWorksheet = workbook.add_worksheet(user.id)
        rowCounters = [0] * 18
        
        __writeToWorkbook(currentWorksheet, rowCounters, 0, "Breeding (commented)")
        __writeToWorkbook(currentWorksheet, rowCounters, 1, "Breeding (mentioned)")
        __writeToWorkbook(currentWorksheet, rowCounters, 2, "Breeding (used)")
        __writeToWorkbook(currentWorksheet, rowCounters, 3, "Ownership (commented)")
        __writeToWorkbook(currentWorksheet, rowCounters, 4, "Ownership (mentioned)")
        __writeToWorkbook(currentWorksheet, rowCounters, 5, "Ownership (used)")
        __writeToWorkbook(currentWorksheet, rowCounters, 6, "Corrections (commented)")
        __writeToWorkbook(currentWorksheet, rowCounters, 7, "Corrections (mentioned)")
        __writeToWorkbook(currentWorksheet, rowCounters, 8, "Corrections (used)")
        __writeToWorkbook(currentWorksheet, rowCounters, 9, "Abandoned (commented)")
        __writeToWorkbook(currentWorksheet, rowCounters, 10, "Abandoned (mentioned)")
        __writeToWorkbook(currentWorksheet, rowCounters, 11, "Abandoned (used)")
        __writeToWorkbook(currentWorksheet, rowCounters, 12, "Tokotines (commented)")
        __writeToWorkbook(currentWorksheet, rowCounters, 13, "Tokotines (mentioned)")
        __writeToWorkbook(currentWorksheet, rowCounters, 14, "Tokotines (used)")
        __writeToWorkbook(currentWorksheet, rowCounters, 15, "Misc (commented)")
        __writeToWorkbook(currentWorksheet, rowCounters, 16, "Misc (mentioned)")
        __writeToWorkbook(currentWorksheet, rowCounters, 17, "Misc (used)")
        currentWorksheet.freeze_panes(1, 0)
        for search in user.searches:
            maxCounter = max(rowCounters)
            for x in range(1, 18):
                rowCounters[x] = maxCounter+1
            currentWorksheet.write(maxCounter, 0, search.searchString)
            rowCounters[0] += 1

            if isinstance(search, SearchResults):
                for link in search.commented:
                    column = int(ThreadType[link.origin])
                    __writeToWorkbook(currentWorksheet, rowCounters, column, link.html)

                for link in search.mentionedIn:
                    column = int(ThreadType[link.origin]) + 1
                    __writeToWorkbook(currentWorksheet, rowCounters, column, link.html)

                for link in search.used:
                    column = int(ThreadType[link.origin]) + 2
                    __writeToWorkbook(currentWorksheet, rowCounters, column, link.html)
                pass
            elif isinstance(search, Tokota):
                commented = list(set(sum([search.tokotnaId.commented, search.deviationId.commented, search.favMeLink.commented], [])))
                mentioned = list(set(sum([search.tokotnaId.mentionedIn, search.deviationId.mentionedIn, search.favMeLink.mentionedIn], [])))
                used = list(set(sum([search.tokotnaId.used, search.deviationId.used, search.favMeLink.used], [])))

                for link in commented:
                    column = int(ThreadType[link.origin])
                    __writeToWorkbook(currentWorksheet, rowCounters, column, link.html)
                
                for link in mentioned:
                    column = int(ThreadType[link.origin]) + 1
                    __writeToWorkbook(currentWorksheet, rowCounters, column, link.html)

                for link in used:
                    column = int(ThreadType[link.origin]) + 2
                    __writeToWorkbook(currentWorksheet, rowCounters, column, link.html)
                pass
    workbook.close()

def __writeToWorkbook(worksheet, rowCounter, column, value):
    worksheet.write(rowCounter[column], column, value)
    rowCounter[column] += 1

class ThreadType(IntEnum):
    breeding = 0
    ownership = 3
    corrections = 6
    abandoned = 9
    tokotines = 12
    misc = 15
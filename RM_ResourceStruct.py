from ResourceStruct_item import ResourceStruct_item
from datetime import datetime

def sortGetIndex(item):
        return item.getIndexFrom()

class RM_ResourceStruct:  
    def __init__(self, totalSize, minChunk):
        print("RM_ResourceStruct created")
        self.totalSize = totalSize
        self.minChunk = minChunk
        initItem = ResourceStruct_item(True, datetime.now(), datetime.now(), 0, totalSize, 0)
        self.listOfItems = [initItem]
        self.actualTimeTest = 0

    def addItemToStruct(self, fromTime, toTime, size, ownerID):
        self.clearSpace()
        if size < self.minChunk:
            size = self.minChunk

        for structItem in self.listOfItems:
            if structItem.isFree == True and structItem.size >= size:   
                newItem = ResourceStruct_item(False, fromTime, toTime, structItem.indexFrom, size, ownerID)
                structItem.setIndexFrom((structItem.indexFrom + size))
                structItem.setSize((structItem.size - size))
                self.listOfItems.append(newItem)
                self.listOfItems.sort(key = sortGetIndex)
                return 0
        
        return -1 #not enought space

    def getActualTime(self):
        now = datetime.now()
        return now

    def clearSpace(self):
        actualTime = self.getActualTime()
        print("ClearSpace at:" + str(actualTime))
        newSpace = False
        for index in range(len(self.listOfItems)):
            if self.listOfItems[index].toTime < actualTime and self.listOfItems[index].isFree == False:
                self.listOfItems[index].isFree = True
                self.listOfItems[index].ownerID = datetime.now()
                self.listOfItems[index].fromTime = datetime.now()
                self.listOfItems[index].toTime = datetime.now()
                newSpace = True

        if newSpace == True:
            while True: #needed for update of "self.listOfItems.count"
                escapeWhile = True
                for index in range(len(self.listOfItems) - 1):
                    if self.listOfItems[index].isFree == True and self.listOfItems[index + 1].isFree == True:
                        escapeWhile = False
                        self.listOfItems[index].setSize((self.listOfItems[index].size + self.listOfItems[index + 1].size))
                        self.listOfItems.pop(index + 1)
                        break

                if escapeWhile == True:
                    break
        return

    def getTotalFreeSpace(self):
        self.clearSpace()
        totalFreeSpace = 0
        for structItem in self.listOfItems:
            if structItem.isFree == True:
                totalFreeSpace = totalFreeSpace + structItem.size
        return totalFreeSpace

    def getMaxChunkOfFreeSpace(self):
        self.clearSpace()
        maxChunk = 0
        for structItem in self.listOfItems:
            if structItem.isFree == True and structItem.size > maxChunk:
                maxChunk = structItem.size
        return maxChunk
        
    def printListOfItems(self):
        print("\nStruct:")
        for x in self.listOfItems:
            print("  Item")
            print("    isFree: " + str(x.isFree))
            print("    fromTime: " + str(x.fromTime))
            print("    toTime: " + str(x.toTime))
            print("    indexFrom: " + str(x.indexFrom))
            print("    size: " + str(x.size))
            print("    ownerID: " + str(x.ownerID))
            print("")
        print("-----------------")
        return

    
from ResourceStruct_item import ResourceStruct_item
from datetime import datetime

def sortGetIndex(item):
        return item.getIndexFrom()

class RM_ResourceStruct:  
    def __init__(self, totalSize, minChunk, id):
        print("RM_ResourceStruct created")
        self.totalSize = totalSize
        self.minChunk = minChunk
        initItem = ResourceStruct_item(True, datetime.now(), 0, totalSize, 0)
        self.listOfItems = [initItem]
        self.id = id

    def addItemToStruct(self, size, ownerID):
        fromTime = self.getActualTime();
        if size < self.minChunk:
            size = self.minChunk

        for structItem in self.listOfItems:
            if structItem.isFree == True and structItem.size >= size:   
                newItem = ResourceStruct_item(False, fromTime, structItem.indexFrom, size, ownerID)
                structItem.setIndexFrom((structItem.indexFrom + size))
                structItem.setSize((structItem.size - size))
                self.listOfItems.append(newItem)
                self.listOfItems.sort(key = sortGetIndex)
                return 0
        
        return -1 #not enought space

    def getActualTime(self):
        now = datetime.now()
        return now

    def deleteItemFromStruct(self, ownerID):
        removeThisItems = []
        retValue = -1 
        for index in range(len(self.listOfItems)):
            if self.listOfItems[index].ownerID == ownerID:
                self.listOfItems[index].isFree = True
                self.listOfItems[index].fromTime = self.getActualTime();
                self.listOfItems[index].ownerID = 0
                retValue = 0

                if index < (len(self.listOfItems) - 1):
                    if self.listOfItems[index + 1].isFree == True: #the neighbour on the right is free
                        self.listOfItems[index].setSize((self.listOfItems[index].size + self.listOfItems[index + 1].size))
                        removeThisItems.append(index + 1)

                if index > 0:
                    if self.listOfItems[index - 1].isFree == True: #the neighbour on the left is free
                        self.listOfItems[index - 1].setSize((self.listOfItems[index].size + self.listOfItems[index - 1].size))
                        self.listOfItems[index - 1].fromTime = self.getActualTime();
                        removeThisItems.append(index)

        for index in removeThisItems:
            self.listOfItems.pop(index)

        return retValue

    def getTotalFreeSpace(self):
        totalFreeSpace = 0
        for structItem in self.listOfItems:
            if structItem.isFree == True:
                totalFreeSpace = totalFreeSpace + structItem.size
        return totalFreeSpace

    def getMaxChunkOfFreeSpace(self):
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
            print("    indexFrom: " + str(x.indexFrom))
            print("    size: " + str(x.size))
            print("    ownerID: " + str(x.ownerID))
            print("")
        print("-----------------")
        return

    
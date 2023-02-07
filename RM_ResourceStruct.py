from ResourceStruct_item import ResourceStruct_item

def sortGetIndex(item):
        return item.getIndexFrom()

class RM_ResourceStruct:  
    def __init__(self, totalSize, minChunk):
        print("RM_ResourceStruct created")
        self.totalSize = totalSize
        self.minChunk = minChunk
        initItem = ResourceStruct_item(True, 0, 0, 0, totalSize, 0)
        self.listOfItems = [initItem]

    def addItemToStruct(self, fromTime, toTime, size, ownerID):
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

    
class ResourceStruct_item:  
    def __init__(self, isFree, fromTime, indexFrom, size, ownerID):
        print("RM item created")
        self.isFree = isFree
        self.fromTime = fromTime
        self.indexFrom = indexFrom
        self.size = size
        self.ownerID = ownerID

    def setSize(self, newSize):
        self.size = newSize

    def setIndexFrom(self, newIndexFrom):
        self.indexFrom = newIndexFrom

    def getIndexFrom(self):
        return  self.indexFrom

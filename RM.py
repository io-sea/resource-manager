from Tables import *
from ResourceAllocation import ResourceAllocation
from ResourceDeallocation import ResourceDeallocation

class ResourceManager:  
    def __init__(self):
        print("RM created")
        self.res_alloc = ResourceAllocation()
        self.res_dealloc = ResourceDeallocation()
        self.engine = create_engine("mysql://root:heslo@localhost/test")
        makeTables(self.engine)
        
    def control(self):
        print("RM control")
    
    def allocRequest(self, servers, cores, msize, ssize):
        print("allocRequest:" + str(servers) + "  " + str(cores) + "  " + str(msize) + "  " + str(ssize))
        self.res_alloc.makeAllocation(self.engine, servers, msize, ssize, cores)
        res = self.res_alloc.getRetJSON();
        return res
        
    def deleteSession(self, groupAllocId):
        print("deleteSession:" + str(groupAllocId))
        res = self.res_dealloc.deallocGroup(self.engine, groupAllocId)
        return res

    def deleteAllSessions(self):
        print("deleteAllSessions:")
        res = self.res_dealloc.deallocAllSpace(self.engine)
        return res
        
    def getSessions(self):
        retSessions = []
        idMap = []
        for x in idMap:
            retSessions.append(str(x))
        return retSessions

    
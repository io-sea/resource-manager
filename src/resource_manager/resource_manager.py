from tables import *
from resource_allocation import resource_allocation
from resource_deallocation import resource_deallocation
from assigned_resource import assigned_resource

class resource_manager:  
    def __init__(self):
        print("RM created")
        self.res_alloc = resource_allocation()
        self.res_dealloc = resource_deallocation()
        self.assigned_resource = assigned_resource()
        self.engine = create_engine("mysql+pymysql://root:heslo@localhost/test")
        makeTables(self.engine)
        
    def control(self):
        print("RM control")
    
    def allocRequest(self, name, user, user_slurm_token, es_type, servers, cores, msize, ssize):
        print("allocRequest:" + str(name) + "  " + str(user) + "  " + str(user_slurm_token) + "  " + str(es_type) + "  " + str(servers) + "  " + str(cores) + "  " + str(msize) + "  " + str(ssize))
        self.res_alloc.makeAllocation(self.engine, name, user, user_slurm_token, es_type, servers, msize, ssize, cores)
        res = self.res_alloc.getRetJSON();
        return res

    def getFlavorProperty(self, name):
        print("getFlavorProperty:" + str(name))
        res = self.res_alloc.getFlavorSettings(self.engine, name);
        print("res1: " + str(res))
        return res

    def getAssignedResource(self, name):
        print("getAssignedResource:" + str(name))
        res = self.assigned_resource.getAssignedResource(self.engine, name)
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

    
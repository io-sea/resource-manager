from tables import *
from resource_allocation import resource_allocation
from resource_deallocation import resource_deallocation
from assigned_resource import assigned_resource
from server_resource import server_resource

class resource_manager:  
    def __init__(self):
        print("RM created")
        self.res_alloc = resource_allocation()
        self.res_dealloc = resource_deallocation()
        self.assigned_resource = assigned_resource()
        self.server_resource = server_resource()
        self.engine = create_engine("mysql+pymysql://root:heslo@localhost/test")
        makeTables(self.engine)
        
    def control(self):
        print("RM control")
    
    def allocRequest(self, name, user, user_slurm_token, es_type, servers, cores, msize, ssize, targets, mountpoint, location):
        print("allocRequest:" + str(name) + "  " + str(user) + "  " + str(user_slurm_token) + "  " + str(es_type) + "  " + str(servers) + "  " + str(cores) + "  " + str(msize) + "  " + str(ssize) + "  " + str(targets) + "  " + str(mountpoint)+ "  " + str(location))
        self.res_alloc.makeAllocation(self.engine, name, user, user_slurm_token, es_type, servers, msize, ssize, cores, targets, mountpoint, location)
        return name

    def getFlavorProperty(self, name):
        print("getFlavorProperty:" + str(name))
        res = self.res_alloc.getFlavorSettings(self.engine, name);
        print("res1: " + str(res))
        return res

    def getAssignedResource(self, name):
        print("getAssignedResource:" + str(name))
        res = self.assigned_resource.getAssignedResource(self.engine, name)
        return res

    def getServerResource(self, name):
        print("getServerResource:" + str(name))
        res = self.server_resource.getServerResource(self.engine, name)
        return res

    def getAllServersResource(self):
        print("getAllServersResource()")
        res = self.server_resource.getAllServersResource(self.engine)
        return res
        
    def deleteSession(self, delete_name):
        print("deleteSession:" + str(delete_name))
        res = self.res_dealloc.deallocGroup(self.engine, delete_name)
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

    
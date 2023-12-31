from tables import *
from resource_allocation import resource_allocation
from resource_deallocation import resource_deallocation
from resource_info import resource_info
from assigned_resource import assigned_resource
from server_resource import server_resource
from init_db import init_db
from settings import settings


class resource_manager:  
    def __init__(self):
        print("RM created")
        self.res_alloc = resource_allocation()
        self.res_dealloc = resource_deallocation()
        self.res_info = resource_info()
        self.assigned_resource = assigned_resource()
        self.server_resource = server_resource()
        self.init_db = init_db()
        self.sett = settings()
        ret = self.sett.loadConfig()
        if(ret == -1):
            return
        connect_string = "mysql+pymysql://" + self.sett.getDicValue("db_user") + ":" + self.sett.getDicValue("db_password") + "@mysql/" + self.sett.getDicValue("db_schem")
        #connect_string = "mysql+pymysql://" + self.sett.getDicValue("db_user") + ":" + self.sett.getDicValue("db_password") + "@" + self.sett.getDicValue("db_adress") + "/" + self.sett.getDicValue("db_schem")
        
        #self.engine = create_engine("mysql+pymysql://root:heslo@158.196.17.182/test", connect_args= dict(host='158.196.17.182', port=3306))
        self.engine = create_engine(connect_string)
        
        makeTables(self.engine)
        
    def control(self):
        print("RM control")
    
    def allocRequest(self, name, user, user_slurm_token, es_type, servers, cores, msize, ssize, targets, mountpoint, location):
        print("allocRequest:" + str(name) + "  " + str(user) + "  " + str(user_slurm_token) + "  " + str(es_type) + "  " + str(servers) + "  " + str(cores) + "  " + str(msize) + "  " + str(ssize) + "  " + str(targets) + "  " + str(mountpoint)+ "  " + str(location))
        res = self.res_alloc.makeAllocation(self.engine, name, user, user_slurm_token, es_type, servers, msize, ssize, cores, targets, mountpoint, location, False)
        return res

    def getFlavorProperty(self, name):
        print("getFlavorProperty:" + str(name))
        res = self.res_alloc.getFlavorSettings(self.engine, name);
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
        update = self.res_alloc.updateQueue(self.engine)
        return res

    def deleteAllSessions(self):
        print("deleteAllSessions:")
        res = self.res_dealloc.deallocAllSpace(self.engine)
        return res

    def initDB(self, settings):
        print("initDB:")
        ret = self.init_db.init_all(self.engine, settings)
        return ret
        
    def getSessions(self):
        retSessions = []
        idMap = []
        for x in idMap:
            retSessions.append(str(x))
        return retSessions

    def getQueueInfo(self):
        print("getQueue:")
        res = self.res_info.getQueueInfo(self.engine)
        return res
    
    def getAllocInfo(self):
        print("getAllocInfo:")
        res = self.res_info.getAllocInfo(self.engine)
        return res
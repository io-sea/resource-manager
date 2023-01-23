class ResourceManager:  
    def __init__(self):
        print("RM created")
        self.id = 0
        self.idMap = {}
        
    def control(self):
        print("RM control")
    
    def allocRequest(self, servers, cores, msize, ssize):
        print("allocRequest:" + str(servers) + "  " + str(cores) + "  " + str(msize) + "  " + str(ssize))
        self.id += 1
        allocId = self.id
        self.idMap[allocId] = "Up"
        res = self.getRetJSON(allocId, servers)
        return res
        
    def deleteSession(self, allocId):
        print("deleteSession:" + str(allocId))
        self.idMap.pop(allocId)
        return
        
    def getRetJSON(self, allocId, servers):
        retProperties = []
        
        serverCoresInfo = [4, 5, 6, 7, 12, 13, 14, 15];
        serverName = "server0"
        coresCount = 8
        msizeAlloc = 6
        ssizeAlloc = 6
        
        serverInfo = {"name": serverName, "cores": coresCount, "core_list": serverCoresInfo, "msize": msizeAlloc, "ssize": ssizeAlloc}
        retProperties.append(serverInfo)
        
        retId = allocId
        retServers = servers
        return {"id": retId, "servers": servers, "properties": retProperties}
        
    def getSessions(self):
        retSessions = []
        for x in self.idMap:
            retSessions.append(str(x))
        return retSessions

    
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
        iallocId = self.id
        self.idMap[id] = "Up"
        res = self.getRetJSON(iallocId, servers)
        return res
    
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
    
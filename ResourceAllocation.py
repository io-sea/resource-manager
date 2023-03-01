from Tables import *

class ResourceAllocation:
    def __init__(self):
        print("Alloc_class created")
        self.allocated_group_id = -1
        self.allocated_Server_count = -1
        self.allocated_RAM_size = []
        self.allocated_disk_size = []
        self.allocated_Core_count = []
        self.allocated_Core_arr = []
        self.allocated_Server_Name = []
        self.correctUpload = False

    def makeAllocation(self, engine, server_count, RAM_size, disk_size, core_count):
        self.allocated_group_id = -1
        self.allocated_Server_count = -1
        self.allocated_RAM_size = []
        self.allocated_disk_size = []
        self.allocated_Core_count = []
        self.allocated_Core_arr = []
        self.allocated_Server_Name = []
        self.correctUpload = False

        with engine.connect() as conn:
            free_servers = self.findFreeServers(conn, server_count, RAM_size, disk_size, core_count);
            if(free_servers[0] == -1):
                return -1;

            result = conn.execute(insert(GroupAllocation).values(valid=True, time_of_allocation=func.now()))
            group_alloc_id_new = result.inserted_primary_key[0]
            self.allocated_group_id = group_alloc_id_new
            self.allocated_Server_count = server_count

            for server_id in free_servers:
                self.addAllocToServer(conn, server_id, RAM_size, disk_size, core_count, group_alloc_id_new)
                server_row = conn.execute(select(Server).where(Server.id == server_id)).first()
                self.allocated_Server_Name.append(server_row.name)

            conn.commit()
            self.correctUpload = True
            print(self.getRetJSON())
            return group_alloc_id_new;

    def addAllocItem(self, conn, resource_id, size, group_alloc_id, is_core_type, core_count):
        stmt = insert(Allocation).values(resource_id=resource_id, size=size, group_allocation_id=group_alloc_id)
        result = conn.execute(stmt)
        allocation_id = result.inserted_primary_key[0]
        resource = conn.execute(select(Resource).where(Resource.id == resource_id)).first()
        free_space_actual = resource.free_space - size
        stmt = update(Resource).values(free_space=free_space_actual).where(Resource.id == resource_id)
        result = conn.execute(stmt)
        if(is_core_type == True):
            free_cores = self.findFreeCores(conn, resource_id, core_count)
            self.allocated_Core_arr.append(free_cores)
            for free_core in free_cores:
                result = conn.execute(insert(Core).values(index=free_core, alloc_id=allocation_id))

    def addAllocToServer(self, conn, server_id, RAM_size, disk_size, core_count, group_alloc_id):
        RAM_row = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 1)).first()
        if(RAM_size < RAM_row.min_chunk):
            RAM_size = RAM_row.min_chunk
        self.addAllocItem(conn, RAM_row.id, RAM_size, group_alloc_id, False, 0)
        self.allocated_RAM_size.append(RAM_size)

        disk_row = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 2)).first()
        if(disk_size < disk_row.min_chunk):
            disk_size = disk_row.min_chunk
        self.addAllocItem(conn, disk_row.id, disk_size, group_alloc_id, False, 0)
        self.allocated_disk_size.append(disk_size)

        CPU_row = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 3)).first()
        if(core_count < CPU_row.min_chunk):
            core_count = CPU_row.min_chunk
        self.addAllocItem(conn, CPU_row.id, core_count, group_alloc_id, True, core_count)
        self.allocated_Core_count.append(core_count)

    def findFreeServers(self, conn, server_count, RAM_size, disk_size, core_count):
        #RAM_id = 1, disk_id = 2, CPU_ID = 3
        free_servers = []
        count_of_found_servers = 0;
        for row in conn.execute(select(Server)):
            if(self.serverFreeSpaceResource(conn, row.id, RAM_size, 1) == True and self.serverFreeSpaceResource(conn, row.id, disk_size, 2) == True and self.serverFreeSpaceResource(conn, row.id, core_count, 3) == True):
                free_servers.append(row.id)
                count_of_found_servers = count_of_found_servers + 1
                if(count_of_found_servers == server_count):
                    return free_servers
        free_servers = [-1]
        return free_servers

    def serverFreeSpaceResource(self, conn, server_id, resource_size, resource_type_id):
        resource_row = conn.execute(select(Resource).where(Resource.resource_type_id == resource_type_id).where(Resource.server_id == server_id)).first()
        if(resource_row == None):
            return False
        if(resource_size < resource_row.min_chunk):
            resource_size = resource_row.min_chunk
        if(resource_size <= resource_row.free_space):
            return True
        else:
            return False

    def findFreeCores(self, conn, resource_id, core_count):  
        CPU_row = conn.execute(select(Resource).where(Resource.id == resource_id)).first()
        CPU_max_size = CPU_row.max_size
        stmt = select(Resource, Core).where(Resource.id == resource_id).where(GroupAllocation.valid == True).join_from(Allocation, Resource).join_from(Allocation, GroupAllocation).join_from(Allocation, Core)
        allocatedCores = []
        freeCores = []
        
        for row in conn.execute(stmt):
            allocatedCores.append(row.index)  
        cores_added = 0

        for i in range(CPU_max_size):
            if(allocatedCores.count(i) == 0):
                cores_added = cores_added + 1
                freeCores.append(i)
            if(cores_added == core_count):
                return freeCores

    def printResources(self):
        print("GroupID:" + str(self.allocated_group_id))
        print("  RAM:" + str(self.allocated_RAM_size))
        print("  Disk:" + str(self.allocated_disk_size))
        print("  Core Count:" + str(self.allocated_Core_count))
        print("  Core Arr:" + str(self.allocated_Core_arr))
        print("  Server Name:" + str(self.allocated_Server_Name) + "\n")

    def getRetJSON(self):
        if(self.correctUpload == False):
            return -1

        retProperties = []
        
        for i in range(self.allocated_Server_count):
            serverInfo = {"name": self.allocated_Server_Name[i], "cores": self.allocated_Core_count[i], "core_list": self.allocated_Core_arr[i], "msize": self.allocated_RAM_size[i], "ssize": self.allocated_disk_size[i]}
            retProperties.append(serverInfo)

        return {"id": self.allocated_group_id, "servers": self.allocated_Server_count, "properties": retProperties}

from Tables import *

class ResourceAllocation:
    def __init__(self):
        print("Alloc_class created")

    def makeAllocation(self, engine, server_count, RAM_size, disk_size):
        with engine.connect() as conn:
            free_servers = self.findFreeServers(conn, server_count, RAM_size, disk_size);
            if(free_servers[0] == -1):
                return -1;

            group_alloc_row = conn.execute(select(GroupAllocation).order_by(GroupAllocation.id.desc())).first()
            group_alloc_id_new = group_alloc_row.id + 1
            conn.execute(insert(GroupAllocation).values(id=group_alloc_id_new, valid=True, time_of_allocation=func.now()))

            for server_id in free_servers:
                self.addAllocToServer(conn, server_id, RAM_size, disk_size, group_alloc_id_new)

            conn.commit()
            return group_alloc_id_new;

    def addAllocItem(self, conn, resource_id, size, group_alloc_id):
        stmt = insert(Allocation).values(resource_id=resource_id, size=size, group_allocation_id=group_alloc_id)
        result = conn.execute(stmt)
        resource = conn.execute(select(Resource).where(Resource.id == resource_id)).first()
        free_space_actual = resource.free_space - size
        stmt = update(Resource).values(free_space=free_space_actual).where(Resource.id == resource_id)
        result = conn.execute(stmt)

    def addAllocToServer(self, conn, server_id, RAM_size, disk_size, group_alloc_id):
        RAM_row = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 1)).first()
        if(RAM_size < RAM_row.min_chunk):
            RAM_size = RAM_row.min_chunk
        self.addAllocItem(conn, RAM_row.id, RAM_size, group_alloc_id)

        disk_row = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 2)).first()
        if(disk_size < disk_row.min_chunk):
            disk_size = disk_row.min_chunk
        self.addAllocItem(conn, disk_row.id, disk_size, group_alloc_id)

    def findFreeServers(self, conn, server_count, RAM_size, disk_size):
        #RAM_id = 1, disk_id = 2, CPU_ID = 3
        free_servers = []
        count_of_found_servers = 0;
        for row in conn.execute(select(Server)):
            if(self.serverFreeSpaceRAM(conn, row.id, RAM_size) == True and self.serverFreeSpaceDisk(conn, row.id, disk_size)):
                free_servers.append(row.id)
                count_of_found_servers = count_of_found_servers + 1
                if(count_of_found_servers == server_count):
                    return free_servers
        free_servers = [-1]
        return free_servers


    def serverFreeSpaceRAM(self, conn, server_id, RAM_size):
        RAM_row = conn.execute(select(Resource).where(Resource.resource_type_id == 1).where(Resource.server_id == server_id)).first()
        if(RAM_row == None):
            return False
        if(RAM_size < RAM_row.min_chunk):
            RAM_size = RAM_row.min_chunk
        if(RAM_size <= RAM_row.free_space):
            return True
        else:
            return False

    def serverFreeSpaceDisk(self, conn, server_id, disk_size):
        disk_row = conn.execute(select(Resource).where(Resource.resource_type_id == 2).where(Resource.server_id == server_id)).first()
        if(disk_row == None):
            return False
        if(disk_size < disk_row.min_chunk):
            disk_size = disk_row.min_chunk
        if(disk_size <= disk_row.free_space):
            return True
        else:
            return False


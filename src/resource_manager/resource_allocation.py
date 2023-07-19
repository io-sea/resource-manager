from tables import *

class resource_allocation:
    def __init__(self):
        print("Alloc_class created")
        self.allocated_Core_arr = []
        self.correctUpload = False

    def makeAllocation(self, engine, name, user, user_slurm_token, es_type, server_count, RAM_size, disk_size, core_count, targets, mountpoint, location, already_in_queue):
        self.allocated_Core_arr = []
        self.correctUpload = False

        with engine.connect() as conn:
            free_servers = self.findFreeServers(conn, server_count, RAM_size, disk_size, core_count);
            if(free_servers[0] == -1 and already_in_queue == True):
                return 1;

            if((free_servers[0] == -1 or self.isQueueEmpty(conn) == False) and already_in_queue == False):
                self.addToQueue(conn, name, user, user_slurm_token, es_type, server_count, RAM_size, disk_size, core_count, targets, mountpoint, location)
                return -1;

            result = conn.execute(insert(GroupAllocation).values(name=name, user=user, user_slurm_token=user_slurm_token, es_type=es_type, valid=True, time_of_allocation=func.now(), allocation_status = "FREE", targets = targets, mountpoint = mountpoint))
            group_alloc_id_new = result.inserted_primary_key[0]

            if(location != None):
                for server_type in location:
                    conn.execute(insert(Location).values(location=server_type, group_allocation_id=group_alloc_id_new))

            for server_id in free_servers:
                self.addAllocToServer(conn, server_id, RAM_size, disk_size, core_count, group_alloc_id_new)

            if(already_in_queue == True):
                conn.execute(delete(Queue).where(Queue.name == name))
            conn.commit()
            self.correctUpload = True
            return name;

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
        if(RAM_size <= 0):
            RAM_size = 0
        else:
            control_size = RAM_size % RAM_row.min_chunk
            if(control_size != 0):
                RAM_size = RAM_size - control_size + RAM_row.min_chunk
        self.addAllocItem(conn, RAM_row.id, RAM_size, group_alloc_id, False, 0)

        disk_row = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 2)).first()
        if(disk_size <= 0):
            disk_size = 0
        else:
            control_size = disk_size % disk_row.min_chunk
            if(control_size != 0):
                disk_size = disk_size - control_size + disk_row.min_chunk
        self.addAllocItem(conn, disk_row.id, disk_size, group_alloc_id, False, 0)

        CPU_row = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 3)).first()
        if(core_count <= 0):
            core_count = 0
        else:
            control_size = core_count % CPU_row.min_chunk
            if(control_size != 0):
                core_count = core_count - control_size + CPU_row.min_chunk
        self.addAllocItem(conn, CPU_row.id, core_count, group_alloc_id, True, core_count)

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

    def getFlavorSettings(self, engine, name):
        with engine.connect() as conn:
            flavor_row = conn.execute(select(Flavor).where(Flavor.name == name)).first()

            if(flavor_row == None):
                return -1

            flavor_property = {
                "name": name,
                "cores": flavor_row.cores,
                "msize": flavor_row.msize,
                "ssize": flavor_row.ssize
            }
        return flavor_property

    def isQueueEmpty(self, conn):
        queue_row = conn.execute(select(Queue)).first()
        if(queue_row == None):
            return True
        else:
            return False

    def addToQueue(self, conn, name, user, user_slurm_token, es_type, server_count, RAM_size, disk_size, core_count, targets, mountpoint, location):
        if(location != None):
            location = str(location)
        conn.execute(insert(Queue).values(name=name, user=user, user_slurm_token=user_slurm_token, es_type=es_type, server_count=server_count, targets=targets, mountpoint=mountpoint, cores=core_count, msize=RAM_size, ssize=disk_size, location=location))
        conn.commit()
        return

    def updateQueue(self, engine):
        queue_row = None
        location_list = None
        with engine.connect() as conn:
            if(self.isQueueEmpty(conn) == True):
                return 0
            queue_row = conn.execute(select(Queue)).first()
            location = queue_row.location
            
            if(location != None):
                list = location.strip('][').split(', ')
                location_list = []
                for item in list:
                    item = item.strip('\'\'')
                    location_list.append(item)
        self.makeAllocation(engine, queue_row.name, queue_row.user, queue_row.user_slurm_token, queue_row.es_type, queue_row.server_count, queue_row.msize, queue_row.ssize, queue_row.cores, queue_row.targets, queue_row.mountpoint, location_list, True)
        return 0
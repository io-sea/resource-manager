from tables import *

class resource_info:
    def __init__(self):
        print("Resource_info created")

    def getQueueInfo(self, engine):

        with engine.connect() as conn:
            resource = conn.execute(select(Queue)).first()
            res = []

            if(resource == None):
                res.append("Empty")
                return res
            
            res.append("name  user  es_type  server_count  targets  mountpoint  cores  msize  ssize  location")
            print(res)
            for row in conn.execute(select(Queue)):
                print(row)
                res.append("" + str(row.name) + "  " + str(row.user) + "  " + str(row.es_type) + "  " + str(row.server_count) + "  " + str(row.targets) + "  " + str(row.mountpoint) + "  " + str(row.cores) + "  " + str(row.msize) + "  " + str(row.ssize) + "  " + str(row.location))

            return res

    def getAllocInfo(self, engine):
        res = []
        with engine.connect() as conn:
            resource = conn.execute(select(GroupAllocation).where(GroupAllocation.valid == True)).first()
            res = []

            if(resource == None):
                res.append("Empty")
                return res

            for row in conn.execute(select(GroupAllocation).where(GroupAllocation.valid == True)):
                print(row)

                group_alloc_id = row.id

                server_IDs = []
                servers_info = []
                for resource_info_row in conn.execute(select(Resource).where(Allocation.group_allocation_id == group_alloc_id).join_from(Allocation, Resource)):
                    #print(server_info_row)
                    if((resource_info_row.server_id in server_IDs) == False):
                        server_IDs.append(resource_info_row.server_id)
                
                for server_id in server_IDs:
                    server_row = conn.execute(select(Server).where(Server.id == server_id)).first()
                    RAM_size = 0
                    disk_size = 0
                    CPU_size = 0

                    resource_row_RAM = conn.execute(select(Allocation, Resource).where(Allocation.group_allocation_id == group_alloc_id).where(Resource.resource_type_id == 1).where(Resource.server_id == server_id).join_from(Allocation, Resource)).first()
                    if(resource_row_RAM != None):
                        RAM_size = resource_row_RAM.size

                    resource_row_disk = conn.execute(select(Allocation, Resource).where(Allocation.group_allocation_id == group_alloc_id).where(Resource.resource_type_id == 2).where(Resource.server_id == server_id).join_from(Allocation, Resource)).first()
                    if(resource_row_RAM != None):
                        disk_size = resource_row_disk.size

                    resource_row_CPU = conn.execute(select(Allocation, Resource).where(Allocation.group_allocation_id == group_alloc_id).where(Resource.resource_type_id == 3).where(Resource.server_id == server_id).join_from(Allocation, Resource)).first()
                    if(resource_row_RAM != None):
                        CPU_size = resource_row_CPU.size
                    
                    server_info_property = {
                        "name": server_row.name,
                        "cores": CPU_size,
                        "msize": RAM_size,
                        "ssize": disk_size
                    }

                    servers_info.append(server_info_property)


                alloc_info_property = {
                    "name": row.name,
                    "user": row.user,
                    "es_type": row.es_type,
                    "targets": row.targets,
                    "mountpoint": row.mountpoint,
                    "allocation_status": row.allocation_status,
                    "time_of_allocation": str(row.time_of_allocation),
                    "servers_count": len(server_IDs),
                    "servers": servers_info,
                }

                res.append(alloc_info_property)
                
        return res
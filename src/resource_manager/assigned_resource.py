from .tables import *

class assigned_resource:
    def __init__(self):
        print("assigned_resource created")

    def getAssignedResource(self, engine, name):
        with engine.connect() as conn:
            group_alloc_row = conn.execute(select(GroupAllocation).where(GroupAllocation.name == name).where(GroupAllocation.valid == True)).first()
            print(group_alloc_row)
            if (group_alloc_row == None):
                return -1
            if (group_alloc_row.allocation_status == "ALLOCATED"):
                return -2

            group_alloc_row = conn.execute(select(GroupAllocation).where(GroupAllocation.name == name).where(GroupAllocation.valid == True)).first()
            group_alloc_id = group_alloc_row.id

            assigned_servers_ids = []
            
            stmt = select(Server).where(Allocation.group_allocation_id == group_alloc_id).join_from(Allocation, Resource).join_from(Resource, Server).distinct()
            for row in conn.execute(stmt):
                assigned_servers_ids.append(row.id)

            properties = []

            for server_id in assigned_servers_ids:
                server_row = conn.execute(select(Server).where(Server.id == server_id)).first()
                server_name = server_row.name

                #CPU
                resource_row_cpu = conn.execute(select(Allocation, Resource).where(Allocation.group_allocation_id == group_alloc_id).where(Resource.server_id == server_id).where(Resource.resource_type_id == 3).join_from(Allocation, Resource)).first()
                allocation_row = conn.execute(select(Allocation).where(Allocation.group_allocation_id == group_alloc_id).where(Resource.server_id == server_id).where(Resource.resource_type_id == 3).join_from(Allocation, Resource)).first()
                cores = []
                for row in conn.execute(select(Core).where(Core.alloc_id == allocation_row.id)):
                    cores.append(row.index)

                #RAM
                resource_row_ram = conn.execute(select(Allocation, Resource).where(Allocation.group_allocation_id == group_alloc_id).where(Resource.server_id == server_id).where(Resource.resource_type_id == 1).join_from(Allocation, Resource)).first()
                msize = resource_row_ram.size

                #Disk
                resource_row_disk = conn.execute(select(Allocation, Resource).where(Allocation.group_allocation_id == group_alloc_id).where(Resource.server_id == server_id).where(Resource.resource_type_id == 2).join_from(Allocation, Resource)).first()
                ssize = resource_row_disk.size

                server_property = {
                    "server_name": server_name,
                    "cores": len(cores),
                    "core_list": cores,
                    "msize": msize,
                    "ssize": ssize
                }

                properties.append(server_property)

            server_allocation_respons = {
                "name": name,
                "servers": len(properties),
                "properties": properties
            }

            #print(server_allocation_respons)

            conn.execute(update(GroupAllocation).values(allocation_status = 'ALLOCATED').where(GroupAllocation.id == group_alloc_id))
            conn.commit()
            
            return server_allocation_respons

from tables import *

class server_resource:
    def __init__(self):
        print("server_resource created")

    def getServerResource(self, engine, name):
        with engine.connect() as conn:
            server_row = conn.execute(select(Server).where(Server.name == name)).first()
            if(server_row == None):
                return -1
            server_id = server_row.id

            #RAM
            resource_row_ram = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 1)).first()
            msize = resource_row_ram.max_size
            free_msize = resource_row_ram.free_space

            #Disk
            resource_row_disk = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 2)).first()
            ssize = resource_row_disk.max_size
            free_ssize = resource_row_disk.free_space

            #CPU
            resource_row_cpu = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 3)).first()
            cores = resource_row_cpu.max_size
            free_cores = resource_row_cpu.free_space

            free_core_list = []
            core_list = []
            for x in range(cores):
                core_list.append(x)

            allocated_core_list = []
            for row in conn.execute(select(Core).join_from(Core, Allocation).join_from(Allocation, GroupAllocation).where(Allocation.resource_id == resource_row_cpu.id).where(GroupAllocation.valid == True)):
                allocated_core_list.append(row.index)

            for core in core_list:
                if(allocated_core_list.count(core) == 0):
                    free_core_list.append(core)

            server_resource = {
                    "free_cores": free_cores,
                    "cores": cores,
                    "free_core_list": free_core_list,
                    "core_list": core_list,
                    "free_msize": free_msize,
                    "msize": msize,
                    "free_ssize": free_ssize,
                    "ssize": ssize
            }

        return server_resource

    def getAllServersResource(self, engine):

        with engine.connect() as conn:
            result = []
            for row in conn.execute(select(Server)):
                server_resources = self.getServerResource(engine, row.name)
                server = {
                    "server_name": row.name,
                    "server_resources": server_resources
                }
                result.append(server)
            return result

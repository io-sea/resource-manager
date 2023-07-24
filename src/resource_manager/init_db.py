from tables import *
from logger import *

class init_db:
    def __init__(self):
        print("Init_db created")

    def init_all(self, engine, settings):
        ret = self.test(engine, settings)
        if(ret != 0):
            return ret

        self.init_resource_type(engine)
        self.init_servers(engine, settings)
        self.init_flavors(engine, settings)
        return 0

    def test(self, engine, settings):
        with engine.connect() as conn:
            res = conn.execute(select(ResourceType)).first()

            if(res != None):
                print("Init_db call - Error - Init already done")
                rm_logger.info('Init_db call - Error - Init already done')
                return -1

            try:
                print(settings["path_to_servers_init"])
                file = open(settings["path_to_servers_init"], 'r')
                file.close()
            except:
                print("Init_db call - Error - Readfile failed - servers_init.txt")
                rm_logger.info('Init_db call - Error - Readfile failed - servers_init.txt')
                return -2

            try:
                print(settings["path_to_flavors_init"])
                file = open(settings["path_to_flavors_init"], 'r')
                file.close()
            except:
                print("Init_db call - Error - Readfile failed - flavors_init.txt")
                rm_logger.info('Init_db call - Error - Readfile failed - flavors_init.txt')
                return -3
            
        return 0
        
    def init_resource_type(self, engine):
        with engine.connect() as conn:
            result = conn.execute(insert(ResourceType).values(id=1, name="RAM"))
            result = conn.execute(insert(ResourceType).values(id=2, name="Disk"))
            result = conn.execute(insert(ResourceType).values(id=3, name="CPU"))

            conn.commit()
            return 0

    def init_servers(self, engine, settings):
        with engine.connect() as conn:
            lines = []
            with open(settings["path_to_servers_init"]) as file:
                lines = [line.rstrip() for line in file]
            
            id = 1
            for item in lines:
                print("server:" + item)
                rm_logger.info('Init_db call - Add Server: ' + item)
                split_line = item.split(" ")
            
                name = split_line[0]
                max_size_RAM = split_line[1]
                free_space_RAM = split_line[2]
                min_chunk_RAM = split_line[3]

                max_size_Disk = split_line[4]
                free_space_Disk = split_line[5]
                min_chunk_Disk = split_line[6]

                max_size_CPU = split_line[7]
                free_space_CPU = split_line[8]
                min_chunk_CPU = split_line[9]

                conn.execute(insert(Server).values(id=id, name=name))
                conn.execute(insert(Resource).values(server_id=id, resource_type_id=1, max_size=max_size_RAM, free_space=free_space_RAM, min_chunk=min_chunk_RAM))
                conn.execute(insert(Resource).values(server_id=id, resource_type_id=2, max_size=max_size_Disk, free_space=free_space_Disk, min_chunk=min_chunk_Disk))
                conn.execute(insert(Resource).values(server_id=id, resource_type_id=3, max_size=max_size_CPU, free_space=free_space_CPU, min_chunk=min_chunk_CPU))

                id += 1

            conn.commit()
            return 0

    def init_flavors(self, engine, settings):
        with engine.connect() as conn:
            lines = []
            with open(settings["path_to_flavors_init"]) as file:
                lines = [line.rstrip() for line in file]

            id = 1
            for item in lines:
                print("Flavor:" + item)
                rm_logger.info('Init_db call - Add Flavor: ' + item)
                split_line = item.split(" ")

                name = split_line[0]
                cores = split_line[1]
                msize = split_line[2]
                ssize = split_line[3]

                conn.execute(insert(Flavor).values(id=id, name=name, cores=cores, msize=msize, ssize=ssize))
                id += 1

            conn.commit()
            return 0

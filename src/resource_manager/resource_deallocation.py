from .tables import *

class resource_deallocation:
    def __init__(self):
        print("Dealloc_class created")

    def deallocItems(self, conn, group_alloc_id):
        stmt = select(Allocation).where(Allocation.group_allocation_id == group_alloc_id)
        for row in conn.execute(stmt):
            resource = conn.execute(select(Resource).where(Resource.id == row.resource_id)).first()
            free_space_actual = resource.free_space + row.size
            stmt = update(Resource).values(free_space=free_space_actual).where(Resource.id == row.resource_id)
            result = conn.execute(stmt)

    def deallocGroup(self, engine, delete_name):
        with engine.connect() as conn:
            group_alloc = conn.execute(select(GroupAllocation).where(GroupAllocation.name == delete_name).where(GroupAllocation.valid == True)).first()
            if(group_alloc == None):
                res = self.deallocFromQueue(conn, delete_name)
                return res
            else:
                self.deallocItems(conn, group_alloc.id)
                conn.execute(update(GroupAllocation).values(valid=False, time_of_deallocation=func.now()).where(GroupAllocation.id == group_alloc.id))
                conn.commit()
                return 0

    def deallocFromQueue(self, conn, delete_name):
        queue_row = conn.execute(select(Queue).where(Queue.name == delete_name)).first()
        if(queue_row == None):
            return -1
        else:
            conn.execute(delete(Queue).where(Queue.id == queue_row.id))
            conn.commit()
            return 1;

    def deallocAllSpace(self, engine):
        with engine.connect() as conn:
            for row in  conn.execute(select(GroupAllocation).where(GroupAllocation.valid == True)):
                self.deallocItems(conn, row.id)
                conn.execute(update(GroupAllocation).values(valid=False, time_of_deallocation=func.now()).where(GroupAllocation.id == row.id))
            conn.commit()





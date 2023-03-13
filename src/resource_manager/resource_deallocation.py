from tables import *

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

    def deallocGroup(self, engine, group_alloc_id):
        with engine.connect() as conn:
            group_alloc = conn.execute(select(GroupAllocation).where(GroupAllocation.id == group_alloc_id)).first()
            if group_alloc.valid == True:
                self.deallocItems(conn, group_alloc_id)
                conn.execute(update(GroupAllocation).values(valid=False, time_of_deallocation=func.now()).where(GroupAllocation.id == group_alloc_id))
                conn.commit()
                return 0
            else:
                return -1

    def deallocAllSpace(self, engine):
        with engine.connect() as conn:
            for row in  conn.execute(select(GroupAllocation).where(GroupAllocation.valid == True)):
                self.deallocItems(conn, row.id)
                conn.execute(update(GroupAllocation).values(valid=False, time_of_deallocation=func.now()).where(GroupAllocation.id == row.id))
            conn.commit()





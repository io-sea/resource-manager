from Tables import *
from ResourceAllocation import ResourceAllocation
from ResourceDeallocation import ResourceDeallocation

engine = create_engine("mysql://root:heslo@localhost/test")
makeTables(engine)

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

def init(engine):
    with engine.connect() as conn:
        stmt = insert(Server).values(id=1, name="Server1")
        result = conn.execute(stmt)
        stmt = insert(Server).values(id=2, name="Server2")
        result = conn.execute(stmt)
        stmt = insert(Server).values(id=3, name="Server3")
        result = conn.execute(stmt)
        stmt = insert(ResourceType).values(id=1, name="RAM")
        result = conn.execute(stmt)
        stmt = insert(ResourceType).values(id=2, name="Disk")
        result = conn.execute(stmt)
        stmt = insert(Resource).values(id=1, server_id=1, resource_type_id=1, max_size=200, free_space = 200, min_chunk=10)
        result = conn.execute(stmt)
        stmt = insert(Resource).values(id=2, server_id=1, resource_type_id=2, max_size=1000, free_space = 1000, min_chunk=100)
        result = conn.execute(stmt)
        stmt = insert(Resource).values(id=3, server_id=2, resource_type_id=1, max_size=200, free_space = 200, min_chunk=10)
        result = conn.execute(stmt)
        stmt = insert(Resource).values(id=4, server_id=2, resource_type_id=2, max_size=1000, free_space = 1000, min_chunk=100)
        result = conn.execute(stmt)
        stmt = insert(GroupAllocation).values(id=1, valid=True, time_of_allocation=func.now())
        result = conn.execute(stmt)
        conn.commit()  

def insertItems():
    print(makeAllocation(engine, 2, 50, 100))
    print(makeAllocation(engine, 1, 50, 100))
    print(makeAllocation(engine, 1, 50, 100))
    print(makeAllocation(engine, 1, 50, 100))


#init(engine)
#insertItems()
res_alloc = ResourceAllocation()
res_dealloc = ResourceDeallocation()
print(res_alloc.makeAllocation(engine, 1, 50, 100))
print(res_dealloc.deallocGroup(engine, 4))


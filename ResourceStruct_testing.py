import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import MetaData, insert, select, update
from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import func

engine = create_engine("mysql://root:heslo@localhost/test")

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

class Base(DeclarativeBase):
    pass

class Server(Base):
    __tablename__ = "server"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    resource: Mapped[List["Resource"]] = relationship(back_populates="server")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

class ResourceType(Base):
    __tablename__ = "resource_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    resource: Mapped[List["Resource"]] = relationship(back_populates="resource_type")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

class Resource(Base):
    __tablename__ = "resource"
    id: Mapped[int] = mapped_column(primary_key=True)
    max_size: Mapped[int] = mapped_column(nullable=False)
    free_space: Mapped[int] = mapped_column(nullable=False)
    min_chunk: Mapped[int] = mapped_column(nullable=False)
    server_id = mapped_column(ForeignKey("server.id"))
    server: Mapped[Server] = relationship(back_populates="resource")
    resource_type_id = mapped_column(ForeignKey("resource_type.id"))
    resource_type: Mapped[ResourceType] = relationship(back_populates="resource")
    allocation: Mapped[List["Allocation"]] = relationship(back_populates="resource")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, max_size={self.max_size!r}, free_space={self.free_space!r}, min_chunk={self.min_chunk!r}, server_id={self.server_id!r}, resource_type_id={self.resource_type_id!r})"

class GroupAllocation(Base):
    __tablename__ = "group_allocation"
    id: Mapped[int] = mapped_column(primary_key=True)
    valid: Mapped[bool] = mapped_column(nullable=False)
    allocation: Mapped[List["Allocation"]] = relationship(back_populates="group_allocation")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, valid={valid.size!r})"

class Allocation(Base):
    __tablename__ = "allocation"
    id: Mapped[int] = mapped_column(primary_key=True)
    size: Mapped[int] = mapped_column(nullable=False)
    resource_id = mapped_column(ForeignKey("resource.id"))
    resource: Mapped[Resource] = relationship(back_populates="allocation")
    group_allocation_id = mapped_column(ForeignKey("group_allocation.id"))
    group_allocation: Mapped[GroupAllocation] = relationship(back_populates="allocation")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, size={self.size!r}, resource_id={self.resource_id!r}, group_allocation_id={self.group_allocation_id!r})"


Base.metadata.create_all(engine)

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
        stmt = insert(GroupAllocation).values(id=1, valid=True)
        result = conn.execute(stmt)

        conn.commit()

def run(engine):
    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in conn.execute(select(Allocation)):
            print(row)
        conn.commit()

def addAllocItem(conn, resource_id, size, group_alloc_id):
    stmt = insert(Allocation).values(resource_id=resource_id, size=size, group_allocation_id=group_alloc_id)
    result = conn.execute(stmt)
    resource = conn.execute(select(Resource).where(Resource.id == resource_id)).first()
    free_space_actual = resource.free_space - size
    stmt = update(Resource).values(free_space=free_space_actual).where(Resource.id == resource_id)
    result = conn.execute(stmt)

def addAllocToServer(conn, server_id, RAM_size, disk_size):
    #RAM_id = 1, disk_id = 2, CPU_ID = 3
    group_alloc_row = conn.execute(select(GroupAllocation).order_by(GroupAllocation.id.desc())).first()
    group_alloc_id_new = group_alloc_row.id + 1

    stmt = insert(GroupAllocation).values(id=group_alloc_id_new, valid=True)
    result = conn.execute(stmt)

    RAM_row = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 1)).first()
    if(RAM_size < RAM_row.min_chunk):
        RAM_size = RAM_row.min_chunk
    addAllocItem(conn, RAM_row.id, RAM_size, group_alloc_id_new)


    disk_row = conn.execute(select(Resource).where(Resource.server_id == server_id).where(Resource.resource_type_id == 2)).first()
    if(disk_size < disk_row.min_chunk):
        disk_size = disk_row.min_chunk
    addAllocItem(conn, disk_row.id, disk_size, group_alloc_id_new)
    

def deallocItems(conn, group_alloc_id):
    stmt = select(Allocation).where(Allocation.group_allocation_id == group_alloc_id)
    for row in conn.execute(stmt):
        resource = conn.execute(select(Resource).where(Resource.id == row.resource_id)).first()
        free_space_actual = resource.free_space + row.size
        stmt = update(Resource).values(free_space=free_space_actual).where(Resource.id == row.resource_id)
        result = conn.execute(stmt)

def deallocGroup(engine, group_alloc_id):
    with engine.connect() as conn:
        group_alloc = conn.execute(select(GroupAllocation).where(GroupAllocation.id == group_alloc_id)).first()
        if group_alloc.valid == True:
            deallocItems(conn, group_alloc_id)
            conn.execute(update(GroupAllocation).values(valid=False).where(GroupAllocation.id == group_alloc_id))
            conn.commit()
            return 0
        else:
            return -1

def insertItems(engine):
    with engine.connect() as conn:
        addAllocToServer(conn, 1, 10, 50)
        addAllocToServer(conn, 1, 20, 200)
        addAllocToServer(conn, 1, 30, 300)
        addAllocToServer(conn, 2, 50, 500)
        conn.commit()


#init(engine)

#insertItems(engine)
deallocGroup(engine, 2)
deallocGroup(engine, 3)
#run(engine)
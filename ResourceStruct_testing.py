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

class Resource(Base):
    __tablename__ = "resource"
    id: Mapped[int] = mapped_column(primary_key=True)
    max_size: Mapped[int] = mapped_column(nullable=False)
    free_space: Mapped[int] = mapped_column(nullable=False)
    min_chunk: Mapped[int] = mapped_column(nullable=False)
    server_id = mapped_column(ForeignKey("server.id"))
    server: Mapped[Server] = relationship(back_populates="resource")
    allocation: Mapped[List["Allocation"]] = relationship(back_populates="resource")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, max_size={self.max_size!r}, free_space={self.free_space!r}, min_chunk={self.min_chunk!r}, server_id={self.server_id!r})"

class Allocation(Base):
    __tablename__ = "allocation"
    id: Mapped[int] = mapped_column(primary_key=True)
    size: Mapped[int] = mapped_column(nullable=False)
    resource_id = mapped_column(ForeignKey("resource.id"))
    resource: Mapped[Resource] = relationship(back_populates="allocation")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, size={self.size!r}, resource_id={self.resource_id!r})"

Base.metadata.create_all(engine)

def init(engine):
    with engine.connect() as conn:
        stmt1 = insert(Server).values(id=1, name="Server1")
        stmt2 = insert(Resource).values(id=1, server_id=1, max_size=100, free_space = 100, min_chunk=10)
        stmt3 = insert(Allocation).values(resource_id=1, size=10)
        stmt4 = insert(Allocation).values(resource_id=1, size=10)
        result = conn.execute(stmt1)
        result = conn.execute(stmt2)
        result = conn.execute(stmt3)
        result = conn.execute(stmt4)
        conn.commit()

def run(engine):
    with engine.connect() as conn:
        for row in conn.execute(select(Allocation)):
            print(row)
        conn.commit()

def addAllocItem(engine, resource_id, size):
    with engine.connect() as conn:
        stmt = insert(Allocation).values(resource_id=resource_id, size=size)
        print(stmt)
        result = conn.execute(stmt)
        resource = conn.execute(select(Resource).where(Resource.id == resource_id)).first()
        free_space_actual = resource.free_space - size
        stmt = update(Resource).values(free_space=free_space_actual).where(Resource.id == resource_id)
        print(stmt)
        result = conn.execute(stmt)
        conn.commit()

#init(engine)
addAllocItem(engine, 1, 50)
#run(engine)
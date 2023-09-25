import sqlalchemy
from sqlalchemy import create_engine, MetaData, insert, select, update, delete
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, text, ForeignKey, func, bindparam
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
import time
from datetime import datetime
from logger import *

class Base(DeclarativeBase):
    pass

class Server(Base):
    __tablename__ = "server"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    resource: Mapped[List["Resource"]] = relationship(back_populates="server")
    def __repr__(self) -> str:
        return f"Server(id={self.id!r}, name={self.name!r})"

class ResourceType(Base):
    __tablename__ = "resource_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    resource: Mapped[List["Resource"]] = relationship(back_populates="resource_type")
    def __repr__(self) -> str:
        return f"ResourceType(id={self.id!r}, name={self.name!r})"

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
        return f"Resource(id={self.id!r}, max_size={self.max_size!r}, free_space={self.free_space!r}, min_chunk={self.min_chunk!r}, server_id={self.server_id!r}, resource_type_id={self.resource_type_id!r})"

class GroupAllocation(Base):
    __tablename__ = "group_allocation"
    id: Mapped[int] = mapped_column(primary_key=True)
    valid: Mapped[bool] = mapped_column(nullable=False)
    time_of_allocation: Mapped[datetime] = mapped_column(nullable=False)
    time_of_deallocation: Mapped[datetime] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user: Mapped[str] = mapped_column(String(30), nullable=False)
    user_slurm_token: Mapped[str] = mapped_column(String(60), nullable=False)
    es_type: Mapped[str] = mapped_column(String(10), nullable=False)
    targets: Mapped[str] = mapped_column(String(100), nullable=True)
    mountpoint: Mapped[str] = mapped_column(String(100), nullable=True)
    allocation_status: Mapped[str] = mapped_column(String(20), nullable=False)
    allocation: Mapped[List["Allocation"]] = relationship(back_populates="group_allocation")
    location: Mapped[List["Location"]] = relationship(back_populates="group_allocation")
    def __repr__(self) -> str:
        return f"GroupAllocation(id={self.id!r}, valid={self.valid!r}, time_of_allocation={self.time_of_allocation!r}, time_of_deallocation={self.time_of_deallocation!r}, name={self.name!r}, user={self.user!r}, user_slurm_token={self.user_slurm_token!r}, es_type={self.es_type!r}, targets={self.targets!r}, mountpoint={self.mountpoint!r}, allocation_status={self.allocation_status!r})"

class Allocation(Base):
    __tablename__ = "allocation"
    id: Mapped[int] = mapped_column(primary_key=True)
    size: Mapped[int] = mapped_column(nullable=False)
    resource_id = mapped_column(ForeignKey("resource.id"))
    resource: Mapped[Resource] = relationship(back_populates="allocation")
    group_allocation_id = mapped_column(ForeignKey("group_allocation.id"))
    group_allocation: Mapped[GroupAllocation] = relationship(back_populates="allocation")
    core: Mapped[List["Core"]] = relationship(back_populates="allocation")
    def __repr__(self) -> str:
        return f"Allocation(id={self.id!r}, size={self.size!r}, resource_id={self.resource_id!r}, group_allocation_id={self.group_allocation_id!r})"

class Core(Base):
    __tablename__ = "core"
    id: Mapped[int] = mapped_column(primary_key=True)
    index: Mapped[int] = mapped_column(nullable=False)
    alloc_id = mapped_column(ForeignKey("allocation.id"))
    allocation: Mapped[Allocation] = relationship(back_populates="core")
    def __repr__(self) -> str:
        return f"Core(id={self.id!r}, index={self.index!r}, alloc_id={self.alloc_id!r})"

class Location(Base):
    __tablename__ = "location"
    id: Mapped[int] = mapped_column(primary_key=True)
    location: Mapped[str] = mapped_column(String(50), nullable=False)
    group_allocation_id = mapped_column(ForeignKey("group_allocation.id"))
    group_allocation: Mapped[GroupAllocation] = relationship(back_populates="location")
    def __repr__(self) -> str:
        return f"Core(id={self.id!r}, location={self.location!r}, group_allocation_id={self.group_allocation_id!r})"

class Flavor(Base):
    __tablename__ = "flavor"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cores: Mapped[int] = mapped_column(nullable=False)
    msize: Mapped[int] = mapped_column(nullable=False)
    ssize: Mapped[int] = mapped_column(nullable=False)
    def __repr__(self) -> str:
        return f"Flavor(id={self.id!r}, name={self.name!r}, cores={self.cores!r}, msize={self.msize!r}, ssize={self.ssize!r})"

class Queue(Base):
    __tablename__ = "queue"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user: Mapped[str] = mapped_column(String(30), nullable=False)
    user_slurm_token: Mapped[str] = mapped_column(String(60), nullable=False)
    es_type: Mapped[str] = mapped_column(String(10), nullable=False)
    server_count: Mapped[int] = mapped_column(nullable=False)
    targets: Mapped[str] = mapped_column(String(100), nullable=True)
    mountpoint: Mapped[str] = mapped_column(String(100), nullable=True)
    cores: Mapped[int] = mapped_column(nullable=False)
    msize: Mapped[int] = mapped_column(nullable=False)
    ssize: Mapped[int] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(String(150), nullable=True)
    def __repr__(self) -> str:
        return f"Flavor(id={self.id!r}, name={self.name!r}, cores={self.cores!r}, msize={self.msize!r}, ssize={self.ssize!r})"

def makeTables(engine):
    try:
        Base.metadata.create_all(engine)
    except:
        rm_logger.info('SQL - Error - API cannot connect to SQL (five attempts left)')
        print('SQL - Error - API cannot connect to SQL (five attempts left)')
        for x in range(4):
            time.sleep(20)
            try:
                Base.metadata.create_all(engine)
                return
            except:
                print("SQL connetion try -- " + str(x))
        rm_logger.info('SQL - Error - API cannot connect to SQL (all attempts exhausted)')
        print('SQL - Error - API cannot connect to SQL (all attempts exhausted)')
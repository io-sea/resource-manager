import sqlalchemy
from sqlalchemy import create_engine, MetaData, insert, select, update
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, text, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
import time
from datetime import datetime

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
    time_of_allocation: Mapped[datetime] = mapped_column(nullable=False)
    time_of_deallocation: Mapped[datetime] = mapped_column(nullable=True)
    allocation: Mapped[List["Allocation"]] = relationship(back_populates="group_allocation")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, valid={self.valid!r}, time_of_allocation={self.time_of_allocation!r}, time_of_deallocation={self.time_of_deallocation!r})"

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

def makeTables(engine):
    Base.metadata.create_all(engine)

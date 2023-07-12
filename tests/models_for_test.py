from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


parents_to_children = Table(
    "parents_to_children",
    Base.metadata,
    Column("parent_id", Integer, ForeignKey("parent_1.id")),
    Column("child_id", Integer, ForeignKey("children.id")),
)


class Parent(Base):
    __tablename__ = "parent_1"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    id_modulo = Column(Integer)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    children = relationship(
        "Child", secondary="parents_to_children", back_populates="parents"
    )


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    parents = relationship(
        "Parent", secondary="parents_to_children", back_populates="children"
    )

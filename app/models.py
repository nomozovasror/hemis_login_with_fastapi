from sqlalchemy import Column, Integer, String, Table, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from .database import Base



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    employee_id = Column(String, unique=True, index=True)
    name = Column(String)
    login = Column(String, unique=True)
    picture = Column(String)
    first_name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    birthday = Column(String)
    phone = Column(String, nullable=True)
    roles = relationship("Role", secondary='user_role', back_populates="users")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    users = relationship("User", secondary='user_role', back_populates="roles")

user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id"))
)
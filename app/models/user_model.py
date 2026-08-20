from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from app.database.database import Base



class RoleEnum(str, Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    projects = relationship(
        'ProjectModel',
        back_populates='user'
    )
    
    members = relationship(
        'ProjectMemberModel',
        back_populates='user',
        cascade='all, delete-orphan'
    )
    
    tasks = relationship(
        'TaskModel',
        back_populates='user',
        cascade='all, delete-orphan'
    )
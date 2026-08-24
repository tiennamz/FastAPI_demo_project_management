from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
from enum import Enum

class RoleProjectMember(str, Enum):
    OWNER = 'OWNER'
    MEMBER = 'MEMBER'

class ProjectModel(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key= True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    
    user = relationship(
        'UserModel',
        back_populates='projects'
    )
    
    members = relationship(
        'ProjectMemberModel',
        back_populates='project'
    )
    
    tasks = relationship(
        'TaskModel',
        back_populates='project'
    )
    
class ProjectMemberModel(Base):
    __tablename__ = 'project_members'
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role = Column(SQLEnum(RoleProjectMember), nullable=False, default='MEMBER')
    joined_at = Column(DateTime, server_default=func.now())
    
    user = relationship(
        'UserModel',
        back_populates='members'
    )
    
    project = relationship(
        'ProjectModel',
        back_populates='members'
    )
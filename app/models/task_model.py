from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from app.database.database import Base


class StatusEnum(str, Enum):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'

class PriorityEnum(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


class TaskModel(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    project_id =Column(Integer, ForeignKey('projects.id'))
    title = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    assignee_id = Column(Integer, ForeignKey('users.id'))
    status = Column(SQLEnum(StatusEnum), nullable=False)
    priority = Column(SQLEnum(PriorityEnum), nullable=False)
    comment = Column(String(100))
    attachment = Column(String(100))
    due_date = Column(DateTime)    
    created_at = Column(DateTime, server_default=func.now())

    project = relationship(
        'ProjectModel',
        back_populates='tasks'
    )
    
    user = relationship(
        'UserModel',
        back_populates='tasks'
    )
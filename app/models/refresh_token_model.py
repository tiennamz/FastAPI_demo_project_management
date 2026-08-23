from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base

class RefreshTokenModel(Base):
    __tablename__ = 'refresh_tokens'
    id = Column(Integer, primary_key=True)
    email_user = Column(String(100), ForeignKey('users.email'), unique=True)
    refresh_token = Column(String(255), nullable=False)

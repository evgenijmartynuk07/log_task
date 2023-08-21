from datetime import datetime


from .engine import Base
from sqlalchemy import Column, Integer, DateTime, Text, String
from fastapi_users.db import SQLAlchemyBaseUserTable


class DBLog(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message = Column(Text, nullable=False)


class DBUser(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)

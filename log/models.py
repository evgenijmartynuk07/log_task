from datetime import datetime


from db.engine import Base
from sqlalchemy import Column, Integer, DateTime, Text


class DBLog(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message = Column(Text, nullable=False)

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String
from db.engine import Base


class DBUser(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)

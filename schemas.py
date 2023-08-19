from datetime import datetime

from pydantic import BaseModel
from fastapi import UploadFile


class FileUpload(BaseModel):
    file: UploadFile


class Log(BaseModel):
    id: int
    timestamp: datetime
    message: str

    class Config:
        orm_mode = True

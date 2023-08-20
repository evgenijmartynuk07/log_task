from datetime import datetime
from typing import Optional
from fastapi import UploadFile, File
from fastapi_users import schemas
from pydantic.version import VERSION as PYDANTIC_VERSION
from pydantic import BaseModel, ConfigDict

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")


class FileUpload(BaseModel):
    file: UploadFile = File(...)


class Log(BaseModel):
    id: int
    timestamp: datetime
    message: str

    class Config:
        from_attributes = True


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    if PYDANTIC_V2:  # pragma: no cover
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:  # pragma: no cover

        class Config:
            orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

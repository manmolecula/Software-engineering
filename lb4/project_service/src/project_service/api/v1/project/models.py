from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class Project(ProjectCreate):
    id: str = Field(..., alias="_id")
    # model_config = model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("id", mode="before")
    def fix_object_id(cls, value: ObjectId) -> str:
        if isinstance(value, ObjectId):
            return str(value)
        else:
            raise ValueError("Expected objectId")

from pydantic import BaseModel
from typing import List, Optional

class Project(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    members: List[int]

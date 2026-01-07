from pydantic import BaseModel
from typing import List

class RecommendRequest(BaseModel):
    student_id: int
    skills: List[str]
    interest_area: str
    level: str

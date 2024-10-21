from pydantic import BaseModel

class ClassifyResultResponse(BaseModel):
    category: str
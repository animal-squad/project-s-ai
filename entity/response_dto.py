from pydantic import BaseModel

class CategorizeMainResponse(BaseModel):
    category: str

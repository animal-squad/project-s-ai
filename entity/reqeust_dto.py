from pydantic import BaseModel

class CategorizeMainRequest(BaseModel):
    type: str
    content: str
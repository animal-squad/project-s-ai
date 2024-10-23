from pydantic import BaseModel

class ClassifyRequest(BaseModel):
    type: str
    content: str
from pydantic import BaseModel

from entity.content import ContentSubCategory


class CategorizeMainResponse(BaseModel):
    category: str

class CategorizeSubResponse(BaseModel):
    data: list[ContentSubCategory]

from pydantic import BaseModel

from entity.content import ContentMainCategory


class CategorizeMainRequest(BaseModel):
    type: str
    content: str

class CategorizeSubRequest(BaseModel):
    sub_categories: list[dict]
    data: list[ContentMainCategory]

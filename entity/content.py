from pydantic import BaseModel

class ContentMainCategory(BaseModel):
    content_id: int
    type: str
    main_category: str
    content: str

class ContentSubCategory(BaseModel):
    content_id: int
    type: str
    sub_categories: list[str]

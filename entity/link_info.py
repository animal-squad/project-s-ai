from pydantic import BaseModel

class LinkInfo(BaseModel):
    linkId: int
    link: str
    content: str

class LinkWithTags(BaseModel):
    linkId: int
    title: str
    tags: list[str]
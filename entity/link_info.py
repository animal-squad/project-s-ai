from pydantic import BaseModel

class LinkInfo(BaseModel):
    linkId: int
    link: str
    content: str | None

class LinkWithTags(BaseModel):
    linkId: int
    title: str | None
    tags: list[str]
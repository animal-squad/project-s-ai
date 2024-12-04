from pydantic import BaseModel

class LinkInfo(BaseModel):
    linkId: str
    URL: str
    content: str | None

class LinkWithTags(BaseModel):
    linkId: str
    title: str | None
    tags: list[str]
    keywords: list[str | None]

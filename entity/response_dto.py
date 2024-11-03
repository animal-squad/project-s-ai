from pydantic import BaseModel

from entity.link_info import LinkWithTags


class CategorizeResponse(BaseModel):
    userId: int
    links: list[LinkWithTags]

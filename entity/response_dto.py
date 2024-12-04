from pydantic import BaseModel

from entity.link_info import LinkWithTags


class ExtractResponse(BaseModel):
    links: list[LinkWithTags]

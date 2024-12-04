from pydantic import BaseModel

from entity.link_info import LinkInfo


class ExtractRequest(BaseModel):
    links: list[LinkInfo]

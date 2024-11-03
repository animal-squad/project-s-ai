from pydantic import BaseModel

from entity.link_info import LinkInfo


class CategorizeRequest(BaseModel):
    userId: int
    links: list[LinkInfo]

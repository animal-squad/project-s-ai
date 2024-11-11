from pydantic import BaseModel

from entity.link_info import LinkInfo


class CategorizeRequest(BaseModel):
    links: list[LinkInfo]
